"""What a model under test, or the small model being trained, must answer.

One JSON object per item, checked by code before it is scored. The shape
follows rule 4: the model never writes a price. It is shown a numbered list
of retrieved comparables, each with a source and a date, and it picks the low
and the high by their numbers. The range is then read off the list, so a
number the model makes up has nowhere to go. Any naira amount written into
its free text is a violation, and so is a pick outside the list.

Observations come first so a model writes what it sees before it decides,
and the decision is one of the engine's loud outcomes. The schema exported
from here is what constrained decoding uses at inference.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from .schema import Decision

Verdict = Literal["supported", "contradicted", "unverified", "unverifiable_remote"]
IdentityStatus = Literal["named", "by_type", "unknown"]

# A price in free text: "N50,000", "₦ 50000", "50k naira", "NGN 1.2m".
_MONEY = re.compile(
    r"(₦|\bN(?=\s?\d)|\bNGN\b)\s?\d[\d,.]*\s?[km]?\b|\b\d[\d,.]*\s?[km]?\s?(naira|ngn)\b",
    re.IGNORECASE,
)


class IdentityAnswer(BaseModel):
    status: IdentityStatus = Field(
        description="named: a brand and model read off the item. by_type: a kind in a buyer's words, "
        "for items that carry no model. unknown: the photos do not say."
    )
    kind: str | None = Field(None, description="The item in a buyer's words, for example 'standing fan'.")
    brand: str | None = None
    model: str | None = None
    read_from: list[str] = Field(
        default_factory=list,
        description="Where the identity was read: 'photo 2 plate', 'photo 1 screen'. Never the seller's text alone.",
    )


class ClaimAnswer(BaseModel):
    claim: str = Field(description="The seller's statement, quoted or shortened.")
    verdict: Verdict
    evidence: str = Field("", description="The photo that proves or contradicts it, or what is missing.")


class RiskAnswer(BaseModel):
    risk: str = Field(description="Something that could be wrong and that the photos cannot show.")
    proof: str = Field(description="The one shot, screenshot or clip that would settle it.")
    if_unproven: str = Field(description="How it is priced until proven, for example 'as not working'.")


class PricePick(BaseModel):
    low: int = Field(ge=0, description="Number of the comparable to use as the low end.")
    high: int = Field(ge=0, description="Number of the comparable to use as the high end.")

    @model_validator(mode="after")
    def _ordered(self) -> PricePick:
        if self.low > self.high:
            raise ValueError("low pick is after the high pick")
        return self


class Reading(BaseModel):
    """The first of two steps: everything but the price.

    The comparables are retrieved for the identity the model gives here, the
    way the engine retrieves candidates only after it has read the item. So a
    wrong identity brings the wrong comparables, and the price shows it.
    """

    observations: list[str] = Field(description="What the photos show, before any decision. Short lines.")
    identity: IdentityAnswer
    claims: list[ClaimAnswer] = Field(default_factory=list)
    risks: list[RiskAnswer] = Field(default_factory=list)
    proof_requests: list[str] = Field(
        default_factory=list, description="What to ask the seller for next, most decisive first."
    )
    decision: Decision
    reason: str = Field(description="One or two sentences. No prices.")

    @model_validator(mode="after")
    def _identity_consistent(self) -> Reading:
        if self.decision == "price" and self.identity.status == "unknown":
            raise ValueError("cannot price an item whose identity is unknown")
        if self.decision == "cannot_identify" and self.identity.status != "unknown":
            raise ValueError("cannot_identify with a known identity")
        if self.identity.status == "named" and not (self.identity.brand or self.identity.model):
            raise ValueError("a named identity needs a brand or a model")
        if self.identity.status == "named" and not self.identity.read_from:
            raise ValueError("a named identity must say which photo it was read from")
        return self


class PriceChoice(BaseModel):
    """The second step: pick the range from the comparables, or refuse them all."""

    same_item: bool = Field(description="False when none of the comparables is the same kind of item.")
    price_pick: PricePick | None = Field(
        None, description="The cheapest and dearest comparable that fit the item as seen and as proven."
    )
    reason: str = Field(description="One sentence on why these comparables. No prices.")


class InspectionAnswer(Reading):
    price_pick: PricePick | None = Field(
        None, description="Only when decision is price: comparables sorted cheapest first, picked by number."
    )

    @model_validator(mode="after")
    def _consistent(self) -> InspectionAnswer:
        if self.decision == "price":
            if self.price_pick is None:
                raise ValueError("decision price needs a price_pick")
        elif self.price_pick is not None:
            raise ValueError(f"decision {self.decision} must not pick a price")
        return self


# Doubt written into a name: "(exact model code not legible)", "IS II or STM".
_DOUBT = re.compile(
    r"\bor\b|\?|possibl|likely|probabl|presumabl|maybe|appears|uncertain|unclear|unknown|unreadable"
    r"|unconfirmed|not (visible|readable|legible|confirmed|shown)|partially legible|\bassumed?\b",
    re.IGNORECASE,
)


def quote(reading: dict, choice: dict | None = None) -> dict:
    """The binding part of an answer: what is bought, at which picks, on which conditions.

    Bergemann et al. (arXiv 2604.16472) score bargaining by separating binding
    offers from natural-language messages. Here the quote is the decision,
    the identity it commits to, the picks and the conditions (each risk's
    "until proven" and each claim left unproven). Every price score reads the
    quote. The fields already have this shape, so recorded answers need no
    conversion.
    """
    identity = reading.get("identity") or {}
    conditions = [r.get("if_unproven") for r in reading.get("risks") or [] if r.get("if_unproven")]
    conditions += [f"{c.get('claim')}: priced as unproven" for c in reading.get("claims") or []
                   if c.get("verdict") in ("unverified", "unverifiable_remote")]
    return {
        "decision": reading.get("decision"),
        "identity": {k: identity.get(k) for k in ("status", "kind", "brand", "model")},
        "pick": (choice or {}).get("price_pick") or reading.get("price_pick"),
        "conditions": conditions,
    }


def message(reading: dict, choice: dict | None = None) -> list[str]:
    """The prose around the quote. It explains and binds nothing."""
    lines = [*(reading.get("observations") or []), reading.get("reason") or ""]
    lines += [c.get("evidence") or "" for c in reading.get("claims") or []]
    lines.append((choice or {}).get("reason") or "")
    return [line for line in lines if line]


def hedged_name(identity: dict) -> bool:
    """A named identity whose own brand or model says it is not sure.

    Committing to a name and writing the doubt into it ("7kg, exact code
    unclear") is hedging inside the quote: the price follows the name, not
    the doubt."""
    if identity.get("status") != "named":
        return False
    return bool(_DOUBT.search(f"{identity.get('brand') or ''} {identity.get('model') or ''}"))


def violations(answer: InspectionAnswer, comparables: int) -> list[str]:
    """Rule breaks the schema cannot see. Empty means the answer may be scored."""
    found: list[str] = []
    if answer.price_pick and answer.price_pick.high >= comparables:
        found.append(f"picked comparable {answer.price_pick.high}, but only {comparables} were given")
    return found + money_written(answer)


def money_written(answer: Reading) -> list[str]:
    """Every free-text line that writes a price, which only retrieval may do."""
    texts = [answer.reason, *answer.observations, *answer.proof_requests]
    texts += [c.evidence for c in answer.claims] + [r.if_unproven for r in answer.risks]
    return [f"wrote a price, which only retrieval may do: {text!r}" for text in texts if _MONEY.search(text or "")]


def parse(raw: str, comparables: int) -> tuple[InspectionAnswer | None, list[str]]:
    """Parse a model's raw output. Never raises: a bad answer is a scored failure."""
    try:
        answer = InspectionAnswer.model_validate_json(raw)
    except ValueError as exc:
        return None, [f"not a valid answer: {str(exc).splitlines()[0]}"]
    return answer, violations(answer, comparables)


def export_schema(path: Path) -> None:
    path.write_text(json.dumps(InspectionAnswer.model_json_schema(), indent=1) + "\n")
