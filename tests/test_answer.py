"""The answer a model must give: picks by number, never a price of its own."""

import json

from buyscape.testify.answer import InspectionAnswer, parse

GOOD = {
    "observations": ["standing fan, base cracked", "no plate visible"],
    "identity": {"status": "by_type", "kind": "standing fan"},
    "claims": [{"claim": "works perfectly", "verdict": "unverified", "evidence": "no clip of it running"}],
    "risks": [{"risk": "motor does not turn", "proof": "10 second clip switched on", "if_unproven": "as not working"}],
    "proof_requests": ["clip of it running"],
    "decision": "price",
    "reason": "Named by type and priced from used fans until the clip arrives.",
    "price_pick": {"low": 0, "high": 2},
}


def answer(**changes):
    return json.dumps({**GOOD, **changes})


def test_a_good_answer_parses_with_no_violations():
    parsed, problems = parse(answer(), comparables=5)
    assert parsed is not None and problems == []


def test_a_price_written_in_text_is_a_violation():
    for money in ("worth about N45,000", "₦45000", "around 45k naira", "NGN 1.2m tops"):
        _, problems = parse(answer(reason=money), comparables=5)
        assert any("wrote a price" in p for p in problems), money


def test_counts_and_ratings_are_not_mistaken_for_prices():
    _, problems = parse(answer(observations=["3 photos", "rated 10 kVA", "16 inch blades"]), comparables=5)
    assert problems == []


def test_a_pick_beyond_the_list_is_a_violation():
    _, problems = parse(answer(price_pick={"low": 0, "high": 7}), comparables=5)
    assert any("only 5 were given" in p for p in problems)


def test_loud_outcomes_are_consistent():
    bad = [
        answer(decision="price", price_pick=None),
        answer(decision="price", identity={"status": "unknown"}),
        answer(decision="cannot_identify", identity={"status": "by_type", "kind": "fan"}, price_pick=None),
        answer(decision="ask_for_proof"),
        answer(identity={"status": "named", "brand": "Ox"}),
        answer(price_pick={"low": 3, "high": 1}),
    ]
    for raw in bad:
        parsed, problems = parse(raw, comparables=5)
        assert parsed is None and problems, raw
    ok, problems = parse(answer(decision="cannot_identify", identity={"status": "unknown"}, price_pick=None), 5)
    assert ok is not None and problems == []


def test_garbage_is_a_scored_failure_not_a_crash():
    parsed, problems = parse("Sure! This fan is worth N20,000.", comparables=5)
    assert parsed is None and problems


def test_schema_exports_for_constrained_decoding(tmp_path):
    from buyscape.testify.answer import export_schema

    path = tmp_path / "answer.schema.json"
    export_schema(path)
    schema = json.loads(path.read_text())
    assert "price_pick" in schema["properties"] and "observations" in schema["required"]
    assert InspectionAnswer.model_validate(GOOD).decision == "price"
