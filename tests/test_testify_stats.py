"""Paired intervals and the coverage curve: a gap inside the noise is a tie,
and a careful model and a bold one are read at the same coverage."""

from buyscape.testify.stats import area, paired_bootstrap, silent_at


def _answers(n: int, priced: int, silent: list[int]) -> dict[str, dict]:
    return {f"i{k}": {"priced": k < priced, "silent": k in silent, "attempted": True, "correct": k not in silent,
                      "error": False, "confidence": (True, 12, -float(k))} for k in range(n)}


def test_the_curve_keeps_the_most_confident_answers_and_ends_at_the_model_s_own_coverage():
    answers = _answers(10, priced=4, silent=[3])
    ids = list(answers)
    assert silent_at(answers, ids, 0.2) == 0.0  # the two surest answers were right
    assert silent_at(answers, ids, 0.4) == 0.25
    assert silent_at(answers, ids, 0.5) is None  # it priced only four of ten
    assert area(answers, ids, 0.4) == (0 + 0 + 0 + 0.25) / 4


def test_identical_models_tie_and_a_large_gap_does_not():
    same = paired_bootstrap({"a": _answers(50, 20, [1]), "b": _answers(50, 20, [1])}, n=200)
    assert same["pairs"]["a - b"]["silent_wrong_rate"]["tie"]
    apart = paired_bootstrap({"a": _answers(50, 40, []), "b": _answers(50, 5, [])}, n=200)
    gap = apart["pairs"]["a - b"]["priced_share"]
    assert not gap["tie"] and gap["difference"] == 0.7


def test_a_model_that_never_prices_does_not_shorten_the_others_curve():
    out = paired_bootstrap({"a": _answers(20, 8, []), "b": _answers(20, 4, []), "c": _answers(20, 0, [])}, n=50)
    assert out["common_coverage"] == 0.2 and out["models"]["c"]["silent_area"]["point"] is None
