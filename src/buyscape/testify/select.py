"""Choose which training adverts the teacher reads: variety first, then what teaches most.

A crawl brings thousands of adverts and the teacher's read is the slow, costly
step, so not every advert is read. First the ones that teach nothing go: an
advert posted again with the same photos, the same title at the same price,
a placeholder price (1, 1111111), no photo, a buyer's advert. Then the rest
are spread across every category and price level, so the model sees every
kind the market has, cheap and dear. Within each, the adverts that teach most
go first:

- one with others for the same item in the pool, which the price step learns
  from (it picks the comparable adverts for the same thing);
- one whose photos show a code the local OCR can read, a model or a plate;
- a faulty, broken or scrap one, a large part of what BuyScrap buys.

Ties are broken by a hash of the advert's id, so a rerun picks the same set.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from ..evalset.score import GENERIC_WORDS
from .comparables import names, words
from .schema import Item

PRICE_BANDS = (10_000, 50_000, 200_000, 1_000_000, 5_000_000)
BAND_NAMES = ("under 10k", "10k to 50k", "50k to 200k", "200k to 1m", "1m to 5m", "over 5m")
_REPEATED = re.compile(r"^(\d)\1{4,}$")
_COUNTING = {"123456", "1234567", "12345678", "123456789"}
FAULTY = re.compile(r"\b(faulty|spoilt|spoiled|broken|scrap|for parts|not working|cracked|dead|condemned)\b",
                    re.IGNORECASE)
_CODE = re.compile(r"(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9-]{4,}")


def placeholder(ngn: int | None) -> bool:
    """A price a seller types to fill the box, not to sell at."""
    if not ngn or ngn < 500 or ngn > 500_000_000:
        return True
    digits = str(int(ngn))
    return bool(_REPEATED.match(digits)) or digits in _COUNTING


def band(ngn: int) -> int:
    return sum(ngn >= edge for edge in PRICE_BANDS)


def category(item: Item) -> str:
    """The kind for a fetched advert, the site's category for a crawled one."""
    return (item.answer.kind or item.answer.identity.text or "other").lower()


# Generic words that are also makers: "hp" is horsepower on a generator and the maker of a laptop.
_MAKERS = {"hp"}


def informative(title: str) -> list[str]:
    """The title's words that name the thing: no units, no category nouns."""
    out: list[str] = []
    for w in words(names(title)):
        if len(w) > 1 and (w not in GENERIC_WORDS or w in _MAKERS) and not w.isdigit() and w not in out:
            out.append(w)
    return out


def clusters(items: list[Item]) -> dict[str, int]:
    """For each advert, how many others share two of its naming words: the same item, to be priced against."""
    index: dict[tuple[str, str], set[str]] = defaultdict(set)
    pairs_of: dict[str, list[tuple[str, str]]] = {}
    for item in items:
        pairs = list(combinations(sorted(informative(item.answer.title)[:4]), 2))
        pairs_of[item.id] = pairs
        for pair in pairs:
            index[pair].add(item.id)
    return {i: len(set().union(*(index[p] for p in pairs)) - {i}) if pairs else 0 for i, pairs in pairs_of.items()}


def readable(item: Item, lines_of) -> bool:
    """Whether the OCR read a code off any photo: letters and digits together, a model or a plate."""
    folder = Path(item.photos.cache or "")
    for photo in sorted(lines_of.photos(folder)):
        if any(_CODE.search(line.replace(" ", "")) for line in lines_of.lines(photo)):
            return True
    return False


def clean(items: list[Item], hashes: dict[str, list[str]]) -> tuple[list[Item], Counter]:
    """The adverts worth reading, and why the rest were left out."""
    kept: list[Item] = []
    dropped: Counter = Counter()
    photos_seen: set[str] = set()
    titles_seen: set[tuple[str, int]] = set()
    for item in sorted(items, key=lambda i: i.id):
        price = item.answer.price
        if item.tier == "not_for_sale" or price.kind == "wanted":
            dropped["a buyer's advert"] += 1
        elif not item.photos.count:
            dropped["no photo"] += 1
        elif placeholder(price.ngn):
            dropped["a placeholder price"] += 1
        elif photos_seen & set(hashes.get(item.id, ())):
            dropped["the same photos as another advert"] += 1
        elif (" ".join(item.answer.title.lower().split()), price.ngn) in titles_seen:
            dropped["the same title at the same price"] += 1
        else:
            kept.append(item)
            photos_seen.update(hashes.get(item.id, ()))
            titles_seen.add((" ".join(item.answer.title.lower().split()), price.ngn))
    return kept, dropped


def _tie(item_id: str) -> int:
    return int(hashlib.sha256(item_id.encode()).hexdigest(), 16)


def choose(items: list[Item], n: int, lines_of=None) -> tuple[list[Item], dict[str, dict]]:
    """Up to `n` adverts, taken in turn from every category and price band, the best of each first.

    Returns the chosen adverts and, for each, why it scored as it did."""
    near = clusters(items)
    why: dict[str, dict] = {}
    strata: dict[tuple[str, int], list[Item]] = defaultdict(list)
    for item in items:
        facts = {"same item in the pool": near[item.id],
                 "a code on a photo": bool(lines_of) and readable(item, lines_of),
                 "faulty or scrap": bool(FAULTY.search(item.answer.title))}
        facts["score"] = (2 * (facts["same item in the pool"] >= 2) + (facts["same item in the pool"] >= 5)
                          + facts["a code on a photo"] + facts["faulty or scrap"])
        why[item.id] = facts
        strata[(category(item), band(item.answer.price.ngn or 0))].append(item)
    for members in strata.values():
        members.sort(key=lambda i: (-why[i.id]["score"], _tie(i.id)))
    order = sorted(strata, key=lambda key: _tie(f"{key[0]}|{key[1]}"))
    chosen: list[Item] = []
    depth = 0
    while len(chosen) < n and any(len(strata[k]) > depth for k in order):
        for key in order:
            if len(strata[key]) > depth and len(chosen) < n:
                chosen.append(strata[key][depth])
        depth += 1
    return chosen, why


class PhotoLines:
    """The OCR cache's sure lines for a folder of photos, without reading any photo again."""

    def __init__(self, root: Path, cache) -> None:
        self.root, self.cache = root, cache

    def photos(self, folder: Path) -> list[Path]:
        where = self.root / folder
        return [p.relative_to(self.root) for p in where.iterdir()] if where.is_dir() else []

    def lines(self, photo: Path) -> list[str]:
        return self.cache.lines(self.root / photo)
