"""Scrap is sold by weight, and the weight is written in the advert.

The tenant's own listings are not phones and generators. They are ten tons of
circuit boards, a ton of titanium nets, a yard of mixed metal. For all of it
the price is a rate times a weight, and a photograph of a heap has nothing in
frame to give it scale. The seller does know the weight, because they weighed
it or bought it by the ton, and the scale at pickup settles the difference.
"""

from __future__ import annotations

from pathlib import Path

from buyscape.pricing.sources import parse_stated_weight_kg

ROOT = Path(__file__).resolve().parents[1]


def test_the_weight_a_seller_states_is_read_from_their_own_words():
    assert parse_stated_weight_kg("10 Ton Scrap Plastic Circuit Boards Needed") == 10_000
    assert parse_stated_weight_kg("1 Ton of Scrap Titanium Nets Required") == 1_000
    assert parse_stated_weight_kg("selling 2.5 tonnes of copper") == 2_500
    assert parse_stated_weight_kg("about 500kg of iron") == 500
    assert parse_stated_weight_kg("30 metric tons available") == 30_000


def test_the_largest_stated_weight_wins_when_several_are_mentioned():
    assert parse_stated_weight_kg("50kg bags, 20 tons in total") == 20_000


def test_a_storage_size_or_a_capacity_is_not_a_weight():
    assert parse_stated_weight_kg("iPhone 14 Pro 256gb dual sim") is None
    assert parse_stated_weight_kg("Hisense 7.5kg washing machine") == 7.5
    assert parse_stated_weight_kg("no numbers here at all") is None


def test_a_stated_tonnage_lifts_a_scrap_quote_out_of_the_photo_estimate():
    """The real miss: ten tons of boards quoted at 8,370 naira against an
    asking price of ten million, because the weight came from a photograph."""
    from buyscape.pricing.engine import price
    from buyscape.pricing.sources import MaterialsFloor

    floor = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    shares = [("circuit_board", 0.6), ("plastic", 0.4)]
    guessed = price([], [], [], materials=floor.fetch(shares, 5.0), identified=False)
    stated = price([], [], [], materials=floor.fetch(shares, 10_000.0), identified=False)
    assert stated.high > guessed.high * 100
    assert stated.weight_conditional, "a stated weight is still settled on the scale"


def test_the_engine_prefers_the_stated_weight_over_the_photo_guess(tmp_path):
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.pricing.sources import JijiComps, MaterialsFloor, ScrapIndex
    from buyscape.protocols.schema import load_protocols
    from buyscape.providers.fake import FakeProvider
    from buyscape.runner import Case, run_case

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    reader = FakeProvider({
        "category": "scrap boards", "category_confidence": 0.9,
        "presentation": "mixed_lot", "estimated_weight_kg": 8.0, "weight_confidence": 0.4,
        "materials": [{"material": "circuit_board", "fraction": 1.0}],
    })
    case = Case(id="lot", images=[image], seller_text="10 Ton Scrap Plastic Circuit Boards")
    result = run_case(
        case, load_protocols(ROOT / "protocols"), load_catalogue(ROOT / "catalogue"),
        JijiComps(ROOT / "eval" / "raw"), ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        reader, FakeProvider(), MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"),
    )
    assert not result.quote.is_failure, "a lot of scrap must always get a price"
    assert result.quote.high > 1_000_000, "ten tons of boards is not worth a few thousand naira"
    assert result.quote.weight_conditional
    assert any(l.name == "weight" and l.outcome == "stated" for l in result.chain.links)


def test_the_engine_never_offers_more_than_the_seller_asked():
    """Ten tons of boards quoted at 38 million against an asking price of ten
    million. A rate estimate that escapes upward is worse than one that is low."""
    from buyscape.pricing.engine import Quote, cap_at_asking

    quote = cap_at_asking(Quote(low=8_000_000.0, high=38_770_000.0), 10_000_000.0)
    assert quote.high == 10_000_000.0
    assert quote.low <= quote.high
    assert any("never offers more" in c for c in quote.conditions)


def test_a_quote_already_below_the_asking_price_is_left_alone():
    from buyscape.pricing.engine import Quote, cap_at_asking

    quote = cap_at_asking(Quote(low=30_000.0, high=47_000.0), 70_000.0)
    assert quote.high == 47_000.0 and not quote.conditions


def test_a_seller_who_named_no_price_is_not_capped():
    from buyscape.pricing.engine import Quote, cap_at_asking

    for asking in (None, 0):
        quote = cap_at_asking(Quote(low=1.0, high=2.0), asking)
        assert quote.high == 2.0


def test_the_board_rate_comes_from_the_tenants_own_wanted_adverts():
    """No dated Nigerian schedule publishes a scrap circuit board rate, so the
    engine uses what this business advertises to pay: three adverts of 25 March
    2025, each working out at 1,000 naira per kilogram. A guess of 1,500 to
    4,000 had the engine offering 38 million for a lot advertised at 10 million."""
    from buyscape.pricing.sources import MaterialsFloor

    floor = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    low, high, published = floor.rate("circuit_board")
    assert (low, high) == (800.0, 1000.0)
    assert published, "a dated wanted advert is evidence, not an estimate"

    obs = floor.fetch([("circuit_board", 1.0)], 10_000.0)
    assert max(o.amount for o in obs) <= 10_000_000
    assert "estimates" not in obs[0].note, "a sourced rate must not be labelled a guess"
