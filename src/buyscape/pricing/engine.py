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
    low: float | None = None
    high: float | None = None
    currency: str = "NGN"
    floor: float | None = None
    ceiling: float | None = None
    failure_code: str | None = None
    reason: str | None = None
    conditions: list[str] = field(default_factory=list)
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


def price(
    comps: list[Observation],
    scrap: list[Observation],
    ledger: list[Claim],
    currency: str = "NGN",
) -> Quote:
    """Build the range. Refuses when the evidence for a number is not there."""
    quote = Quote(currency=currency)
    quote.conditions = conditions(ledger)
    quote.worst_case_multiplier = worst_case_multiplier(ledger)

    scrap_values = [o.amount for o in scrap]
    if scrap_values:
        quote.floor = min(scrap_values)
        quote.sources.append(scrap[0].source)

    comp_values = [o.amount for o in comps]
    quote.observation_count = len(comp_values)

    if len(comp_values) < MIN_OBSERVATIONS:
        if len(scrap_values) >= 2:
            # Fall back to the published whole-unit band. Wide and honest.
            low = min(scrap_values) * quote.worst_case_multiplier
            high = max(scrap_values)
            quote.low, quote.high = round(low, 2), round(high, 2)
            quote.ceiling = high
            quote.method = "scrap_band_only"
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
