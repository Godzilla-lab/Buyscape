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
