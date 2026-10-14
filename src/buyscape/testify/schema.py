"""One benchmark item: what a seller sent, and what turned out to be true.

The item is written so it can be published. It points at photos by link and
count, never by content. Every label says where it came from, so an asking
price is never mistaken for a settled one and a title is never mistaken for a
plate reading.
"""

from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, Field

Tier = Literal["branded_electronics", "small_goods", "material_lot", "adversarial", "not_for_sale"]
Decision = Literal["price", "ask_for_proof", "cannot_identify", "no_price_data", "fraud_suspected"]
PriceKind = Literal["settled", "sold", "asking", "wanted"]

# Adverts that ask to buy rather than offer to sell. They are not valuations.
WANTED = re.compile(r"\b(required|needed|wanted|we buy|buying|buyers?)\b", re.I)

# Categories whose items carry a brand and model, against those named by type
# or sold by weight. A category missing here is small goods: named by type.
TIERS: dict[str, Tier] = {
    "phone": "branded_electronics",
    "laptop": "branded_electronics",
    "television": "branded_electronics",
    "split_ac": "branded_electronics",
    "washing_machine": "branded_electronics",
    "generator": "branded_electronics",
    "vehicle": "branded_electronics",
    "material_lot": "material_lot",
}


def tier_for(category: str | None) -> Tier:
    return TIERS.get(category or "", "small_goods")


class Photos(BaseModel):
    """Where the photos are, without the photos."""

    count: int = 0
    public: bool = False
    cache: str | None = Field(None, description="Path under eval/raw, gitignored.")
    note: str = ""


class Identity(BaseModel):
    text: str | None = None
    source: Literal["title", "adjudicated", "none"] = "title"
    must_abstain: bool = False


class PriceTruth(BaseModel):
    ngn: int | None = None
    kind: PriceKind = "asking"
    used: bool | None = None
    note: str = ""


class Answer(BaseModel):
    """Never shown to a model under test."""

    title: str
    category: str | None = None
    kind: str | None = Field(None, description="The item in a buyer's words, from a hand label.")
    identity: Identity = Field(default_factory=Identity)
    price: PriceTruth = Field(default_factory=PriceTruth)
    hidden_condition: str = Field("unknown", description="Known only for the staged gold set.")


class RiskSeed(BaseModel):
    """A hidden risk drafted from the category protocol, pending human review."""

    risk: str
    proof: list[str] = Field(default_factory=list)
    worst_case: str | None = None
    pickup_check: str | None = None
    source: str
    reviewed: bool = False


class Baseline(BaseModel):
    """What one recorded model pair answered, read from its case report."""

    decision: Decision
    failure_code: str | None = None
    answer: str | None = None
    price_low: int | None = None
    price_high: int | None = None
    basis: str | None = None
    report: str


class Item(BaseModel):
    id: str
    source: Literal["jiji", "buyscrap", "staged"]
    url: str
    split: Literal["dev", "test", "train"]
    tier: Tier
    market: str = "lagos"
    currency: str = "NGN"
    photos: Photos = Field(default_factory=Photos)
    seller_text: str | None = None
    seller_claims: list[str] = Field(default_factory=list)
    answer: Answer
    risks: list[RiskSeed] = Field(default_factory=list)
    baselines: dict[str, Baseline] = Field(default_factory=dict)
    review: dict | None = Field(None, description="Photo review from eval/testify/review_dev.yaml, when one exists.")
    exclude: str | None = Field(None, description="Why the item is not scored, or None to score it.")


def split_for(item_id: str, dev_share: float = 0.25) -> Literal["dev", "test"]:
    """Stable split from the id, so reruns never move an item between splits."""
    bucket = int(hashlib.sha256(item_id.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    return "dev" if bucket < dev_share else "test"
