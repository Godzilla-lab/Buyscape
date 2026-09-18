"""Tests for the parts that decide whether a wrong price can be produced."""

from __future__ import annotations

from pathlib import Path

import pytest

from buyscape.claims.ledger import Claim, ClaimStatus, build_ledger, conditions, worst_case_multiplier
from buyscape.evalset.score import model_matches
from buyscape.identify.catalogue import load_catalogue, search
from buyscape.pricing.engine import price
from buyscape.pricing.sources import JijiComps, ScrapIndex, SourceUnavailable
from buyscape.protocols.schema import load_protocols
from buyscape.providers.tasks import ClaimDraft

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def catalogue():
    return load_catalogue(ROOT / "catalogue")


@pytest.fixture(scope="module")
def protocols():
    return load_protocols(ROOT / "protocols")


def test_every_protocol_loads_and_has_pickup_rules(protocols):
    assert set(protocols) >= {"generic", "phone", "generator", "split_ac", "washing_machine"}
    for name, p in protocols.items():
        assert p.pickup_protocol, f"{name} has no pickup protocol"
        assert p.required_shots, f"{name} requires no evidence"


def test_non_generic_protocols_ask_the_seller_to_open_the_item(protocols):
    for name in ("generator", "split_ac", "washing_machine"):
        assert protocols[name].opening_shots, f"{name} never asks for an interior shot"


def test_laptops_have_a_protocol_that_opens_the_panel_and_a_catalogue(protocols, catalogue):
    laptop = protocols["laptop"]
    assert "bottom_panel_off" in {s.id for s in laptop.opening_shots}
    assert {s.id for s in laptop.required_shots} >= {"code_shot", "about_screen", "bottom_sticker"}
    hits = search(catalogue, "LENOVO 14W AMD A4-9120C", "laptop")
    assert hits and hits[0][0].model == "14w"


def test_retrieval_finds_the_right_model_and_refuses_junk(catalogue):
    hits = search(catalogue, "Apple iPhone 13 128 GB", "phone")
    assert hits and hits[0][0].model == "iPhone 13"
    assert search(catalogue, "qwertyuiop nonsense", "phone") == []


def test_scoring_is_strict_about_model_numbers():
    assert model_matches("Apple", "iPhone 13", "Apple iPhone 13 128 GB White")
    assert not model_matches("Apple", "iPhone 14", "Apple iPhone 13 128 GB White")
    assert not model_matches(None, None, "Apple iPhone 13")


def test_scoring_rejects_a_pro_max_answer_for_a_plain_model():
    """The miss the lenient rule let through: a 13 Pro Max scored as a 13."""
    assert not model_matches("Apple", "iPhone 13 Pro Max 128GB Graphite", "Apple iPhone 13 128 GB White")
    assert model_matches("Samsung", "Galaxy S10+", "New Samsung Galaxy S10 Plus 128 GB Black")
    assert model_matches("Nokia", "110 Africa Edition", "New Nokia 110 Green")


def test_scoring_meets_a_plate_code_written_as_seller_shorthand():
    assert model_matches("Kemage", "KM5000i", "Kemage 5000i 4.5kva Low-Noise Inverter Generator")
    assert model_matches("Star Arc", "Welding Generator-350", "Star Arc Welding Generator 350a")
    assert not model_matches("Elepaq", "TAMARIN 6.5KVA", "15kva Elepaq Constant Generator")
    assert model_matches("Corolla", "CL7800E-2R", "COROLLA Cl7800e2r 4.5kva Petrol Gen Remote Control")
    assert model_matches("Thuraya", "XT-LITE Satellite phone", "New Thuraya XT Lite 64 GB Gray")


def test_a_seller_stating_another_rating_blocks_the_answer():
    from buyscape.identify.chain import rating_contradiction

    assert rating_contradiction("15kva Elepaq Constant Generator", "6.5kVA Elepaq TAMARIN")
    assert rating_contradiction("Kemage 5000i 4.5kva", "4.5kVA KM5000i") is None
    assert rating_contradiction("Original Hisense 7.5kg washing machine", "8kg HW80-1468") is None
    assert rating_contradiction("clean generator", "6.5kVA") is None


def test_a_seller_naming_another_generation_blocks_the_answer(catalogue):
    from buyscape.identify.chain import seller_contradiction

    phones = catalogue["phone"]
    assert seller_contradiction("14 pro 256gb 680k 128gb 640k", "Apple iPhone 13 Pro Max", phones)
    assert seller_contradiction("iPhone 14pro 128gb 98% battery", "Apple iPhone 13 Pro Max", phones)
    assert seller_contradiction("Brand new S10+ available", "Samsung Galaxy S10+", phones) is None
    assert seller_contradiction("13 pro 128gb", "Apple iPhone 13 Pro", phones) is None
    assert seller_contradiction("Clean phone, works well", "Apple iPhone 13", phones) is None


def test_comps_refuse_rather_than_substitute_a_different_model():
    comps = JijiComps(ROOT / "eval" / "raw")
    with pytest.raises(SourceUnavailable):
        comps.fetch("phone", "Nokia 3310")


def test_scrap_index_refuses_above_published_bands():
    index = ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml")
    with pytest.raises(SourceUnavailable):
        index.fetch("generator", 500.0)


def test_no_comparable_prices_produces_a_loud_failure_not_a_number():
    quote = price(comps=[], scrap=[], ledger=[])
    assert quote.is_failure
    assert quote.failure_code == "NO_PRICE_DATA"
    assert quote.low is None and quote.high is None


def test_unproven_claims_only_ever_lower_the_price(protocols):
    drafts = [
        ClaimDraft(
            text="battery health is 95 percent",
            kind="spec",
            attribute="battery_health_pct",
            value="95",
            checkable_remotely=True,
        ),
        ClaimDraft(
            text="phone works perfectly",
            kind="works",
            attribute=None,
            value=None,
            checkable_remotely=True,
        ),
    ]
    ledger = build_ledger(drafts, protocols["phone"], slots_present=set())
    assert all(c.status is ClaimStatus.UNVERIFIED for c in ledger)
    multiplier = worst_case_multiplier(ledger)
    assert multiplier < 1.0
    assert conditions(ledger), "unproven claims must appear as quote conditions"

    proven = build_ledger(
        drafts, protocols["phone"], slots_present={"battery_health", "front_screen_on", "power_on_clip"}
    )
    assert worst_case_multiplier(proven) == 1.0
    assert worst_case_multiplier(proven) >= multiplier


def test_a_lie_cannot_raise_the_remote_price(protocols):
    """The same item, described honestly and then with an unprovable boast."""
    from buyscape.pricing.sources import Observation

    comps = [
        Observation("jiji_asking", "asking", amount, "NGN", "2026-09-04")
        for amount in (300000, 320000, 350000, 380000)
    ]
    honest = price(comps, [], build_ledger([], protocols["phone"], set()))
    boastful = price(
        comps,
        [],
        build_ledger(
            [
                ClaimDraft(
                    text="battery is brand new 100 percent",
                    kind="spec",
                    attribute="battery_health_pct",
                    value="100",
                    checkable_remotely=True,
                )
            ],
            protocols["phone"],
            slots_present=set(),
        ),
    )
    assert boastful.low <= honest.low
    assert boastful.high <= honest.high


def test_an_unidentified_item_is_still_priced_as_material():
    """The open world rule: not knowing what it is never means no price."""
    from buyscape.pricing.sources import MaterialsFloor

    floor = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    obs = floor.fetch([("iron", 0.8), ("steel", 0.15), ("copper", 0.05)], 15.0)
    quote = price([], [], [], materials=obs, identified=False)
    assert not quote.is_failure
    assert quote.basis == "material_floor"
    assert quote.low and quote.low > 0
    assert quote.weight_conditional, "an estimated weight must be settled at the scale"


def test_no_weight_and_no_identity_is_a_loud_failure():
    quote = price([], [], [], materials=[], identified=False)
    assert quote.is_failure and quote.failure_code == "CANNOT_IDENTIFY"


def test_derived_material_rates_are_labelled_as_estimates():
    from buyscape.pricing.sources import MaterialsFloor

    floor = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    published = floor.fetch([("copper", 1.0)], 10.0)
    assert "estimates" not in published[0].note
    derived = floor.fetch([("pet_bottle", 1.0)], 10.0)
    assert "estimates" in derived[0].note


def test_identification_lifts_the_price_above_the_material_floor():
    """Knowing what it is should be worth more than knowing what it is made of."""
    from buyscape.pricing.sources import MaterialsFloor, Observation

    floor = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    materials = floor.fetch([("steel", 0.6), ("plastic", 0.3), ("copper", 0.1)], 5.0)
    comps = [
        Observation("jiji_asking", "asking", amount, "NGN", "2026-09-04")
        for amount in (300000, 320000, 350000, 380000)
    ]
    as_material = price([], [], [], materials=materials, identified=False)
    as_item = price(comps, [], [], materials=materials, identified=True)
    assert as_item.high > as_material.high
    assert as_item.basis == "resale"


def test_scorer_does_not_punish_detail_the_listing_title_omits():
    """A seller's title is shorthand, not a spec sheet.

    These were all counted as failures by the first scorer, which made the
    engine look worse than it was.
    """
    assert model_matches("Google", "Pixel Fold 512GB", "New Google Pixel Fold 512 GB Black")
    assert model_matches("Nokia", "110 Africa Edition", "New Nokia 110 Green")
    assert model_matches("Xiaomi", "Redmi 15C 256GB", "New Xiaomi Redmi 15C 4G 128 GB Black")


def test_scorer_still_catches_the_errors_that_cost_money():
    """A wrong generation is the error that produces a wrong price."""
    assert not model_matches("Apple", "iPhone 14", "Apple iPhone 13 128 GB White")
    assert not model_matches("Apple", "iPhone 12 Pro", "Apple iPhone 13 128 GB White")
    assert not model_matches("Samsung", "Galaxy S22 Ultra", "Samsung Galaxy S23 Ultra 512 GB")
    assert not model_matches("LG", "T2108", "Hisense 9kg Top Loader Washing Machine")


def test_nothing_to_rank_means_no_reasoner_call(catalogue):
    """Three quarters of cases abstain; they must not pay for the decider first."""
    from buyscape.identify import chain
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider

    class Exploding:
        name = model = "never"

        def structured_call(self, request):
            raise AssertionError("the reasoner was called with nothing to rank")

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    reader = FakeProvider({"category": "chest freezer", "category_confidence": 0.9})
    result = chain.run((ImageRef(image),), "old freezer", catalogue, reader, Exploding(), CostMeter())
    assert result.abstained and result.failure_code == "CANNOT_IDENTIFY"


def test_ranking_sends_few_small_images_and_the_reader_keeps_full_frames():
    from buyscape.providers.base import ImageRef
    from buyscape.providers.tasks import Reading, identify, read_evidence

    seen = {}

    class Capture:
        name = model = "capture"

        def structured_call(self, request):
            seen[request.task] = request
            payload = {"candidates": [], "cannot_identify": True} if request.task == "identify" else {}
            from buyscape.providers.base import CallMeta

            return request.output_schema.model_validate(payload), CallMeta("c", "c", request.task, 0)

    images = tuple(ImageRef(p) for p in list((ROOT / "eval" / "raw" / "media").rglob("*.jp*"))[:5])
    read_evidence(Capture(), images)
    identify(Capture(), images, Reading(), [], "")
    assert len(seen["read_evidence"].images) == 5 and seen["read_evidence"].image_max_side is None
    assert len(seen["identify"].images) == 3 and seen["identify"].image_max_side == 1024
    assert seen["identify"].max_tokens <= 700
    mime, small = images[0].encoded(1024)
    assert len(small) <= len(images[0].path.read_bytes())


def test_every_name_a_model_used_reaches_a_real_protocol(protocols):
    """The words the models actually produced across every proof run so far.

    An exact dictionary lookup sent all of these to the generic protocol, and
    with them went the rating plate, the winding photo and the settings
    screenshot that make the price defensible.
    """
    from buyscape.protocols.schema import resolve

    expected = {
        "generator": [
            "generator", "portable generator", "gasoline generator", "diesel generator",
            "inverter generator", "welding generator", "solar generator", "petrol generator set",
        ],
        "phone": ["phone", "smartphone", "satellite phone", "mobile phone", "android phone"],
        "washing_machine": ["washing machine", "twin tub washing machine", "washer dryer"],
        "split_ac": ["split air conditioner", "air conditioner", "split ac", "1.5hp split unit"],
        "laptop": ["laptop", "macbook", "notebook computer"],
    }
    for category, spoken_names in expected.items():
        for spoken in spoken_names:
            assert resolve(protocols, spoken).category == category, spoken


def test_an_item_in_no_category_still_gets_the_generic_protocol(protocols):
    """Rule: people sell anything. Nothing is refused for lacking a protocol."""
    from buyscape.protocols.schema import resolve

    for spoken in ["sewing machine", "electric motor", "phone holder stand", "chest freezer", "", None]:
        protocol = resolve(protocols, spoken)
        assert protocol.category == "generic"
        assert protocol.opening_shots, "an unknown item must still be opened before payment"


def test_comps_are_found_even_when_the_category_word_differs():
    """An identified model is worth its price whatever shelf the comps sit on."""
    comps = JijiComps(ROOT / "eval" / "raw")
    found = comps.fetch("portable computer", "HP EliteBook 2570P")
    assert found and all(o.amount > 0 for o in found)


def test_the_label_on_the_item_outranks_the_shortlist():
    """A real silent wrong: plate read 'WM-200', answer said 'Hisense WTJA801'."""
    from buyscape.identify.chain import label_contradiction
    from buyscape.providers.tasks import Reading

    plate = Reading(model_text="WM-200", visible_text=["Model: WM-200", "Capacity: 7kg"])
    assert label_contradiction(plate, "Hisense WTJA801 8kg top loader")
    assert label_contradiction(plate, "Famos WM-200 7kg") is None
    assert label_contradiction(Reading(), "Hisense WTJA801") is None, "no label, nothing to contradict"


def test_the_answer_may_not_invent_a_rating_the_item_never_showed():
    """A generator's kVA is its price, so an unevidenced kVA is an invented price."""
    from buyscape.identify.chain import invented_rating
    from buyscape.providers.tasks import Reading

    plate = Reading(visible_text=["ELEPAQ", "GASOLINE GENERATOR", "YADPENG"], model_text="SY6500")
    assert invented_rating(plate, "clean generator for sale", "ELEPAQ SY6500 1.5KVA")
    assert invented_rating(plate, "4.5kva elepaq constant", "ELEPAQ SY6500 4.5KVA") is None
    shown = Reading(visible_text=["MODEL: BAC-12000", "RATING: 1.5HP"], model_text="BAC-12000")
    assert invented_rating(shown, "", "Bona BAC-12000 1.5HP split type") is None
    assert invented_rating(shown, "", "Bona BAC-12000 2.5HP") is not None


def test_a_model_code_and_a_rating_that_cannot_both_be_true(catalogue):
    """A real hallucination: the reader transcribed a whole plate that read
    'MODEL: SY6500' and 'OUTPUT: 1.5KVA'. A SY6500 is a six and a half kilowatt
    machine, so the two numbers cannot both be right and neither can be priced."""
    from buyscape.identify.chain import code_rating_contradiction
    from buyscape.providers.tasks import Reading

    invented = Reading(model_text="SY6500", rating_text="1.5KVA", visible_text=["OUTPUT: 1.5KVA"])
    assert code_rating_contradiction(invented)

    # Every generator in the catalogue must pass, or the band is too tight.
    for entry in catalogue["generator"]:
        kva = entry.attrs.get("kva")
        if not kva:
            continue
        honest = Reading(model_text=entry.model, rating_text=f"{kva}kVA")
        assert code_rating_contradiction(honest) is None, f"{entry.key} wrongly flagged"

    assert code_rating_contradiction(Reading(model_text="iPhone 14 Pro")) is None
    assert code_rating_contradiction(Reading(rating_text="8kg")) is None


def test_air_conditioner_is_a_category_not_a_tier_word():
    """The bug that scored every split AC wrong.

    "Air" is a tier word because an iPhone Air is not an iPhone. But "Air
    Conditioner" is the name of the category every one of these listings
    carries, so the rule fired on all 45 of them and the correct answer
    scored as a miss.
    """
    assert model_matches("Hisense", "AS-12 1.5HP", "Hisense 1.5HP Efficient Split Air Conditioner")
    assert model_matches("LG", "S4-Q18 2HP", "LG 2HP Split Air-conditioning Unit")
    assert model_matches("Midea", "MSAF-12 1.5HP", "Midea 1.5hp Air Condition Inverter")
    # The tier word still bites where it is genuinely a tier.
    assert not model_matches("Apple", "MacBook Pro 13", "Apple MacBook Air 13 256GB")


def test_a_unit_is_not_an_identity():
    """The bug that let a wrong brand score as the right answer.

    An appliance title is mostly brand, capacity and category. If the shared
    word is allowed to be the unit itself, then "LG 1.5HP" and "Hisense 1.5HP"
    share "hp", agree on 15, and the wrong brand scores correct. Capacity is
    not identity, so units cannot carry the match on their own.
    """
    assert not model_matches("LG", "S4-Q12 1.5HP", "Hisense 1.5HP Split Air Conditioner")
    assert not model_matches("Samsung", "AR12 1.5HP", "Hisense 1.5HP Split Air Conditioner")
    assert not model_matches("LG", "T2108 8kg top loader", "Hisense 8kg Top Load Washing Machine")
    # The right brand still matches on the same evidence.
    assert model_matches("Hisense", "AS-12 1.5HP", "Hisense 1.5HP Split Air Conditioner")


def test_the_witnesses_look_at_the_photos_at_the_same_time_and_the_page_hears_each_stage(catalogue):
    """Two readers, the OCR and the claims extraction are independent, so they
    overlap; the seller waits for the slowest, not the sum."""
    import threading
    import time

    from buyscape.identify import chain
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider

    class Slow(FakeProvider):
        def structured_call(self, request):
            time.sleep(0.4)
            return super().structured_call(request)

    def slow_ocr(images):
        time.sleep(0.4)
        return ["FIRMAN", "SPG3000"]

    seen = {"category": "generator", "category_confidence": 0.9, "model_text": "SPG3000",
            "brand_text": "FIRMAN", "brand_source": "FIRMAN", "model_source": "SPG3000",
            "has_label_or_plate": True, "visible_text": ["FIRMAN", "SPG3000"]}
    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    stages: list[str] = []
    started = time.perf_counter()
    result = chain.run((ImageRef(image),), "firman gen", catalogue, Slow(seen), FakeProvider(), CostMeter(),
                       corroborator=Slow(seen), ocr=slow_ocr, progress=stages.append)
    elapsed = time.perf_counter() - started
    assert elapsed < 1.0, f"three 0.4 s witnesses took {elapsed:.2f} s: they ran one after another"
    assert result.reading.model_text == "SPG3000" and result.ocr_lines == ["FIRMAN", "SPG3000"]
    assert stages[0] == "reading"
