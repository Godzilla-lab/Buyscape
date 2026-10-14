"""Testify items: stable splits, honest baselines, nothing private released."""

from pathlib import Path

import yaml

from buyscape.testify.convert import baseline_from_report, redact, risk_seeds
from buyscape.testify.schema import Item, split_for
from buyscape.protocols.schema import load_protocols

ROOT = Path(__file__).resolve().parents[1]

ABSTAINED = """## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** nothing legible

## Price
**5,000 to 5,000 NGN** (priced as material, width 0.0, method material_floor, 0 comparable prices)
"""

ANSWERED = """## Identification
**Answer: Samsung Galaxy S22** (margin 0.6)

## Price
**180,000 to 240,000 NGN** (priced as a working item, width 0.3, method comps, 9 comparable prices)
"""

NO_DATA = """**Answer: Nexus 7kg** (margin 0.5)

## Price
**NO_PRICE_DATA.** nothing dated
"""


def test_split_is_stable_and_roughly_a_quarter_dev():
    assert split_for("abc") == split_for("abc")
    ids = [f"item-{n}" for n in range(2000)]
    dev = sum(split_for(i) == "dev" for i in ids)
    assert 400 < dev < 600


def test_baseline_reads_abstention_answer_and_missing_price():
    abstained = baseline_from_report(ABSTAINED, "a.md")
    assert abstained.decision == "cannot_identify"
    assert abstained.answer is None
    assert (abstained.price_low, abstained.basis) == (5000, "priced as material")

    answered = baseline_from_report(ANSWERED, "b.md")
    assert answered.decision == "price"
    assert answered.answer == "Samsung Galaxy S22"
    assert (answered.price_low, answered.price_high) == (180000, 240000)

    assert baseline_from_report(NO_DATA, "c.md").decision == "no_price_data"


def test_contact_details_never_survive():
    text = "Call 08012345678 or +234 801 234 5678, mail seller@example.com"
    clean = redact(text)
    assert "0801" not in clean and "example.com" not in clean
    assert clean.count("[phone]") == 2 and "[email]" in clean


def test_every_protocol_claim_becomes_a_risk_with_its_proof():
    laptop = load_protocols(ROOT / "protocols")["laptop"]
    seeds = risk_seeds(laptop)
    assert [s.risk for s in seeds] == [c.id for c in laptop.claims]
    assert all(s.proof for s in seeds if s.risk == "ram_gb")
    assert all(not s.reviewed for s in seeds)


def test_hand_labels_name_real_tiers_and_protocols():
    labels = yaml.safe_load((ROOT / "eval" / "testify" / "labels.yaml").read_text())
    protocols = load_protocols(ROOT / "protocols")
    tiers = set(Item.model_fields["tier"].annotation.__args__)
    for item_id, label in labels.items():
        assert label["tier"] in tiers, item_id
        assert label["protocol"] in protocols, item_id


def test_released_items_hold_links_not_photos():
    path = ROOT / "eval" / "testify" / "items.jsonl"
    for line in path.read_text().splitlines():
        item = Item.model_validate_json(line)
        assert item.photos.public is False
        assert item.url.startswith("https://")
        assert redact(item.seller_text) == item.seller_text


def test_a_source_missing_here_keeps_its_previous_items(tmp_path):
    from buyscape.testify.convert import all_items, write

    root = tmp_path / "repo"
    (root / "eval").mkdir(parents=True)
    for name in ("protocols", "docs", "tenants"):
        (root / name).symlink_to(ROOT / name)
    (root / "eval" / "adjudications.yaml").symlink_to(ROOT / "eval" / "adjudications.yaml")
    previous = tmp_path / "items.jsonl"
    old = Item.model_validate_json((ROOT / "eval" / "testify" / "items.jsonl").read_text().splitlines()[0])
    kept = old.model_copy(update={"id": "only-on-another-machine", "source": "buyscrap"})
    write([kept], previous)

    items = all_items(root, previous=previous)
    ids = {i.id for i in items}
    assert "only-on-another-machine" in ids
    assert sum(i.source == "jiji" for i in items) == 178


def test_fetch_asks_in_nigerian_second_hand_words_and_skips_new_and_buyers():
    from buyscape.testify.fetch import keep, phrasings

    assert phrasings(("used freezer",)) == [
        "used freezer", "tokunbo freezer", "fairly used freezer", "uk used freezer",
    ]
    assert keep({"condition": "Brand New", "title": "Standing fan"}) == "brand new"
    assert keep({"condition": "Used", "title": "We Buy Scrap Batteries"}) == "buyer, not seller"
    assert keep({"condition": "Used", "title": "Scrap Buyer, Convert Your Scrap To Cash"}) == "buyer, not seller"
    assert keep({"condition": "Used", "title": "Tokunbo standing fan"}) is None


def test_a_kaggle_metadata_file_beside_the_adverts_is_not_an_advert(tmp_path):
    import json

    from buyscape.testify.fetch import load

    (tmp_path / "dataset-metadata.json").write_text(json.dumps({"title": "x", "id": "u/x"}))
    (tmp_path / "fan.json").write_text(json.dumps([{"id": "a", "tier": "small_goods", "kind": "fan", "title": "Fan"}]))
    (tmp_path / "broken.json").write_text("{not json")
    assert [r["id"] for r in load(tmp_path)] == ["a"]


def test_a_slow_jiji_is_retried_and_then_skipped_not_fatal():
    import httpx

    from buyscape.testify.fetch import _patiently

    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise httpx.ReadTimeout("slow")
        return ["ok"]

    assert _patiently(flaky, waits=(0, 0)) == ["ok"]

    def dead():
        raise httpx.ReadTimeout("slow")

    assert _patiently(dead, waits=(0, 0)) is None


def test_skip_done_fetches_only_kinds_never_fetched(tmp_path, monkeypatch):
    from buyscape.testify import fetch

    asked = []
    monkeypatch.setattr(fetch, "fetch_category", lambda q, *a, **k: asked.append(q.category) or [])
    (tmp_path / "rechargeable_torchlight.json").write_text("[]")
    fetch.build(tmp_path, only=("rechargeable torchlight", "tyres"), skip_done=True)
    assert set(asked) == {"tyres"}


def test_new_stock_pool_and_benchmark_never_share_an_advert():
    from buyscape.testify.fetch import keep, phrasings

    new = {"condition": "Brand New", "title": "Standing fan"}
    used = {"condition": "Used", "title": "Tokunbo standing fan"}
    assert keep(new, "new") is None and keep(new, "used") == "brand new"
    assert keep(used, "used") is None and keep(used, "new") == "second-hand"
    assert keep({"condition": "Brand New", "title": "We buy fans"}, "new") == "buyer, not seller"
    assert phrasings(("standing fan",), "new") == ["standing fan", "brand new standing fan"]


def test_training_items_are_split_train(tmp_path):
    import json

    from buyscape.testify.convert import wider_items

    raw = tmp_path / "eval" / "raw" / "testify_new"
    raw.mkdir(parents=True)
    (tmp_path / "protocols").symlink_to(ROOT / "protocols")
    row = {"id": "n1", "tier": "small_goods", "kind": "standing fan", "title": "Ox fan",
           "url": "/lagos/fan-n1.html", "media": ["n1/00.jpg"], "price_ngn": 30000,
           "is_used": False, "condition": "Brand New", "description": "New"}
    (raw / "standing_fan.json").write_text(json.dumps([row]))
    [item] = wider_items(tmp_path, "testify_new")
    assert item.split == "train"
    assert item.photos.cache == "eval/raw/testify_new/media/n1/"


def test_each_city_is_fetched_once_and_lagos_history_counts(tmp_path, monkeypatch):
    from buyscape.testify import fetch

    asked = []
    monkeypatch.setattr(fetch, "fetch_category", lambda q, *a, region="lagos", **k: asked.append(region) or [])
    (tmp_path / "tyres.json").write_text("[]")
    fetch.build(tmp_path, only=("tyres",), skip_done=True, region="lagos")
    assert asked == []
    fetch.build(tmp_path, only=("tyres",), skip_done=True, region="abuja")
    assert set(asked) == {"abuja"}
    asked.clear()
    fetch.build(tmp_path, only=("tyres",), skip_done=True, region="abuja")
    assert asked == []


def test_a_search_word_that_keeps_finding_nothing_is_dropped(tmp_path, monkeypatch):
    from buyscape.evalset.jiji import Listing
    from buyscape.testify import fetch

    asked = []

    def fake(q, *a, **k):
        asked.append(q.query)
        if " " in q.query and q.query.split()[0] in ("used", "tokunbo", "fairly", "uk"):
            return []
        n = len(asked)
        return [Listing(id=f"a{n}", category=q.category, title=q.query, price_ngn=1, description="",
                        condition="Used", is_used=True, attrs={}, image_urls=[], url="", fetched_at="")]

    monkeypatch.setattr(fetch, "fetch_category", fake)
    monkeypatch.setattr(fetch, "download_media", lambda listings, *a, **k: [setattr(l, "media", ["x.jpg"]) for l in listings])
    kinds = tuple(k[1] for k in fetch.KINDS[:6])
    fetch.build(tmp_path, only=kinds)
    tokunbo = [q for q in asked if q.startswith("tokunbo ")]
    plain = [q for q in asked if not q.split()[0] in ("used", "tokunbo", "fairly", "uk")]
    assert len(tokunbo) == fetch.DRY_LIMIT
    assert len(plain) >= 6


def test_jiji_photos_take_the_largest_size_an_advert_lists():
    import base64

    from buyscape.evalset.jiji import _image_urls, _url_width

    def pic(w, h):
        token = base64.urlsafe_b64encode(f"{w}-{h}-abc123-2".encode()).decode().rstrip("=")
        return f"https://pictures-nigeria.jijistatic.net/1_{token}.jpg"

    assert _url_width(pic(300, 225)) == 300
    assert _url_width("https://example.com/plain.jpg") == 0
    advert = {
        "images": [{"url": pic(300, 225), "full": pic(1080, 810), "small": pic(150, 110)}, pic(640, 480)],
        "image_obj": {"url": pic(300, 225)},
    }
    assert _image_urls(advert) == [pic(1080, 810), pic(640, 480)]
    assert _image_urls({"image_obj": {"url": pic(300, 225)}}) == [pic(300, 225)]


def test_a_cached_thumbnail_advert_gets_its_bigger_photos(tmp_path, monkeypatch):
    import base64
    import json

    from buyscape.evalset.jiji import Listing
    from buyscape.testify import fetch

    def pic(w):
        token = base64.urlsafe_b64encode(f"{w}-{w}-abc-2".encode()).decode().rstrip("=")
        return f"https://pictures-nigeria.jijistatic.net/9_{token}.jpg"

    (tmp_path / "media" / "a1").mkdir(parents=True)
    (tmp_path / "media" / "a1" / "00.jpg").write_bytes(b"thumb")
    row = {"id": "a1", "tier": "small_goods", "kind": "tyres", "title": "Tyre", "condition": "Used",
           "image_urls": [pic(300)], "media": ["a1/00.jpg"]}
    (tmp_path / "tyres.json").write_text(json.dumps([row]))
    big = Listing(id="a1", category="tyres", title="Tyre", price_ngn=1, description="", condition="Used",
                  is_used=True, attrs={}, image_urls=[pic(1080)], url="", fetched_at="")
    monkeypatch.setattr(fetch, "fetch_category", lambda *a, **k: [big])

    def save(listings, root, client=None):
        for l in listings:
            (root / l.id / "00.jpg").write_bytes(b"full")
            l.media = [f"{l.id}/00.jpg"]

    monkeypatch.setattr(fetch, "download_media", save)
    counts = fetch.build(tmp_path, only=("tyres",))
    assert counts["tyres"]["sharper photos"] == 1
    assert (tmp_path / "media" / "a1" / "00.jpg").read_bytes() == b"full"
    assert json.loads((tmp_path / "tyres.json").read_text())[0]["image_urls"] == [pic(1080)]


def test_photo_review_drops_items_from_scoring_and_fixes_used():
    from buyscape.testify.convert import load_items

    items = {i.id: i for i in load_items(ROOT / "eval" / "testify" / "items.jsonl")}
    reviews = yaml.safe_load((ROOT / "eval" / "testify" / "review_dev.yaml").read_text())
    assert len(reviews) == 100 and all(items[r["id"]].split == "dev" for r in reviews)
    for r in reviews:
        item = items[r["id"]]
        assert (item.exclude is not None) == (r["keep_in_benchmark"] == "drop")
        if r["looks_actually_used"] == "no":
            assert item.answer.price.used is False


def test_advert_page_gives_every_photo_at_its_biggest_size():
    import base64

    from buyscape.evalset.jiji import page_photos

    def pic(n, w, h, ext="jpg"):
        token = base64.urlsafe_b64encode(f"{w}-{h}-6ed0811e07".encode()).decode().rstrip("=")
        return f"https://pictures-nigeria.jijistatic.net/{n}_{token}.{ext}"

    html = " ".join([
        pic(136029311, 96, 96),            # seller avatar
        pic(200646914, 111, 197, "webp"),
        pic(200646914, 300, 533),
        pic(200646914, 620, 1102, "webp"),
        pic(200646915, 111, 197, "webp"),
        pic(200646917, 111, 197, "webp"),
        pic(199000001, 300, 300),          # another advert on the page
    ])
    assert page_photos(html, "200646914") == [
        pic(200646914, 620, 1102, "webp"), pic(200646915, 111, 197, "webp"), pic(200646917, 111, 197, "webp"),
    ]
