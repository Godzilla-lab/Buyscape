"""Price sources produce observations. Nothing here invents a number.

Two sources are enough for the proof: comparable asking prices scraped from
Jiji, and the Lagos scrap and item price list. Both carry a date and a URL, and
both refuse rather than extrapolate when they have nothing to say.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from ..identify.catalogue import tokens


@dataclass(frozen=True)
class Observation:
    """One price point with its provenance."""

    source: str
    kind: str  # asking | scrap_floor | rate_card | settled
    amount: float
    currency: str
    observed_on: str
    url: str | None = None
    note: str = ""
    is_used: bool = True


class SourceUnavailable(RuntimeError):
    """The source has nothing for this item. Callers must not substitute."""


class JijiComps:
    """Asking prices for used items, from the cached listing set.

    Asking is not sold. The pricing engine applies a discount factor to turn
    one into the other, and that factor is the first thing calibration should
    replace with a measured number.
    """

    source_id = "jiji_asking"

    def __init__(self, cache_dir: Path, exclude_ids: frozenset[str] = frozenset()) -> None:
        self._rows: list[dict] = []
        for path in sorted(cache_dir.glob("*.json")):
            for row in json.loads(path.read_text()):
                if row.get("id") in exclude_ids:
                    continue
                if not row.get("is_used"):
                    continue  # a dealer's new stock is not a used-price comp
                self._rows.append(row)

    def fetch(self, category: str, model_key: str, limit: int = 12) -> list[Observation]:
        want = set(tokens(model_key))
        if not want:
            raise SourceUnavailable("no model key to search on")
        # Model numbers are what separate an iPhone 13 from an iPhone 14, so
        # every digit-bearing token in the key must appear in the comp. Token
        # overlap alone silently prices one model off another.
        want_numeric = {t for t in want if any(ch.isdigit() for ch in t)}
        scored: list[tuple[float, dict]] = []
        for row in self._rows:
            if row.get("category") != category:
                continue
            have = set(tokens(row.get("title", "")))
            if not have:
                continue
            if want_numeric and not want_numeric.issubset(have):
                continue
            overlap = len(want & have) / len(want)
            if overlap >= 0.6:
                scored.append((overlap, row))
        if not scored:
            raise SourceUnavailable(f"no used comps for {model_key!r}")
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [
            Observation(
                source=self.source_id,
                kind="asking",
                amount=float(row["price_ngn"]),
                currency="NGN",
                observed_on=str(row.get("fetched_at", ""))[:10],
                url=row.get("url"),
                note=row.get("title", "")[:80],
            )
            for _, row in scored[:limit]
        ]


class ScrapIndex:
    """The Lagos published list: per-kg grades and whole-unit buy ranges."""

    source_id = "scrap_index_lagos"

    def __init__(self, path: Path) -> None:
        self._data = yaml.safe_load(path.read_text())
        self._observed_on = str(self._data["observed_on"])
        self._url = self._data.get("url")
        self._max_age = int(self._data.get("max_age_days", 365))

    @property
    def age_days(self) -> int:
        observed = dt.date.fromisoformat(self._observed_on)
        return (dt.date.today() - observed).days

    @property
    def is_stale(self) -> bool:
        return self.age_days > self._max_age

    def fetch(self, category: str, rating: float | None = None) -> list[Observation]:
        if self.is_stale:
            raise SourceUnavailable(
                f"price list is {self.age_days} days old, past its "
                f"{self._max_age} day limit"
            )
        rules = (self._data.get("items") or {}).get(category)
        if not rules:
            raise SourceUnavailable(f"no published range for {category}")
        chosen = None
        for rule in rules:
            cap = rule.get("max_kva")
            if cap is None or (rating is not None and rating <= float(cap)):
                chosen = rule
                break
        if chosen is None:
            raise SourceUnavailable(
                f"{category} rating {rating} is above the published bands; "
                "site assessment required"
            )
        low, high = chosen["range"]
        note = "derived from scrap mass, not a published price" if chosen.get("derived") else "published list"
        return [
            Observation(
                source=self.source_id,
                kind="scrap_floor",
                amount=float(low),
                currency="NGN",
                observed_on=self._observed_on,
                url=self._url,
                note=f"{note} (low)",
            ),
            Observation(
                source=self.source_id,
                kind="scrap_floor",
                amount=float(high),
                currency="NGN",
                observed_on=self._observed_on,
                url=self._url,
                note=f"{note} (high)",
            ),
        ]


_RATING = re.compile(r"(\d+(?:\.\d+)?)\s*(kva|hp|kg)", re.I)


def parse_rating(text: str) -> float | None:
    """Pull a kVA, HP or kg number out of free text."""
    m = _RATING.search(text or "")
    return float(m.group(1)) if m else None
