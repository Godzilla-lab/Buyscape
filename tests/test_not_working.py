"""A unit that does not work is priced on a dead basis, never off working prices."""

from __future__ import annotations

import json
from pathlib import Path

from buyscape.answers import review_answers
from buyscape.pricing.engine import price
from buyscape.pricing.sources import JijiComps, Observation, is_faulty_listing
from buyscape.protocols.schema import load_protocols
from buyscape.runner import says_not_working
from buyscape.tenant import load_tenant

ROOT = Path(__file__).resolve().parents[1]


def _obs(amount: float) -> Observation:
    return Observation(source="jiji_asking", kind="asking", amount=amount, currency="NGN", observed_on="2026-09-18")


def test_the_sellers_answer_or_words_say_it_does_not_work():
    protocols = load_protocols(ROOT / "protocols")
    assert review_answers(protocols["generic"], {"works_now": "no"}).not_working
    assert not review_answers(protocols["generic"], {"works_now": "yes"}).not_working
    assert review_answers(protocols["laptop"], {"what_is_wrong": "screen and battery"}).not_working
    assert not review_answers(protocols["laptop"], {"what_is_wrong": "None"}).not_working
    assert says_not_working("old hp laptop, not powering on")
    assert says_not_working("Faulty phone for parts")
    assert not says_not_working("clean laptop, works perfectly")


def test_faulty_listings_are_their_own_market_and_never_pollute_the_working_one(tmp_path):
    rows = [
        {"id": "a", "category": "laptop", "title": "Apple MacBook Air M2 2022 8GB", "price_ngn": 800000, "is_used": True},
        {"id": "b", "category": "laptop", "title": "MacBook Air M2 2022 16GB", "price_ngn": 950000, "is_used": True},
        {"id": "c", "category": "laptop", "title": "Faulty MacBook Air M2 2022 for parts", "price_ngn": 60000, "is_used": True},
        {"id": "d", "category": "laptop", "title": "MacBook Air M2 2022 not working", "price_ngn": 45000, "is_used": True},
    ]
    (tmp_path / "laptop.json").write_text(json.dumps(rows))
    comps = JijiComps(tmp_path)
    assert sorted(o.amount for o in comps.fetch("laptop", "Apple MacBook Air M2 2022")) == [800000.0, 950000.0]
    assert sorted(o.amount for o in comps.fetch("laptop", "Apple MacBook Air M2 2022", faulty=True)) == [45000.0, 60000.0]
    assert is_faulty_listing("HP EliteBook 840 G6 spoilt screen") and not is_faulty_listing("HP EliteBook 840 G6 clean")


def test_a_dead_unit_is_priced_from_faulty_listings_first():
    quote = price([_obs(45000), _obs(60000)], [], [], identified=True, not_working=True, comps_are_faulty=True)
    assert quote.basis == "not_working" and quote.method == "faulty_comps"
    assert quote.high <= 60000 * 0.70 and quote.low >= 45000 * 0.45 * quote.worst_case_multiplier


def test_then_from_the_businesss_dead_unit_share_of_the_working_price():
    tenant = load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")
    share = tenant.dead_fraction_for("laptop")
    assert share == (0.08, 0.15)
    working = [_obs(800000), _obs(850000), _obs(950000)]
    quote = price(working, [], [], identified=True, not_working=True, dead_fraction=share)
    assert quote.basis == "not_working" and quote.method == "dead_fraction"
    assert quote.high <= 950000 * 0.15 * 0.70
    assert quote.low >= 800000 * 0.08 * 0.45 * quote.worst_case_multiplier * 0.99
    alive = price(working, [], [], identified=True)
    assert quote.high < alive.low, "a dead unit must price below a working one's low end"
    assert "not working" in quote.explanation


def test_and_finally_as_material_when_nothing_else_is_on_file():
    material = [Observation(source="scrap_index_lagos", kind="scrap_floor", amount=a, currency="NGN", observed_on="2026-09-01", note="1.2 kg of aluminium, estimate") for a in (1500.0, 2200.0)]
    quote = price([], [], [], materials=material, identified=True, not_working=True)
    assert quote.basis == "not_working" and quote.method == "material_floor"
    assert quote.high == 2200.0 and not quote.is_failure


def test_a_working_item_is_untouched():
    working = [_obs(800000), _obs(850000), _obs(950000)]
    assert price(working, [], [], identified=True).basis == "resale"
