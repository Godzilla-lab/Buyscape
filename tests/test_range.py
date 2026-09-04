"""The output is a range, and the range is the product.

A quote that is wide is not a guess, it is an honest statement of how much
nobody has proven yet. Every unproven claim pushes the bottom down, so the
width is the cost of missing evidence rather than a flaw in the arithmetic.
That is what makes asking the seller for one more photograph worth doing: the
range narrows towards a number, and these tests hold the engine to that.

Until settled pickup prices exist there is nothing to calibrate against, so
the range is deliberately wide and says so. Rule 5.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from buyscape.claims.ledger import build_ledger
from buyscape.pricing.engine import price
from buyscape.pricing.sources import Observation
from buyscape.protocols.schema import load_protocols
from buyscape.providers.tasks import ClaimDraft

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def protocols():
    return load_protocols(ROOT / "protocols")


def comps():
    return [
        Observation("jiji_asking", "asking", amount, "NGN", "2026-09-04")
        for amount in (300_000, 320_000, 350_000, 380_000, 400_000, 420_000)
    ]


def claims():
    return [
        ClaimDraft(text="battery health is 95 percent", kind="spec",
                   attribute="battery_health_pct", value="95", checkable_remotely=True),
        ClaimDraft(text="storage is 256gb", kind="spec", attribute="storage_gb",
                   value="256", checkable_remotely=True),
        ClaimDraft(text="screen is original", kind="condition", attribute="screen_original",
                   value=None, checkable_remotely=True),
        ClaimDraft(text="it works perfectly", kind="works", attribute=None,
                   value=None, checkable_remotely=True),
    ]


def width(quote):
    return quote.width_ratio


def test_evidence_narrows_the_range_towards_a_number(protocols):
    """The whole reason for asking the seller for one more photograph."""
    phone = protocols["phone"]
    nothing = price(comps(), [], build_ledger(claims(), phone, slots_present=set()))
    some = price(comps(), [], build_ledger(
        claims(), phone, slots_present={"battery_health", "settings_about"}))
    everything = price(comps(), [], build_ledger(
        claims(), phone,
        slots_present={"battery_health", "settings_about", "screen_closeup",
                       "front_screen_on", "power_on_clip"}))

    assert width(nothing) > width(some) > width(everything), (
        f"widths must fall as evidence arrives: {width(nothing)}, "
        f"{width(some)}, {width(everything)}"
    )
    assert everything.low > nothing.low, "proving a claim lifts the floor, never the ceiling"
    assert everything.high == nothing.high, "evidence must not raise the top of the range"


def test_the_top_of_the_range_never_moves_on_a_seller_s_say_so(protocols):
    """A lie can only ever cost the seller, which is rule 3 stated as a range."""
    phone = protocols["phone"]
    honest = price(comps(), [], build_ledger([], phone, set()))
    boastful = price(comps(), [], build_ledger(claims(), phone, set()))
    assert boastful.high <= honest.high
    assert boastful.low <= honest.low


def test_a_wide_range_says_out_loud_that_it_is_uncalibrated(protocols):
    quote = price(comps(), [], build_ledger(claims(), protocols["phone"], set()))
    assert quote.method == "uncalibrated_wide"
    assert quote.width_ratio > 0.5, "with nothing proven the range must stay wide"
    assert quote.conditions, "and it must say which claims are holding it open"


def test_every_condition_on_the_quote_names_what_would_close_it(protocols):
    quote = price(comps(), [], build_ledger(claims(), protocols["phone"], set()))
    for line in quote.conditions:
        assert "not proven remotely" in line
        assert line.rstrip().endswith("."), line
