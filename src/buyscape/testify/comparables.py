"""Comparables for a priced answer, retrieved from the cached adverts.

Rule 4: the model never writes a price. It names the item, this module finds
other adverts for that item, each with a source and a date, and the model
picks the low and the high from the list by number. A wrong name brings the
wrong comparables, so a wrong identity shows up in the price.

Only second-hand asking prices are comparables. Dealers' new stock, buyers'
offers and adverts with no date are left out, and so is the item under test
along with any repost of it.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from ..evalset.score import GENERIC_WORDS, _norm, model_matches
from .answer import IdentityAnswer
from .schema import Item

# Words that describe an advert, never the item.
_STOP = {
    "used", "tokunbo", "fairly", "uk", "us", "london", "foreign", "new", "brand", "neat", "clean",
    "for", "sale", "and", "of", "the", "a", "an", "with", "in", "on", "good", "condition",
    "working", "perfect", "original", "quality", "available", "item", "items",
}
# A set or a pack is a different unit of sale from one piece.
_SET_WORDS = {"set", "sets", "pieces", "pcs", "pack", "packs", "pairs", "lot", "bundle", "dozen"}
_WORD = re.compile(r"[a-z0-9]+")


def _stem(word: str) -> str:
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith(("ses", "xes", "ches", "shes")):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


# The same thing in the words the market uses. A word maps to one or more
# canonical words, so "inverter AC" meets "air conditioner".
_SYNONYMS = {
    "tv": ["television"], "telly": ["television"], "fridge": ["refrigerator"],
    "couch": ["sofa"], "settee": ["sofa"], "tire": ["tyre"], "ac": ["air", "conditioner"],
    "aircon": ["air", "conditioner"], "notebook": ["laptop"], "handset": ["phone"],
    "smartphone": ["phone"], "cellphone": ["phone"], "gen": ["generator"], "genset": ["generator"],
}
# Heads too broad to match on alone: a drilling machine is not a washing machine.
_BROAD_HEADS = {"machine", "set", "part", "kit", "tool", "box", "bag", "case", "cover", "stand",
                "accessory", "unit", "system", "equipment", "device", "appliance", "scrap"}


def words(text: str | None) -> list[str]:
    """Content words of a kind or title, stemmed and made canonical, in order."""
    out: list[str] = []
    for w in _WORD.findall((text or "").lower()):
        if w in _STOP:
            continue
        stem = _stem(w)
        out.extend(_SYNONYMS.get(w) or _SYNONYMS.get(stem) or [stem])
    return out


@dataclass(frozen=True)
class Comparable:
    item_id: str
    price_ngn: int
    title: str
    kind: str
    market: str
    observed_on: str
    url: str
    photos: tuple[str, ...] = ()

    @property
    def source(self) -> str:
        return f"jiji:{self.observed_on}:{self.item_id}" if "jiji" in self.url else f"{self.url} ({self.observed_on})"

    def line(self, number: int) -> str:
        return f"#{number}: {self.price_ngn:,} NGN | {self.title} | {self.market} | {self.source}"


def build_pool(items: Iterable[Item], hashes: dict[str, list[str]] | None = None) -> list[Comparable]:
    """Every second-hand asking price with a date, from the benchmark's own cache."""
    pool: list[Comparable] = []
    for item in items:
        price = item.answer.price
        if not price.ngn or price.kind == "wanted" or not price.observed_on or price.used is False:
            continue
        if item.tier == "not_for_sale":
            continue
        if item.exclude and ("new stock" in item.exclude or "not for sale" in item.exclude):
            continue
        pool.append(
            Comparable(
                item_id=item.id,
                price_ngn=int(price.ngn),
                title=item.answer.title,
                kind=item.answer.kind or "",
                market=item.market,
                observed_on=price.observed_on,
                url=item.url,
                photos=tuple((hashes or {}).get(item.id, ())),
            )
        )
    return pool


def _same_photo(a: Iterable[str], b: Iterable[str]) -> bool:
    from ..ui.sessions import DUPLICATE_DISTANCE, _hamming

    return any(_hamming(x, y) <= DUPLICATE_DISTANCE for x in a for y in b)


def _kind_score(kind_words: list[str], comparable: Comparable, strict: bool = True) -> float:
    """Share of the named kind's words the comparable carries, 0 unless the head noun is one.

    Strict, a kind of two or more words also needs one of its other words. The
    loose pass, used only when strict finds too few, lets a head noun match
    alone unless it is too broad to mean anything by itself.
    """
    if not kind_words:
        return 0.0
    labelled = words(comparable.kind)
    have = set(words(comparable.title)) | set(labelled)
    # The head must be what the comparable is, not a word it mentions: a TV
    # antenna is not a TV. Its kind label says what it is, when it has one.
    if (labelled[-1] != kind_words[-1]) if labelled else kind_words[-1] not in have:
        return 0.0
    numbers = {w for w in kind_words if w.isdigit()}
    if numbers and not numbers <= have:
        return 0.0  # a 2 seater is not a 3 seater
    if not (set(kind_words) & _SET_WORDS) and have & _SET_WORDS:
        return 0.0  # one piece is not priced from a set
    if len(kind_words) > 1 and not any(w in have for w in kind_words[:-1]):
        if strict or kind_words[-1] in _BROAD_HEADS:
            return 0.0  # a sewing machine is not a washing machine
        return 0.4
    return sum(w in have for w in kind_words) / len(kind_words)


def find(
    identity: IdentityAnswer,
    market: str,
    pool: list[Comparable],
    item: Item,
    limit: int = 12,
    min_local: int = 5,
    own_photos: Iterable[str] = (),
) -> list[Comparable]:
    """Comparables for what the model said the item is, cheapest first.

    A named item is matched on brand and model the way the Phase 0 gate
    matches them. Anything else, or a name with too few adverts, is matched on
    its kind. The same city comes first, and other cities fill in only when it
    has fewer than `min_local`. A repost of the item, by title and price or by
    a matching photo, is never its own comparable.
    """
    own = (" ".join(sorted(_norm(item.answer.title))), item.answer.price.ngn)
    own_photos = tuple(own_photos)
    candidates = [
        c for c in pool
        if c.item_id != item.id and c.url != item.url
        and (" ".join(sorted(_norm(c.title))), c.price_ngn) != own
        and not (own_photos and _same_photo(own_photos, c.photos))
    ]
    scored: list[tuple[float, Comparable]] = []
    if identity.status == "named" and (identity.brand or identity.model):
        name_words = (_norm(identity.brand) | _norm(identity.model)) - GENERIC_WORDS
        if name_words:
            scored = [(2.0, c) for c in candidates if model_matches(identity.brand, identity.model, c.title)]
    kind_words = words(identity.kind)
    for strict in (True, False):
        if len(scored) >= 3 or not kind_words:
            break
        taken = {c.item_id for _, c in scored}
        for c in candidates:
            s = _kind_score(kind_words, c, strict)
            if s >= 0.4 and c.item_id not in taken:
                scored.append((s, c))
    local = [(s, c) for s, c in scored if c.market == market]
    chosen = sorted(local, key=lambda sc: -sc[0])[:limit]
    if len(chosen) < min_local:
        others = sorted(((s, c) for s, c in scored if c.market != market), key=lambda sc: -sc[0])
        chosen += others[: limit - len(chosen)]
    return sorted((c for _, c in chosen), key=lambda c: c.price_ngn)


def photo_hashes(items: Iterable[Item], root, cache=None) -> dict[str, list[str]]:
    """Perceptual hashes of every item's photos, kept in a file so a rerun is quick.

    Hashes are not photos and may be published; they are how a repost is
    caught here and how the release lets others dedupe.
    """
    import json
    from pathlib import Path

    from ..ui.sessions import _phash
    from .label import photos_for

    path = Path(cache) if cache else Path(root) / "eval" / "testify" / "photo_hashes.json"
    known: dict[str, list[str]] = json.loads(path.read_text()) if path.exists() else {}
    changed = False
    for item in items:
        if item.id in known:
            continue
        found = [h for h in (_phash(p) for p in photos_for(item, Path(root))) if h]
        if found:
            known[item.id] = found
            changed = True
    if changed:
        path.write_text(json.dumps(dict(sorted(known.items())), indent=0) + "\n")
    return known
