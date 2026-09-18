"""One case in, one report out.

This is the whole engine for the proof: read, retrieve, identify or abstain,
extract claims, tie them to evidence, price from stored observations or fail
loudly. No server, no database. State is the report.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from dataclasses import asdict, dataclass, field
from pathlib import Path

from .answers import review_answers, unanswered
from .assess import Assessment, CaptureRequest, assess, capture_requests
from .claims.crosscheck import CrossCheck, Testimony, crosscheck
from .claims.ledger import Claim, ClaimStatus, build_ledger
from .identify import chain
from .identify.ocr import OcrReader
from .identify.catalogue import Entry, tokens
from .pricing.engine import MIN_OBSERVATIONS, Quote, cap_at_asking, price
from .pricing.sources import (
    JijiComps,
    MaterialsFloor,
    ScrapIndex,
    SourceUnavailable,
    parse_rating,
    parse_stated_weight_kg,
)
from .protocols.schema import Protocol, resolve
from .tenant import Tenant
from .providers.base import CostMeter, ImageRef, MissingFixture, ProviderError, VisionProvider
from .providers.tasks import extract_claims


@dataclass
class Case:
    """The input. `truth` is only ever read by the scorer, never by the engine."""

    id: str
    images: list[Path]
    seller_text: str = ""
    category_hint: str | None = None
    slots_present: set[str] = field(default_factory=set)
    # What the seller says they want for it, when they have said. A production
    # input, never taken from the answer key: it caps the offer, never raises it.
    asking_price: float | None = None
    # What the seller answered when asked. Only they know the age, the drops
    # and whether it still holds charge, and those move the price most.
    answers: dict[str, str] = field(default_factory=dict)
    # What the item said about itself, one record per protocol shot, and the
    # opening shots the seller declined. Both are inputs, never model output.
    testimony: list[Testimony] = field(default_factory=list)
    # What the seller picked on the tenant's page, so staff questions for
    # that category are still honoured after the reader renames the item.
    tenant_category: str | None = None
    # Told 'reading', 'deciding', 'pricing' as the work moves, for the page.
    progress: Callable[[str], None] | None = field(default=None, compare=False, repr=False)
    refused_slots: set[str] = field(default_factory=set)
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
    crosscheck: CrossCheck | None = None
    assessment: Assessment | None = None
    asks: list[CaptureRequest] = field(default_factory=list)
    questions: list = field(default_factory=list)
    answer_notes: list[str] = field(default_factory=list)
    spent_usd: float = 0.0  # cost_usd counts replayed calls at their recorded price; this does not
    timing: list[dict] = field(default_factory=list)
    # Calls overlap when they run in parallel, so this is what a seller waited.
    wall_ms: int = 0

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
    corroborator: VisionProvider | None = None,
    tenant: Tenant | None = None,
    ocr: OcrReader | None = None,
) -> CaseResult:
    meter = CostMeter()
    started = time.perf_counter()
    images = tuple(ImageRef(p) for p in case.images)

    # Claims come from the seller's words alone, so they are extracted while
    # the readers are still looking at the photos.
    claims_job = None
    if case.seller_text.strip():
        claims_pool = ThreadPoolExecutor(max_workers=1)
        claims_job = claims_pool.submit(extract_claims, reader, case.seller_text)
        claims_pool.shutdown(wait=False)

    try:
        result = chain.run(
            images,
            case.seller_text,
            catalogue,
            reader,
            reasoner,
            meter,
            case.category_hint,
            corroborator,
            ocr,
            case.progress,
        )
    except (ProviderError, MissingFixture) as exc:
        code = "NO_FIXTURE" if isinstance(exc, MissingFixture) else "PROVIDER_ERROR"
        return CaseResult(
            case_id=case.id,
            chain=chain.ChainResult(failure_code=code, reason=str(exc)),
            ledger=[],
            quote=Quote(failure_code=code, reason=str(exc)),
            cost_usd=meter.total_usd,
            latency_ms=meter.total_ms,
            cost_by_task=meter.by_task(),
            reader_model=reader.model,
            reasoner_model=reasoner.model,
            error=str(exc),
            spent_usd=meter.spent_usd,
        )

    # What the model called it is free text, so the protocol is resolved by
    # name and alias rather than by an exact dictionary hit. A miss here used
    # to send every 'portable generator' to the generic protocol, and with it
    # went the rating plate and winding photos that price the thing.
    category = result.category or case.category_hint or "generic"
    if tenant is not None and result.category:
        protocol = tenant.protocol_for(protocols, category)
    elif result.category:
        protocol = resolve(protocols, category)
    else:
        protocol = protocols.get(category) or protocols["generic"]
    category = protocol.category
    if tenant is not None:
        protocol = tenant.with_questions(protocol, case.tenant_category)

    # A sofa has no model number to be identified by. Where the protocol says
    # the type is the identity, what two readers judged it to be is the
    # answer, and it is priced from listings of that type below.
    if protocol.identity_by_type:
        chain.name_by_type(result, case.seller_text)

    # The item's own testimony, checked against itself, against the identity
    # the chain chose and against the catalogue. No model is asked whether the
    # item is genuine; two records that should agree and do not is the answer.
    slots = set(case.slots_present) | {t.slot for t in case.testimony}
    soft_flags = list(result.fraud_flags)
    check = crosscheck(case.testimony, _entry_for(catalogue, category, result.model_key), result.model_key, case.refused_slots)
    result.fraud_flags.extend(check.fraud_flags)
    if check.fraud_flags:
        result.links.append(chain.LinkLog("crosscheck", "fraud", "; ".join(check.fraud_flags)))
    elif case.testimony:
        result.links.append(
            chain.LinkLog("crosscheck", "ok", "; ".join(check.notes) or "no overlapping records")
        )

    entry = _entry_for(catalogue, category, result.model_key)
    review = review_answers(protocol, case.answers, entry)
    if review.notes:
        result.links.append(chain.LinkLog("answers", "checked", "; ".join(review.notes)))

    if case.progress:
        case.progress("pricing")
    ledger: list[Claim] = []
    if claims_job is not None:
        try:
            # Text in, claims out: the reader model does this at a fiftieth of
            # the reasoner's price and the ledger rules do the judging anyway.
            drafts, meta = claims_job.result()
            meter.record(meta)
            ledger = build_ledger(
                drafts.claims,
                protocol,
                slots,
                contradictions=check.contradicted + review.contradictions,
                refused_slots=case.refused_slots,
            )
        except (ProviderError, MissingFixture):
            ledger = []

    # Answers are claims too: unprovable remotely, priced at the worst case,
    # and checked against the catalogue where the catalogue knows.
    if review.drafts:
        ledger.extend(
            build_ledger(
                review.drafts, protocol, slots,
                contradictions=check.contradicted + review.contradictions,
                refused_slots=case.refused_slots,
            )
        )

    # Declining to open a cover is a claim about what is behind it, and it is
    # priced as the worst thing that could be there.
    for shot in protocol.opening_shots:
        if shot.id in case.refused_slots:
            ledger.append(
                Claim(
                    text=f"Seller declined to open: {shot.ask}",
                    kind="condition",
                    attribute=None,
                    value=None,
                    status=ClaimStatus.REFUSED_TO_OPEN,
                    required_evidence=[shot.id],
                    worst_case="whatever is behind the cover is assumed to be the worst case",
                    pickup_check="Agent opens it before any money moves",
                    penalty=0.7,
                )
            )

    # Any shot the protocol requires that the seller never sent is an unproven
    # condition in its own right, so it is recorded like a claim.
    missing = [
        s for s in protocol.required_shots if s.id not in slots and s.id not in case.refused_slots
    ]
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
        # A photograph of a yard of scrap has nothing in frame to give it
        # scale, so a stated tonnage beats an estimate every time. It is still
        # settled on the scale, so it can move the quoted total and never the
        # rate per kilogram that the seller is actually paid.
        weight = reading.estimated_weight_kg
        weight_confident = (reading.weight_confidence or 0.0) >= 0.6
        stated = parse_stated_weight_kg(case.seller_text)
        if stated is not None and (weight is None or stated > (weight or 0)):
            weight = stated
            weight_confident = False
            result.links.append(
                chain.LinkLog("weight", "stated", f"{stated:g} kg from the seller's words")
            )
        try:
            material_obs = materials.fetch(shares, weight)
        except SourceUnavailable:
            material_obs = []

    identified = bool(result.model_key) and not result.abstained

    # Not working, by the seller's answer or the seller's words. The photos
    # cannot prove a dead board, so the seller's own statement decides, and
    # it can only lower the price.
    not_working = review.not_working or says_not_working(case.seller_text)
    if not_working:
        result.links.append(chain.LinkLog("condition", "not working", "by the seller's own account"))

    comp_obs: list = []
    new_obs: list = []
    scrap_obs: list = []
    comps_are_faulty = False
    if identified:
        # Comparable prices are found by brand and model. The variant, RAM,
        # storage and colour, is a claim in the ledger, not part of the
        # identity: demanding 16 GB in every title threw away the two
        # MacBook Air M2 listings that were in the pool.
        comps_key = result.type_name if result.named_type else " ".join(filter(None, [result.brand, result.model]))
        if not_working:
            # The dead market first: faulty and for-parts listings of the
            # same model are the honest comparable for a unit that does not
            # work. Working listings are the fallback, scaled by the tenant.
            try:
                comp_obs = comps.fetch(category, comps_key, faulty=True, by_type=result.named_type)
                comps_are_faulty = len(comp_obs) >= MIN_OBSERVATIONS
            except SourceUnavailable:
                comp_obs = []
        if not comps_are_faulty:
            try:
                comp_obs = comps.fetch(category, comps_key, by_type=result.named_type)
            except SourceUnavailable:
                comp_obs = []
        if len(comp_obs) < MIN_OBSERVATIONS and not not_working:
            # Too few used listings to price from. Dealers list new stock
            # of nearly everything, and the business's own share-of-new
            # rate turns those into a used price. The engine decides below
            # whether it may be used; here it is only fetched.
            try:
                new_obs = comps.fetch(category, comps_key, by_type=result.named_type, new=True)
            except SourceUnavailable:
                new_obs = []
            if new_obs:
                result.links.append(chain.LinkLog("comps", "new stock", f"{len(new_obs)} new asking prices for {comps_key!r}"))
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

    if check.fraud_suspected:
        # A loud failure, by rule 8. The range is not reduced, it is withheld.
        quote = Quote(
            failure_code="FRAUD_SUSPECTED",
            reason=(
                "Records that should agree do not: "
                + "; ".join(check.fraud_flags)
                + ". No price until an agent has the item in hand."
            ),
            conditions=[f"Fraud signal: {f}" for f in check.fraud_flags],
        )
    else:
        quote = price(
            comp_obs,
            scrap_obs,
            ledger,
            materials=material_obs,
            identified=identified,
            weight_confident=weight_confident,
            not_working=not_working,
            dead_fraction=tenant.dead_fraction_for(category) if tenant is not None else None,
            comps_are_faulty=comps_are_faulty,
            new_comps=new_obs,
            resale_fraction=tenant.resale_fraction_for(category) if tenant is not None else None,
        )
    # What this business will not buy at any price, in their own published
    # words. A refusal is an outcome: quoting a small number for something
    # nobody will collect wastes the agent's day and the seller's.
    if tenant is not None:
        spoken = " ".join(
            filter(None, [result.category, case.seller_text, *(reading.visible_text if reading else [])])
        )
        refusal = tenant.refusal(spoken)
        if refusal is not None:
            quote = Quote(
                failure_code="NOT_PURCHASED",
                reason=refusal.because,
                conditions=[f"{refusal.because} Source: {refusal.url or 'tenant policy'}"],
            )
        else:
            floor_price = tenant.minimum_for(category)
            if (
                floor_price
                and not quote.is_failure
                and result.presentation == "single_unit"
                and (quote.high or 0) < floor_price
            ):
                quote.low = round(max(quote.low or 0.0, floor_price), 2)
                quote.high = round(floor_price, 2)
                quote.conditions.insert(
                    0,
                    f"Raised to the {floor_price:,.0f} {quote.currency} minimum this "
                    "business publishes for this kind of item.",
                )

    quote = cap_at_asking(quote, case.asking_price)
    if soft_flags:
        quote.conditions = [f"Evidence flag: {f}" for f in soft_flags] + quote.conditions
    if not identified and not quote.is_failure and result.reason:
        quote.conditions.insert(0, f"Not identified: {result.reason}")

    return CaseResult(
        case_id=case.id,
        chain=result,
        ledger=ledger,
        quote=quote,
        assessment=assess(result, quote, ledger),
        asks=capture_requests(result, protocol, slots),
        questions=unanswered(protocol, case.answers),
        answer_notes=review.notes,
        cost_usd=meter.total_usd,
        latency_ms=meter.total_ms,
        cost_by_task=meter.by_task(),
        reader_model=reader.model,
        reasoner_model=reasoner.model,
        crosscheck=check,
        spent_usd=meter.spent_usd,
        timing=[{"task": m.task, "model": m.model, "ms": m.latency_ms, "replayed": bool(m.replayed)} for m in meter.calls],
        wall_ms=int((time.perf_counter() - started) * 1000),
    )


# Ways a Lagos seller says a thing is dead. Their words, and only a lowering.
NOT_WORKING_PHRASES = (
    "not working", "doesn't work", "does not work", "dont work", "don't work", "faulty",
    "not powering", "no power", "not coming on", "won't come on", "wont come on", "dead",
    "spoilt", "spoiled", "not turning on", "won't turn on", "wont turn on", "for parts",
)


def says_not_working(text: str) -> bool:
    t = f" {(text or '').lower()} "
    return any(p in t for p in NOT_WORKING_PHRASES)


def _entry_for(catalogue: dict[str, list[Entry]], category: str, key: str | None) -> Entry | None:
    """The catalogue row behind an identification, so its facts can be checked.

    Exact key first. Otherwise the most specific entry whose every token the
    chosen name contains, so 'Samsung Galaxy S22 SM-S901E' still finds the
    Galaxy S22 row. Nothing found means nothing is checked, honestly.
    """
    if not key:
        return None
    pool = catalogue.get(category) or [e for rows in catalogue.values() for e in rows]
    for entry in pool:
        if entry.key == key:
            return entry
    chosen = set(tokens(key))
    fits = [e for e in pool if set(tokens(e.key)) and set(tokens(e.key)).issubset(chosen)]
    return max(fits, key=lambda e: len(tokens(e.key)), default=None)


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
    if c.corroboration_notes:
        lines += ["", "## Two readers"] + [f"- {n}" for n in c.corroboration_notes]
    if c.ocr_lines:
        lines += ["", "## OCR read off the photos"] + [f"- {t}" for t in c.ocr_lines[:12]]

    lines += ["", "## Chain"]
    for link in c.links:
        lines.append(f"- **{link.name}** -> {link.outcome}. {link.detail}")

    # Where the seconds went, call by call, so a slow valuation can be read
    # like a bill rather than guessed at.
    if result.timing:
        lines += ["", "## Timing"] + [
            f"- {t['task']} on {t['model']}: {t['ms']} ms{' (replayed)' if t['replayed'] else ''}"
            for t in result.timing
        ] + [f"- total across calls: {result.latency_ms} ms; wall clock: {result.wall_ms} ms"]

    if case.testimony or case.refused_slots or (result.crosscheck and result.crosscheck.fraud_flags):
        lines += ["", "## Testimony"]
        for record in case.testimony:
            values = ", ".join(f"{k}={v}" for k, v in record.values.items())
            lines.append(f"- {record.slot}: {values}")
        for slot in sorted(case.refused_slots):
            lines.append(f"- {slot}: seller declined to open")
        if result.crosscheck:
            lines += [f"- FRAUD: {f}" for f in result.crosscheck.fraud_flags]
            lines += [f"- {n}" for n in result.crosscheck.notes]

    lines += ["", "## Identification"]
    if c.candidates:
        lines.append("Shortlist from the catalogue:")
        lines += [f"  - {k} ({s})" for k, s in c.candidates]
    else:
        lines.append("No catalogue candidates matched.")
    if result.identified and c.named_from_label:
        lines.append(f"\n**Answer: {c.model_key}** (named from the item's own label; not in the catalogue)")
    elif result.identified and c.named_type:
        lines.append(f"\n**Answer: {c.model_key}** (named by type; nothing on the item gives a brand or model, and none is expected)")
    elif result.identified:
        lines.append(f"\n**Answer: {c.model_key}** (margin {c.margin})")
    else:
        lines.append(f"\n**Not identified: {c.failure_code}.** {c.reason}")
    if c.fraud_flags:
        lines.append("\nEvidence flags: " + "; ".join(c.fraud_flags))

    if result.assessment:
        a = result.assessment
        lines += [
            "",
            "## How sure the engine is (back office)",
            f"**{a.sentence()}**",
            "",
            f"- Identification confidence: {a.percent}% ({a.band})",
            f"- Price confidence: {int(a.price_confidence * 100)}%",
        ]
        if a.alternatives:
            lines.append("- It is weighing: " + ", ".join(f"{n} ({s})" for n, s in a.alternatives))
        lines += [f"- {d}" for d in a.drivers]
        lines.append("")
        lines.append(
            "These are stated strengths from the evidence, not calibrated "
            "probabilities. They become calibrated once settled pickup prices exist."
        )

    if result.asks:
        lines += ["", "## What the seller is asked for next (shown in the app)"]
        for i, ask in enumerate(result.asks, 1):
            label = {"video": "VIDEO", "text": "TEXT"}.get(ask.kind, "PHOTO")
            lines.append(f"{i}. [{label}] {ask.ask}")
            lines.append(f"   _why: {ask.because}_")

    if result.questions:
        lines += ["", "## What the seller is asked (only they know these)"]
        for q in result.questions[:4]:
            lines.append(f"- {q.ask}")
    if result.answer_notes:
        lines += ["", "## Checking their answers (back office)"] + [f"- {n}" for n in result.answer_notes]

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
