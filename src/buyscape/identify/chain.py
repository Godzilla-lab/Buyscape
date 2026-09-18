"""Identification as a chain of links, each one logged.

Order: read the item (tier 1), build a retrieval query from what was read plus
the seller's own words, search the catalogue, then let tier 2 rank that
shortlist with the photos in front of it. Abstention is decided by rules here,
outside the model, because models are known to recognise their own uncertainty
internally and still answer confidently.

The listing title is never an input. It is the answer key.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ..providers.base import CallMeta, CostMeter, ImageRef, VisionProvider
from ..providers.tasks import Identification, Reading, identify, read_evidence
from .catalogue import Entry, search, tokens
from .corroborate import corroborate
from .ocr import OcrReader

# Two candidates within this score of each other is a coin toss, so refuse.
MIN_MARGIN = 0.15
# The reasoner's own score for its choice. Below this it was not sure either.
MIN_SCORE = 0.70
# The floor on assessed confidence. An answer below this is a guess, and a
# guess is worth less than a request for one more photograph, which costs the
# seller a few seconds and costs the buyer nothing. Swept over the recorded
# phone set on 4 Sep 2026: at 0.30 the engine answered more and was right 75
# percent of the time, at 0.45 it answered less and was right every time with
# no silent wrong answers at all. Raising it further only silences it.
MIN_CONFIDENCE = 0.45
# What a brand and model read off the label by two readers and the OCR are
# worth before the usual discounts for missing corroboration or fraud flags.
# The same as a sure decider, because it is the same evidence read one more
# way: at 0.85 a catalogue image halved it to 0.42 and four plates the
# decider had answered correctly went silent.
LABEL_NAMED_STRENGTH = 0.90


def identification_strength(result: ChainResult) -> tuple[float, list[str]]:
    """How much the evidence supports the answer, and why.

    One formula, used both to gate the answer here and to report the number to
    the back office, so the two can never tell a reviewer different things.
    """
    ident = result.identification
    ranked = sorted(ident.candidates, key=lambda c: c.score, reverse=True) if ident else []
    score = ranked[0].score if ranked else 0.0
    why: list[str] = []
    if result.named_from_label:
        # Brand and model both survived two readers and a witness that cannot
        # invent. That is the strongest read the system makes, and the
        # catalogue not knowing the item is a gap in the catalogue.
        score = LABEL_NAMED_STRENGTH
        why.append("named from the item's own label, which the catalogue does not list")

    if result.used_label:
        why.append("read off the item's own label")
    else:
        score *= 0.85
        why.append("no label, plate or settings screen was legible")
    if result.corroboration_failed:
        score *= 0.7
        why.append("only one reader saw these photos, the second was unavailable")
    if result.corroborated:
        if result.reading is not None and result.reading.corroborated_lines:
            why.append(f"{result.reading.corroborated_lines} lines seen by both readers")
        else:
            score *= 0.8
            why.append("the two readers agreed on nothing legible")
    uncorroborated = list(result.uncorroborated_fields)
    if uncorroborated:
        # Kept, because a blank from the other reader is not a contradiction,
        # but never worth as much as text both readers produced.
        score *= 0.8
        named = ", ".join(f.replace("_text", "") for f in uncorroborated)
        why.append(f"the {named} was read by only one reader and is not confirmed")
    if result.margin is not None and result.margin < 0.30:
        score *= 0.9
        why.append(f"the next candidate was only {result.margin} behind")
    if result.fraud_flags:
        score *= 0.5
        why.extend(result.fraud_flags)
    return round(max(0.0, min(score, 1.0)), 2), why
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
    presentation: str = "single_unit"
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
    corroborated: bool = False
    # Identifying fields that survived on one reader's word alone: weaker
    # evidence than a corroborated read, and everything downstream is told so.
    uncorroborated_fields: list[str] = field(default_factory=list)
    corroboration_failed: bool = False
    corroboration_notes: list[str] = field(default_factory=list)
    # What the character level OCR engine read, kept for the report. It
    # confirms a reader's text and never adds facts of its own.
    ocr_lines: list[str] = field(default_factory=list)
    # Named from the item's own label with no catalogue row behind it.
    named_from_label: bool = False
    fraud_flags: list[str] = field(default_factory=list)

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


def _generation_tokens(text: str, pool: list[Entry]) -> set[str]:
    """Tokens in `text` that name a model generation in this catalogue.

    '14' in '14 pro 256gb' is one, because the catalogue has an iPhone 14.
    '256gb' and '680k' are not. This is how the seller's own words are compared
    with what was read off the item without parsing prose.
    """
    known = {t for e in pool for t in tokens(e.model) if any(c.isdigit() for c in t)}
    # Sellers write '14pro' and '13promax' as one word. Split a leading number
    # from the letters after it, but leave codes like 's23' alone.
    spaced = re.sub(r"\b(\d+)([a-z]+)", r"\1 \2", (text or "").lower())
    return {t for t in tokens(spaced) if t in known}


_RATING = re.compile(r"(\d+(?:\.\d+)?)\s*(kva|kw|hp|kg|btu)\b", re.I)
RATING_TOLERANCE = 0.20


def _ratings(text: str) -> dict[str, float]:
    """The first rating per unit in a piece of text: '4.5kva' -> {'kva': 4.5}."""
    out: dict[str, float] = {}
    for number, unit in _RATING.findall(text or ""):
        out.setdefault(unit.lower(), float(number))
    return out


def rating_contradiction(seller_text: str, item_text: str) -> str | None:
    """The seller's stated rating is not the rating printed on the item.

    Generator adverts on Jiji routinely pair a stock photo of one model with a
    title claiming a different kVA. Reading the plate faithfully and then
    pricing the seller's number would be a silent wrong answer either way.
    """
    said = _ratings(seller_text)
    printed = _ratings(item_text)
    for unit, value in printed.items():
        claimed = said.get(unit)
        if claimed is None or value == 0:
            continue
        if abs(claimed - value) > RATING_TOLERANCE * value:
            return (
                f"The item reads {value:g}{unit} but the seller says {claimed:g}{unit}. "
                "A clear photo of the rating plate on this exact unit would settle it."
            )
    return None


def ungrounded_fields(reading: Reading) -> list[str]:
    """Fields the reader stated but could not point to in its own transcript.

    Vision models complete specification tables: shown half a generator plate
    they will supply the fuel tank capacity, the noise level and an output the
    plate never carried. Making the reader cite the line it copied each value
    from turns that from an invisible failure into an arithmetic one, because
    a cited line that is not in the transcript did not exist.
    """
    transcript = " ".join(reading.visible_text).lower()
    bad: list[str] = []
    for name, value, source in (
        ("brand", reading.brand_text, reading.brand_source),
        ("model", reading.model_text, reading.model_source),
        ("rating", reading.rating_text, reading.rating_source),
    ):
        if not value:
            continue
        cited = (source or "").lower().strip()
        if not cited or cited not in transcript or value.lower().strip() not in cited:
            bad.append(name)
    return bad


def _norm_key(text: str) -> str:
    return "".join(sorted(_joined(text)))


def _joined(text: str) -> list[str]:
    """Tokenise with hyphens closed up, so WM-200 stays one code, not two."""
    return tokens(re.sub(r"(?<=[A-Za-z0-9])-(?=[A-Za-z0-9])", "", text or ""))


# A number with a unit is a rating, not a part number: 1.5HP, 12000BTU, 8kg.
# Ratings are checked by invented_rating, so they are excluded here.
_UNIT_ONLY = re.compile(r"^\d+(?:\.\d+)?(?:hp|kva|kw|kg|g|gb|tb|mb|btu|w|v|hz|l|ton|tons|rpm)$")


def _codes(text: str) -> set[str]:
    """Tokens that look like a part number: letters and digits together."""
    return {
        t
        for t in _joined(text)
        if any(c.isdigit() for c in t) and any(c.isalpha() for c in t) and not _UNIT_ONLY.match(t)
    }


# A generator model code carries its output in watts: SPG3000 is 3kW, KM6500
# is 6.5kW. Nigerian sellers rate the same machine anywhere from 0.45 to 1.3
# times that, max output against rated output, so only a wild mismatch counts.
_CODE_WATTS = re.compile(r"(?<!\d)([2-9]\d{3}|1[0-5]\d{3})(?!\d)")
CODE_RATING_BAND = (0.40, 1.35)


def code_rating_contradiction(reading: Reading) -> str | None:
    """The model code and the stated rating are two records that must agree.

    A plate read as 'MODEL: SY6500' and 'OUTPUT: 1.5KVA' cannot both be true:
    the code says six and a half kilowatts. Vision models will transcribe a
    whole plausible specification table that was never on the plate, and this
    is the cheapest way to catch one doing it, since the two numbers come from
    the same reading and no second model call is needed.
    """
    stated = _ratings(" ".join([reading.rating_text or "", *reading.visible_text]))
    kva = stated.get("kva") or stated.get("kw")
    code = reading.model_text or ""
    watts = _CODE_WATTS.search(code)
    if not (kva and watts):
        return None
    implied = int(watts.group(1)) / 1000
    low, high = CODE_RATING_BAND
    if not (implied * low <= kva <= implied * high):
        return (
            f"The item reads as model {code} and also as {kva:g}kVA, but a {code} "
            f"is about {implied:g}kW. One of the two was misread, so the plate "
            "needs a clearer photo before this can be priced."
        )
    return None


def invented_code(
    reading: Reading, seller_text: str, chosen: str, ocr_lines: list[str] = ()
) -> str | None:
    """The answer carries a part number that nothing in evidence contains.

    'SAMSUNG AR12TYFQDBG' was answered off photographs whose whole transcript
    was SAMSUNG, DIGITAL INVERTER, AIR CONDITIONER, R410A. The code is real,
    it belongs to a real product, and it came from the model's memory rather
    than from this machine. A shortlist entry is not exempt: a box reading
    'EliteBook 630 G9' was answered as the shortlist's 820 G6, because the
    shortlist is persuasive and the catalogue had no 630. The item beats the
    shortlist, and an item the catalogue does not know is CANNOT_IDENTIFY,
    not the nearest thing the catalogue does know.
    """
    evidence = " ".join([*reading.visible_text, reading.model_text or "",
                         reading.rating_text or "", reading.brand_text or "", seller_text, *ocr_lines])
    seen = set(_joined(evidence))
    for code in _codes(chosen):
        if code not in seen:
            return (
                f"The answer names {code}, which appears nowhere on the item or in "
                "the seller's words. A photo of the plate would confirm or correct it."
            )
    return None


def label_identity(
    reading: Reading,
    ocr_lines: list[str],
    seller_text: str,
    hits: list[tuple[Entry, float]],
    pool: list[Entry],
) -> tuple[str, str] | None:
    """Brand and model read off the item that the catalogue does not know.

    Rule 1 says identification is a chain that ends in the catalogue, but a
    plate that two readers and the OCR engine agree on is better evidence than
    any shortlist. When no candidate carries the code that was read, the item
    is named from its label and the decider is not asked to pick the nearest
    thing the catalogue happens to know. It is then priced from the published
    band for its category or its material, since nothing else has data.
    """
    brand, model = reading.brand_text, reading.model_text
    if not brand or not model:
        return None
    codes = _codes(model)
    if not codes:
        return None
    if unwitnessed_code(model, ocr_lines, seller_text):
        return None
    # The brand too must come from a witness that cannot invent, not from a
    # reader's own word: a Lutian carton behind a Maxi is in the transcript.
    witnessed = " ".join([*ocr_lines, seller_text]).lower()
    if not any(w in witnessed for w in _joined(brand) if len(w) >= 3):
        return None
    for entry, _ in hits:
        if _codes(" ".join([entry.model, entry.variant or ""])) & codes:
            return None
    return brand.strip(), model.strip()


def unwitnessed_code(chosen: str, ocr_lines: list[str], seller_text: str) -> str | None:
    """No witness that cannot invent saw the code the answer rests on.

    Two language models can agree on a fabrication: both transcribed
    'Model: HSC-12000I' off a Hisense box that carries no model code, and
    both read 'EliteBook 820 G6' off a label that says 630 G9. Agreement
    between two readers is the first defence and it is not enough on its own.
    A part number in the answer must also have been read by the OCR engine
    or said by the seller. Measured on the recorded Jiji set: this keeps all
    fourteen correct answers and drops both wrong ones.
    """
    codes = _codes(chosen)
    if not codes:
        return None
    seen = set(_joined(" ".join([*ocr_lines, seller_text])))
    if codes & seen:
        return None
    return (
        f"The answer rests on {sorted(codes)[0]}, which the OCR engine did not read off "
        "the item and the seller did not say. Two readers transcribing the same code is "
        "not enough on its own. This needs a sharp photo of the label."
    )


def label_contradiction(reading: Reading, chosen: str) -> str | None:
    """The answer names a different model from the one printed on the item.

    A washing machine whose plate reads 'Model: WM-200' was answered as a
    Hisense WTJA801, because the shortlist offered one and the shortlist is
    persuasive. The label outranks the shortlist every time.
    """
    printed = _codes(reading.model_text or "")
    if not printed:
        return None
    answered = set(_joined(chosen))
    if printed & answered:
        return None
    return (
        f"The item's own label reads {reading.model_text!r}, but the answer is "
        f"{chosen!r}. The label decides, so this needs a clearer photo of it."
    )


def unsupported_brand(
    reading: Reading,
    ocr_lines: list[str],
    seller_text: str,
    chosen_brand: str,
    chosen_model: str | None,
    pool: list[Entry],
    brand_disputed: bool = False,
) -> str | None:
    """The answer names a brand that no witness produced.

    A Sumec Maxi plate whose brand the two readers disagreed on, so it was
    dropped, came back as a Lutian: the code E33KWH survived by OCR, the
    shortlist offered a Lutian, and the decider stitched the two together. A
    brand has to be read off the item, said by the seller, or be the brand the
    catalogue gives the model code that was read. Otherwise it is a guess.
    """
    words = [w for w in _joined(chosen_brand) if len(w) >= 3]
    if not words:
        return None
    if brand_disputed:
        # The two readers read different brands, so the transcript is where
        # the wrong one lives: a Maxi photographed in front of a Lutian box
        # carries both words. Only the OCR engine or the seller can settle it.
        evidence = " ".join([*ocr_lines, seller_text]).lower()
        if any(w in evidence for w in words):
            return None
        return (
            f"The two readers disagreed about the brand and the answer's {chosen_brand!r} "
            "is not what the OCR read off the item or what the seller said. This needs "
            "a clear photo of the brand on the item."
        )
    evidence = " ".join(
        [*reading.visible_text, reading.brand_text or "", reading.model_text or "", *ocr_lines, seller_text]
    ).lower()
    if any(w in evidence for w in words):
        return None
    # 'iPhone 13' in the seller's words supports Apple, because the catalogue
    # says whose model that is. A brand no entry ties to the read text is not.
    read = set(_joined(evidence))
    for entry in pool:
        if _joined(entry.brand) == _joined(chosen_brand) and set(_joined(entry.model)) <= read:
            return None
    return (
        f"The answer names {chosen_brand!r}, which appears nowhere on the item, in the "
        "seller's words, or in the catalogue for the code that was read. This needs a "
        "clear photo of the brand on the item."
    )


def invented_rating(reading: Reading, seller_text: str, chosen: str) -> str | None:
    """The answer states a capacity or rating that nothing in evidence showed.

    A generator's kVA is its price, so a kVA that came from the model's own
    knowledge of a product line rather than from the plate is a made-up price.
    Rule 4 applies to specifications, not only to money.
    """
    claimed = _ratings(chosen)
    if not claimed:
        return None
    evidence = " ".join([*reading.visible_text, reading.rating_text or "", reading.model_text or "", seller_text])
    shown = _ratings(evidence)
    for unit, value in claimed.items():
        if unit not in shown:
            return (
                f"The answer states {value:g}{unit}, but no {unit} rating is legible "
                "on the item and the seller never stated one."
            )
        if abs(shown[unit] - value) > RATING_TOLERANCE * value:
            return (
                f"The answer states {value:g}{unit} but the evidence shows "
                f"{shown[unit]:g}{unit}."
            )
    return None


def seller_contradiction(seller_text: str, chosen_key: str, pool: list[Entry]) -> str | None:
    """The seller names a different generation from the one on the item.

    Real listings do this in two ways: a gallery that mixes handsets, and a
    sticker that says one thing while the caption says another. Both were
    silent wrong answers in the proof. The honest output is to ask for the
    Settings screen, not to pick a side.
    """
    said = _generation_tokens(seller_text, pool)
    chosen = _generation_tokens(chosen_key, pool)
    if said and chosen and not (said & chosen):
        return (
            f"The item reads as {chosen_key} but the seller's text says "
            f"{', '.join(sorted(said))}. A Settings or About screen would settle it."
        )
    return None


def run(
    images: tuple[ImageRef, ...],
    seller_text: str,
    catalogue: dict[str, list[Entry]],
    reader: VisionProvider,
    reasoner: VisionProvider,
    meter: CostMeter,
    category_hint: str | None = None,
    corroborator: VisionProvider | None = None,
    ocr: OcrReader | None = None,
) -> ChainResult:
    """Run the whole chain. Never raises for a bad item, it returns a failure."""
    result = ChainResult()

    if not images:
        result.failure_code = "EVIDENCE_INCOMPLETE"
        result.reason = "No photos were supplied."
        result.links.append(LinkLog("input", "fail", "no images"))
        return result

    # Link 1: read the item, twice where a second reader is configured. Only
    # what both readers independently produced is treated as read, because a
    # single model will invent a plate code and cite its own invention.
    reading, meta = read_evidence(reader, images)
    meter.record(meta)
    second: Reading | None = None
    if corroborator is not None:
        try:
            second, meta_b = read_evidence(corroborator, images)
            meter.record(meta_b)
        except Exception as exc:
            # A safety net that disappears when it is busy is not a safety net.
            # Five of six air conditioner errors on 4 Sep were single reader
            # answers at 90 percent confidence, taken while the second reader
            # was rate limited. An outage still produces a quote, but never a
            # confident identification.
            result.corroboration_failed = True
            result.links.append(LinkLog("corroborate", "unavailable", str(exc)[:120]))
    # A third witness of a different kind: OCR reads glyphs and cannot compose
    # a plate, so it can confirm what one model read but never add to it.
    ocr_lines: list[str] = []
    if ocr is not None:
        try:
            ocr_lines = ocr(images)
            result.ocr_lines = ocr_lines
            result.links.append(LinkLog("ocr", "ok", f"{len(ocr_lines)} lines: {' | '.join(ocr_lines)[:120]}"))
        except Exception as exc:
            result.links.append(LinkLog("ocr", "unavailable", str(exc)[:120]))
    check = corroborate(reading, second, ocr_lines)
    reading = check.reading
    if second is not None or ocr_lines:
        result.corroborated = second is not None
        result.links.append(
            LinkLog(
                "corroborate",
                "dispute" if (check.disputed or check.only_one_saw) else "agree",
                "; ".join(check.notes) or "nothing identifying was read by either",
            )
        )
        result.corroboration_notes = check.notes
        result.uncorroborated_fields = list(check.uncorroborated)
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

    # Anything the reader could not point at in its own transcript is dropped
    # before it can reach retrieval or the decider. A fact with no line behind
    # it is not evidence, and downstream everything treats it as unread.
    ungrounded = ungrounded_fields(reading)
    for name in ungrounded:
        setattr(reading, f"{name}_text", None)
    if ungrounded:
        result.fraud_flags.append(
            "the reader stated " + ", ".join(ungrounded) + " it could not point to in the photos"
        )
        result.links.append(LinkLog("grounding", "dropped", ", ".join(ungrounded)))

    result.category = reading.category
    result.presentation = reading.presentation or "single_unit"
    if reading.stock_photo_suspected:
        result.fraud_flags.append("looks like a catalogue or stock image")
    if reading.screenshot_of_gallery:
        result.fraud_flags.append("screenshot of a gallery rather than a photo of the item")
    if result.fraud_flags:
        result.links.append(LinkLog("forensics", "flag", "; ".join(result.fraud_flags)))

    # A heap of bottles or a pile of boards has no model to find. Asking which
    # one it is would produce either a guess or a refusal, and both are wrong:
    # it is priced by material and weight.
    if result.presentation == "mixed_lot":
        result.abstained = True
        result.failure_code = "CANNOT_IDENTIFY"
        result.reason = "This is a mixed lot, so it is priced by material and weight rather than identified."
        result.links.append(LinkLog("gate", "lot", "priced by material, identification skipped"))
        return result

    if reading.multiple_items:
        result.abstained = True
        result.failure_code = "EVIDENCE_INCOMPLETE"
        result.reason = "The photos show more than one item, so no single item can be identified."
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

    # An item the catalogue does not know, with its own name on its own label.
    pool = catalogue.get(category_hint or "") or [e for rows in catalogue.values() for e in rows]
    named = label_identity(reading, ocr_lines, seller_text, hits, pool) if ocr is not None else None
    if named is not None:
        result.brand, result.model = named
        result.named_from_label = True
        result.links.append(LinkLog("identify", "label", f"named from the label: {result.model_key}, not in the catalogue"))
        strength, why = identification_strength(result)
        if strength < MIN_CONFIDENCE:
            result.brand = result.model = None
            result.named_from_label = False
            result.abstained = True
            result.failure_code = "EVIDENCE_INCOMPLETE"
            result.reason = (
                f"The label names it, but the evidence only supports that at {int(strength * 100)} "
                "percent. One clear photo of the label would settle it."
            )
            result.links.append(LinkLog("abstain", "abstain", f"confidence {strength}: {'; '.join(why)}"))
            return result
        result.links.append(LinkLog("abstain", "pass", f"confidence={strength} from the label"))
        return result

    # No shortlist and no model string on the item means the reasoner would
    # have nothing to rank and nothing to read. Abstain here instead of paying
    # for a call whose only honest answer is a refusal.
    if not hits and not reading.model_text:
        result.abstained = True
        result.failure_code = "CANNOT_IDENTIFY"
        result.reason = (
            "No catalogue entry matched what was read and no model string was "
            "legible on the item, so there is nothing to rank."
        )
        result.links.append(LinkLog("gate", "abstain", "no candidates and no model text"))
        return result

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
    if top < MIN_SCORE:
        result.abstained = True
        result.failure_code = "CANNOT_IDENTIFY"
        result.reason = f"The best candidate scored only {top}, which is not sure enough to price."
        result.links.append(LinkLog("abstain", "abstain", f"top score {top}"))
        return result
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

    chosen_key = " ".join(filter(None, [ident.chosen_brand, ident.chosen_model]))
    pool = catalogue.get(category_hint or "") or [e for rows in catalogue.values() for e in rows]
    item_text = " ".join(
        filter(None, [reading.rating_text, reading.model_text, chosen_key, ident.chosen_variant])
    )
    full_answer = " ".join(filter(None, [chosen_key, ident.chosen_variant]))
    clash = (
        code_rating_contradiction(reading)
        or label_contradiction(reading, full_answer)
        or invented_code(reading, seller_text, full_answer, ocr_lines)
        or (unwitnessed_code(full_answer, ocr_lines, seller_text) if ocr is not None else None)
        or invented_rating(reading, seller_text, full_answer)
        or unsupported_brand(
            reading, ocr_lines, seller_text, ident.chosen_brand, ident.chosen_model, pool,
            brand_disputed="brand_text" in check.disputed,
        )
        or seller_contradiction(seller_text, chosen_key, pool)
        or rating_contradiction(seller_text, item_text)
    )
    if clash:
        result.abstained = True
        result.failure_code = "EVIDENCE_INCOMPLETE"
        result.reason = clash
        result.links.append(LinkLog("abstain", "abstain", "seller names another generation"))
        return result

    result.brand = ident.chosen_brand
    result.model = ident.chosen_model
    result.variant = ident.chosen_variant

    # Last gate: the assembled evidence, not any single number. An iPhone 13
    # answered as an iPhone 13 Pro from a transcript reading only 'APPLE
    # WARRANTY' scored 42 here, and was priced anyway before this existed.
    strength, why = identification_strength(result)
    if strength < MIN_CONFIDENCE:
        result.brand = result.model = result.variant = None
        result.abstained = True
        result.failure_code = "EVIDENCE_INCOMPLETE"
        result.reason = (
            f"The evidence only supports this answer at {int(strength * 100)} percent, "
            "which is a guess. One clear photo of the label would settle it."
        )
        result.links.append(LinkLog("abstain", "abstain", f"confidence {strength}: {'; '.join(why)}"))
        return result

    result.links.append(LinkLog("abstain", "pass", f"confidence={strength} margin={result.margin}"))
    return result
