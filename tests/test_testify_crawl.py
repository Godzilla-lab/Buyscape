"""A category crawl keeps second-hand sellers only, passes over the benchmark,
names each advert by the site's own category, and resumes where it stopped."""

import json

import httpx

from buyscape.testify import crawl


def _advert(i, condition="Used", title=None, category="Refrigerators"):
    return {"guid": i, "title": title or f"LG fridge {i}", "price_obj": {"value": 90000},
            "images": [{"url": f"https://pictures-nigeria.jijistatic.net/{i}_x.jpg"}],
            "attrs": [{"name": "Condition", "value": condition}], "url": f"/lagos/fridges/{i}.html",
            "category_name": category}


def _jiji(pages, asked=None):
    def handler(request):
        number = int(request.url.params["page"])
        if asked is not None:
            asked.append(number)
        adverts = pages[number - 1] if number <= len(pages) else []
        return httpx.Response(200, json={"adverts_list": {"adverts": adverts, "total_pages": len(pages)}})
    return httpx.Client(transport=httpx.MockTransport(handler))


def _no_downloads(monkeypatch):
    monkeypatch.setattr(crawl, "_from_page", lambda listing, client: [])
    monkeypatch.setattr(crawl, "download_media",
                        lambda listings, *a, **k: [setattr(x, "media", [f"{x.id}/00.jpg"]) for x in listings])
    monkeypatch.setattr(crawl.time, "sleep", lambda s: None)


def test_second_hand_sellers_only_and_the_benchmark_passed_over(tmp_path, monkeypatch):
    _no_downloads(monkeypatch)
    pages = [[_advert("a"), _advert("b", "Brand New"), _advert("c", title="We buy used fridges"), _advert("bench")]]
    tally = crawl.crawl(tmp_path, "lagos", "home-appliances", pages=3, avoid=frozenset({"bench"}),
                        client=_jiji(pages))
    rows = json.loads((tmp_path / "home-appliances.json").read_text())
    assert [r["id"] for r in rows] == ["a"]
    assert rows[0]["kind"] == "refrigerators" and rows[0]["region"] == "lagos" and rows[0]["tier"] == "small_goods"
    assert tally["in the benchmark"] == 1 and tally["buyer, not seller"] == 1


def test_pages_are_visited_at_random_across_the_listing_and_a_crawl_resumes(tmp_path, monkeypatch):
    _no_downloads(monkeypatch)
    pages = [[_advert(f"p{n}")] for n in range(40)]
    asked = []
    crawl.crawl(tmp_path, "lagos", "home-appliances", pages=5, client=_jiji(pages, asked))
    visited = json.loads((tmp_path / ".progress" / "lagos" / "home-appliances.json").read_text())
    assert len(visited) == 5 and visited != [1, 2, 3, 4, 5] and max(visited) > 5
    assert [n for n in asked[1:]] == [n for n in crawl.order(40, "lagos", "home-appliances") if n != 1][:5] \
        or 1 in crawl.order(40, "lagos", "home-appliances")[:5]
    tally = crawl.crawl(tmp_path, "lagos", "home-appliances", pages=8, held=frozenset(), client=_jiji(pages))
    assert tally["pages"] == 3 and len(json.loads((tmp_path / "home-appliances.json").read_text())) == 8
    assert crawl.order(40, "lagos", "furniture") != crawl.order(40, "lagos", "home-appliances")


def test_a_crawl_stops_once_pages_bring_nothing_new(tmp_path, monkeypatch):
    _no_downloads(monkeypatch)
    pages = [[_advert("a")]] * 21
    tally = crawl.crawl(tmp_path, "lagos", "home-appliances", pages=50, client=_jiji(pages))
    assert tally["kept"] == 1 and tally["pages"] == 1 + crawl.STALE_PAGES


def test_a_phone_is_filed_under_its_protocol_and_a_slug_is_checked():
    assert crawl.CATEGORIES["mobile-phones"] == ("branded_electronics", "phone")
    assert crawl.kind_of({"category": {"name": "Mobile Phones"}}, "mobile-phones") == "mobile phones"
    assert crawl.kind_of({}, "tv-dvd-equipment") == "tv dvd equipment"
    assert crawl.valid_slug("home-appliances") and not crawl.valid_slug("../etc")


def test_a_crawl_keeps_at_most_its_share_and_a_dealers_page_is_still_new(tmp_path, monkeypatch):
    _no_downloads(monkeypatch)
    dealers = [[_advert(f"n{p}{i}", "Brand New") for i in range(3)] for p in range(8)]
    used = [[_advert(f"u{i}")] for i in range(4)]
    tally = crawl.crawl(tmp_path, "lagos", "home-appliances", pages=20, keep=2, client=_jiji(dealers + used))
    assert tally["kept"] == 2 and tally["pages"] >= 2


def test_a_crawled_advert_has_no_kind_label_so_its_title_finds_comparables(tmp_path):
    import json as j

    from buyscape.testify.convert import wider_items

    raw = tmp_path / "eval" / "raw" / "testify_crawl"
    raw.mkdir(parents=True)
    (tmp_path / "protocols").symlink_to(__import__("pathlib").Path(__file__).resolve().parents[1] / "protocols")
    row = {"id": "x1", "title": "LG double door fridge", "price_ngn": 250000, "condition": "Used", "is_used": True,
           "media": ["x1/00.jpg"], "url": "/lagos/home-appliances/x1.html", "fetched_at": "2026-11-01T10:00:00Z",
           "tier": "small_goods", "kind": "home appliances", "region": "lagos", "protocol": None}
    (raw / "home-appliances.json").write_text(j.dumps([row]))
    [item] = wider_items(tmp_path, "testify_crawl")
    assert item.answer.kind is None and item.answer.identity.text == "home appliances" and item.split == "train"


def test_the_advert_page_is_opened_only_when_the_listing_photos_are_small():
    import base64

    def url(width):
        code = base64.b64encode(f"{width}-{width}-abc".encode()).decode().rstrip("=")
        return f"https://pictures-nigeria.jijistatic.net/1_{code}.webp"

    assert crawl.sharp_enough([url(800), url(1000), url(720)], 3)
    assert not crawl.sharp_enough([url(300), url(1000)], 3)
    assert not crawl.sharp_enough([url(1000)], 3)
