"""The data pack puts every cache together, one row per advert, keeps the
benchmark's test answers out of the public version, and never lets a phone
number, a photo or a seller's words into it."""

import json

import pytest

from buyscape.testify import pack


def _advert(i, **extra):
    row = {"id": i, "title": f"Samsung 43 inch smart TV number {i} in very good condition", "price_ngn": 120000,
           "description": "Clean TV, works well, no fault at all. Call 0803 123 4567 to see it today",
           "condition": "Used", "is_used": True, "attrs": {}, "url": f"/lagos/tv/{i}.html",
           "fetched_at": "2026-11-01T10:00:00Z", "media": [f"{i}/00.jpg"], "category": "tv", "kind": "tv"}
    row.update(extra)
    return row


def _cache(root, name, rows):
    folder = root / "eval" / "raw" / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "rows.json").write_text(json.dumps(rows))
    for row in rows:
        for media in row["media"]:
            (folder / "media" / media).parent.mkdir(parents=True, exist_ok=True)
            (folder / "media" / media).write_bytes(b"jpeg")


def _bench(root, items):
    path = root / "eval" / "testify" / "items.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(i) + "\n" for i in items))


def test_every_cache_in_one_row_per_advert_with_its_photos_and_no_phone(tmp_path):
    _cache(tmp_path, "testify", [_advert("a"), _advert("b")])
    _cache(tmp_path, "testify_train", [_advert("b", region="lagos"), _advert("c", region="abuja")])
    _bench(tmp_path, [{"id": "1-tv", "split": "test", "url": "x", "photos": {"cache": "eval/raw/testify/media/a/"}}])
    counts = pack.build(tmp_path, tmp_path / "pack")
    rows = {r["id"]: r for r in map(json.loads, (tmp_path / "pack" / "adverts.jsonl").read_text().splitlines())}
    assert set(rows) == {"a", "b", "c"} and counts["adverts"] == 3
    assert rows["a"]["role"] == "benchmark" and rows["a"]["split"] == "test" and rows["a"]["benchmark_id"] == "1-tv"
    assert rows["b"]["role"] == "held back" and rows["b"]["also_in"] == ["testify_train"]
    assert rows["c"]["role"] == "training" and rows["c"]["city"] == "abuja" and rows["c"]["split"] == "train"
    assert rows["a"]["url"] == "https://jiji.ng/lagos/tv/a.html" and rows["a"]["area"] == "lagos"
    assert rows["c"]["photos"] == ["photos/c/00.jpg"] and (tmp_path / "pack" / "photos" / "c" / "00.jpg").exists()
    assert "0803" not in (tmp_path / "pack" / "adverts.jsonl").read_text()
    assert "Buyscape market data" in (tmp_path / "pack" / "README.md").read_text()


def test_the_public_version_has_links_and_labels_and_no_test_answer(tmp_path):
    _cache(tmp_path, "testify", [_advert("a"), _advert("d")])
    _bench(tmp_path, [{"id": "1-tv", "split": "test", "url": "x", "photos": {"cache": "eval/raw/testify/media/a/"}},
                      {"id": "2-tv", "split": "dev", "url": "y", "photos": {"cache": "eval/raw/testify/media/d/"}}])
    pack.build(tmp_path, tmp_path / "pack")
    public = {r["id"]: r for r in map(json.loads, (tmp_path / "pack" / "public" / "adverts.jsonl").read_text().splitlines())}
    text = (tmp_path / "pack" / "public" / "adverts.jsonl").read_text()
    assert "Samsung 43 inch" not in text and "Clean TV" not in text and "photos/" not in text
    assert "price_ngn" not in public["a"] and "kind" not in public["a"] and public["a"]["url"].endswith("/a.html")
    assert public["d"]["price_ngn"] == 120000 and public["d"]["photo_count"] == 1


def test_a_public_row_with_a_phone_number_or_seller_words_is_refused():
    private = [_advert("a", split="dev")]
    assert pack.check_public([{"id": "a", "note": "call 0803 123 4567"}], private)
    words = "Samsung 43 inch smart TV number a in very good condition"
    assert pack.check_public([{"id": "a", "note": words}], private)
    assert not pack.check_public([{"id": "a", "url": "https://jiji.ng/lagos/tv/a.html"}], private)


def test_an_unreadable_cache_file_is_passed_over(tmp_path):
    folder = tmp_path / "eval" / "raw" / "testify_crawl"
    folder.mkdir(parents=True)
    (folder / "broken.json").write_text("{not json")
    _cache(tmp_path, "testify_crawl", [_advert("e", region="kano")])
    assert pack.build(tmp_path, tmp_path / "pack")["adverts"] == 1


def test_an_advert_the_photo_check_left_out_is_held_back_and_keeps_its_split(tmp_path):
    _cache(tmp_path, "testify", [_advert("f")])
    _bench(tmp_path, [{"id": "3-tv", "split": "test", "url": "z", "market": "abuja", "exclude": "no photo of the item",
                       "photos": {"cache": "eval/raw/testify/media/f/"}}])
    pack.build(tmp_path, tmp_path / "pack")
    [row] = map(json.loads, (tmp_path / "pack" / "adverts.jsonl").read_text().splitlines())
    assert row["role"] == "held back" and row["split"] == "test" and row["city"] == "abuja"
    assert row["left_out"] == "no photo of the item"


@pytest.mark.parametrize("row,expected", [
    ({"role": "training", "condition": "", "is_used": False}, "used, by the seller's words"),
    ({"role": "training", "condition": "Used", "is_used": True}, "used, by the site's field"),
    ({"role": "new stock", "condition": "Brand New", "is_used": False}, "new"),
])
def test_condition_is_told_apart(row, expected):
    assert pack.condition_of(row) == expected
