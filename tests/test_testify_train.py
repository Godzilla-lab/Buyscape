"""The fine-tuning set: only right reads are kept, a known item is priced at
its worst case, nothing named beyond the photos, and every twin's lie comes
from the training lies, never the benchmark's."""

import json
from pathlib import Path

from PIL import Image

from buyscape.testify import train
from buyscape.testify.run import lie_for
from buyscape.testify.schema import Answer, Item, PriceTruth


def _item(item_id: str, kind: str, title: str) -> Item:
    return Item(
        id=item_id, source="jiji", url=f"https://jiji.ng/x/{item_id}.html", split="train", tier="small_goods",
        market="kano", seller_text="Very clean, no fault",
        answer=Answer(title=title, kind=kind, price=PriceTruth(ngn=50000, used=True, observed_on="2026-10-17")),
    )


def _read(decision="ask_for_proof", status="by_type", kind="standing fan", **identity):
    return {
        "observations": ["a standing fan with three blades"],
        "identity": {"status": status, "kind": kind, **identity},
        "claims": [{"claim": "no fault", "verdict": "unverified", "evidence": "no clip of it running"}],
        "risks": [{"risk": "motor may be weak", "proof": "clip of it running", "if_unproven": "as not working"}],
        "proof_requests": ["clip of it running"],
        "decision": decision,
        "reason": "it may not work",
    }


FAN = _item("f1", "standing fan", "Ox standing fan")


def test_a_right_read_becomes_a_price_at_the_worst_case_and_keeps_its_doubts():
    answer, why = train.target(FAN, _read())
    assert why == "kept: price at worst case"
    assert answer.decision == "price" and answer.reason == train.WORST_CASE_REASON
    assert answer.claims[0].verdict == "unverified" and answer.proof_requests == ["clip of it running"]


def test_a_wrong_read_is_dropped_and_an_honest_unknown_is_kept_as_declining():
    assert train.target(FAN, _read(kind="sewing machine"))[0] is None
    answer, why = train.target(FAN, _read(status="unknown", kind=None))
    assert why == "kept: cannot identify" and answer.decision == "cannot_identify"


def test_a_model_the_photos_cannot_show_is_cut_back_to_the_kind():
    named = _read(status="named", brand="Ox", model="SF-16", read_from=["photo 0 label"])
    answer, _ = train.target(FAN, named, {"identity_from_photos_alone": "by_type"})
    assert answer.identity.status == "by_type" and answer.identity.brand is None
    kept, _ = train.target(FAN, named, {"identity_from_photos_alone": "named"})
    assert kept.identity.brand == "Ox"


def test_a_teacher_that_writes_a_price_is_dropped():
    pricey = _read()
    pricey["observations"] = ["a standing fan, worth about N25,000"]
    assert train.target(FAN, pricey) == (None, "teacher wrote a price")


def test_a_twin_lists_the_lie_as_unproven_and_changes_nothing_else():
    answer, _ = train.target(FAN, _read())
    lied = train.twin(answer, "Bought new last month")
    assert lied.decision == answer.decision and lied.identity == answer.identity
    assert lied.claims[-1].claim == "Bought new last month" and lied.claims[-1].verdict == "unverified"


def test_training_lies_never_repeat_the_benchmark_and_are_stable():
    lie = train.train_lie(FAN)
    assert lie != lie_for(FAN) and lie == train.train_lie(FAN)
    benchmark = (Path(train.TRAIN_LIES).parent / "lies.yaml").read_text()
    for entry in train._train_lies():
        for line in entry["lies"]:
            assert line not in benchmark


def test_build_writes_the_exact_prompt_with_photo_paths_and_a_twin(tmp_path: Path):
    photo = tmp_path / "eval" / "raw" / "testify_train" / "media" / "f1" / "00.jpg"
    photo.parent.mkdir(parents=True)
    Image.new("RGB", (32, 24), "blue").save(photo)
    rows = [{"id": "f1", "variant": "clean", "reading": _read()}]
    examples, tally = train.build([(FAN, [photo])], rows, {}, tmp_path)
    assert tally == {"kept: price at worst case": 1} and [e["variant"] for e in examples] == ["clean", "lie"]
    system, user, said = examples[1]["messages"]
    assert "JSON Schema" in system["content"] and "Ox standing fan" not in json.dumps(examples)
    assert {"type": "image", "image": "eval/raw/testify_train/media/f1/00.jpg"} in user["content"]
    assert train.train_lie(FAN) in user["content"][0]["text"]
    assert json.loads(said["content"])["claims"][-1]["claim"] == train.train_lie(FAN)


def test_a_name_on_an_unchecked_advert_stays_only_if_the_ocr_found_it(tmp_path: Path):
    photo = tmp_path / "00.jpg"
    Image.new("RGB", (32, 24), "blue").save(photo)
    named = _read(status="named", brand="Ox", model="SF-16", read_from=["photo 0 label"])
    rows = [{"id": "f1", "variant": "clean", "reading": named}]
    seen = train.build([(FAN, [photo])], rows, {}, tmp_path, ocr=lambda images: ["OX", "MODEL SF 16"])[0]
    assert json.loads(seen[0]["messages"][2]["content"])["identity"]["model"] == "SF-16"
    unseen, tally = train.build([(FAN, [photo])], rows, {}, tmp_path, ocr=lambda images: ["OXFORD", "220V"])
    assert json.loads(unseen[0]["messages"][2]["content"])["identity"]["status"] == "by_type"
    assert tally == {"kept: price at worst case, name cut to the kind": 1}
    blind = train.build([(FAN, [photo])], rows, {}, tmp_path, ocr=None)[0]
    assert json.loads(blind[0]["messages"][2]["content"])["identity"]["status"] == "by_type"


def test_a_short_name_must_be_a_whole_word_on_the_photo():
    read = _read(status="named", brand="LG", model="")
    assert train.on_photos(read, ["LG", "Inverter"])
    assert not train.on_photos(read, ["SLG-2201 part"])


def test_the_trainer_shrinks_big_photos_and_keeps_both_twins_on_one_side():
    from buyscape.testify import sft_lora

    big = sft_lora.shrink(Image.new("RGB", (4000, 3000)), 576)
    assert big.size[0] * big.size[1] <= 576 * sft_lora.PIXELS_PER_TOKEN and abs(big.size[0] / big.size[1] - 4 / 3) < 0.01
    assert sft_lora.shrink(Image.new("RGB", (320, 240)), 576).size == (320, 240)
    twins = [{"id": f"a{n}", "variant": v} for n in range(200) for v in ("clean", "lie")]
    sides = {}
    for e in twins:
        sides.setdefault(e["id"], set()).add(sft_lora.held_out(e, 0.05))
    assert all(len(s) == 1 for s in sides.values()) and 0 < sum(s == {True} for s in sides.values()) < 30


def test_a_training_read_is_judged_by_the_title_not_the_word_it_was_searched_under():
    from buyscape.testify.score import title_kind_matches

    bed = _item("b1", "bed frame", "Electric Hospital Bed")
    assert train.target(bed, _read(kind="electric hospital bed"))[0] is not None
    carbon = _item("c1", "pallets", "Pallet Activated Carbon")
    assert train.target(carbon, _read(kind="activated carbon"))[0] is not None
    assert not title_kind_matches("drill press", "Drilling Machine")
    assert title_kind_matches("gas cooker with oven", "Gas Cooker")
    assert title_kind_matches("PS4 Pro console", "Ps4 Pro 2 Pads 7 Free Games")
    assert not title_kind_matches("washing machine", "Industrial Sewing Machine")
    assert title_kind_matches("bed frame", "Bedframe for Sale")
    assert title_kind_matches("headlight assembly", "Headlamp for Toyota 4runner")
    microwave = _item("m1", "microwave", "Hisense Microwave")
    assert train.target(microwave, _read(kind="microwave oven"))[0] is not None
    drill = _item("d1", "drilling machine", "INGCO 20V Cordless Drill / Driver")
    named = _read(status="named", brand="INGCO", model="CDLI200528", kind="cordless drill", read_from=["photo 0"])
    assert train.target(drill, named, {"identity_from_photos_alone": "named"})[0] is not None
    fridge = _item("r1", "refrigerator", "Thermofrost Refrigerator")
    assert train.target(fridge, _read(kind="single door refrigerator"))[0] is not None
    assert train.target(fridge, _read(kind="chest freezer"))[0] is None
    service = _item("s1", "refrigerator", "AC Fridge Repair, Installation Gas Refilling")
    assert train.target(service, _read(kind="air conditioner")) == (None, "the advert sells a service or wants to buy")


def test_a_vision_check_keeps_a_logo_name_and_a_code_needs_the_title_or_the_ocr(tmp_path: Path):
    photo = tmp_path / "00.jpg"
    Image.new("RGB", (32, 24), "blue").save(photo)
    sewing = _item("e1", "industrial sewing machine", "Emel Industrial Sewing Machine")
    named = _read(status="named", brand="EMEL", model="EM 8500", kind="industrial sewing machine", read_from=["photo 0"])
    rows = [{"id": "e1", "variant": "clean", "reading": named}]
    checked = {"e1": {"identity_from_photos_alone": "named"}}
    # The logo is no text the OCR can read, but the vision check saw it: the brand stays, the unconfirmed code goes.
    out, tally = train.build([(sewing, [photo])], rows, checked, tmp_path, ocr=lambda images: [])
    said = json.loads(out[0]["messages"][2]["content"])["identity"]
    assert said["brand"] == "EMEL" and "model" not in said and tally == {"kept: price at worst case, model code cut": 1}
    # A code on the sticker the OCR read is kept.
    out, _ = train.build([(sewing, [photo])], rows, checked, tmp_path, ocr=lambda images: ["EM8500"])
    assert json.loads(out[0]["messages"][2]["content"])["identity"]["model"] == "EM 8500"
    assert train.code_confirmed("PlayStation 4", "Uk Used Clean Ps4 Fat", None)


def test_a_cut_code_leaves_no_note_that_it_was_read():
    sewing = _item("e2", "industrial sewing machine", "Emel Industrial Sewing Machine")
    read = _read(status="named", brand="EMEL", model="EM 8500", kind="industrial sewing machine", read_from=["photo 1"])
    read["observations"] = ["a white industrial sewing machine on a table", "The model number 'EM 8500' is on a sticker."]
    read["claims"] = [{"claim": "EM 8500 model", "verdict": "supported", "evidence": "sticker reads EM 8500"}]
    answer, why = train.target(sewing, read, {"identity_from_photos_alone": "named"}, keep_code=False)
    assert why == "kept: price at worst case, model code cut"
    assert answer.observations == ["a white industrial sewing machine on a table"]
    assert answer.claims[0].verdict == "unverified" and "EM 8500" not in answer.model_dump_json().replace(answer.claims[0].claim, "")
    read["claims"] = [{"claim": "Model: EM 850", "verdict": "contradicted", "evidence": "the sticker says EM 8500"}]
    answer, _ = train.target(sewing, read, {"identity_from_photos_alone": "named"}, keep_code=False)
    assert answer.claims[0].verdict == "unverified" and answer.claims[0].evidence == train.UNREADABLE
    fan = _item("x3", "standing fan", "X3 Rechargeable Standing Fan")
    short = _read(status="named", brand="Ox", model="X3", read_from=["photo 0"])
    short["reason"] = "Clearly the X3 model."
    short["decision"] = "price"
    answer, _ = train.target(fan, short, {"identity_from_photos_alone": "named"}, keep_code=False)
    assert answer.reason == train.WORST_CASE_REASON
    only_the_code = dict(read, observations=["sticker reads EM 8500"])
    assert train.target(sewing, only_the_code, {"identity_from_photos_alone": "named"}, keep_code=False)[0] is None


def test_a_cut_code_that_was_the_whole_name_leaves_the_kind():
    fan = _item("c9", "standing fan", "Industrial Standing Fan")
    read = _read(status="named", model="SF-1650", kind="standing fan", read_from=["photo 0"])
    answer, why = train.target(fan, read, {"identity_from_photos_alone": "named"}, keep_code=False)
    assert why == "kept: price at worst case, name cut to the kind"
    assert answer.identity.status == "by_type" and answer.identity.kind == "standing fan"
