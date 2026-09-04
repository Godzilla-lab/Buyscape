"""Turn observations plus the claims ledger into a range, or a loud failure.

The model is never asked for a number. Prices come from stored observations,
and when there are not enough of them the answer is NO_PRICE_DATA, not a guess.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field

from ..claims.ledger import Claim, conditions, worst_case_multiplier
from .sources import Observation

# Asking price is not sold price. Until settlements exist, this is the honest
# spread between what a Lagos seller asks and what a buyback pays. Calibration
# replaces it with a measured number as soon as there are settled pickups.
ASK_TO_BUY = (0.45, 0.70)
MIN_OBSERVATIONS = 2


@dataclass
class Quote:
    basis: str = "resale"  # resale | material_floor | retail_new
    low: float | None = None
    high: float | None = None
    currency: str = "NGN"
    floor: float | None = None
    ceiling: float | None = None
    failure_code: str | None = None
    reason: str | None = None
    conditions: list[str] = field(default_factory=list)
    weight_conditional: bool = False
    worst_case_multiplier: float = 1.0
    observation_count: int = 0
    sources: list[str] = field(default_factory=list)
    method: str = "uncalibrated_wide"
    explanation: str = ""

    @property
    def is_failure(self) -> bool:
        return self.failure_code is not None

    @property
    def width_ratio(self) -> float | None:
        if self.low is None or self.high is None or self.high <= 0:
            return None
        mid = (self.low + self.high) / 2
        return round((self.high - self.low) / mid, 4) if mid else None


def _quantile(values: list[float], q: float) -> float:
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    return float(statistics.quantiles(ordered, n=100, method="inclusive")[int(q * 100) - 1])


def cap_at_asking(quote: Quote, asking: float | None) -> Quote:
    """A buyback never offers more than the seller is asking.

    Ten tons of circuit boards offered at four times the asking price is not
    generosity, it is a rate estimate escaping into the real world. The seller
    named their price, so that is the ceiling, whatever the per kilogram
    estimate says. The floor is untouched: if the material really is worth
    more, the agent finds that out on the scale and the seller keeps the
    difference they asked for.
    """
    if asking is None or asking <= 0 or quote.is_failure or quote.high is None:
        return quote
    if quote.high > asking:
        quote.high = round(asking, 2)
        quote.low = round(min(quote.low or asking, asking), 2)
        quote.ceiling = round(asking, 2)
        quote.conditions.insert(
            0,
            "Capped at the price the seller asked for: the engine never offers "
            "more than that, whatever the material rate suggests.",
        )
    return quote


def price(
    comps: list[Observation],
    scrap: list[Observation],
    ledger: list[Claim],
    currency: str = "NGN",
    materials: list[Observation] | None = None,
    identified: bool = True,
    weight_confident: bool = False,
) -> Quote:
    """Build the range.

    Anything at all can be bought for its material, so an unidentified item
    falls through to the material floor rather than to no answer. Identification
    is what lifts a price above that floor, never what decides whether a price
    exists at all.
    """
    quote = Quote(currency=currency)
    quote.conditions = conditions(ledger)
    quote.worst_case_multiplier = worst_case_multiplier(ledger)
    materials = materials or []

    material_values = [o.amount for o in materials]
    if material_values:
        quote.floor = min(material_values)
        quote.sources.append(materials[0].source)

    scrap_values = [o.amount for o in scrap]
    if scrap_values:
        floor = min(scrap_values)
        quote.floor = floor if quote.floor is None else max(quote.floor, floor)
        quote.sources.append(scrap[0].source)

    comp_values = [o.amount for o in comps] if identified else []
    quote.observation_count = len(comp_values)

    # Not identified, but made of something. Price the material and say so.
    if not identified:
        if not material_values:
            quote.failure_code = "CANNOT_IDENTIFY"
            quote.reason = (
                "The item could not be identified and the photos give no sense "
                "of its size or material, so not even a scrap value can be "
                "estimated. A photo showing the whole item next to something "
                "of known size would fix this."
            )
            return quote
        quote.basis = "material_floor"
        quote.method = "material_floor"
        quote.weight_conditional = not weight_confident
        quote.low = round(min(material_values) * quote.worst_case_multiplier, 2)
        quote.high = round(max(material_values), 2)
        quote.explanation = (
            "This item was not identified, so it is priced as material rather "
            f"than as a working item: {materials[0].note.rsplit(',', 1)[0]}. "
            "Anything it is worth above scrap needs a clearer photo of its "
            "label or plate. The weight is an estimate from the photos and the "
            "price is settled on the scale at pickup."
        )
        return quote

    if len(comp_values) < MIN_OBSERVATIONS:
        if len(scrap_values) >= 2 or len(material_values) >= 2:
            band = scrap_values if len(scrap_values) >= 2 else material_values
            # Fall back to the published whole-unit band. Wide and honest.
            low = min(band) * quote.worst_case_multiplier
            high = max(band)
            quote.low, quote.high = round(low, 2), round(high, 2)
            quote.ceiling = high
            quote.method = "scrap_band_only"
            quote.basis = "material_floor"
            quote.explanation = (
                f"No usable comparable sales ({len(comp_values)} found, "
                f"{MIN_OBSERVATIONS} needed), so the range comes from the "
                f"published Lagos buy band for this category, reduced by "
                f"{quote.worst_case_multiplier} for unproven claims."
            )
            return quote
        quote.failure_code = "NO_PRICE_DATA"
        quote.reason = (
            f"Only {len(comp_values)} comparable asking prices were found and "
            "there is no published band for this category, so no honest range "
            "can be produced."
        )
        return quote

    if comps:
        quote.sources.append(comps[0].source)
    low_ask = _quantile(comp_values, 0.20)
    high_ask = _quantile(comp_values, 0.80)
    low = low_ask * ASK_TO_BUY[0] * quote.worst_case_multiplier
    high = high_ask * ASK_TO_BUY[1]
    if quote.floor is not None:
        low = max(low, quote.floor)
        high = max(high, quote.floor)

    quote.low, quote.high = round(low, 2), round(high, 2)
    quote.ceiling = round(high_ask, 2)
    quote.explanation = (
        f"{len(comp_values)} used asking prices, 20th to 80th percentile "
        f"{int(low_ask):,} to {int(high_ask):,} {currency}, converted to a buy "
        f"range with the {ASK_TO_BUY[0]} to {ASK_TO_BUY[1]} ask-to-buy spread"
        + (
            f", then reduced by {quote.worst_case_multiplier} for unproven claims"
            if quote.worst_case_multiplier < 1.0
            else ""
        )
        + (f", floored at the scrap value {int(quote.floor):,}" if quote.floor else "")
        + "."
    )
    return quote
