"""Items made unanswerable by construction: the photo or the text that names
the model is taken away, so the right answer is to ask for it, and photos that
cannot be priced come back as items to refuse."""

from pathlib import Path

from PIL import Image

from buyscape.testify import construct
from buyscape.testify.schema import Answer, Item, PriceTruth


def _item(title: str, tier="branded_electronics", exclude=None, item_id="c1") -> Item:
    return Item(
        id=item_id, source="jiji", url=f"https://jiji.ng/x/{item_id}.html", split="dev", tier=tier,
        seller_text="Nikon D3300, clean", exclude=exclude,
        answer=Answer(title=title, category="camera", price=PriceTruth(ngn=200000, observed_on="2026-10-17")),
    )


def _photos(tmp_path: Path, n: int) -> list[Path]:
    out = []
    for k in range(n):
        path = tmp_path / "media" / f"{k:02d}.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (200, 100), "white").save(path)
        out.append(path)
    return out


def _reader(text_on: dict[str, str]):
    """Fake OCR: the text each photo carries, in one box, until the box is painted dark."""
    def read(path: Path):
        text = text_on.get(path.name.split(".")[0].replace("photo_", "0"), "")
        if not text:
            return []
        with Image.open(path) as im:
            if im.getpixel((50, 50)) != (255, 255, 255):
                return []
        return [(text, [(40.0, 40.0), (160.0, 40.0), (160.0, 60.0), (40.0, 60.0)])]
    return read


def test_the_code_is_the_item_not_its_extras_or_a_year():
    assert construct.code_tokens("Nikon Camera D3300 + 18-55mm Lens") == {"d3300"}
    assert construct.code_tokens("Toyota Corolla 2008 Model") == set()
    assert construct.code_tokens("Xiaomi Redmi 9 with 2 cases") == {"redmi9"}
    assert construct.code_tokens("LG Washing Machine DirectDrive 7kg") == {"7kg"}


def test_a_short_code_must_be_a_whole_word():
    assert construct.carries("d90", "NIKON D90")
    assert not construct.carries("d90", "SERIAL D9012")
    assert construct.carries("d3300", "NikonD3300 kit")


def test_the_photo_with_the_code_is_dropped_when_another_photo_shows_the_item(tmp_path):
    photos = _photos(tmp_path, 3)
    record = construct.construct(
        _item("Nikon D3300 DSLR"), photos, _reader({"01": "D3300"}), tmp_path / "out", tmp_path)
    assert record["route"] == "drop" and record["removed"] == [1]
    assert record["photos"] == ["media/00.jpg", "media/02.jpg"]
    assert record["expected"] == "ask_for_proof" and record["checked"] is None


def test_the_code_is_painted_out_when_every_photo_carries_it(tmp_path):
    photos = _photos(tmp_path, 1)
    record = construct.construct(
        _item("Nikon D3300 DSLR"), photos, _reader({"00": "D3300"}), tmp_path / "out", tmp_path)
    assert record["route"] == "blank" and record["photos"] == ["out/c1/photo_0.jpg"]
    with Image.open(tmp_path / record["photos"][0]) as im:
        assert im.getpixel((100, 50)) == (40, 40, 40)


def test_items_named_by_type_and_items_with_no_code_on_a_photo_do_not_qualify(tmp_path):
    photos = _photos(tmp_path, 2)
    reader = _reader({"00": "D3300"})
    assert construct.construct(_item("Nikon D3300", tier="small_goods"), photos, reader, tmp_path, tmp_path) is None
    assert construct.construct(_item("Nikon D3300"), photos, _reader({}), tmp_path, tmp_path) is None


def test_a_code_past_the_photos_shown_was_never_evidence(tmp_path):
    photos = _photos(tmp_path, 5)
    assert construct.construct(_item("Nikon D3300"), photos, _reader({"04": "D3300"}), tmp_path, tmp_path) is None


def test_an_advert_whose_photo_is_not_the_item_comes_back_to_be_refused():
    record = construct.bad_photo(_item("Xbox One", exclude="the photo is not the seller's item"))
    assert record["route"] == "bad_photo" and record["expected"] == "refuse"
    assert construct.bad_photo(_item("Fan", exclude="new stock, not second-hand")) is None


def test_a_request_for_the_plate_counts_and_a_word_inside_another_does_not():
    assert construct.asks_for_identity(["Close-up of the rating plate", "clip of it running"]) == (True, True)
    assert construct.asks_for_identity(["clip of it running", "photo of the model number"]) == (False, True)
    assert construct.asks_for_identity(["the seller moving it"]) == (False, False)


def _row(decision, variant="noproof", model=None, requests=()):
    identity = {"status": "named", "brand": "Nikon", "model": model, "read_from": ["photo 0"]} if model else \
        {"status": "by_type", "kind": "camera"}
    return {"id": "c1", "variant": variant, "decision": decision,
            "reading": {"decision": decision, "identity": identity, "proof_requests": list(requests)}}


def test_scoring_counts_abstention_the_hidden_code_and_the_pairs():
    item = _item("Nikon D3300 DSLR")
    records = [{"id": "c1", "route": "drop", "found": ["d3300"]}]
    rows = [_row("price", model="D3300")]
    clean = [{**_row("price", variant="clean", model="D3300"), "variant": "clean"}]
    result = construct.score(rows, records, {"c1": item}, clean)
    assert result["noproof_named_the_hidden_code"] == 1.0 and result["noproof_abstained"] == 0.0
    assert result["pairs_named_while_shown"] == 1.0 and result["pecs_style"] == 0.5

    held = construct.score([_row("ask_for_proof", requests=["photo of the bottom sticker"])], records, {"c1": item}, clean)
    assert held["noproof_abstained"] == 1.0 and held["proof_asked_first"] == 1.0 and held["pairs_both"] == 1.0


def test_a_bad_photo_is_refused_or_not():
    rows = [_row("cannot_identify", variant="bad_photo"), {**_row("price", variant="bad_photo"), "id": "c2"}]
    assert construct.score(rows, [], {})["bad_photo_refused"] == 0.5
