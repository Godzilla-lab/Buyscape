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


def test_retrieval_finds_the_right_model_and_refuses_junk(catalogue):
    hits = search(catalogue, "Apple iPhone 13 128 GB", "phone")
    assert hits and hits[0][0].model == "iPhone 13"
    assert search(catalogue, "qwertyuiop nonsense", "phone") == []


def test_scoring_is_strict_about_model_numbers():
    assert model_matches("Apple", "iPhone 13", "Apple iPhone 13 128 GB White")
    assert not model_matches("Apple", "iPhone 14", "Apple iPhone 13 128 GB White")
    assert not model_matches(None, None, "Apple iPhone 13")


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
