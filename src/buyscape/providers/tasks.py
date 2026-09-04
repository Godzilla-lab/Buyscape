"""Typed model tasks: the prompts and schemas live here, never in an adapter.

Each function builds a ModelRequest, calls the provider and returns a validated
object. Bumping a prompt_version deliberately invalidates recorded fixtures.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .base import CallMeta, ImageRef, ModelRequest, VisionProvider

HONESTY = (
    "You are grading second-hand goods for a buyback company. A wrong confident "
    "answer costs the company real money, an honest 'I cannot tell' costs "
    "nothing. Never guess a brand, model or number that you cannot actually "
    "read or clearly recognise in the images. When the evidence is not there, "
    "say so in the dedicated field and leave the value null."
)


class Reading(BaseModel):
    """What tier 1 could actually read and see. No opinions about identity."""

    category: str | None = Field(
        None,
        description=(
            "Broad kind of item in plain words, for example 'phone', "
            "'generator', 'split air conditioner', 'washing machine', "
            "'laptop'. Null if the photos do not show a single clear item."
        ),
    )
    category_confidence: float = Field(0.0, ge=0.0, le=1.0)
    visible_text: list[str] = Field(
        default_factory=list,
        description="Every legible line of text on the item, labels, plates and screens. Verbatim.",
    )
    brand_text: str | None = Field(
        None, description="Brand only if it is legible on the item or its label. Not inferred from shape."
    )
    model_text: str | None = Field(
        None, description="Model or part number only if legible on the item, label, plate or a Settings screen."
    )
    serial_text: str | None = None
    rating_text: str | None = Field(
        None, description="Capacity or rating as printed, for example '8kg', '1.5HP', '5.5kVA', '128GB'."
    )
    has_label_or_plate: bool = Field(
        False, description="True only if a data plate, sticker or Settings screen is legible in some photo."
    )
    is_screenshot: bool = False
    condition_notes: list[str] = Field(
        default_factory=list,
        description="Visible damage or wear only: cracks, rust, dents, missing parts, stains.",
    )
    multiple_items: bool = Field(
        False, description="True if the photos show several different items rather than one."
    )
    stock_photo_suspected: bool = Field(
        False,
        description="True if this looks like a manufacturer or catalogue image rather than a photo of a real unit.",
    )


class Candidate(BaseModel):
    brand: str
    model: str
    variant: str | None = None
    score: float = Field(0.0, ge=0.0, le=1.0)
    why: str = Field("", description="The specific evidence for this candidate.")


class Identification(BaseModel):
    """Tier 2 ranks supplied candidates. It may refuse."""

    candidates: list[Candidate] = Field(default_factory=list, max_length=5)
    chosen_brand: str | None = None
    chosen_model: str | None = None
    chosen_variant: str | None = None
    cannot_identify: bool = Field(
        False,
        description="True when the evidence does not support any single model. Prefer this over a guess.",
    )
    reason_if_cannot: str | None = None
    evidence_used: list[str] = Field(
        default_factory=list, description="Which specific things in the photos drove the answer."
    )


class ClaimDraft(BaseModel):
    text: str = Field(description="The seller's statement, quoted or closely paraphrased.")
    kind: str = Field(
        description="One of: works, spec, condition, provenance, included_parts, other."
    )
    attribute: str | None = Field(None, description="Short machine name, for example 'capacity_kg'.")
    value: str | None = None
    checkable_remotely: bool = Field(
        description="True only if a photo, screenshot or clip could prove this without handling the item."
    )


class ClaimSet(BaseModel):
    claims: list[ClaimDraft] = Field(default_factory=list, max_length=20)


def read_evidence(
    provider: VisionProvider, images: tuple[ImageRef, ...]
) -> tuple[Reading, CallMeta]:
    """Tier 1: read the item. Cheap model, high resolution, no identity guessing."""
    request = ModelRequest(
        task="read_evidence",
        prompt_version="read_evidence.v1",
        system=(
            f"{HONESTY}\n\n"
            "Your job is to READ and DESCRIBE, not to identify. Transcribe text "
            "exactly as printed, including model numbers that look like noise. "
            "Do not infer a brand from a logo shape or a housing colour: if the "
            "brand name is not legible somewhere, brand_text is null."
        ),
        user_text=(
            "Read this item. List every legible line of text, then fill in the "
            "brand, model, serial and rating fields only from text you can "
            "actually read. Note visible damage. Say if these look like "
            "catalogue images rather than photos of a real unit."
        ),
        output_schema=Reading,
        images=images,
        max_tokens=1600,
    )
    reading, meta = provider.structured_call(request)
    return reading, meta  # type: ignore[return-value]


def identify(
    provider: VisionProvider,
    images: tuple[ImageRef, ...],
    reading: Reading,
    candidates: list[str],
    seller_text: str,
) -> tuple[Identification, CallMeta]:
    """Tier 2: rank a supplied shortlist. Retrieval is what makes this work."""
    shortlist = "\n".join(f"- {c}" for c in candidates) if candidates else "(none found)"
    request = ModelRequest(
        task="identify",
        prompt_version="identify.v1",
        system=(
            f"{HONESTY}\n\n"
            "You are given photos, the text another system read off the item, "
            "the seller's own words, and a shortlist of catalogue entries. Pick "
            "the entry the evidence supports. You may pick something outside the "
            "shortlist only if the item's own label states it plainly. If two "
            "candidates fit about equally, or nothing fits, set cannot_identify "
            "and explain what evidence is missing. A shortlist entry is not "
            "proof: never choose one just because it is the only option."
        ),
        user_text=(
            f"Text read off the item:\n{reading.visible_text}\n\n"
            f"Brand read: {reading.brand_text}\nModel read: {reading.model_text}\n"
            f"Rating read: {reading.rating_text}\n"
            f"Label or plate legible: {reading.has_label_or_plate}\n\n"
            f"Seller says: {seller_text or '(nothing)'}\n\n"
            f"Catalogue shortlist:\n{shortlist}\n\n"
            "Rank up to five candidates with a score each, then give your choice "
            "or refuse."
        ),
        output_schema=Identification,
        images=images,
        max_tokens=1600,
    )
    ident, meta = provider.structured_call(request)
    return ident, meta  # type: ignore[return-value]


def extract_claims(provider: VisionProvider, seller_text: str) -> tuple[ClaimSet, CallMeta]:
    """Turn the seller's description into claims that evidence can be tied to."""
    request = ModelRequest(
        task="extract_claims",
        prompt_version="extract_claims.v1",
        system=(
            f"{HONESTY}\n\n"
            "Split the seller's description into separate factual claims about "
            "this item. Ignore sales talk, delivery terms, prices and contact "
            "details. Each claim must be something that could later be proven "
            "true or false at pickup."
        ),
        user_text=f"Seller's description:\n{seller_text}",
        output_schema=ClaimSet,
        images=(),
        max_tokens=1200,
    )
    claims, meta = provider.structured_call(request)
    return claims, meta  # type: ignore[return-value]
