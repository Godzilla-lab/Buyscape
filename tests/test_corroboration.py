"""A fact is read when two readers independently produce it, not before.

Measured on this project: the same generator photograph was read as model
SY6500 on one run and GP-1000 on the next, each time with a cited source line
and 90 percent stated confidence. A single model cannot audit itself, so the
identifying text has to survive a second, independent pair of eyes.
"""

from __future__ import annotations

from pathlib import Path

from buyscape.identify.corroborate import corroborate
from buyscape.providers.tasks import Reading

ROOT = Path(__file__).resolve().parents[1]


def test_two_readers_that_agree_keep_the_reading():
    a = Reading(brand_text="FIRMAN", model_text="SPG3000", rating_text="3.1kVA",
                has_label_or_plate=True, visible_text=["FIRMAN", "SPG3000"])
    b = Reading(brand_text="Firman", model_text="SPG-3000", rating_text="3.1 kVA",
                has_label_or_plate=True, visible_text=["FIRMAN", "SPG 3000"])
    out = corroborate(a, b)
    assert out.reading.model_text and out.reading.rating_text
    assert set(out.agreed) >= {"brand_text", "model_text", "rating_text"}
    assert not out.disputed


def test_two_readers_that_invent_different_codes_read_nothing():
    """The real failure: same photos, SY6500 one run, GP-1000 the next."""
    a = Reading(model_text="SY6500", rating_text="1.5KVA", has_label_or_plate=True,
                visible_text=["ELEPAQ", "MODEL: SY6500", "OUTPUT: 1.5KVA"])
    b = Reading(model_text="GP-1000", rating_text="4.5KVA", has_label_or_plate=True,
                visible_text=["ELEPAQ", "GP-1000"])
    out = corroborate(a, b)
    assert out.reading.model_text is None
    assert out.reading.rating_text is None
    assert set(out.disputed) >= {"model_text", "rating_text"}
    assert any("treated as unread" in n for n in out.notes)


def test_a_fact_only_one_reader_saw_is_not_a_fact():
    a = Reading(model_text="HWM80-1400", has_label_or_plate=True, visible_text=["Model: HWM80-1400"])
    b = Reading(model_text=None, has_label_or_plate=True, visible_text=["Hisense"])
    out = corroborate(a, b)
    assert out.reading.model_text is None
    assert "model_text" in out.only_one_saw


def test_a_longer_reading_of_the_same_plate_is_agreement_not_conflict():
    a = Reading(model_text="SPG3000", visible_text=["SPG3000"])
    b = Reading(model_text="FIRMAN SPG3000", visible_text=["FIRMAN SPG3000"])
    out = corroborate(a, b)
    assert out.reading.model_text == "FIRMAN SPG3000"
    assert "model_text" in out.agreed


def test_either_reader_seeing_two_items_or_a_stock_photo_is_enough():
    a = Reading(multiple_items=False, stock_photo_suspected=False)
    b = Reading(multiple_items=True, stock_photo_suspected=True)
    merged = corroborate(a, b).reading
    assert merged.multiple_items and merged.stock_photo_suspected


def test_a_label_counts_as_legible_only_if_both_readers_could_read_it():
    a = Reading(has_label_or_plate=True)
    b = Reading(has_label_or_plate=False)
    assert corroborate(a, b).reading.has_label_or_plate is False


def test_one_reader_alone_still_runs_and_says_it_was_not_corroborated():
    a = Reading(model_text="SPG3000")
    out = corroborate(a, None)
    assert out.reading.model_text == "SPG3000"
    assert not out.agreed and not out.disputed and not out.notes


def test_a_disputed_reading_makes_the_engine_ask_for_a_better_photo():
    """End to end: two readers disagree, so the seller is asked, not guessed at."""
    from buyscape.assess import capture_requests
    from buyscape.identify import chain
    from buyscape.protocols.schema import load_protocols
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider
    from buyscape.identify.catalogue import load_catalogue

    protocols = load_protocols(ROOT / "protocols")
    catalogue = load_catalogue(ROOT / "catalogue")
    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    reader = FakeProvider({"category": "generator", "category_confidence": 0.9,
                           "model_text": "SY6500", "has_label_or_plate": True,
                           "visible_text": ["ELEPAQ", "SY6500"]})
    other = FakeProvider({"category": "generator", "category_confidence": 0.9,
                          "model_text": "GP-1000", "has_label_or_plate": True,
                          "visible_text": ["ELEPAQ", "GP-1000"]})
    result = chain.run((ImageRef(image),), "strong generator", catalogue, reader,
                       FakeProvider(), CostMeter(), corroborator=other)
    assert result.abstained, "two readers naming different models must not produce an answer"
    asks = capture_requests(result, protocols["generator"], slots_present=set())
    assert asks and any("plate" in a.ask.lower() or "label" in a.ask.lower() for a in asks)


def test_a_line_only_one_reader_transcribed_never_reaches_the_decider():
    """Where fabrication actually lives: the invented line in the transcript.

    Dropping the extracted model code is not enough. The decider is handed the
    transcript, so an invented line inside it is an invented answer waiting to
    happen, and it must not survive either.
    """
    a = Reading(
        model_text="SY6500",
        visible_text=["ELEPAQ", "GASOLINE GENERATOR", "MODEL: SY6500", "OUTPUT: 1.5KVA",
                      "NOISE LEVEL: 72dB(A)", "DIMENSIONS: 680x450x480mm"],
    )
    b = Reading(model_text=None, visible_text=["ELEPAQ", "GASOLINE GENERATOR"])
    merged = corroborate(a, b).reading
    assert merged.visible_text == ["ELEPAQ", "GASOLINE GENERATOR"]
    assert merged.corroborated_lines == 2
    joined = " ".join(merged.visible_text)
    assert "SY6500" not in joined and "1.5KVA" not in joined and "72dB" not in joined


def test_a_corroborator_outage_never_produces_a_confident_answer():
    """Five of six air conditioner errors on 4 Sep were single reader answers
    at 90 percent, taken while the second reader was rate limited. A safety
    net that disappears when it is busy is not a safety net."""
    from buyscape.identify.chain import ChainResult, identification_strength
    from buyscape.providers.tasks import Candidate, Identification

    ident = Identification(candidates=[Candidate(brand="Samsung", model="AR12", score=0.95)],
                           chosen_brand="Samsung", chosen_model="AR12")
    both = ChainResult(used_label=True, identification=ident, margin=0.8)
    alone = ChainResult(used_label=True, identification=ident, margin=0.8, corroboration_failed=True)
    assert identification_strength(alone)[0] < identification_strength(both)[0]
    assert any("second was unavailable" in w for w in identification_strength(alone)[1])


def test_an_answer_code_that_appears_nowhere_in_the_evidence_is_refused():
    """The real case: 'SAMSUNG AR12TYFQDBG' answered off a transcript reading
    only SAMSUNG, DIGITAL INVERTER, AIR CONDITIONER, R410A."""
    from buyscape.identify.chain import invented_code
    from buyscape.providers.tasks import Reading

    seen = Reading(visible_text=["SAMSUNG", "DIGITAL INVERTER", "AIR CONDITIONER", "R410A"],
                   brand_text="SAMSUNG")
    assert invented_code(seen, "1.5hp split ac", "SAMSUNG AR12TYFQDBG 1.5HP")
    assert invented_code(seen, "", "SAMSUNG 1.5HP split") is None

    read = Reading(visible_text=["Model: AC12BQ", "LG"], model_text="AC12BQ")
    assert invented_code(read, "", "LG AC12BQ 1.5 Ton Inverter Split") is None


def test_a_brand_one_reader_saw_survives_but_says_it_is_uncorroborated():
    """A blank is not a contradiction, and a brand is not a plate code.

    Measured on the Jiji set: 45 of 178 cases lost the brand because one
    reader named it and the other named nothing, which is absence of
    evidence rather than conflict. Fabrication lives in alphanumeric codes,
    which a model composes character by character. A brand is a logo from a
    small set, so a single read is weak evidence, not no evidence. It
    survives, marked, and the decider weighs it lower.
    """
    a = Reading(brand_text="Hisense", has_label_or_plate=True, visible_text=["Hisense"])
    b = Reading(brand_text=None, has_label_or_plate=True, visible_text=["8kg"])
    out = corroborate(a, b)
    assert out.reading.brand_text == "Hisense"
    assert "brand_text" in out.uncorroborated
    assert "brand_text" not in out.only_one_saw
    assert any("only one reader" in n for n in out.notes)


def test_two_readers_naming_different_brands_still_read_nothing():
    a = Reading(brand_text="Hisense", has_label_or_plate=True, visible_text=["Hisense"])
    b = Reading(brand_text="Haier", has_label_or_plate=True, visible_text=["Haier"])
    out = corroborate(a, b)
    assert out.reading.brand_text is None
    assert "brand_text" in out.disputed


def test_a_model_code_one_reader_saw_is_still_dropped():
    """The strict rule stays exactly where fabrication actually happens."""
    a = Reading(model_text="SY6500", has_label_or_plate=True, visible_text=["SY6500"])
    b = Reading(model_text=None, has_label_or_plate=True, visible_text=["ELEPAQ"])
    out = corroborate(a, b)
    assert out.reading.model_text is None
    assert "model_text" in out.only_one_saw


def test_an_answer_leaning_on_one_readers_brand_is_less_sure():
    """Keeping the brand is not the same as confirming it.

    A brand one reader saw is weaker evidence than one both produced, so the
    number the back office reads has to say so. Otherwise the softer rule
    would quietly buy confidence it did not earn.
    """
    from buyscape.identify.chain import ChainResult, identification_strength
    from buyscape.providers.tasks import Candidate, Identification

    ident = Identification(candidates=[Candidate(brand="Hisense", model="8kg", score=0.95)],
                           chosen_brand="Hisense", chosen_model="8kg")
    seen = Reading(brand_text="Hisense", corroborated_lines=4)
    both = ChainResult(used_label=True, identification=ident, margin=0.8,
                       corroborated=True, reading=seen)
    one = ChainResult(used_label=True, identification=ident, margin=0.8,
                      corroborated=True, reading=seen,
                      uncorroborated_fields=["brand_text"])
    assert identification_strength(one)[0] < identification_strength(both)[0]
    assert any("only one reader" in w for w in identification_strength(one)[1])


# OCR is a third witness that reads glyphs and cannot compose a plate, so a
# code one language model produced and the OCR also produced was on the photo.


def test_ocr_confirms_a_code_only_one_reader_saw():
    a = Reading(model_text="CL7800E2R", has_label_or_plate=True, visible_text=["COROLLA", "CL7800E2R"])
    b = Reading(model_text=None, has_label_or_plate=True, visible_text=["COROLLA"])
    out = corroborate(a, b, ocr_lines=["COROLLA", "CL7800E2R", "Y-12-070-7"])
    assert out.reading.model_text == "CL7800E2R"
    assert "model_text" in out.confirmed_by_ocr
    assert "model_text" not in out.only_one_saw
    assert "CL7800E2R" in out.reading.visible_text


def test_ocr_settles_a_dispute_for_the_reader_it_agrees_with():
    a = Reading(model_text="SY6500", has_label_or_plate=True, visible_text=["MODEL: SY6500"])
    b = Reading(model_text="GP-1000", has_label_or_plate=True, visible_text=["GP-1000"])
    out = corroborate(a, b, ocr_lines=["ELEPAQ", "GP1000"])
    assert out.reading.model_text == "GP-1000"
    assert "model_text" in out.confirmed_by_ocr
    assert "model_text" not in out.disputed


def test_ocr_that_matches_neither_side_changes_nothing():
    a = Reading(model_text="SY6500", visible_text=["MODEL: SY6500"])
    b = Reading(model_text="GP-1000", visible_text=["GP-1000"])
    out = corroborate(a, b, ocr_lines=["ELEPAQ", "GASOLINE GENERATOR"])
    assert out.reading.model_text is None
    assert "model_text" in out.disputed
    assert not out.confirmed_by_ocr


def test_ocr_never_adds_a_fact_no_reader_produced():
    a = Reading(visible_text=["ELEPAQ"])
    b = Reading(visible_text=["ELEPAQ"])
    out = corroborate(a, b, ocr_lines=["ELEPAQ", "SC30000"])
    assert out.reading.model_text is None
    assert out.reading.visible_text == ["ELEPAQ"]


def test_a_single_reader_is_marked_confirmed_when_ocr_agrees():
    a = Reading(model_text="FPG15000SE", visible_text=["FIRMAN", "FPG15000SE"])
    out = corroborate(a, None, ocr_lines=["KIRMAN", "FPG15000SE"])
    assert out.reading.model_text == "FPG15000SE"
    assert "model_text" in out.confirmed_by_ocr
    assert any("OCR" in n for n in out.notes)


def test_the_chain_hands_ocr_lines_to_corroboration_and_the_report():
    """A code one model read and the OCR also read is an answer, not a dispute."""
    from buyscape.identify import chain
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider
    from buyscape.runner import Case, CaseResult, report_markdown
    from buyscape.pricing.engine import Quote

    catalogue = load_catalogue(ROOT / "catalogue")
    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    reader = FakeProvider({"category": "generator", "category_confidence": 0.9,
                           "model_text": "SPG3000", "has_label_or_plate": True,
                           "visible_text": ["FIRMAN", "SPG3000"]})
    other = FakeProvider({"category": "generator", "category_confidence": 0.9,
                          "model_text": None, "has_label_or_plate": True,
                          "visible_text": ["FIRMAN"]})
    seen: list[int] = []

    def ocr(images):
        seen.append(len(images))
        return ["FIRMAN", "SPG3000", "GASOLINE GENERATOR"]

    result = chain.run((ImageRef(image),), "generator", catalogue, reader, FakeProvider(),
                       CostMeter(), corroborator=other, ocr=ocr)
    assert seen == [1]
    assert result.reading.model_text == "SPG3000"
    assert result.ocr_lines == ["FIRMAN", "SPG3000", "GASOLINE GENERATOR"]
    assert any(l.name == "ocr" and l.outcome == "ok" for l in result.links)
    assert any("confirmed by OCR" in n for n in result.corroboration_notes)
    report = report_markdown(
        Case(id="x", images=[image], seller_text="generator"),
        CaseResult(case_id="x", chain=result, ledger=[], quote=Quote(failure_code="NO_PRICE_DATA", reason="t"),
                   cost_usd=0.0, latency_ms=0, cost_by_task={}, reader_model="fake", reasoner_model="fake"),
    )
    assert "## OCR read off the photos" in report and "SPG3000" in report


def test_an_ocr_engine_that_fails_is_logged_and_the_chain_goes_on():
    from buyscape.identify import chain
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())

    def broken(images):
        raise RuntimeError("model file missing")

    result = chain.run((ImageRef(image),), "thing", load_catalogue(ROOT / "catalogue"),
                       FakeProvider(), FakeProvider(), CostMeter(), ocr=broken)
    assert any(l.name == "ocr" and l.outcome == "unavailable" for l in result.links)
    assert result.ocr_lines == []


def test_the_bundled_ocr_engine_reads_a_real_plate():
    """The engine itself, on a Jiji generator photo: a plate code comes back."""
    from buyscape.identify.ocr import default_reader
    from buyscape.providers.base import ImageRef

    reader = default_reader()
    assert reader is not None, "rapidocr and onnxruntime are project dependencies"
    lines = reader((ImageRef(ROOT / "eval" / "raw" / "media" / "v4y9denCn3Xfb9uDQmPWNVgJ" / "00.jpg"),))
    assert "CL7800E2R" in lines and "COROLLA" in lines


def test_a_corroborated_field_keeps_a_source_line_so_grounding_does_not_drop_it():
    """Found on the recorded runs: corroboration blanked the source lines and the
    grounding rule then dropped every model both readers had agreed on."""
    from buyscape.identify.chain import ungrounded_fields

    a = Reading(brand_text="Samsung", model_text="Galaxy S21+ 5G", brand_source="Samsung",
                model_source="Galaxy S21+ 5G", has_label_or_plate=True,
                visible_text=["Samsung", "Galaxy S21+ 5G"])
    b = Reading(brand_text="SAMSUNG", model_text="Galaxy S21+ 5G", has_label_or_plate=True,
                visible_text=["SAMSUNG", "Galaxy S21+ 5G"])
    merged = corroborate(a, b).reading
    assert merged.model_text == "Galaxy S21+ 5G"
    assert ungrounded_fields(merged) == []


def test_a_field_written_differently_from_its_line_is_still_cited():
    from buyscape.identify.chain import ungrounded_fields

    a = Reading(model_text="SPG-3000", visible_text=["FIRMAN", "SPG 3000"])
    b = Reading(model_text="SPG3000", visible_text=["SPG 3000"])
    merged = corroborate(a, b).reading
    assert merged.model_text == "SPG-3000"
    assert ungrounded_fields(merged) == []


def test_a_short_ocr_line_confirms_nothing():
    """A line reading '2' is inside 'HSC-12000I' and confirmed an invented spec
    sheet on a Hisense box. Both sides need length, and a partial line must
    cover at least half of what it confirms."""
    a = Reading(model_text="HSC-12000I", visible_text=["Inverter 12000 BTU", "HSC-12000I"])
    b = Reading(model_text=None, visible_text=["Hisense"])
    out = corroborate(a, b, ocr_lines=["2", "XE", "Energy", "AIR CONDITIONER"])
    assert out.reading.model_text is None
    assert "Inverter 12000 BTU" not in out.reading.visible_text
    # A truncated but substantial read still counts: FPG15000 for FPG15000SE.
    out = corroborate(Reading(model_text="FPG15000SE"), Reading(), ocr_lines=["FPG15000"])
    assert out.reading.model_text == "FPG15000SE"


def test_a_shortlist_entry_the_item_does_not_carry_is_not_an_answer():
    from buyscape.identify.chain import invented_code

    read = Reading(brand_text="HP", visible_text=["HP", "512", "8"])
    assert invented_code(read, "HP EliteBook 630 G9 8GB", "HP EliteBook 820 G6")
    assert invented_code(read, "HP EliteBook 630 G9 8GB", "HP EliteBook 630 G9") is None
    assert invented_code(read, "", "HP EliteBook 630 G9", ["EliteBook 630 G9"]) is None


def test_a_code_two_readers_agreed_on_still_needs_the_ocr_or_the_seller():
    """Both readers transcribed 'Model: HSC-12000I' off a Hisense box that has
    no model code. Agreement between two language models is not enough."""
    from buyscape.identify.chain import unwitnessed_code

    assert unwitnessed_code("Hisense HSC-12000I Inverter", ["Hisense", "AIR CONDITIONER"], "1.5hp hisense")
    assert unwitnessed_code("HP EliteBook 820 G6", ["SULTECH-COMPUTERS", "512"], "HP EliteBook 630 G9")
    assert unwitnessed_code("Senci SC30000 key start", ["SE CI", "SC30000"], "") is None
    assert unwitnessed_code("Samsung Galaxy S23 Ultra", [], "S23 ultra 512 GB") is None
    assert unwitnessed_code("Apple iPhone 14 Pro", [], "") is None, "no code, nothing to witness"
