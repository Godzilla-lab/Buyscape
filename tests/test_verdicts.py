"""Human verdicts outrank the listing title, and a must-abstain set is a gate row.

The Jiji title is not a trustworthy answer key outside phones: sellers title a
generator by an inflated kVA while the plate says otherwise. A person who has
looked at the plate settles it, and the scorer must honour that verdict over
the title. Separately, ten cases nobody could identify from the photos must
come back as an abstention every time, which is a gate row of its own.
"""

from __future__ import annotations

from pathlib import Path

from buyscape.evalset.score import GATE, Verdicts, load_verdicts, score
from buyscape.identify.chain import ChainResult
from buyscape.pricing.engine import Quote
from buyscape.runner import Case, CaseResult


def _pair(case_id: str, title: str, brand: str | None, model: str | None, **chain_kw):
    case = Case(id=case_id, images=[], truth={"title": title, "category": "generator"})
    chain = ChainResult(category="generator", brand=brand, model=model, used_label=True, **chain_kw)
    result = CaseResult(
        case_id=case_id, chain=chain, ledger=[], quote=Quote(), cost_usd=0.0,
        latency_ms=0, cost_by_task={}, reader_model="r", reasoner_model="d",
    )
    return case, result


def test_title_scores_the_plate_answer_wrong_until_a_person_settles_it():
    pair = _pair("g1", "Elepaq 11kva Generator", "Elepaq", "EP-6500")
    assert score([pair]).summary()["model_top1_accuracy_with_label"] == 0.0
    verdicts = Verdicts(adjudicated={"g1": "correct"})
    summary = score([pair], verdicts).summary()
    assert summary["model_top1_accuracy_with_label"] == 1.0
    assert summary["silent_wrong_rate"] == 0.0
    assert summary["adjudicated"] == 1


def test_a_person_can_also_overrule_a_lucky_title_match():
    pair = _pair("g2", "Senci SC5000 generator", "Senci", "SC5000")
    assert score([pair]).summary()["silent_wrong_rate"] == 0.0
    summary = score([pair], Verdicts(adjudicated={"g2": "wrong"})).summary()
    assert summary["silent_wrong_rate"] == 1.0


def test_must_abstain_set_is_held_only_by_a_real_abstention():
    held = _pair("a1", "Generator", None, None, abstained=True, failure_code="CANNOT_IDENTIFY")
    broke = _pair("a2", "Generator", None, None, failure_code="PROVIDER_ERROR")
    guessed = _pair("a3", "Generator", "Elepaq", "SV2200")
    verdicts = Verdicts(must_abstain={"a1", "a2", "a3"})
    summary = score([held, broke, guessed], verdicts).summary()
    assert summary["must_abstain_held"] == round(1 / 3, 4)
    assert GATE["must_abstain_held"] == 1.0


def test_no_must_abstain_set_means_no_data_not_a_pass():
    pair = _pair("x", "Generator", None, None, abstained=True)
    assert score([pair]).summary()["must_abstain_held"] is None


def test_verdict_files_load_from_the_eval_directory(tmp_path: Path):
    (tmp_path / "adjudications.yaml").write_text(
        "- id: g1\n  verdict: correct\n  seen: plate reads EP-6500\n  by: someone\n  on: 2026-09-05\n"
    )
    (tmp_path / "must_abstain.yaml").write_text("- id: a1\n  why: no label in any photo\n")
    v = load_verdicts(tmp_path)
    assert v.adjudicated == {"g1": "correct"}
    assert v.must_abstain == {"a1"}
    empty = load_verdicts(tmp_path / "nowhere")
    assert empty.adjudicated == {} and empty.must_abstain == set()
