"""Some facts are only in the seller's head, and they still have to be checked.

No photograph says how old a laptop is or whether it was dropped. The seller
knows. Asking is cheap and the answer moves the price, so the engine asks, and
then checks the answer against what the catalogue knows rather than believing it.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from buyscape.answers import review_answers, unanswered
from buyscape.identify.catalogue import load_catalogue
from buyscape.protocols.schema import load_protocols

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 9, 4)


@pytest.fixture(scope="module")
def protocols():
    return load_protocols(ROOT / "protocols")


@pytest.fixture(scope="module")
def catalogue():
    return load_catalogue(ROOT / "catalogue")


def entry(catalogue, category, key):
    return next(e for e in catalogue[category] if e.key == key)


def test_every_protocol_asks_only_things_a_photo_cannot_answer(protocols):
    for name, protocol in protocols.items():
        assert protocol.questions, f"{name} asks the seller nothing"
        assert len(protocol.questions) <= 4, f"{name} asks too much of a seller"
        for q in protocol.questions:
            assert q.ask.endswith("?") or q.ask.endswith("."), q.ask
            assert len(q.ask) < 120, "a question a seller will not read"


def test_a_seller_calling_a_2011_laptop_twenty_years_old_is_contradicted(protocols, catalogue):
    """The user's own example. A 2011 machine is about fifteen years old now."""
    mac = entry(catalogue, "laptop", "Apple MacBook Pro 17-inch 2011")
    assert mac.attrs["year"] == "2011"
    out = review_answers(protocols["laptop"], {"age_years": "20"}, mac, today=TODAY)
    assert out.contradictions, "twenty years against a fifteen year old machine must be flagged"
    assert any("shipped in 2011" in n for n in out.notes)


def test_an_age_that_fits_the_catalogue_is_accepted(protocols, catalogue):
    mac = entry(catalogue, "laptop", "Apple MacBook Pro 17-inch 2011")
    out = review_answers(protocols["laptop"], {"age_years": "15"}, mac, today=TODAY)
    assert not out.contradictions
    assert any("agrees" in n for n in out.notes)


def test_calling_a_2011_machine_two_years_old_is_contradicted(protocols, catalogue):
    mac = entry(catalogue, "laptop", "Apple MacBook Pro 17-inch 2011")
    out = review_answers(protocols["laptop"], {"age_years": "2"}, mac, today=TODAY)
    assert out.contradictions


def test_an_answer_becomes_a_claim_that_can_only_lower_the_price(protocols, catalogue):
    from buyscape.claims.ledger import build_ledger, worst_case_multiplier

    out = review_answers(protocols["phone"], {"age_years": "3", "screen_replaced": "yes"},
                         entry(catalogue, "phone", "Apple iPhone 13"), today=TODAY)
    assert out.drafts
    ledger = build_ledger(out.drafts, protocols["phone"], slots_present=set())
    assert worst_case_multiplier(ledger) < 1.0, "an unproven answer must lower, never raise"


def test_a_seller_saying_no_is_recorded_as_the_worst_case(protocols, catalogue):
    out = review_answers(protocols["laptop"], {"holds_charge": "no"}, None, today=TODAY)
    assert any("says no" in n for n in out.notes)
    assert out.drafts and out.drafts[0].checkable_remotely is False


def test_questions_already_answered_are_not_asked_again(protocols):
    asked = unanswered(protocols["laptop"], {"age_years": "5"})
    assert "age_years" not in {q.id for q in asked}
    assert asked, "the rest are still worth asking"


def test_no_catalogue_entry_means_no_check_and_no_false_accusation(protocols):
    out = review_answers(protocols["laptop"], {"age_years": "20"}, None, today=TODAY)
    assert not out.contradictions, "an unidentified item cannot contradict a spec we do not have"
    assert out.drafts
