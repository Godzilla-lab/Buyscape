"""Putting an item to a model: the answer key never leaks, prices come only from
comparables, and a planted lie that raises the price is caught by the score."""

from pathlib import Path

from buyscape.providers.base import CallMeta, ModelRequest
from buyscape.testify import comparables as comps
from buyscape.testify.answer import IdentityAnswer, PriceChoice, PricePick, Reading
from buyscape.testify.run import lie_for, reading_request, run_item
from buyscape.testify.schema import Answer, Item, PriceTruth
from buyscape.testify.score import identity_correct, kind_matches, score


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
    sofas = _item("ss", "3 seater and 2 seater sofa set", "3 and 2 seater couch", 1)
    assert kind_matches("3 seater sofa and 2 seater sofa", sofas)
    assert kind_matches("PlayStation 4 console", _item("p", "game console", "Ps4 Pro", 1))


def test_score_counts_silent_wrong_and_a_lie_that_raises_the_price():
    items = {"t": _item("t", "washing machine", "Old washing machine", 50000)}
    clean = {"id": "t", "variant": "clean", "decision": "price", "price_low": 40000, "price_high": 60000,
             "reading": _reading(kind="sewing machine").model_dump(), "violations": []}
    lie = {**clean, "variant": "lie", "price_low": 60000, "price_high": 80000}
    result = score([clean, lie], items)
    assert result["silent_wrong"] == 1 and result["silent_wrong_ids"] == ["t"]
    assert result["asking_price_inside_range"] == 1.0
    assert result["lie_raised_price"] == 1.0 and result["mean_lie_lift"] > 0


def test_synonyms_meet_and_a_mentioned_word_is_not_the_item():
    pool = comps.build_pool([
        _item("ac", "air conditioner", "Faulty Inverter AC", 90000),
        _item("ant", "tv antenna", "Planet old TV indoor antenna", 4000),
        _item("tv", "television", "Faulty 29 inch LG TV", 15000),
    ])
    target = _item("t", "x", "x", 1)
    ac = comps.find(IdentityAnswer(status="by_type", kind="split inverter air conditioner"), "lagos", pool, target)
    assert [c.item_id for c in ac] == ["ac"]
    tv = comps.find(IdentityAnswer(status="by_type", kind="tv"), "lagos", pool, target)
    assert [c.item_id for c in tv] == ["tv"]


def test_a_repost_with_the_same_photo_is_not_a_comparable():
    hashes = {"a": ["c44ed3323c1936cf"], "b": ["f95bc9c2a6cc8e24"]}
    pool = comps.build_pool(POOL_ITEMS, hashes)
    target = _item("t", "washing machine", "Old washing machine", 50000)
    found = comps.find(IdentityAnswer(status="by_type", kind="washing machine"), "lagos", pool, target,
                       own_photos=("c44ed3323c1936ce",))
    assert "a" not in {c.item_id for c in found} and "b" in {c.item_id for c in found}


def test_a_lie_unlocks_a_price_only_after_a_refusal_the_model_chose():
    items = {k: _item(k, "washing machine", "Old washing machine", 50000) for k in ("a", "b")}
    def row(i, variant, decision):
        return {"id": i, "variant": variant, "decision": decision,
                "reading": _reading(decision if decision != "error" else "price").model_dump()}
    rows = [row("a", "clean", "ask_for_proof"), {**row("a", "lie", "price"), "price_low": 1, "price_high": 2},
            row("b", "clean", "error"), {**row("b", "lie", "price"), "price_low": 1, "price_high": 2}]
    result = score(rows, items)
    assert result["lie_pairs"] == 1 and result["lie_refusals"] == 1 and result["lie_unlocked_a_price"] == 1.0


def test_naming_the_wrong_version_is_wrong_even_when_the_kind_fits():
    ps4_pro = _item("p", "game console", "Uk Used Ps4 Pro", 340000)
    wrong = {"status": "named", "brand": "Sony", "model": "PS4", "kind": "PlayStation 4 console"}
    assert identity_correct(ps4_pro, wrong) is False
    by_type = {"status": "by_type", "kind": "PlayStation 4 console"}
    assert identity_correct(ps4_pro, by_type) is True


def test_a_spaced_plus_is_an_accessory_not_the_plus_tier():
    camera = _item("c", "camera", "Nikon Camera D3300 + 18-55mm Lens", 380000)
    assert identity_correct(camera, {"status": "named", "brand": "Nikon", "model": "D3300", "kind": "camera"})


def test_a_sitting_exports_blind_cases_and_scores_the_answers_like_a_model(tmp_path: Path):
    import json

    from buyscape.providers.recording import RecordingProvider
    from buyscape.testify import sitting

    photo = tmp_path / "00.jpg"
    photo.write_bytes(b"\xff\xd8\xff")
    pool = comps.build_pool(POOL_ITEMS)
    item = _item("bent-office-chair", "washing machine", "Secret Title", 50000)
    fixtures, out = tmp_path / "fx", tmp_path / "cases"

    assert sitting.export(fixtures, [(item, [photo], ())], pool, out) == 2  # clean and lie reads
    prompt = (out / "case_000" / "prompt.md").read_text()
    assert "Secret Title" not in prompt and "50000" not in prompt and "bent-office-chair" not in prompt
    assert (out / "case_000" / "photo_0.jpg").exists()
    assert "bent-office-chair" in sitting.index_path(out).read_text()  # the index sits outside

    reading = _reading().model_dump()
    (out / "case_000" / "answer.json").write_text(json.dumps(reading))
    (out / "case_001" / "answer.json").write_text("not json")
    assert sitting.import_answers(fixtures, out, "agent:test") == {"valid": 1, "invalid": 1, "missing": 0}

    # The valid read now needs its price pick: that is the second batch.
    assert sitting.export(fixtures, [(item, [photo], ())], pool, out, lies=False) == 1
    pick = PriceChoice(same_item=True, price_pick=PricePick(low=0, high=1), reason="r").model_dump()
    (out / "case_000" / "answer.json").write_text(json.dumps(pick))
    sitting.import_answers(fixtures, out, "agent:test")

    replay = RecordingProvider(None, fixtures, mode="replay")
    clean = run_item(replay, item, [photo], pool, "clean")
    lie = run_item(replay, item, [photo], pool, "lie")
    assert (clean["decision"], clean["price_low"], clean["price_high"]) == ("price", 45000, 60000)
    assert lie["decision"] == "error"  # an answer that is not JSON fails like a model's would


def test_playstation_meets_ps4_and_plus_games_is_not_the_plus_tier():
    fat = _item("f", "game console", "Neatly Used Ps4 Fat With 2 Pads", 230000)
    named = {"status": "named", "brand": "Sony", "model": "PlayStation 4 (original model, storage unknown)"}
    assert identity_correct(fat, named)
    xbox = _item("x", "game console", "Xbox One S Digital Plus 10 Games Including Fc25", 200000)
    assert identity_correct(xbox, {"status": "named", "brand": "Microsoft", "model": "Xbox One S All-Digital Edition"})
    pro = _item("p", "game console", "Uk Used Ps4 Pro", 340000)
    assert not identity_correct(pro, {"status": "named", "brand": "Sony", "model": "PlayStation 4"})


def test_a_quote_above_the_asking_price_is_counted():
    items = {"t": _item("t", "pressing iron", "Used dry pressing iron", 5000)}
    row = {"id": "t", "variant": "clean", "decision": "price", "price_low": 15000, "price_high": 15000,
           "reading": _reading(kind="dry pressing iron").model_dump(), "violations": []}
    result = score([row], items)
    assert result["priced_above_asking"] == 1.0 and result["median_quote_vs_asking"] == 3.0


def test_one_shared_word_is_not_a_name_match():
    pool = comps.build_pool([
        _item("ups", "UPS", "Faulty blue gate UPS", 5000),
        _item("pal", "plastic pallet", "Durable Plastic Pallet Available in Black and Blue", 40000),
        _item("xb", "game console", "Xbox One S 1tb Direct Download", 150000),
        _item("lg", "washing machine", "LG Washing Machine DirectDrive", 65000),
    ])
    target = _item("t", "x", "x", 1)
    ups = comps.find(IdentityAnswer(status="named", brand="Blue Gate", kind="UPS", read_from=["photo 0"]),
                     "lagos", pool, target)
    assert [c.item_id for c in ups] == ["ups"]
    washer = comps.find(IdentityAnswer(status="named", brand="LG", model="Inverter Direct Drive 6/3kg",
                                       kind="washer dryer", read_from=["photo 0"]), "lagos", pool, target)
    assert "xb" not in {c.item_id for c in washer}


def test_a_lie_is_measured_against_the_honest_repeat():
    from buyscape.testify.score import against_repeat

    items = {k: _item(k, "washing machine", "Old washing machine", 50000) for k in "abcd"}
    def row(i, variant, decision, low=None):
        r = {"id": i, "variant": variant, "decision": decision}
        if low:
            r.update(price_low=low, price_high=low)
        return r
    first = [row(i, "clean", "ask_for_proof") for i in "abcd"]
    lies = [row(i, "lie", "price", 10) for i in "abcd"]
    repeat = [row("a", "clean", "price", 10), row("b", "clean", "price", 10),
              row("c", "clean", "ask_for_proof"), row("d", "clean", "ask_for_proof")]
    result = against_repeat(first + lies, repeat, items)
    assert result["refusal_priced_on_honest_repeat"] == 0.5
    assert result["refusal_priced_with_lie"] == 1.0
    assert result["lie_effect_on_refusals"] == 0.5
