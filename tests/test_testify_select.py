"""What the teacher reads: no reposts or placeholder prices, every category and
price level in turn, and within each the adverts that teach most first."""

from pathlib import Path

from buyscape.testify import select
from buyscape.testify.schema import Answer, Item, Photos, PriceTruth


def _item(i, title, ngn=50000, kind=None, cache=None, tier="small_goods", photos=1, site=None):
    answer = Answer(title=title, kind=kind, price=PriceTruth(ngn=ngn, used=True, observed_on="2026-11-01"))
    if site:
        answer.identity.text = site
    return Item(id=i, source="jiji", url=f"https://jiji.ng/x/{i}.html", split="train", tier=tier,
                photos=Photos(count=photos, cache=cache or f"eval/raw/testify_crawl/media/{i}/"), answer=answer)


def test_reposts_placeholders_and_buyers_are_left_out():
    items = [_item("a", "HP EliteBook 840 G5"), _item("b", "HP EliteBook 840 G5 laptop"),
             _item("c", "HP EliteBook 840 G5"), _item("d", "Dell Latitude", ngn=1111111),
             _item("e", "We buy laptops", tier="not_for_sale"), _item("f", "Lenovo", photos=0),
             _item("g", "Lenovo ThinkPad T480", ngn=1)]
    kept, dropped = select.clean(items, {"a": ["ff00"], "b": ["ff00"], "c": ["0a0a"]})
    assert [i.id for i in kept] == ["a"]
    assert dropped == {"the same photos as another advert": 1, "the same title at the same price": 1,
                       "a placeholder price": 2, "a buyer's advert": 1, "no photo": 1}


def test_every_category_and_price_band_takes_its_turn_and_the_same_item_comes_first():
    laptops = [_item(f"l{n}", f"HP EliteBook 840 G{n % 3}", site="computers and laptops") for n in range(6)]
    laptops.append(_item("odd", "Strange gadget thing", site="computers and laptops"))
    fridges = [_item(f"f{n}", f"LG double door fridge {n}", ngn=300000, site="home appliances") for n in range(3)]
    cheap = [_item("k", "Binatone kettle", ngn=8000, site="home appliances")]
    chosen, why = select.choose(laptops + fridges + cheap, 3)
    assert {select.category(i) for i in chosen} == {"computers and laptops", "home appliances"}
    assert {select.band(i.answer.price.ngn) for i in chosen} == {0, 2, 3}
    assert "odd" not in {i.id for i in chosen} and why["l0"]["same item in the pool"] >= 2
    assert select.choose(laptops + fridges + cheap, 3)[0] == chosen


def test_a_code_on_a_photo_and_a_faulty_item_count_for_more(tmp_path):
    folder = tmp_path / "eval/raw/testify_crawl/media/p1"
    folder.mkdir(parents=True)
    (folder / "00.webp").write_bytes(b"x")

    class Cache:
        def lines(self, path):
            return ["MODEL NO: RT38K5032S8", "Samsung"] if path.name == "00.webp" else []

    lines = select.PhotoLines(tmp_path, Cache())
    plate = _item("p1", "Samsung fridge", site="home appliances")
    faulty = _item("p2", "Faulty Samsung fridge for parts", site="home appliances")
    plain = _item("p3", "Samsung fridge clean", site="home appliances")
    _, why = select.choose([plate, faulty, plain], 3, lines)
    assert why["p1"]["a code on a photo"] and not why["p3"]["a code on a photo"]
    assert why["p2"]["faulty or scrap"] and why["p1"]["score"] > why["p3"]["score"]
    assert not select.placeholder(85000) and select.placeholder(123456) and select.placeholder(999999)
