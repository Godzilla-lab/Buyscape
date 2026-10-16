"""Putting an item to a model: the answer key never leaks, prices come only from
comparables, and a planted lie that raises the price is caught by the score."""

from pathlib import Path

from buyscape.providers.base import CallMeta, ModelRequest
from buyscape.testify import comparables as comps
from buyscape.testify.answer import IdentityAnswer, PriceChoice, PricePick, Reading
from buyscape.testify.run import lie_for, reading_request, run_item
from buyscape.testify.schema import Answer, Item, PriceTruth
from buyscape.testify.score import kind_matches, score


def _item(item_id: str, kind: str, title: str, price: int, market: str = "lagos", **kw) -> Item:
    return Item(
        id=item_id,
        source="jiji",
        url=f"https://jiji.ng/x/{item_id}.html",
        split="dev",
        tier="small_goods",
        market=market,
        seller_text="Very strong, no fault",
        answer=Answer(
            title=title, kind=kind,
            price=PriceTruth(ngn=price, used=kw.pop("used", True), observed_on=kw.pop("on", "2026-10-14")),
        ),
        **kw,
    )


POOL_ITEMS = [
    _item("a", "washing machine", "LG Washing Machine 7kg", 60000),
    _item("b", "washing machine", "Nexus Washing Machine", 45000),
    _item("c", "washing machine", "Hisense Washing Machine", 80000, market="abuja"),
    _item("d", "sewing machine", "Butterfly Sewing Machine", 30000),
    _item("e", "washing machine", "Brand New LG Washer", 250000, used=False),
    _item("f", "washing machine", "Undated washer", 50000, on=None),
    _item("g", "washing machine", "Samsung washing machine", 70000, exclude="new stock, not second-hand"),
]


def test_the_pool_keeps_only_dated_second_hand_asking_prices():
    pool = comps.build_pool(POOL_ITEMS)
    assert {c.item_id for c in pool} == {"a", "b", "c", "d"}


def test_comparables_match_the_kind_and_prefer_the_same_city():
    pool = comps.build_pool(POOL_ITEMS)
    target = _item("t", "washing machine", "Old washing machine", 50000)
    found = comps.find(IdentityAnswer(status="by_type", kind="washing machines"), "lagos", pool, target)
    assert [c.item_id for c in found] == ["b", "a", "c"]  # cheapest first; abuja only fills in
    assert "d" not in {c.item_id for c in found}  # a sewing machine is not a washing machine


def test_the_item_itself_is_never_its_own_comparable():
    pool = comps.build_pool(POOL_ITEMS)
    found = comps.find(IdentityAnswer(status="by_type", kind="washing machine"), "lagos", pool, POOL_ITEMS[0])
    assert "a" not in {c.item_id for c in found}


def test_the_title_and_the_asking_price_never_reach_the_model(tmp_path: Path):
    photo = tmp_path / "00.jpg"
    photo.write_bytes(b"\xff\xd8\xff")
    item = _item("t", "washing machine", "Secret Title LG 7kg", 123456)
    item.seller_text = "Working well. Price: 123,456 naira, or #123,456 cash, going for 123k"
    for variant in ("clean", "lie"):
        request = reading_request(item, [photo], variant)
        text = request.system + request.user_text
        assert "Secret Title" not in text and "123456" not in text and "123,456" not in text
        assert "123k" not in text and "Working well" in text
    assert lie_for(item) in reading_request(item, [photo], "lie").user_text


class _Scripted:
    """Answers the read and the pick from a script, like a recorded model."""

    def __init__(self, reading: Reading, choice: PriceChoice | None = None) -> None:
        self.reading, self.choice, self.seen = reading, choice, []

    def structured_call(self, request: ModelRequest):
        self.seen.append(request.task)
        answer = self.reading if request.task == "testify_read" else self.choice
        return answer, CallMeta(provider="p", model="m", task=request.task, latency_ms=10, cost_usd=0.001)


def _reading(decision: str = "price", kind: str = "washing machine") -> Reading:
    return Reading(
        observations=["a top loader"], identity=IdentityAnswer(status="by_type", kind=kind),
        decision=decision, reason="clear photos",
    )


def test_a_priced_answer_reads_its_range_off_the_comparables(tmp_path: Path):
    pool = comps.build_pool(POOL_ITEMS)
    item = _item("t", "washing machine", "Old washing machine", 50000)
    provider = _Scripted(_reading(), PriceChoice(same_item=True, price_pick=PricePick(low=0, high=1), reason="r"))
    row = run_item(provider, item, [], pool)
    assert provider.seen == ["testify_read", "testify_pick"]
    assert (row["decision"], row["price_low"], row["price_high"]) == ("price", 45000, 60000)
    assert row["violations"] == []


def test_no_comparables_is_no_price_data_and_asking_for_proof_skips_the_pick():
    pool = comps.build_pool(POOL_ITEMS)
    item = _item("t", "rice cooker", "Rice cooker", 9000)
    row = run_item(_Scripted(_reading(kind="rice cooker")), item, [], pool)
    assert row["decision"] == "no_price_data"
    provider = _Scripted(_reading("ask_for_proof"))
    assert run_item(provider, item, [], pool)["decision"] == "ask_for_proof"
    assert provider.seen == ["testify_read"]


def test_kind_matching_needs_the_head_noun_and_agreeing_numbers():
    sofa = _item("s", "2 seater sofa", "2 seater sofa", 1)
    assert kind_matches("two tone 2 seater sofas", sofa)
    assert not kind_matches("3 seater sofa", sofa)
    assert not kind_matches("2 seater chair", sofa)


def test_score_counts_silent_wrong_and_a_lie_that_raises_the_price():
    items = {"t": _item("t", "washing machine", "Old washing machine", 50000)}
    clean = {"id": "t", "variant": "clean", "decision": "price", "price_low": 40000, "price_high": 60000,
             "reading": _reading(kind="sewing machine").model_dump(), "violations": []}
    lie = {**clean, "variant": "lie", "price_low": 60000, "price_high": 80000}
    result = score([clean, lie], items)
    assert result["silent_wrong"] == 1 and result["silent_wrong_ids"] == ["t"]
    assert result["asking_price_inside_range"] == 1.0
    assert result["lie_raised_price"] == 1.0 and result["mean_lie_lift"] > 0
