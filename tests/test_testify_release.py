"""The public release carries links and labels, never photos, sellers' words or test answers."""

import json

from buyscape.testify import release
from buyscape.testify.schema import Answer, Item, PriceTruth

SELLER = "Neat used office chair, adjustable, comes from abroad, call me on 08031234567 for more details today"


def _item(item_id: str, split: str, **kw) -> Item:
    return Item(
        id=item_id, source="jiji", url=f"https://jiji.ng/x/{item_id}.html", split=split, tier="small_goods",
        seller_text=SELLER, photos={"count": 2, "cache": f"eval/raw/testify/media/{item_id}/"},
        answer=Answer(title="Office Chair", kind="office chair",
                      price=PriceTruth(ngn=25000, used=True, observed_on="2026-10-14")),
        ai_label={"identity_from_photos_alone": "by_type", "looks_actually_used": "yes"}, **kw,
    )


def test_dev_carries_its_answer_and_test_carries_none():
    dev = release.public_item(_item("d", "dev"), {"d": ["abc"]})
    test = release.public_item(_item("t", "test"), {})
    assert dev["answer"]["asking_price"] == 25000 and dev["photo_hashes"] == ["abc"] and dev["planted_lie"]
    assert set(test) == {"id", "url", "source", "market", "currency", "split", "photo_count", "photo_hashes"}
    text = json.dumps([dev, test])
    assert "eval/raw" not in text and SELLER[:40] not in text and "08031234567" not in text


def test_the_check_refuses_anything_private():
    items = [_item("d", "dev"), _item("t", "test")]
    assert release.check([release.public_item(i, {}) for i in items], items) == []
    leaky = [{"id": "d", "note": SELLER}]
    found = release.check(leaky, items)
    assert any("phone" in f for f in found) and any("seller's own words" in f for f in found)
    assert release.check([{"id": "t", "answer": {"title": "x"}}], items) == ["an answer for test item t"]
    assert release.check([{"id": "d", "photo": "eval/raw/testify/media/d/00.jpg"}], items)


def test_a_title_the_seller_repeated_is_not_their_words():
    item = _item("d", "dev")
    item.seller_text = "Office Chair\n" + SELLER
    rows = [release.public_item(item, {})]
    assert release.check(rows, [item]) == []
    assert release.check(rows + [{"id": "x", "note": SELLER}], [item])
