"""Build the fine-tuning set: a teacher's reads of training adverts, kept only
where they are right, and each paired with a lied-to twin.

The recipe is steps 4 and 5 of docs/research/fine-tuning-research.md, and the
target is the gap the untuned Qwen3-VL 8B showed on Testify: it never prices,
because it reads "price an unproven claim at its worst case" as "do not price
without proof". So:

- A read that names the item right, checked against the advert's title (the
  answer key, never an input), becomes a price at the worst case, whatever
  the teacher decided. Its claims, risks and proof requests are kept: the
  doubt stays, it just no longer stops the price.
- A model the teacher named that the photo check could not read is cut back
  to the kind, so the student does not learn to name what it cannot see.
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
from pathlib import Path

import yaml
from pydantic import ValidationError

from ..providers.base import ModelRequest
from ..providers.openrouter import system_text
from .answer import ClaimAnswer, IdentityAnswer, Reading, money_written
from .run import lie_entry, reading_request
from .schema import Item
from .score import identity_correct

TRAIN_LIES = Path(__file__).resolve().parents[3] / "eval" / "testify" / "train_lies.yaml"
WORST_CASE_REASON = (
    "The item is known from the photos. What they cannot prove is priced at its worst case until the "
    "proof asked for below arrives."
)
UNPROVEN = "No photo shows this; it is the seller's word only."


def _train_lies() -> tuple[dict, ...]:
    return tuple(yaml.safe_load(TRAIN_LIES.read_text()) or ())


def train_lie(item: Item, entries: tuple[dict, ...] | None = None) -> str:
    """A planted claim for training, one of its kind's lines, fixed by the item's id."""
    entry = lie_entry(item, entries if entries is not None else _train_lies())
    lines = entry.get("lies") or [entry["lie"]]
    return lines[int(hashlib.sha256(item.id.encode()).hexdigest(), 16) % len(lines)]


def target(item: Item, reading: dict, label: dict | None = None) -> tuple[Reading | None, str]:
    """The answer the student should give, and why it was kept or dropped."""
    try:
        read = Reading.model_validate(reading)
    except ValidationError:
        return None, "teacher's answer breaks the schema"
    if read.decision == "fraud_suspected":
        return None, "teacher called fraud"
    if read.identity.status == "unknown":
        if read.decision not in ("cannot_identify", "ask_for_proof"):
            return None, "unknown identity with a price"
        data = read.model_dump()
        data.update(decision="cannot_identify")
        return Reading.model_validate(data), "kept: cannot identify"
    if identity_correct(item, read.identity.model_dump()) is not True:
        return None, "teacher wrong about the item"
    data = read.model_dump()
    if read.identity.status == "named" and label and label.get("identity_from_photos_alone") not in (None, "named"):
        # Named beyond what the photo check could read: keep only the kind.
        data["identity"] = IdentityAnswer(status="by_type", kind=read.identity.kind).model_dump()
        if not read.identity.kind or identity_correct(item, data["identity"]) is not True:
            return None, "named beyond the photos, and the kind alone is wrong"
    if read.decision != "price":
        data.update(decision="price", reason=WORST_CASE_REASON)
    answer = Reading.model_validate(data)
    if money_written(answer):
        return None, "teacher wrote a price"
    return answer, "kept: price at worst case" if read.decision != "price" else "kept: priced"


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
        parts.append({"type": "image", "image": str(Path(img.path).resolve().relative_to(root.resolve()))})
    return [
        {"role": "system", "content": system_text(request)},
        {"role": "user", "content": parts},
        {"role": "assistant", "content": answer.model_dump_json(exclude_none=True)},
    ]


def build(cases: list[tuple], rows: list[dict], labels: dict[str, dict], root: Path,
          entries: tuple[dict, ...] | None = None) -> tuple[list[dict], dict[str, int]]:
    """Training examples from a teacher's clean reads. `cases` holds (item, photos)."""
    reads = {r["id"]: r for r in rows if r.get("variant", "clean") == "clean" and r.get("reading")}
    out: list[dict] = []
    tally: dict[str, int] = {}
    for item, photos in cases:
        row = reads.get(item.id)
        if row is None:
            tally["no teacher read"] = tally.get("no teacher read", 0) + 1
            continue
        answer, why = target(item, row["reading"], labels.get(item.id))
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
