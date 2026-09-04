"""Two audiences, one set of evidence.

The back office gets a number and the reasons behind it. The seller gets the
next thing to point the camera at and never sees a score, a model name or a
percentage. These tests hold that line, because leaking one into the other is
how a seller learns to argue with the engine instead of photographing the plate.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from buyscape.assess import assess, capture_requests
from buyscape.identify.chain import ChainResult
from buyscape.pricing.engine import Quote
from buyscape.protocols.schema import load_protocols
from buyscape.providers.tasks import Candidate, Identification, Reading

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def protocols():
    return load_protocols(ROOT / "protocols")


def confident_result() -> ChainResult:
    ident = Identification(
        candidates=[
            Candidate(brand="Apple", model="iPhone 13", score=0.95),
            Candidate(brand="Apple", model="iPhone 12", score=0.2),
        ],
        chosen_brand="Apple",
        chosen_model="iPhone 13",
    )
    return ChainResult(
        category="phone", brand="Apple", model="iPhone 13", margin=0.75,
        used_label=True, identification=ident, reading=Reading(has_label_or_plate=True),
    )


def torn_result() -> ChainResult:
    ident = Identification(
        candidates=[
            Candidate(brand="Elepaq", model="SV6800", score=0.55),
            Candidate(brand="Elepaq", model="SV2200", score=0.52),
        ],
        cannot_identify=True,
    )
    return ChainResult(
        category="generator", abstained=True, failure_code="CANNOT_IDENTIFY",
        reason="Two candidates scored within 0.03 of each other.",
        margin=0.03, used_label=False, identification=ident, reading=Reading(),
    )


def test_a_clear_label_and_a_wide_margin_reads_as_high_confidence():
    a = assess(confident_result(), Quote(low=1.0, high=2.0, observation_count=9), [])
    assert a.percent >= 85 and a.band == "certain"
    assert "iPhone 13" in a.sentence() and "%" in a.sentence()
    assert a.price_confidence >= 0.9


def test_two_candidates_too_close_reads_as_unsure_and_names_both():
    a = assess(torn_result(), Quote(failure_code="CANNOT_IDENTIFY"), [])
    assert a.band in ("unsure", "unknown")
    assert a.percent < 65
    sentence = a.sentence()
    assert "Not sure" in sentence and "SV6800" in sentence and "SV2200" in sentence
    assert a.price_confidence == 0.0


def test_unproven_claims_lower_the_price_confidence_not_the_identification():
    from buyscape.claims.ledger import build_ledger
    from buyscape.providers.tasks import ClaimDraft

    protocols_ = load_protocols(ROOT / "protocols")
    ledger = build_ledger(
        [ClaimDraft(text="battery is new", kind="spec", attribute="battery_health_pct",
                    value="100", checkable_remotely=True)],
        protocols_["phone"], slots_present=set(),
    )
    quote = Quote(low=1.0, high=2.0, observation_count=9)
    with_claims = assess(confident_result(), quote, ledger)
    without = assess(confident_result(), quote, [])
    assert with_claims.price_confidence < without.price_confidence
    assert with_claims.percent == without.percent


def test_the_seller_is_asked_for_the_label_when_identity_is_the_problem(protocols):
    asks = capture_requests(torn_result(), protocols["generator"], slots_present=set())
    assert asks, "an unsure answer must always produce a next step"
    assert any("plate" in a.ask.lower() or "rating" in a.ask.lower() for a in asks)


def test_two_items_in_frame_is_asked_about_before_anything_else(protocols):
    result = ChainResult(
        category="phone", abstained=True, failure_code="EVIDENCE_INCOMPLETE",
        reading=Reading(multiple_items=True),
    )
    asks = capture_requests(result, protocols["phone"], slots_present=set())
    assert "one item on its own" in asks[0].ask


def test_a_screenshot_of_a_gallery_is_asked_to_be_retaken(protocols):
    result = ChainResult(category="phone", reading=Reading(screenshot_of_gallery=True))
    asks = capture_requests(result, protocols["phone"], slots_present=set())
    assert "not a picture of another screen" in asks[0].ask


def test_nothing_shown_to_the_seller_mentions_a_score_or_a_model_name(protocols):
    """The seller-facing text is a camera instruction, never a verdict."""
    banned = ("%", "confidence", "score", "candidate", "catalogue", "sv6800", "iphone", "model_")
    for result, protocol in [
        (torn_result(), protocols["generator"]),
        (confident_result(), protocols["phone"]),
        (ChainResult(reading=Reading(stock_photo_suspected=True)), protocols["generic"]),
    ]:
        for ask in capture_requests(result, protocol, slots_present=set()):
            lowered = ask.ask.lower()
            for word in banned:
                assert word not in lowered, f"{word!r} leaked into a seller instruction: {ask.ask}"


def test_the_seller_is_never_shown_more_than_three_things_at_once(protocols):
    asks = capture_requests(torn_result(), protocols["generator"], slots_present=set())
    assert 1 <= len(asks) <= 3


def test_an_answer_the_evidence_barely_supports_is_not_priced():
    """The real miss: an iPhone 13 answered as a 13 Pro at 42 percent, and
    priced anyway. The label was legible but the two readers shared no lines,
    so almost nothing about the item was actually established."""
    from buyscape.identify import chain
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.providers.base import CallMeta, CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider

    class Torn:
        name = model = "torn"

        def structured_call(self, request):
            payload = {
                "candidates": [
                    {"brand": "Apple", "model": "iPhone 13 Pro", "score": 0.72},
                    {"brand": "Apple", "model": "iPhone 13", "score": 0.50},
                ],
                "chosen_brand": "Apple", "chosen_model": "iPhone 13 Pro",
            }
            return request.output_schema.model_validate(payload), CallMeta("t", "t", request.task, 0)

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    seen = {"category": "phone", "category_confidence": 0.95, "has_label_or_plate": True,
            "visible_text": ["APPLE WARRANTY"], "stock_photo_suspected": True}
    other = {"category": "phone", "category_confidence": 0.95, "has_label_or_plate": True,
             "visible_text": ["NO LCD WARRANTY"]}
    result = chain.run((ImageRef(image),), "iphone 13", load_catalogue(ROOT / "catalogue"),
                       FakeProvider(seen), Torn(), CostMeter(),
                       corroborator=FakeProvider(other))
    assert result.abstained, "a 42 percent answer must not be priced"
    assert result.failure_code == "EVIDENCE_INCOMPLETE"
    assert "guess" in (result.reason or "")
    assert result.model is None


def test_the_gate_number_and_the_reported_number_are_the_same_number():
    from buyscape.identify.chain import identification_strength

    r = confident_result()
    assert identification_strength(r)[0] == assess(r, Quote(low=1.0, high=2.0), []).confidence


def test_readers_that_disagree_get_a_guided_video_not_another_still(protocols):
    """Two models that cannot agree on a plate will not agree on a second
    photo of the same angle either. A video gives hundreds of frames, shows
    the item running, and cannot be a picture of somebody else's machine."""
    from buyscape.assess import capture_requests
    from buyscape.identify.chain import ChainResult
    from buyscape.providers.tasks import Reading

    result = ChainResult(
        category="generator", abstained=True, failure_code="CANNOT_IDENTIFY",
        reading=Reading(), corroborated=True,
        corroboration_notes=["model_text differed between the two readers, so it is treated as unread"],
    )
    asks = capture_requests(result, protocols["generator"], slots_present=set())
    video = [a for a in asks if a.kind == "video"]
    assert video, "a disagreement between readers must escalate to a video"
    script = video[0].ask
    assert "one take" in script and "every side" in script
    assert "rating plate" in script or "plate" in script
    assert "side cover" in script, "the video should also cover what must be opened"


def test_every_protocol_can_produce_a_video_script(protocols):
    """A new category gets a sensible video by writing YAML, not code."""
    from buyscape.assess import video_script

    for name, protocol in protocols.items():
        script = video_script(protocol)
        assert script.count(".") >= 3, f"{name} produced a thin script"
        assert "thirty seconds" in script and "Do not cut" in script


def test_a_video_never_asks_the_seller_to_film_a_screenshot(protocols):
    """You cannot film a screenshot. On a phone the identifying evidence lives
    on its own screen, so the instruction has to be to use it while filming."""
    from buyscape.assess import video_script

    phone = video_script(protocols["phone"])
    assert "Screenshot of" not in phone
    assert "still filming" in phone and "own screen" in phone
    generic = video_script(protocols["generic"])
    assert generic.count("walk") <= 1, "the walkaround must not be repeated as the finish"


def test_a_video_ask_still_says_nothing_about_models_or_scores(protocols):
    from buyscape.assess import video_script

    for protocol in protocols.values():
        lowered = video_script(protocol).lower()
        for word in ("%", "confidence", "score", "candidate", "catalogue"):
            assert word not in lowered
