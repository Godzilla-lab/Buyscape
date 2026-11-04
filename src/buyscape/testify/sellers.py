"""Who posted an advert, read off the advert itself.

Jiji sellers repost the same unit, sometimes across cities, so a training
advert from a seller who is also in the benchmark can carry the benchmark's
answers. The cached adverts do not record the seller, but the adverts do:
Jiji stamps every photo with "POSTED ON JIJI" and the seller's name, which the
local OCR reads, and sellers write their phone number into their words.
Either one links two adverts to one seller.
"""

from __future__ import annotations

import re

# The stamp is faint, so the OCR often reads only part of it: "POSTED ONJIH", "POSTED O".
STAMP = re.compile(r"\bpost\w{0,3}\s*o", re.IGNORECASE)
_NAME = re.compile(r"[A-Za-z][A-Za-z .&'-]{3,40}")
_PHONE = re.compile(r"(?:\+?234|0)\s*[789][01](?:[\s-]?\d){8}")

# A box as the OCR cache holds it: text, confidence, corners.
Box = tuple[str, float, list[list[float]]]


def _height(box: Box) -> float:
    ys = [y for _, y in box[2]] or [0.0]
    return max(ys) - min(ys)


def stamp_name(boxes: list[Box]) -> str | None:
    """The seller's name from a photo's Jiji stamp, or None when the photo carries no stamp.

    The name is the line next to "POSTED ON JIJI", above it or below it, in
    the larger letters; only letters and spaces count, so a stray price or
    code beside the stamp is never taken for a name."""
    for k, (text, _, _) in enumerate(boxes):
        if not STAMP.search(text):
            continue
        near = [b for b in (boxes[k - 1] if k else None, boxes[k + 1] if k + 1 < len(boxes) else None)
                if b and _NAME.fullmatch(b[0].strip()) and not STAMP.search(b[0])]
        if near:
            return _clean(max(near, key=_height)[0])
    return None


def _clean(name: str) -> str:
    return re.sub(r"[^A-Z]", "", name.upper())


def phones(text: str | None) -> set[str]:
    """Nigerian phone numbers in the seller's words, as their last ten digits."""
    return {re.sub(r"\D", "", m)[-10:] for m in _PHONE.findall(text or "")}


def same(a: str, b: str) -> bool:
    """Whether two seller keys name one seller. Stamped names are read through a
    faint watermark ("QLAJIDE" for "OLAJIDE"), so they match when nearly equal."""
    if a == b:
        return True
    if not (a.startswith("name:") and b.startswith("name:")):
        return False
    x, y = a[5:], b[5:]
    if min(len(x), len(y)) < 6 or abs(len(x) - len(y)) > 2:
        return False
    from difflib import SequenceMatcher

    return SequenceMatcher(None, x, y).ratio() >= 0.85


def keys(photo_boxes: list[list[Box]], seller_text: str | None) -> set[str]:
    """Every key that names this advert's seller: stamped names, and phone numbers."""
    names = {n for boxes in photo_boxes if (n := stamp_name(boxes)) and len(n) >= 4}
    return {f"name:{n}" for n in names} | {f"phone:{p}" for p in phones(seller_text)}
