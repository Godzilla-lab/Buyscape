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
        def search(rows: list[dict]) -> list[tuple[float, dict]]:
            found: list[tuple[float, dict]] = []
            for row in rows:
                have = set(tokens(row.get("title", "")))
                if not have:
                    continue
                if want_numeric and not want_numeric.issubset(have):
                    continue
                overlap = len(want & have) / len(want)
                if overlap >= 0.6:
                    found.append((overlap, row))
            return found

        scored = search([r for r in self._rows if r.get("category") == category])
        if not scored:
            # The category the model chose is not where the comps happen to be
            # filed. A model key is specific enough to search the whole pool:
            # every number in it must still appear in the comp's title.
            scored = search(self._rows)
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


class MaterialsFloor:
    """What an item is worth as raw material, whatever it turns out to be.

    This is what makes the engine open world. Identification lifts a price above
    this floor when it succeeds, but nothing ever falls through to no answer at
    all: a sewing machine nobody has a catalogue entry for is still fifteen
    kilos of cast iron. Weight cannot be seen from a photo, so the floor is
    always conditional on the scale reading at pickup, and it says so.
    """

    source_id = "materials_floor"

    def __init__(self, path: Path) -> None:
        data = yaml.safe_load(path.read_text())
        self._published: dict[str, list] = data.get("per_kg") or {}
        self._derived: dict[str, list] = data.get("per_kg_derived") or {}
        self._observed_on = str(data["observed_on"])
        self._url = data.get("url")
        # What the tenant itself advertises to buy at. Dated and attributable,
        # so it counts as published: it is the price this business pays.
        tenant = data.get("per_kg_tenant") or {}
        self._tenant: dict[str, list] = tenant.get("rates") or {}
        self._tenant_source = tenant.get("source")
        self._tenant_observed_on = str(tenant.get("observed_on") or self._observed_on)

    def rate(self, material: str) -> tuple[float, float, bool]:
        """Return low, high and whether the rate is published or derived."""
        key = (material or "unknown").strip().lower()
        if key in self._tenant:
            low, high = self._tenant[key]
            return float(low), float(high), True
        if key in self._published:
            low, high = self._published[key]
            return float(low), float(high), True
        if key in self._derived:
            low, high = self._derived[key]
            return float(low), float(high), False
        low, high = self._derived.get("unknown", [150, 400])
        return float(low), float(high), False

    def fetch(
        self, materials: list[tuple[str, float]], weight_kg: float | None
    ) -> list[Observation]:
        """Blend the per-kg rates by mass share and multiply by the weight."""
        if not weight_kg or weight_kg <= 0:
            raise SourceUnavailable("no weight estimate, so no material floor")
        shares = [(m, f) for m, f in materials if f > 0]
        if not shares:
            shares = [("unknown", 1.0)]
        total = sum(f for _, f in shares)
        shares = [(m, f / total) for m, f in shares]

        low = high = 0.0
        derived_used: list[str] = []
        for material, fraction in shares:
            r_low, r_high, published = self.rate(material)
            low += r_low * fraction * weight_kg
            high += r_high * fraction * weight_kg
            if not published:
                derived_used.append(material)

        breakdown = ", ".join(f"{m} {int(f * 100)}%" for m, f in shares)
        note = f"{weight_kg:g} kg of {breakdown}"
        if derived_used:
            note += f" (rates for {', '.join(sorted(set(derived_used)))} are estimates, not published)"
        return [
            Observation(
                source=self.source_id,
                kind="scrap_floor",
                amount=round(low, 2),
                currency="NGN",
                observed_on=self._observed_on,
                url=self._url,
                note=f"{note}, low",
            ),
            Observation(
                source=self.source_id,
                kind="scrap_floor",
                amount=round(high, 2),
                currency="NGN",
                observed_on=self._observed_on,
                url=self._url,
                note=f"{note}, high",
            ),
        ]


# How a Lagos seller writes a quantity. Tons dominate scrap adverts, and the
# number in the text is worth more than any estimate from a photograph: a heap
# of boards in a yard has no scale in frame, but the seller weighed it.
_QUANTITY = re.compile(
    r"(\d[\d,]*(?:\.\d+)?)\s*"
    r"(metric\s+tons?|tonnes?|tons?|kgs?|kilo(?:gram)?s?|g\b)",
    re.I,
)
_TO_KG = {"ton": 1000.0, "tonne": 1000.0, "metric ton": 1000.0, "kg": 1.0, "kilo": 1.0, "kilogram": 1.0, "g": 0.001}


def parse_stated_weight_kg(text: str) -> float | None:
    """The weight the seller stated, in kilograms, or None.

    For anything sold by weight this is the price, and no photograph can
    supply it: a yard of scrap boards has nothing in frame to give it scale.
    The seller does know, because they weighed it or bought it by the ton.

    Using their number cannot be exploited. Material is paid per kilogram
    against the scale at pickup, so overstating the tonnage moves the quoted
    total and never the rate. The seller is quoted a rate and an estimate, and
    the estimate is settled on the scale, which is exactly what the yard does.
    """
    best: float | None = None
    for amount, unit in _QUANTITY.findall(text or ""):
        try:
            value = float(amount.replace(",", ""))
        except ValueError:
            continue
        unit = unit.lower().rstrip("s").replace("metric ton", "ton")
        unit = {"tonne": "ton", "kgs": "kg", "kilogram": "kilo"}.get(unit, unit)
        factor = _TO_KG.get(unit)
        if factor is None:
            continue
        kilos = value * factor
        # Ignore obvious non weights: a 128gb phone, a 50 kg price typo.
        if 0.05 <= kilos <= 5_000_000 and (best is None or kilos > best):
            best = kilos
    return best
