"""One case in, one report out.

This is the whole engine for the proof: read, retrieve, identify or abstain,
extract claims, tie them to evidence, price from stored observations or fail
loudly. No server, no database. State is the report.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

from .claims.ledger import Claim, ClaimStatus, build_ledger
from .identify import chain
from .identify.catalogue import Entry
from .pricing.engine import Quote, price
from .pricing.sources import (
    JijiComps,
    MaterialsFloor,
    ScrapIndex,
    SourceUnavailable,
    parse_rating,
)
from .protocols.schema import Protocol
from .providers.base import CostMeter, ImageRef, ProviderError, VisionProvider
from .providers.tasks import extract_claims


@dataclass
class Case:
    """The input. `truth` is only ever read by the scorer, never by the engine."""

    id: str
    images: list[Path]
    seller_text: str = ""
    category_hint: str | None = None
    slots_present: set[str] = field(default_factory=set)
    truth: dict = field(default_factory=dict)


@dataclass
class CaseResult:
    case_id: str
    chain: chain.ChainResult
    ledger: list[Claim]
    quote: Quote
    cost_usd: float
    latency_ms: int
    cost_by_task: dict[str, float]
    reader_model: str
    reasoner_model: str
    error: str | None = None

    @property
    def identified(self) -> bool:
        return bool(self.chain.model_key) and not self.chain.abstained


def run_case(
    case: Case,
    protocols: dict[str, Protocol],
    catalogue: dict[str, list[Entry]],
    comps: JijiComps,
    scrap: ScrapIndex,
    reader: VisionProvider,
    reasoner: VisionProvider,
    materials: MaterialsFloor | None = None,
) -> CaseResult:
    meter = CostMeter()
    images = tuple(ImageRef(p) for p in case.images)

    try:
        result = chain.run(
            images,
            case.seller_text,
            catalogue,
            reader,
            reasoner,
            meter,
            case.category_hint,
        )
    except ProviderError as exc:
        return CaseResult(
            case_id=case.id,
            chain=chain.ChainResult(failure_code="PROVIDER_ERROR", reason=str(exc)),
            ledger=[],
            quote=Quote(failure_code="PROVIDER_ERROR", reason=str(exc)),
            cost_usd=meter.total_usd,
            latency_ms=meter.total_ms,
            cost_by_task=meter.by_task(),
            reader_model=reader.model,
            reasoner_model=reasoner.model,
            error=str(exc),
        )

    category = result.category or case.category_hint or "generic"
    protocol = protocols.get(category) or protocols["generic"]

    ledger: list[Claim] = []
    if case.seller_text.strip():
        try:
            drafts, meta = extract_claims(reasoner, case.seller_text)
            meter.record(meta)
            ledger = build_ledger(drafts.claims, protocol, case.slots_present)
        except ProviderError:
            ledger = []

    # Any shot the protocol requires that the seller never sent is an unproven
    # condition in its own right, so it is recorded like a claim.
    missing = [s for s in protocol.required_shots if s.id not in case.slots_present]
    for shot in missing:
        ledger.append(
            Claim(
                text=f"Required evidence '{shot.id}' was not supplied",
                kind="condition",
                attribute=None,
                value=None,
                status=ClaimStatus.UNVERIFIED,
                required_evidence=[shot.id],
                worst_case="priced as if the worst case is true",
                pickup_check=shot.ask,
                penalty=0.95,
            )
        )

    reading = result.reading
    material_obs: list = []
    weight_confident = False
    if materials is not None and reading is not None:
        shares = [(m.material, m.fraction) for m in reading.materials]
        weight = reading.estimated_weight_kg
        weight_confident = (reading.weight_confidence or 0.0) >= 0.6
        try:
            material_obs = materials.fetch(shares, weight)
        except SourceUnavailable:
            material_obs = []

    identified = bool(result.model_key) and not result.abstained

    comp_obs: list = []
    scrap_obs: list = []
    if identified:
        try:
            comp_obs = comps.fetch(category, result.model_key or "")
        except SourceUnavailable:
            comp_obs = []
        rating = parse_rating(
            " ".join(
                filter(
                    None,
                    [
                        reading.rating_text if reading else None,
                        result.model_key,
                        case.seller_text,
                    ],
                )
            )
        )
        try:
            scrap_obs = scrap.fetch(category, rating)
        except SourceUnavailable:
            scrap_obs = []

    quote = price(
        comp_obs,
        scrap_obs,
        ledger,
        materials=material_obs,
        identified=identified,
        weight_confident=weight_confident,
    )
    if result.fraud_flags:
        quote.conditions = [f"Evidence flag: {f}" for f in result.fraud_flags] + quote.conditions
    if not identified and not quote.is_failure and result.reason:
        quote.conditions.insert(0, f"Not identified: {result.reason}")

    return CaseResult(
        case_id=case.id,
        chain=result,
        ledger=ledger,
        quote=quote,
        cost_usd=meter.total_usd,
        latency_ms=meter.total_ms,
        cost_by_task=meter.by_task(),
        reader_model=reader.model,
        reasoner_model=reasoner.model,
    )


def report_markdown(case: Case, result: CaseResult) -> str:
    """A case report a non-engineer can read and check."""
    c = result.chain
    lines: list[str] = [
        f"# Case {case.id}",
        "",
        f"Photos: {len(case.images)}  |  reader: {result.reader_model}  |  "
        f"reasoner: {result.reasoner_model}  |  cost: ${result.cost_usd:.4f}  |  "
        f"{result.latency_ms} ms",
        "",
        "## What the engine saw",
    ]
    if c.reading:
        r = c.reading
        materials = ", ".join(f"{m.material} {int(m.fraction * 100)}%" for m in r.materials)
        lines += [
            f"- Presentation: {r.presentation}",
            f"- Category: {r.category} (confidence {r.category_confidence})",
            f"- Made of: {materials or 'not stated'}",
            f"- Estimated weight: {r.estimated_weight_kg or 'unknown'} kg "
            f"(confidence {r.weight_confidence})",
            f"- Brand read off the item: {r.brand_text or 'nothing legible'}",
            f"- Model read off the item: {r.model_text or 'nothing legible'}",
            f"- Rating read: {r.rating_text or 'none'}",
            f"- Label, plate or settings screen legible: {'yes' if r.has_label_or_plate else 'no'}",
            f"- Damage noted: {', '.join(r.condition_notes) or 'none'}",
            f"- Looks like a catalogue image: {'yes' if r.stock_photo_suspected else 'no'}",
            f"- Screenshot of a gallery: {'yes' if r.screenshot_of_gallery else 'no'}",
        ]
        if r.visible_text:
            lines.append(f"- Text read: {' | '.join(r.visible_text[:8])}")
    lines += ["", "## Chain"]
    for link in c.links:
        lines.append(f"- **{link.name}** -> {link.outcome}. {link.detail}")

    lines += ["", "## Identification"]
    if c.candidates:
        lines.append("Shortlist from the catalogue:")
        lines += [f"  - {k} ({s})" for k, s in c.candidates]
    else:
        lines.append("No catalogue candidates matched.")
    if result.identified:
        lines.append(f"\n**Answer: {c.model_key}** (margin {c.margin})")
    else:
        lines.append(f"\n**Not identified: {c.failure_code}.** {c.reason}")
    if c.fraud_flags:
        lines.append("\nEvidence flags: " + "; ".join(c.fraud_flags))

    lines += ["", "## Claims"]
    if result.ledger:
        for claim in result.ledger:
            mark = "proven" if claim.status == ClaimStatus.SUPPORTED else f"{claim.status}"
            lines.append(f"- [{mark}] {claim.text}")
            if claim.is_priced_at_worst_case and claim.worst_case:
                lines.append(f"    priced as: {claim.worst_case}. {claim.pickup_check or ''}")
    else:
        lines.append("No claims were extracted.")

    q = result.quote
    lines += ["", "## Price"]
    if q.is_failure:
        lines.append(f"**{q.failure_code}.** {q.reason}")
    else:
        basis = {
            "resale": "priced as a working item",
            "material_floor": "priced as material",
            "retail_new": "priced against new retail",
        }.get(q.basis, q.basis)
        lines.append(
            f"**{int(q.low):,} to {int(q.high):,} {q.currency}** ({basis}, "
            f"width {q.width_ratio}, method {q.method}, "
            f"{q.observation_count} comparable prices)"
        )
        if q.weight_conditional:
            lines.append(
                "\nThe weight is estimated from the photos, so this price is "
                "settled on the scale at pickup."
            )
        lines.append(f"\n{q.explanation}")
        if q.floor:
            lines.append(f"\nScrap floor: {int(q.floor):,} {q.currency}")
    if q.conditions:
        lines += ["", "Conditions attached to this price:"]
        lines += [f"- {c_}" for c_ in q.conditions]

    if case.truth:
        lines += ["", "## Answer key (not shown to the engine)", f"`{case.truth}`"]
    return "\n".join(lines) + "\n"
