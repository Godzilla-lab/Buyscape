"""Items made unanswerable by construction: the proof is taken away.

MM-AQA (arXiv 2604.14799) builds unanswerable items from answerable ones
along an evidence sufficiency axis. Here the evidence is the text on the item
that names its model: a plate, a sticker, a code on the body. The local OCR
finds it, so no model on the leaderboard builds the set. Take it away and the
right answer is ask_for_proof, and the request is known: the identity shot of
the category's protocol.

Two ways to take it away:
- drop: the code is on some of the photos shown, so those photos go;
- blank: the code is on every photo shown, so each line of text that carries
  a digit is painted over on them, and the OCR reads the result again to make
  sure nothing of the code is left.

Only items named by brand and model qualify. A sofa stays a sofa with its
label gone (rule 1), so taking a label away proves nothing.

Photos that cannot be priced are the second slice: an advert whose photo is
not the seller's item, a dealer's showcase of many units. The photo check
found them and they are kept out of the scored set; here they come back as
items a model must refuse (Han et al., arXiv 2012.06009, screen the image
before they price it).

A person checks every constructed item before it is scored (`checked`).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from itertools import pairwise
from pathlib import Path

from .comparables import names
from .schema import Item

# The reader is shown this many photos (`run.reading_request`), so a code on
# a later photo was never evidence.
SHOWN = 4

# A line the OCR found, with the corners of its box in the photo's pixels.
Boxes = list[tuple[str, list[tuple[float, float]]]]
BoxReader = Callable[[Path], Boxes]

_YEAR = re.compile(r"(19|20)\d\d")
_JOINERS = {"with", "and", "plus", "for", "of", "in", "x"}

# Words that ask for the shot that names the item: a plate, a sticker, a
# label, or the screen that shows the model. A proof request that uses one is
# asking for the identity.
IDENTITY_WORDS = re.compile(
    r"\b(plates?|stickers?|labels?|nameplate|serial|imei|vin|model (number|no|name|code)|service tag"
    r"|settings|about (phone|this mac)|system information|spec sheet|specifications?)\b",
    re.IGNORECASE,
)

# Exclusion reasons that mean the photo, not the advert, cannot be priced.
BAD_PHOTO = re.compile(r"not the seller's item|showcase|stolen|photo showing multiple|two entirely different"
                       r"|photo shows a .* while the title", re.IGNORECASE)


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def code_tokens(title: str) -> set[str]:
    """The parts of a title a photo would have to carry to name the model.

    A word with a digit in it ("D3300", "7kg", "M281fdn"), or a word and the
    small number after it ("Redmi 9"). Only the item, not its extras: what
    follows "with", "plus" or "+" is a lens or a game, not the model. Years and
    counts are not a model."""
    item = re.split(r"\b(?:with|plus)\b|\+", title, maxsplit=1, flags=re.IGNORECASE)[0]
    words = [w for w in re.split(r"[^A-Za-z0-9]+", names(item)) if w]
    out: set[str] = set()
    for word in words:
        if _YEAR.fullmatch(word):
            continue
        if any(c.isdigit() for c in word) and (any(c.isalpha() for c in word) or len(word) >= 3):
            out.add(_norm(word))
    for a, b in pairwise(words):
        if a.isalpha() and len(a) > 1 and a.lower() not in _JOINERS and b.isdigit() and len(b) <= 2:
            out.add(_norm(a + b))
    return out


def carries(token: str, text: str) -> bool:
    """Whether a line of text carries the token. A short one must be a whole word."""
    if len(token) >= 4:
        return token in _norm(text)
    return token in {_norm(w) for w in re.split(r"[^A-Za-z0-9]+", text)}


def _hits(tokens: set[str], boxes: Boxes) -> set[str]:
    return {t for t in tokens for text, _ in boxes if carries(t, text)}


def blank(path: Path, boxes: Boxes, out: Path) -> None:
    """The photo with every line that carries a digit painted over, a little past its box."""
    from PIL import Image, ImageDraw

    with Image.open(path) as im:
        im = im.convert("RGB")
        draw = ImageDraw.Draw(im)
        for text, corners in boxes:
            if not corners or not any(c.isdigit() for c in text):
                continue
            xs, ys = [x for x, _ in corners], [y for _, y in corners]
            # The engine's boxes hug the glyphs, and a code's last letters can sit just outside.
            tall = max(ys) - min(ys)
            draw.rectangle((min(xs) - tall, min(ys) - tall / 3, max(xs) + tall, max(ys) + tall / 3), fill=(40, 40, 40))
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=92)


def construct(item: Item, photos: list[Path], read_boxes: BoxReader, out_dir: Path, root: Path) -> dict | None:
    """One item with its model code taken away, or None when it does not qualify."""
    if item.tier != "branded_electronics" or item.exclude:
        return None
    tokens = code_tokens(item.answer.title)
    shown = photos[:SHOWN]
    if not tokens or not shown:
        return None
    boxes = [read_boxes(p) for p in shown]
    found = [_hits(tokens, b) for b in boxes]
    carrying = [k for k, hit in enumerate(found) if hit]
    if not carrying:
        return None
    record = {
        "id": item.id, "split": item.split, "category": item.answer.category,
        "found": sorted(set().union(*found)), "removed": carrying, "expected": "ask_for_proof", "checked": None,
    }
    if len(carrying) < len(shown):
        kept = [p for k, p in enumerate(shown) if k not in carrying]
        return {**record, "route": "drop", "photos": [str(p.relative_to(root)) for p in kept]}
    painted = []
    for k, path in enumerate(shown):
        target = out_dir / item.id / f"photo_{k}.jpg"
        blank(path, boxes[k], target)
        if _hits(tokens, read_boxes(target)):
            return None  # the code survived the paint, so the proof is still there
        painted.append(str(target.relative_to(root)))
    return {**record, "route": "blank", "photos": painted}


def bad_photo(item: Item) -> dict | None:
    """An advert dropped because its photo cannot be priced, back as an item to refuse."""
    if not item.exclude or not BAD_PHOTO.search(item.exclude):
        return None
    return {"id": item.id, "split": item.split, "category": item.answer.category, "route": "bad_photo",
            "reason": item.exclude, "expected": "refuse", "checked": None}


def asks_for_identity(requests: list[str]) -> tuple[bool, bool]:
    """Whether the first proof request, and whether any, asks for the shot that names the item."""
    hits = [bool(IDENTITY_WORDS.search(r or "")) for r in requests]
    return (bool(hits) and hits[0]), any(hits)


def _read_decision(row: dict) -> str | None:
    """What the model decided, before retrieval could turn a price into no_price_data."""
    return (row.get("reading") or {}).get("decision")


def score(rows: list[dict], records: list[dict], items: dict[str, Item], clean: list[dict] | None = None) -> dict:
    """How a model did on items with the proof taken away, and on photos that cannot be priced.

    `clean` is the same model's honest run on the untouched items, for the
    pairs: name it right while the code is there, and abstain once it is gone.
    That is TRAPSBench's PECS idea (arXiv 2608.13167), so neither always
    refusing nor never refusing scores well.
    """
    from .score import REFUSALS, identity_correct

    by_id = {(r["id"], r["route"]): r for r in records}
    proof = [r for r in rows if r.get("variant") == "noproof"]
    bad = [r for r in rows if r.get("variant") == "bad_photo"]
    out: dict = {"noproof_items": len(proof), "bad_photo_items": len(bad)}

    abstained = priced = named = hidden = first = anywhere = errors = 0
    hidden_ids: list[str] = []
    for row in proof:
        record = next((r for (i, route), r in by_id.items() if i == row["id"] and route != "bad_photo"), None)
        decision = _read_decision(row)
        if decision is None:
            errors += 1
            continue
        reading = row["reading"]
        identity = reading.get("identity") or {}
        abstained += decision in ("ask_for_proof", "cannot_identify")
        priced += decision == "price"
        said = f"{identity.get('brand') or ''} {identity.get('model') or ''}"
        if identity.get("status") == "named" and identity.get("model"):
            named += 1
        if record and any(carries(t, said) for t in record["found"]):
            hidden += 1
            hidden_ids.append(row["id"])
        asked_first, asked = asks_for_identity(reading.get("proof_requests") or [])
        first += asked_first
        anywhere += asked
    answered = len(proof) - errors
    out.update({
        "noproof_abstained": _share(abstained, answered),
        "noproof_priced": _share(priced, answered),
        "noproof_named_a_model": _share(named, answered),
        "noproof_named_the_hidden_code": _share(hidden, answered),
        "noproof_hidden_code_ids": hidden_ids,
        "proof_asked_first": _share(first, answered),
        "proof_asked_at_all": _share(anywhere, answered),
        "noproof_errors": errors,
    })

    decided = [r for r in bad if _read_decision(r) is not None]
    out["bad_photo_refused"] = _share(sum(_read_decision(r) in REFUSALS for r in decided), len(decided))
    out["bad_photo_errors"] = len(bad) - len(decided)

    if clean is not None:
        before = {r["id"]: r for r in clean if r.get("variant", "clean") == "clean"}
        right = gone = both = pairs = 0
        for row in proof:
            item, base = items.get(row["id"]), before.get(row["id"])
            if item is None or base is None or _read_decision(row) is None or _read_decision(base) is None:
                continue
            pairs += 1
            knew = identity_correct(item, (base.get("reading") or {}).get("identity") or {}) is True
            held = _read_decision(row) in ("ask_for_proof", "cannot_identify")
            right += knew
            gone += held
            both += knew and held
        out.update({
            "pairs": pairs,
            "pairs_named_while_shown": _share(right, pairs),
            "pairs_abstained_once_gone": _share(gone, pairs),
            "pairs_both": _share(both, pairs),
            "pecs_style": _share(right + gone, 2 * pairs),
        })
    return out


def _share(num: int, den: int) -> float | None:
    return round(num / den, 3) if den else None
