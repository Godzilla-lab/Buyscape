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


def words(text: str | None) -> list[str]:
    """Content words of a kind or title, stemmed, in order."""
    return [_stem(w) for w in _WORD.findall((text or "").lower()) if w not in _STOP]


@dataclass(frozen=True)
class Comparable:
    item_id: str
    price_ngn: int
    title: str
    kind: str
    market: str
    observed_on: str
    url: str

    @property
    def source(self) -> str:
        return f"jiji:{self.observed_on}:{self.item_id}" if "jiji" in self.url else f"{self.url} ({self.observed_on})"

    def line(self, number: int) -> str:
        return f"#{number}: {self.price_ngn:,} NGN | {self.title} | {self.market} | {self.source}"


def build_pool(items: Iterable[Item]) -> list[Comparable]:
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
            )
        )
    return pool


def _kind_score(kind_words: list[str], comparable: Comparable) -> float:
    """Share of the named kind's words the comparable carries, 0 unless the head noun is one."""
    if not kind_words:
        return 0.0
    have = set(words(comparable.title)) | set(words(comparable.kind))
    if kind_words[-1] not in have:
        return 0.0
    numbers = {w for w in kind_words if w.isdigit()}
    if numbers and not numbers <= have:
        return 0.0  # a 2 seater is not a 3 seater
    if not (set(kind_words) & _SET_WORDS) and have & _SET_WORDS:
        return 0.0  # one piece is not priced from a set
    if len(kind_words) > 1 and not any(w in have for w in kind_words[:-1]):
        return 0.0  # a sewing machine is not a washing machine
    return sum(w in have for w in kind_words) / len(kind_words)


def find(
    identity: IdentityAnswer,
    market: str,
    pool: list[Comparable],
    item: Item,
    limit: int = 12,
    min_local: int = 5,
) -> list[Comparable]:
    """Comparables for what the model said the item is, cheapest first.

    A named item is matched on brand and model the way the Phase 0 gate
    matches them. Anything else, or a name with too few adverts, is matched on
    its kind. The same city comes first, and other cities fill in only when it
    has fewer than `min_local`.
    """
    own = (" ".join(sorted(_norm(item.answer.title))), item.answer.price.ngn)
    candidates = [
        c for c in pool
        if c.item_id != item.id and c.url != item.url
        and (" ".join(sorted(_norm(c.title))), c.price_ngn) != own
    ]
    scored: list[tuple[float, Comparable]] = []
    if identity.status == "named" and (identity.brand or identity.model):
        name_words = (_norm(identity.brand) | _norm(identity.model)) - GENERIC_WORDS
        if name_words:
            scored = [(2.0, c) for c in candidates if model_matches(identity.brand, identity.model, c.title)]
    if len(scored) < 3 and identity.kind:
        kind_words = words(identity.kind)
        named = {c.item_id for _, c in scored}
        for c in candidates:
            s = _kind_score(kind_words, c)
            if s >= 0.5 and c.item_id not in named:
                scored.append((s, c))
    local = [(s, c) for s, c in scored if c.market == market]
    chosen = sorted(local, key=lambda sc: -sc[0])[:limit]
    if len(chosen) < min_local:
        others = sorted(((s, c) for s, c in scored if c.market != market), key=lambda sc: -sc[0])
        chosen += others[: limit - len(chosen)]
    return sorted((c for _, c in chosen), key=lambda c: c.price_ngn)
