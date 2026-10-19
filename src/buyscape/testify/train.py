"""Build the fine-tuning set: a teacher's reads of training adverts, kept only
where they are right, and each paired with a lied-to twin.

The recipe is steps 4 and 5 of docs/research/fine-tuning-research.md, and the
target is the gap the untuned Qwen3-VL 8B showed on Testify: it never prices,
because it reads "price an unproven claim at its worst case" as "do not price
without proof". So:

- A read that names the item right, checked against the advert's title (the
  answer key, never an input), becomes a price at the worst case, whatever
  the teacher decided. The title, not the kind the advert was searched
  under: Jiji's search is literal, so a search for "pallets" brings back
  activated carbon sold by the pallet. Its claims, risks and proof requests are kept: the
  doubt stays, it just no longer stops the price.
- A model the teacher named that the photo check could not read is cut back
  to the kind, so the student does not learn to name what it cannot see. The
  check is the benchmark's own (`testify-label --split train`, a vision
  model asked what the photos alone show), which sees logos, sideways text
  and a console's shape. An advert it has not checked falls back on the
  local OCR: every brand and model word must be text the OCR found.
- A model code (any model with a digit in it) stays only when the title or
  the OCR carries it too; otherwise the brand stays and the code goes. A cut
  name leaves no trace: a note that says it was read goes with it, so the
  student never learns to claim it read what the answer does not use. Codes
  are where the benchmark's silent wrong answers came from: a cover badge
  read as an engine's model, a 7kg washer named with a code for another.
- A read where the teacher could not tell what the item is stays a
  cannot_identify example, so the student also learns to decline.
- A read that is wrong about the item is dropped. A wrong label teaches more
  than a missing one.
- Each kept example gets a twin: the same photos and words plus a planted
  claim from train_lies.yaml, never the benchmark's lies.yaml. The twin's
  answer is the same, with the claim listed as unverified.

Training items are priced only against training adverts, so no benchmark
title or price reaches a training prompt (`_testify_pool` in cli.py).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

import yaml
from pydantic import ValidationError

from ..identify.ocr import OcrReader
from ..providers.base import ImageRef, ModelRequest
from ..providers.openrouter import system_text
from .answer import ClaimAnswer, IdentityAnswer, Reading, money_written
from .comparables import names
from .run import lie_entry, reading_request
from .schema import Item
from .score import identity_correct

TRAIN_LIES = Path(__file__).resolve().parents[3] / "eval" / "testify" / "train_lies.yaml"
WORST_CASE_REASON = (
    "The item is known from the photos. What they cannot prove is priced at its worst case until the "
    "proof asked for below arrives."
)
UNPROVEN = "No photo shows this; it is the seller's word only."
UNREADABLE = "No photo shows this clearly enough to read."
# Title words of an advert that sells no item: a repair service or a buyer.
# The benchmark leaves these out by its photo check; training adverts have
# none, so their titles are read for it. The title only grades, never prompts.
NOT_FOR_SALE = re.compile(
    r"\b(repairs?|repairing|installation|servicing|services?|we buy|buying|wanted|for hire|for rent)\b", re.IGNORECASE
)


def _train_lies() -> tuple[dict, ...]:
    return tuple(yaml.safe_load(TRAIN_LIES.read_text()) or ())


def train_lie(item: Item, entries: tuple[dict, ...] | None = None) -> str:
    """A planted claim for training, one of its kind's lines, fixed by the item's id."""
    entry = lie_entry(item, entries if entries is not None else _train_lies())
    lines = entry.get("lies") or [entry["lie"]]
    return lines[int(hashlib.sha256(item.id.encode()).hexdigest(), 16) % len(lines)]


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def on_photos(reading: dict, lines: list[str]) -> bool:
    """Whether every brand and model word in a read is text the OCR found on a photo.

    Each name must sit inside one OCR line, spaces and dashes ignored. A name
    shorter than four letters must be a whole word of the line, so "LG" is
    not found inside a part number."""
    identity = reading.get("identity") or {}
    names = [n for n in (identity.get("brand"), identity.get("model")) if n and _norm(n)]
    if not names:
        return False
    for name in names:
        want = _norm(name)
        if len(want) < 4:
            found = any(want in (_norm(w) for w in re.split(r"[^A-Za-z0-9]+", line)) for line in lines)
        else:
            found = any(want in _norm(line) for line in lines)
        if not found:
            return False
    return True


def ocr_label(reading: dict, photos: list[Path], ocr: OcrReader | None, max_photos: int = 4,
              lines: list[str] | None = None) -> dict:
    """A photo check for an advert no labeller saw, from the photos the model was shown.
    Without the OCR engine nothing can be confirmed, so a name is cut to the kind."""
    if ocr is None:
        return {"identity_from_photos_alone": "unchecked"}
    if lines is None:
        lines = ocr(tuple(ImageRef(p) for p in photos[:max_photos]))
    return {"identity_from_photos_alone": "named" if on_photos(reading, lines) else "by_type"}


def code_confirmed(model: str | None, title: str, lines: list[str] | None) -> bool:
    """A model with no digit is a name the photo check covers. A code must be in the title,
    or be text the OCR found on a photo (`lines`, None when it was not run)."""
    if not model or not any(c.isdigit() for c in model):
        return True
    want = _norm(names(model))
    if want and want in _norm(names(title)):
        return True
    return lines is not None and on_photos({"identity": {"model": model}}, lines)


def _forget(data: dict, gone: list[str]) -> dict | None:
    """The answer with no word of a cut name left in it. A note that saw the name goes,
    a claim proven only by reading it falls back to unverified, and a reason naming it
    becomes the worst-case reason. None when nothing seen would be left."""
    keys = [_norm(g) for g in gone if g and len(_norm(g)) >= 3]
    if not keys:
        return data

    def names_it(text: str | None) -> bool:
        return any(k in _norm(text or "") for k in keys)

    data["observations"] = [o for o in data["observations"] if not names_it(o)]
    if not data["observations"]:
        return None
    for claim in data["claims"]:
        if claim["verdict"] == "supported" and names_it(claim.get("evidence")):
            claim.update(verdict="unverified", evidence=UNREADABLE)
    if names_it(data.get("reason")):
        data["reason"] = WORST_CASE_REASON
    return data


def target(item: Item, reading: dict, label: dict | None = None,
           keep_code: bool = True) -> tuple[Reading | None, str]:
    """The answer the student should give, and why it was kept or dropped.
    `keep_code` False drops a named read's model code and keeps its brand."""
    try:
        read = Reading.model_validate(reading)
    except ValidationError:
        return None, "teacher's answer breaks the schema"
    if NOT_FOR_SALE.search(item.answer.title or ""):
        return None, "the advert sells a service or wants to buy"
    if read.decision == "fraud_suspected":
        return None, "teacher called fraud"
    if read.identity.status == "unknown":
        if read.decision not in ("cannot_identify", "ask_for_proof"):
            return None, "unknown identity with a price"
        data = read.model_dump()
        data.update(decision="cannot_identify")
        return Reading.model_validate(data), "kept: cannot identify"
    if identity_correct(item, read.identity.model_dump(), by_title=True) is not True:
        return None, "teacher wrong about the item"
    data = read.model_dump()
    cut = ""
    gone: list[str] = []
    if read.identity.status == "named" and label and label.get("identity_from_photos_alone") not in (None, "named"):
        # Named beyond what the photo check could read: keep only the kind.
        data["identity"] = IdentityAnswer(status="by_type", kind=read.identity.kind).model_dump()
        if not read.identity.kind or identity_correct(item, data["identity"], by_title=True) is not True:
            return None, "named beyond the photos, and the kind alone is wrong"
        cut, gone = ", name cut to the kind", [read.identity.brand, read.identity.model]
    elif read.identity.status == "named" and read.identity.model and not keep_code:
        data["identity"]["model"] = None
        cut, gone = ", model code cut", [read.identity.model]
    if gone and (data := _forget(data, gone)) is None:
        return None, "nothing seen is left once the name is cut"
    if read.decision != "price":
        data.update(decision="price", reason=WORST_CASE_REASON)
    answer = Reading.model_validate(data)
    if money_written(answer):
        return None, "teacher wrote a price"
    return answer, ("kept: price at worst case" if read.decision != "price" else "kept: priced") + cut


def twin(answer: Reading, lie: str) -> Reading:
    """The same answer for the lied-to advert: the claim is listed, unproven, and nothing else moves."""
    claims = [*answer.claims, ClaimAnswer(claim=lie, verdict="unverified", evidence=UNPROVEN)]
    return answer.model_copy(update={"claims": claims})


def messages(request: ModelRequest, answer: Reading, root: Path) -> list[dict]:
    """The chat a model is trained on: the exact system and user turns an API model is sent,
    with photos as paths rather than inline data, then the answer."""
    parts: list[dict] = [{"type": "text", "text": request.user_text}]
    for img in request.images:
        if img.label:
            parts.append({"type": "text", "text": f"[{img.label}]"})
        # Absolute, not resolved: eval/raw may be a link to another checkout's photos.
        parts.append({"type": "image", "image": os.path.relpath(os.path.abspath(img.path), os.path.abspath(root))})
    return [
        {"role": "system", "content": system_text(request)},
        {"role": "user", "content": parts},
        {"role": "assistant", "content": answer.model_dump_json(exclude_none=True)},
    ]


def build(cases: list[tuple], rows: list[dict], labels: dict[str, dict], root: Path,
          entries: tuple[dict, ...] | None = None, ocr: OcrReader | None = None) -> tuple[list[dict], dict[str, int]]:
    """Training examples from a teacher's clean reads. `cases` holds (item, photos).
    When the teacher named the item, `ocr` checks a model code the title does
    not carry, and the whole name on an advert with no photo check."""
    reads = {r["id"]: r for r in rows if r.get("variant", "clean") == "clean" and r.get("reading")}
    out: list[dict] = []
    tally: dict[str, int] = {}
    for item, photos in cases:
        row = reads.get(item.id)
        if row is None:
            tally["no teacher read"] = tally.get("no teacher read", 0) + 1
            continue
        label, keep_code = labels.get(item.id), True
        identity = row["reading"].get("identity") or {}
        if identity.get("status") == "named":
            title = item.answer.title or ""
            lines = None
            if ocr is not None and (label is None or not code_confirmed(identity.get("model"), title, None)):
                lines = ocr(tuple(ImageRef(p) for p in photos[:4]))
            if label is None:
                label = ocr_label(row["reading"], photos, ocr, lines=lines)
            keep_code = code_confirmed(identity.get("model"), title, lines)
        answer, why = target(item, row["reading"], label, keep_code)
        tally[why] = tally.get(why, 0) + 1
        if answer is None:
            continue
        lie = train_lie(item, entries)
        for variant, said, request in (
            ("clean", answer, reading_request(item, photos, "clean")),
            ("lie", twin(answer, lie), reading_request(item, photos, "lie", lie=lie)),
        ):
            out.append({"id": item.id, "variant": variant, "market": item.market,
                        "messages": messages(request, said, root)})
    return out, tally


def write(examples: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in examples))
