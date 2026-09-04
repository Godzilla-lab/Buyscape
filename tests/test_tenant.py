"""Onboarding a business is a file. If it needs code, that is a bug.

BuyScrap's twenty categories are mostly materials, not products: aluminium,
carton, old newspapers, food waste. The engine is built around identifying
items, so without this mapping every one of them fell through to the generic
protocol, which asks a heap of copper for its model number.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from buyscape.protocols.schema import load_protocols
from buyscape.tenant import load_tenant

ROOT = Path(__file__).resolve().parents[1]

SITE_CATEGORIES = [
    "Aluminium", "Brass", "Carton", "Copper", "E-waste", "Fabrics and Textiles",
    "Food Waste", "Glass", "Glass Bottles", "Industrial Machines", "Iron",
    "Office Chair", "Old Newspapers", "Papers", "Plastic and Rubbers", "Premium",
    "Scrap Car", "Scrap Vehicles", "Used Books", "Wood and Furnitures",
]


@pytest.fixture(scope="module")
def tenant():
    return load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")


@pytest.fixture(scope="module")
def protocols():
    return load_protocols(ROOT / "protocols")


def test_every_category_on_the_tenants_site_is_covered(tenant):
    assert {c.name for c in tenant.categories} == set(SITE_CATEGORIES)


def test_every_category_reaches_a_protocol_that_suits_it(tenant, protocols):
    for name in SITE_CATEGORIES:
        protocol = tenant.protocol_for(protocols, name)
        assert protocol.category in {"material_lot", "vehicle", "generic"}, name
        assert protocol.pickup_protocol, name


def test_every_category_has_a_rate_the_engine_can_price_from(tenant):
    index = yaml.safe_load((ROOT / "tenants" / "scrap_index_lagos.yaml").read_text())
    known = set(index.get("per_kg") or {}) | set(index.get("per_kg_derived") or {})
    known |= set((index.get("per_kg_tenant") or {}).get("rates") or {})
    for entry in tenant.categories:
        assert entry.material in known or entry.material == "unknown", entry.name


def test_copper_defaults_to_the_cheaper_grade(tenant):
    """Bare copper is four times insulated. It is never assumed, only proven."""
    assert tenant.material_for("Copper") == "copper_insulated"


def test_the_material_lot_protocol_makes_the_seller_cut_the_wire(protocols):
    lot = protocols["material_lot"]
    assert "cut_or_open" in {s.id for s in lot.opening_shots}
    assert any("bare" in q.ask.lower() or "covered" in q.ask.lower() for q in lot.questions)
    assert any("cut a sample" in line.lower() for line in lot.pickup_protocol)


def test_a_vehicle_is_never_bought_without_papers(protocols):
    vehicle = protocols["vehicle"]
    ownership = next(c for c in vehicle.claims if c.id == "ownership")
    assert ownership.penalty <= 0.3, "no papers must gut the price, not dent it"
    assert any("papers" in line.lower() for line in vehicle.pickup_protocol)
    assert {"engine_bay", "boot_and_cabin"} <= {s.id for s in vehicle.opening_shots}


def test_something_the_tenant_never_listed_still_resolves(tenant, protocols):
    """People sell things nobody wrote down. None of them may be refused."""
    for spoken in ["sewing machine", "chest freezer", "shawarma machine", "septic tank"]:
        assert tenant.protocol_for(protocols, spoken).pickup_protocol


def test_the_tenants_own_published_minimum_is_honoured(tenant):
    """Their blog says they buy scrap laptops starting from 5,000 naira. The
    engine quoted 4,318 for a MacBook, contradicting its own operator."""
    assert tenant.minimum_for("laptop") == 5000.0
    assert tenant.minimum_for("phone") is None


def test_things_the_tenant_refuses_are_an_outcome_not_a_low_price(tenant):
    """Their brass guide says plainly that they do not purchase brass shells."""
    refusal = tenant.refusal("a box of brass shell casings from a range")
    assert refusal and "not purchase" in refusal.because.lower()
    assert tenant.refusal("a coil of copper wire") is None


def test_the_brass_grades_are_the_tenants_own_words(tenant):
    names = {g["name"] for g in tenant.grades["brass"]}
    assert {"red brass", "yellow brass", "brass turnings"} <= names
    red = next(g for g in tenant.grades["brass"] if g["name"] == "red brass")
    turnings = next(g for g in tenant.grades["brass"] if g["name"] == "brass turnings")
    assert red["copper_pct"] > turnings["copper_pct"], "red brass is the dearer grade"


def test_the_magnet_test_is_asked_for_because_it_grades_metal_for_nothing(protocols):
    lot = protocols["material_lot"]
    magnet = next(s for s in lot.shots if s.id == "magnet_test")
    assert "magnetic" in magnet.extract
    assert any("magnet" in line.lower() for line in lot.pickup_protocol)


def _run(seller_text, overrides, tenant, protocols, asking=None):
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.pricing.sources import JijiComps, MaterialsFloor, ScrapIndex
    from buyscape.providers.fake import FakeProvider
    from buyscape.runner import Case, run_case

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    case = Case(id="t", images=[image], seller_text=seller_text, asking_price=asking)
    return run_case(
        case, protocols, load_catalogue(ROOT / "catalogue"),
        JijiComps(ROOT / "eval" / "raw"), ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        FakeProvider(overrides), FakeProvider(),
        MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"), None, tenant,
    )


def test_a_refused_item_is_a_loud_outcome_not_a_small_number(tenant, protocols):
    result = _run("selling brass shell casings from a shooting range",
                  {"category": "brass", "category_confidence": 0.9,
                   "materials": [{"material": "brass", "fraction": 1.0}],
                   "estimated_weight_kg": 20.0}, tenant, protocols)
    assert result.quote.failure_code == "NOT_PURCHASED"
    assert result.quote.low is None


def test_a_laptop_is_never_quoted_below_the_published_minimum(tenant, protocols):
    # The real reading from their own MacBook Pro advert, which priced at 4,318.
    result = _run("old macbook, battery bad",
                  {"category": "laptop", "category_confidence": 0.95,
                   "materials": [{"material": "aluminium", "fraction": 0.6},
                                 {"material": "plastic", "fraction": 0.3},
                                 {"material": "circuit_board", "fraction": 0.05},
                                 {"material": "steel", "fraction": 0.05}],
                   "estimated_weight_kg": 2.1}, tenant, protocols)
    assert not result.quote.is_failure
    assert result.quote.high >= 5000, "their blog says laptops start at 5,000 naira"
    assert any("minimum this business publishes" in c for c in result.quote.conditions)


def test_a_pile_of_scrap_gets_the_material_protocol_not_the_generic_one(tenant, protocols):
    result = _run("about 500kg of copper wire",
                  {"category": "copper", "category_confidence": 0.9, "presentation": "mixed_lot",
                   "materials": [{"material": "copper_insulated", "fraction": 1.0}]},
                  tenant, protocols)
    assert not result.quote.is_failure
    assert any("cut" in c.lower() or "weigh" in c.lower() for c in result.quote.conditions) or result.quote.weight_conditional
