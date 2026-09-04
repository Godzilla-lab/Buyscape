"""Identification as a chain of links, each one logged.

Order: read the item (tier 1), build a retrieval query from what was read plus
the seller's own words, search the catalogue, then let tier 2 rank that
shortlist with the photos in front of it. Abstention is decided by rules here,
outside the model, because models are known to recognise their own uncertainty
internally and still answer confidently.

The listing title is never an input. It is the answer key.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..providers.base import CallMeta, CostMeter, ImageRef, VisionProvider
from ..providers.tasks import Identification, Reading, identify, read_evidence
from .catalogue import Entry, search

# Two candidates within this score of each other is a coin toss, so refuse.
MIN_MARGIN = 0.15
# Without a label, plate or Settings screen, the reasoner must be very sure.
MIN_SCORE_NO_LABEL = 0.85
MIN_CATEGORY_CONFIDENCE = 0.50


@dataclass
class LinkLog:
    """One step of the chain, so a failure can be attributed to a link."""

    name: str
    outcome: str
    detail: str = ""
    meta: CallMeta | None = None


@dataclass
class ChainResult:
    category: str | None = None
    brand: str | None = None
    model: str | None = None
    variant: str | None = None
    candidates: list[tuple[str, float]] = field(default_factory=list)
    margin: float | None = None
    abstained: bool = False
    failure_code: str | None = None
    reason: str | None = None
    reading: Reading | None = None
    identification: Identification | None = None
    links: list[LinkLog] = field(default_factory=list)
    used_label: bool = False

    @property
    def model_key(self) -> str | None:
        if not (self.brand and self.model):
            return None
        parts = [self.brand, self.model]
        if self.variant:
            parts.append(self.variant)
        return " ".join(parts)


def build_query(reading: Reading, seller_text: str) -> str:
    """What we ask the catalogue. Only things the item or the seller said."""
    pieces: list[str] = []
    if reading.brand_text:
        pieces.append(reading.brand_text)
    if reading.model_text:
        pieces.append(reading.model_text)
    if reading.rating_text:
        pieces.append(reading.rating_text)
    pieces.extend(reading.visible_text[:12])
    if seller_text:
        pieces.append(seller_text[:400])
    return " ".join(pieces)


def run(
    images: tuple[ImageRef, ...],
    seller_text: str,
    catalogue: dict[str, list[Entry]],
    reader: VisionProvider,
    reasoner: VisionProvider,
    meter: CostMeter,
    category_hint: str | None = None,
) -> ChainResult:
    """Run the whole chain. Never raises for a bad item, it returns a failure."""
    result = ChainResult()

    if not images:
        result.failure_code = "EVIDENCE_INCOMPLETE"
        result.reason = "No photos were supplied."
        result.links.append(LinkLog("input", "fail", "no images"))
        return result

    # Link 1: read the item.
    reading, meta = read_evidence(reader, images)
    meter.record(meta)
    result.reading = reading
    result.used_label = reading.has_label_or_plate
    result.links.append(
        LinkLog(
            "read_evidence",
            "ok",
            f"category={reading.category} brand={reading.brand_text} "
            f"model={reading.model_text} label={reading.has_label_or_plate} "
            f"lines={len(reading.visible_text)}",
            meta,
        )
    )

    result.category = reading.category
    if reading.multiple_items:
        result.failure_code = "EVIDENCE_INCOMPLETE"
        result.reason = "The photos show more than one item, so nothing can be priced."
        result.links.append(LinkLog("gate", "abstain", "multiple items in frame"))
        return result
    if not reading.category or reading.category_confidence < MIN_CATEGORY_CONFIDENCE:
        result.failure_code = "CANNOT_IDENTIFY"
        result.abstained = True
        result.reason = "Could not tell what kind of item this is from the photos."
        result.links.append(
            LinkLog("gate", "abstain", f"category confidence {reading.category_confidence}")
        )
        return result

    # Link 2: retrieval.
    query = build_query(reading, seller_text)
    hits = search(catalogue, query, category_hint, limit=5)
    result.candidates = [(e.key, s) for e, s in hits]
    result.links.append(
        LinkLog(
            "retrieval",
            "ok" if hits else "empty",
            f"query='{query[:90]}' hits={[e.key for e, _ in hits]}",
        )
    )

    # Link 3: the reasoner ranks the shortlist with the photos present.
    ident, meta2 = identify(
        reasoner, images, reading, [e.key for e, _ in hits], seller_text
    )
    meter.record(meta2)
    result.identification = ident
    scores = sorted((c.score for c in ident.candidates), reverse=True)
    result.margin = round(scores[0] - scores[1], 4) if len(scores) >= 2 else None
    result.links.append(
        LinkLog(
            "identify",
            "refused" if ident.cannot_identify else "ok",
            f"chosen={ident.chosen_brand} {ident.chosen_model} margin={result.margin}",
            meta2,
        )
    )

    # Link 4: abstention rules, applied outside the model.
    if ident.cannot_identify or not (ident.chosen_brand and ident.chosen_model):
        result.abstained = True
        result.failure_code = "CANNOT_IDENTIFY"
        result.reason = ident.reason_if_cannot or "The model declined to identify this item."
        result.links.append(LinkLog("abstain", "abstain", "model refused"))
        return result

    top = scores[0] if scores else 0.0
    if result.margin is not None and result.margin < MIN_MARGIN:
        result.abstained = True
        result.failure_code = "CANNOT_IDENTIFY"
        result.reason = (
            f"Two candidates scored within {result.margin} of each other, "
            "which is too close to call remotely."
        )
        result.links.append(LinkLog("abstain", "abstain", f"margin {result.margin}"))
        return result
    if not reading.has_label_or_plate and top < MIN_SCORE_NO_LABEL:
        result.abstained = True
        result.failure_code = "CANNOT_IDENTIFY"
        result.reason = (
            "No label, plate or settings screen was legible, and the visual "
            f"match alone scored only {top}."
        )
        result.links.append(LinkLog("abstain", "abstain", f"no label, top score {top}"))
        return result

    result.brand = ident.chosen_brand
    result.model = ident.chosen_model
    result.variant = ident.chosen_variant
    result.links.append(LinkLog("abstain", "pass", f"top={top} margin={result.margin}"))
    return result
