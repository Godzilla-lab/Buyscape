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


def test_the_money_score_charges_overpaying_asking_and_refusing():
    from buyscape.testify.schema import Answer, Item, PriceTruth
    from buyscape.testify.stats import expected_loss

    def item(i):
        return Item(id=i, source="jiji", url=f"https://jiji.ng/{i}.html", split="dev", tier="small_goods",
                    answer=Answer(title="fan", price=PriceTruth(ngn=10000)))
    items = {i: item(i) for i in ("a", "b", "c", "d")}
    rows = [
        {"id": "a", "decision": "price", "price_low": 14000, "price_high": 20000},  # 4,000 over the asking price
        {"id": "b", "decision": "price", "price_low": 6000, "price_high": 9000},    # under: no loss
        {"id": "c", "decision": "ask_for_proof"},                                  # half the sellers drop off
        {"id": "d", "decision": "cannot_identify"},                                # the deal is lost
    ]
    out = expected_loss(rows, items, lost_deal=8000, proof_dropoff=0.5)
    assert out["loss_per_item"] == (4000 + 0 + 4000 + 8000) / 4
    assert out["overpaid_per_item"] == 1000 and out["refused_per_item"] == 2000
