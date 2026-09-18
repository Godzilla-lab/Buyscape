"""A sofa has no model number. What it is, in a buyer's words, is its identity,
and it is priced from listings of that type, never as fifteen kilograms of
cloth and wood."""

from __future__ import annotations

import json
from pathlib import Path

from buyscape.identify import chain
from buyscape.identify.catalogue import load_catalogue
from buyscape.identify.corroborate import corroborate
from buyscape.pricing.sources import JijiComps, MaterialsFloor, ScrapIndex, SourceUnavailable, is_set_listing, type_key
from buyscape.protocols.schema import load_protocols
from buyscape.providers.fake import FakeProvider
from buyscape.providers.tasks import Reading
from buyscape.runner import Case, run_case
from buyscape.tenant import load_tenant

ROOT = Path(__file__).resolve().parents[1]

SOFA = {
    "category": "sofa", "category_confidence": 0.95, "item_type": "single seater sofa",
    "materials": [{"material": "textile", "fraction": 0.7}, {"material": "wood", "fraction": 0.2}, {"material": "steel", "fraction": 0.1}],
    "estimated_weight_kg": 15.0, "weight_confidence": 0.8, "visible_text": [],
}


def _row(i, title, price_ngn, category="furniture"):
    return {"id": f"sofa{i}", "category": category, "title": title, "price_ngn": price_ngn,
            "is_used": True, "url": "", "fetched_at": "2026-09-18T12:00:00Z"}


def _abstained(reading: Reading) -> chain.ChainResult:
    r = chain.ChainResult(reading=reading, category=reading.category, type_name=reading.item_type,
                          abstained=True, failure_code="CANNOT_IDENTIFY", corroborated=True,
                          presentation=reading.presentation, type_gate=True)
    return r


def test_the_type_becomes_the_identity_only_for_want_of_a_model():
    r = _abstained(Reading(**SOFA))
    assert chain.name_by_type(r)
    assert r.model_key == "single seater sofa" and not r.abstained and r.failure_code is None
    strength, why = chain.identification_strength(r)
    assert strength == 0.8 and any("named by type" in w for w in why)
    # A heap is still a heap and two items are still two items.
    assert not chain.name_by_type(_abstained(Reading(**SOFA, presentation="mixed_lot")))
    assert not chain.name_by_type(_abstained(Reading(**{**SOFA, "multiple_items": True})))
    # An unsure category is not an identity.
    assert not chain.name_by_type(_abstained(Reading(**{**SOFA, "category_confidence": 0.4})))
    # Other abstentions are not overturned.
    other = _abstained(Reading(**SOFA)); other.failure_code = "EVIDENCE_INCOMPLETE"
    assert not chain.name_by_type(other)
    # A decider that refused a real shortlist is not overturned either.
    after = _abstained(Reading(**SOFA)); after.type_gate = False
    assert not chain.name_by_type(after)
    # A plate one reader read carries the identity, even if the other missed it.
    plated = _abstained(Reading(**SOFA)); plated.plate_seen = True
    assert not chain.name_by_type(plated)


def test_a_type_one_reader_gave_alone_needs_the_sellers_word():
    alone = _abstained(Reading(**{**SOFA, "category": "earphones", "item_type": "wired earphones"}))
    alone.uncorroborated_fields = ["item_type"]
    assert not chain.name_by_type(alone, "")
    assert not chain.name_by_type(alone, "selling my old charger")
    assert chain.name_by_type(alone, "earpiece")
    agreed = _abstained(Reading(**SOFA))
    assert chain.name_by_type(agreed, "")


def test_a_stock_photo_of_a_sofa_still_abstains():
    r = _abstained(Reading(**SOFA))
    r.fraud_flags.append("looks like a catalogue or stock image")
    assert not chain.name_by_type(r)
    assert r.abstained and r.failure_code == "EVIDENCE_INCOMPLETE" and "sofa" in r.reason


def test_two_readers_sharing_a_word_for_the_type_agree():
    a = Reading(**SOFA)
    b = Reading(**{**SOFA, "item_type": "one seater sofa chair"})
    out = corroborate(a, b)
    assert "item_type" in out.agreed and out.reading.item_type == "single seater sofa"
    c = Reading(**{**SOFA, "item_type": "armchair"})
    out = corroborate(a, c)
    assert "item_type" in out.uncorroborated and out.reading.item_type == "single seater sofa"
    d = Reading(**{**SOFA, "item_type": None})
    assert corroborate(d, a).reading.item_type == "single seater sofa"


def test_type_comps_are_single_pieces_of_that_type(tmp_path):
    rows = [_row(1, "Single Seater Sofa", 50000), _row(2, "Single Seater Sofa Modern Design", 220000),
            _row(3, "3 Seater + 2 Single Seater Sofa Set", 250000), _row(4, "Single Seater Sofa", 30000),
            _row(5, "3 Seater and One Seater Sofa", 200000), _row(6, "Sofa Cushion Chairs", 300000)]
    (tmp_path / "furniture.json").write_text(json.dumps(rows))
    comps = JijiComps(tmp_path)
    got = comps.fetch("furniture", "single seater sofa", by_type=True)
    assert sorted(o.amount for o in got) == [30000.0, 50000.0, 220000.0]
    assert is_set_listing("3 Seater + 2 Single Seater Sofa Set") and not is_set_listing("Single Seater Sofa")


def test_a_reader_says_two_seater_and_the_market_says_2_seater(tmp_path):
    rows = [_row(1, "Barely Used 2 Seater Sofa", 70000), _row(2, "A Pair of Neatly Used 2 Seater Sofas", 230000),
            _row(3, "3 Seater and 2 Seater Sofa/Chairs With Throw Pillows", 300000), _row(4, "2 Seater Sofa Chair", 90000)]
    (tmp_path / "furniture.json").write_text(json.dumps(rows))
    got = JijiComps(tmp_path).fetch("furniture", "two seater sofa", by_type=True)
    assert sorted(o.amount for o in got) == [70000.0, 90000.0]
    assert type_key("Single Seater Sofa") == "1 seater sofa"


def test_a_sofa_is_priced_from_sofas_not_as_cloth_and_wood(tmp_path):
    protocols = load_protocols(ROOT / "protocols")
    tenant = load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")
    asked = []

    def live(key, category, pages=2, used=True):
        asked.append((key, category))
        return [_row(1, "Single Seater Sofa", 50000), _row(2, "Single Seater Sofa Modern Design", 220000),
                _row(3, "3 Seater + 2 Single Seater Sofa Set", 250000), _row(4, "Single Seater Sofa", 30000)]

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    case = Case(id="sofa", images=[image], seller_text="", answers={"intact": "yes"})
    result = run_case(
        case, protocols, load_catalogue(ROOT / "catalogue"),
        JijiComps(tmp_path, live=live), ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        FakeProvider(SOFA), FakeProvider(),
        MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"), FakeProvider(SOFA), tenant,
    )
    assert result.identified and result.chain.named_type
    assert result.chain.model_key == "single seater sofa"
    # Asked in every spelling the market uses, used stock only: three comps
    # were enough, so the new stock was never asked for.
    assert [q for q, _ in asked] == ["single seater sofa", "1 seater sofa", "1 seater couch", "1 seater sofa chair"]
    assert all(c == "furniture" for _, c in asked)
    q = result.quote
    assert not q.is_failure and q.basis == "resale" and q.observation_count == 3
    # Asking 30,000 to 220,000 for singles: the buy range sits under that,
    # far above the 1,125 the same photos fetched as cloth and wood.
    assert q.high >= 50000 and q.low > 5 * q.floor, f"a sofa priced at {q.low} to {q.high}"
    assert q.worst_case_multiplier < 1.0, "unproven claims still pull the low end down"
    # The furniture protocol asks about the frame, never for a label or whether it works.
    assert not any("label" in a.ask.lower() for a in result.asks)
    assert not any("still work" in c.text for c in result.ledger)
    assert "by type" in result.chain.links[-1].detail or any(l.outcome == "type" for l in result.chain.links)


def test_with_no_comps_a_person_prices_it_never_the_floor(tmp_path):
    protocols = load_protocols(ROOT / "protocols")
    tenant = load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")
    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    case = Case(id="sofa", images=[image], seller_text="")
    result = run_case(
        case, protocols, load_catalogue(ROOT / "catalogue"),
        JijiComps(tmp_path), ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        FakeProvider(SOFA), FakeProvider(),
        MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"), None, tenant,
    )
    assert result.identified and result.chain.model_key == "single seater sofa"
    assert result.quote.failure_code == "NO_PRICE_DATA"
    assert result.quote.floor and result.quote.floor > 0


def test_a_phone_with_no_legible_label_is_not_named_by_type(tmp_path):
    """The type path is for kinds of item the model number does not price."""
    protocols = load_protocols(ROOT / "protocols")
    tenant = load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")
    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    seen = {**SOFA, "category": "phone", "item_type": "android smartphone",
            "materials": [{"material": "mixed_electronic", "fraction": 1.0}], "estimated_weight_kg": 0.2}
    result = run_case(
        Case(id="p", images=[image], seller_text=""), protocols, load_catalogue(ROOT / "catalogue"),
        JijiComps(tmp_path), ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        FakeProvider(seen), FakeProvider(),
        MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"), None, tenant,
    )
    assert not result.identified and result.chain.failure_code == "CANNOT_IDENTIFY"
    assert result.chain.type_name == "android smartphone" and not result.chain.named_type


def _new(i, title, price_ngn, category="furniture"):
    return {**_row(i, title, price_ngn, category), "id": f"new{i}", "is_used": False}


def test_a_thin_used_market_is_priced_as_a_share_of_new():
    from buyscape.pricing.engine import price
    from buyscape.pricing.sources import Observation

    used = [Observation(source="jiji_asking", kind="asking", amount=70000.0, currency="NGN", observed_on="2026-09-18")]
    new = [Observation(source="jiji_asking_new", kind="asking_new", amount=a, currency="NGN", observed_on="2026-09-18")
           for a in (150000.0, 180000.0, 200000.0, 250000.0)]
    q = price(used, [], [], identified=True, new_comps=new, resale_fraction=(0.25, 0.45))
    assert not q.is_failure and q.basis == "retail_new" and q.method == "share_of_new"
    assert q.high <= 250000 * 0.45 * 0.70 and q.low >= 150000 * 0.25 * 0.45 * q.worst_case_multiplier * 0.99
    assert "share of new" in q.explanation and "25 to 45 percent" in q.explanation
    # Without the business's rate there is no share to apply: a person prices it.
    assert price(used, [], [], identified=True, new_comps=new).failure_code == "NO_PRICE_DATA"
    # Enough used comps: the used market wins, new stock is not consulted.
    assert price(used * 3, [], [], identified=True, new_comps=new, resale_fraction=(0.25, 0.45)).basis == "resale"
    # A dead unit is never a share of new.
    assert price(used, [], [], identified=True, not_working=True, new_comps=new, resale_fraction=(0.25, 0.45)).basis != "retail_new"


def test_new_stock_is_only_asked_for_when_the_used_market_is_thin(tmp_path):
    protocols = load_protocols(ROOT / "protocols")
    tenant = load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")
    asked = []

    def live(key, category, pages=2, used=True):
        asked.append((key, used))
        if used:
            return [_row(1, "Barely Used 2 Seater Sofa", 70000)] if key == "2 seater sofa" else []
        return [_new(1, "2 Seater Sofa", 150000), _new(2, "Quality 2 Seater Sofa", 180000),
                _new(3, "2 Seater Sofa Chair", 200000), _new(4, "3 Seater Sofa", 400000)]

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    seen = {**SOFA, "item_type": "two seater sofa"}
    result = run_case(
        Case(id="sofa", images=[image], seller_text=""), protocols, load_catalogue(ROOT / "catalogue"),
        JijiComps(tmp_path, live=live), ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        FakeProvider(seen), FakeProvider(),
        MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"), FakeProvider(seen), tenant,
    )
    assert result.chain.model_key == "two seater sofa"
    q = result.quote
    assert q.basis == "retail_new" and q.observation_count == 3, q.explanation
    assert q.high >= 200000 * 0.25 * 0.45 and q.low > 5 * q.floor
    assert any(u is False for _, u in asked) and any(l.outcome == "new stock" for l in result.chain.links)
    # Both markets were asked in the digit spelling the sellers use.
    assert ("2 seater sofa", False) in asked
