"""Authenticity is structural. The item testifies, and its records must agree.

No model is asked whether a phone is genuine or a coil is copper. These tests
prove that the records the item gives about itself are compared mechanically,
that a disagreement stops the price, and that refusing to open something is
priced as the worst thing that could be inside.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from buyscape.claims import crosscheck as cc
from buyscape.claims.ledger import ClaimStatus, build_ledger, worst_case_multiplier
from buyscape.identify.catalogue import Entry, load_catalogue
from buyscape.pricing.sources import JijiComps, MaterialsFloor, ScrapIndex
from buyscape.protocols.schema import load_protocols
from buyscape.providers.fake import FakeProvider
from buyscape.providers.tasks import ClaimDraft
from buyscape.runner import Case, report_markdown, run_case

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def catalogue():
    return load_catalogue(ROOT / "catalogue")


@pytest.fixture(scope="module")
def protocols():
    return load_protocols(ROOT / "protocols")


def phone_entry(catalogue, key: str) -> Entry:
    return next(e for e in catalogue["phone"] if e.key == key)


def test_the_same_imei_from_two_screens_must_agree():
    settings = cc.Testimony("settings_about", {"imei": "35 693010 123456 7", "model_name": "iPhone 14 Pro"})
    dial = cc.Testimony("imei_dial", {"imei": "356930101234567"})
    assert not cc.crosscheck([settings, dial], None, "Apple iPhone 14 Pro").fraud_suspected

    other = cc.Testimony("imei_dial", {"imei": "356930109999999"})
    check = cc.crosscheck([settings, other], None, "Apple iPhone 14 Pro")
    assert check.fraud_suspected
    assert "imei" in check.fraud_flags[0]


def test_a_settings_screen_naming_a_different_model_is_fraud():
    settings = cc.Testimony("settings_about", {"model_name": "iPhone 14"})
    check = cc.crosscheck([settings], None, "Apple iPhone 14 Pro")
    assert check.fraud_suspected, "an iPhone 14 sold as a 14 Pro is the wrong-part case"

    fuller = cc.Testimony("settings_about", {"model_name": "Galaxy S22 5G"})
    assert not cc.crosscheck([fuller], None, "Samsung Galaxy S22").fraud_suspected


def test_weight_off_the_catalogue_spec_is_fraud(catalogue):
    entry = phone_entry(catalogue, "Apple iPhone 14 Pro")
    assert entry.attrs["weight_g"] == "206"
    light = cc.crosscheck([cc.Testimony("scale", {"weight_g": "180"})], entry, entry.key)
    assert light.fraud_suspected
    close = cc.crosscheck([cc.Testimony("scale", {"weight_g": "204 g"})], entry, entry.key)
    assert not close.fraud_suspected


def test_the_makers_own_diagnostics_contradict_an_original_screen_claim(protocols):
    phone = protocols["phone"]
    check = cc.crosscheck([cc.Testimony("parts_history", {"non_genuine_parts": "display"})], None, None)
    assert "screen_original" in check.contradicted
    assert not check.fraud_suspected, "a replaced screen is a condition, not a lie"

    ledger = build_ledger(
        [
            ClaimDraft(
                text="screen is original",
                kind="condition",
                attribute="screen_original",
                value=None,
                checkable_remotely=True,
            )
        ],
        phone,
        slots_present={"parts_history", "screen_closeup", "settings_about"},
        contradictions=check.contradicted,
    )
    assert ledger[0].status is ClaimStatus.CONTRADICTED
    assert worst_case_multiplier(ledger) < 1.0


def test_refusing_to_open_is_priced_at_the_worst_case(protocols):
    ledger = build_ledger(
        [
            ClaimDraft(
                text="100 percent copper coil",
                kind="spec",
                attribute="winding_copper",
                value="copper",
                checkable_remotely=True,
            )
        ],
        protocols["generator"],
        slots_present=set(),
        refused_slots={"side_cover_off"},
    )
    assert ledger[0].status is ClaimStatus.REFUSED_TO_OPEN
    assert ledger[0].is_priced_at_worst_case


def test_a_catalogue_interior_fact_contradicts_what_the_open_cover_shows():
    entry = Entry("generator", "Elepaq", "SV2200", "2.5kVA", (), {"winding": "aluminium"})
    shown = cc.Testimony("side_cover_off", {"winding": "copper"})
    check = cc.crosscheck([shown], entry, entry.key)
    assert check.fraud_suspected, "a model that shipped with aluminium cannot show copper"


def test_fraud_suspected_withholds_the_price_entirely(protocols, catalogue):
    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    case = Case(
        id="clone",
        images=[image],
        seller_text="iPhone 14 Pro 256gb, 100% original",
        category_hint="phone",
        testimony=[
            cc.Testimony("settings_about", {"imei": "356930101234567", "model_name": "iPhone 14 Pro"}),
            cc.Testimony("imei_dial", {"imei": "356930109999999"}),
        ],
    )
    result = run_case(
        case,
        protocols,
        catalogue,
        JijiComps(ROOT / "eval" / "raw"),
        ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml"),
        FakeProvider(),
        FakeProvider(),
        materials=MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml"),
    )
    assert result.quote.failure_code == "FRAUD_SUSPECTED"
    assert result.quote.low is None and result.quote.high is None
    assert any("imei" in f for f in result.chain.fraud_flags)
    report = report_markdown(case, result)
    assert "## Testimony" in report and "FRAUD" in report
