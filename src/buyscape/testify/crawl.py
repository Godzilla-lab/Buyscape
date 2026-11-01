"""Jiji categories paged through, for training data far past what search gives.

Search gives about twenty adverts a phrasing whatever the page number. A
category's own listing pages go on: on 1 Nov page 20 of home appliances,
furniture and mobile phones in Lagos each still gave about two dozen new
adverts. A crawl takes every second-hand advert in a category, of every kind
in it, which is what a model must see to name whatever a seller sends, not
only the benchmark's kinds. Training data only: the benchmark's adverts are
passed over before any photo is fetched, and every row is split `train`.

Each advert keeps the site's own category as its kind ("Refrigerators"), so
comparables group the way the market groups them. Run from an ordinary
connection, like testify-fetch: Jiji answers datacenter addresses with a bot
check.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import httpx

from ..evalset.jiji import BASE, UA, Listing, _attrs, _image_urls, _is_used, _url_width, download_media
from .convert import redact
from .fetch import _from_page, _patiently
from .schema import WANTED

# Category slug: (tier, protocol). The protocol names the evidence a seller is
# asked for; None is the generic one. Slugs as Jiji's own web addresses write them.
# In crawl order: e-waste and electronics first, BuyScrap's biggest trade, then
# parts, machines, tools and the rest. Slugs checked from a home connection on
# 1 Nov or read off the web addresses of adverts already cached. Scrap and
# material lots have no category of their own on Jiji, so testify-fetch's
# searches stay their source.
CATEGORIES: dict[str, tuple[str, str | None]] = {
    "computers-and-laptops": ("branded_electronics", "laptop"),
    "mobile-phones": ("branded_electronics", "phone"),
    "tv-dvd-equipment": ("branded_electronics", None),
    "home-appliances": ("small_goods", None),
    "kitchen-appliances": ("small_goods", None),
    "computer-hardware": ("branded_electronics", None),
    "audio-and-music-equipment": ("small_goods", None),
    "video-games-and-consoles": ("branded_electronics", None),
    "printers-and-scanners": ("branded_electronics", None),
    "cameras-video-cameras-and-accessories": ("branded_electronics", None),
    "car-parts-and-accessories": ("small_goods", None),
    "power-equipments": ("small_goods", None),
    "manufacturing-equipments": ("small_goods", None),
    "power-tools": ("small_goods", None),
    "hand-and-power-tools": ("small_goods", None),
    "furniture": ("small_goods", "furniture"),
    "motorcycles-and-scooters": ("small_goods", None),
    "personal-mobility": ("small_goods", None),
    "sports-bicycles-and-fitness": ("small_goods", None),
    "musical-instruments": ("small_goods", None),
    "salon-equipment": ("small_goods", None),
    "restaurant-and-catering-equipment": ("small_goods", None),
    "store-equipments": ("small_goods", None),
    "plumbing-and-water-supply": ("small_goods", None),
    "manufacturing-materials-and-tools": ("small_goods", None),
    "medical-equipment": ("small_goods", None),
    "lighting": ("small_goods", None),
}

# Photos this wide or wider read a rating plate; a listing offering them
# saves opening the advert's own page, the slow part on a home connection.
SHARP = 700

# A run of pages showing no advert not seen before means the listing has
# wrapped or ended. A page of dealers' new stock is still a new page.
STALE_PAGES = 5


def site_category(advert: dict) -> str | None:
    """The category the site files the advert under, in its own words."""
    for key in ("category_name", "category_title", "category"):
        value = advert.get(key)
        if isinstance(value, dict):
            value = value.get("name") or value.get("title")
        if isinstance(value, str) and value.strip() and not value.strip().isdigit():
            return value.strip()
    return None


def kind_of(advert: dict, slug: str) -> str:
    """The advert's kind: the site's category in lower case, else the crawl's own."""
    named = site_category(advert)
    return (named or slug.replace("-", " ")).lower()


def page(slug: str, number: int, region: str, client: httpx.Client) -> tuple[list[tuple[Listing, dict]], int] | None:
    """One listing page as (listing, raw advert) pairs and the listing's page count, or None when it fails."""
    r = client.get(BASE, params={"region_slug": region, "slug": slug, "page": str(number)})
    if r.status_code != 200:
        return None
    listing_info = r.json().get("adverts_list") or {}
    adverts = listing_info.get("adverts") or []
    total = int(listing_info.get("total_pages") or 0)
    out = []
    for advert in adverts:
        price = (advert.get("price_obj") or {}).get("value")
        images = _image_urls(advert)
        if not images or not isinstance(price, (int, float)) or price <= 0:
            continue
        attrs = _attrs(advert)
        listing = Listing(
            id=str(advert.get("guid") or advert.get("id")),
            category=slug,
            title=str(advert.get("title") or ""),
            price_ngn=int(price),
            description=str(advert.get("details") or advert.get("short_description") or ""),
            condition=attrs.get("Condition", ""),
            is_used=_is_used(attrs),
            attrs=attrs,
            image_urls=images[:8],
            url=str(advert.get("url") or ""),
            fetched_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        out.append((listing, advert))
    return out, total


def sharp_enough(urls: list[str], max_photos: int) -> bool:
    """Whether the listing already offers enough photos wide enough to read a plate."""
    wanted = urls[:max_photos]
    return len(wanted) >= min(max_photos, 2) and min(_url_width(u) for u in wanted) >= SHARP


def why_not(listing: Listing) -> str | None:
    """Why an advert is left out of the crawl, or None to keep it: second-hand sellers only."""
    if WANTED.search(listing.title):
        return "buyer, not seller"
    if (listing.condition or "").strip().lower() == "brand new" or not listing.is_used:
        return "brand new or condition not stated"
    return None


def _progress(out_dir: Path, region: str, slug: str) -> Path:
    return out_dir / ".progress" / region / f"{slug}.json"


def order(total: int, region: str, slug: str) -> list[int]:
    """Every page of the listing in a fixed random order for this city and category.

    The first pages are paid promotions and the newest posts, mostly dealers; a
    sample across the whole listing sees every kind and price the market has.
    The same order every run, so a stopped crawl resumes where it was."""
    import random

    pages = list(range(1, total + 1))
    random.Random(f"{region}/{slug}").shuffle(pages)
    return pages


def crawl(
    out_dir: Path,
    region: str,
    slug: str,
    pages: int = 100,
    keep: int = 400,
    max_photos: int = 3,
    avoid: frozenset[str] = frozenset(),
    held: frozenset[str] = frozenset(),
    progress=None,
    client: httpx.Client | None = None,
) -> dict[str, int]:
    """Visit `pages` pages of one category in one city, picked at random across
    its whole listing, keeping new second-hand adverts.

    Resumes with the pages not yet visited, and saves after every page, so a
    stopped run loses one page at most. `avoid` is the benchmark's adverts and
    `held` the training adverts already cached elsewhere. At most `keep` new
    adverts a run, so one huge category never crowds out the rest."""
    tier, protocol = CATEGORIES.get(slug, ("small_goods", None))
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug}.json"
    rows: dict[str, dict] = {r["id"]: r for r in json.loads(path.read_text())} if path.exists() else {}
    mark = _progress(out_dir, region, slug)
    visited: set[int] = set(json.loads(mark.read_text())) if mark.exists() else set()
    tally = {"kept": 0, "pages": 0, "in the benchmark": 0, "held already": 0, "buyer, not seller": 0,
             "brand new or condition not stated": 0, "failed pages": 0}
    own = client is None
    client = client or httpx.Client(headers={"User-Agent": UA}, timeout=30.0)
    stale = 0
    try:
        first = _patiently(lambda: page(slug, 1, region, client))
        if first is None:
            tally["failed pages"] += 1
            return tally
        todo = [n for n in order(max(first[1], 1), region, slug) if n not in visited][: max(0, pages - len(visited))]
        if progress:
            progress(f"{region} {slug}: {first[1]} pages listed, visiting {len(todo)} of them at random")
        for number in todo:
            got = first if number == 1 else _patiently(lambda: page(slug, number, region, client))
            if got is None:
                tally["failed pages"] += 1
                if tally["failed pages"] >= 3:
                    break
                continue
            found = got[0]
            if not found:
                visited.add(number)
                continue
            unseen = [listing for listing, _ in found
                      if listing.id not in avoid and listing.id not in held and listing.id not in rows]
            fresh = []
            for listing, advert in found:
                if listing.id in avoid:
                    tally["in the benchmark"] += 1
                elif listing.id in held or listing.id in rows:
                    tally["held already"] += 1
                elif reason := why_not(listing):
                    tally[reason] += 1
                else:
                    fresh.append((listing, advert))
            if progress and fresh:
                progress(f"{region} {slug} page {number}: {len(fresh)} second-hand adverts, fetching their photos")
            for listing, _ in fresh:
                if not sharp_enough(listing.image_urls, max_photos) and listing.url:
                    listing.image_urls = _from_page(listing, client) or listing.image_urls
                listing.image_urls = listing.image_urls[:max_photos]
            download_media([listing for listing, _ in fresh], out_dir / "media", client=client)
            for listing, advert in fresh:
                if listing.media:
                    row = listing.to_json()
                    # Item fields only: a seller's phone number or email in the text is never kept.
                    row["description"] = redact(row["description"])
                    row.update(tier=tier, kind=kind_of(advert, slug), region=region, protocol=protocol,
                               site_category=site_category(advert))
                    rows[listing.id] = row
                    tally["kept"] += 1
            path.write_text(json.dumps(list(rows.values()), indent=1))
            visited.add(number)
            mark.parent.mkdir(parents=True, exist_ok=True)
            mark.write_text(json.dumps(sorted(visited)))
            tally["pages"] += 1
            stale = 0 if unseen else stale + 1
            if progress:
                progress(f"{region} {slug} page {number}: {len(fresh)} new, {tally['kept']} kept this run")
            if stale >= STALE_PAGES or tally["kept"] >= keep:
                break
            time.sleep(0.7)
    finally:
        if own:
            client.close()
    return tally


def held_ids(*caches: Path) -> frozenset[str]:
    """Advert ids already in other caches, so a crawl never fetches one twice."""
    ids: set[str] = set()
    for cache in caches:
        for path in cache.glob("*.json"):
            try:
                rows = json.loads(path.read_text())
            except json.JSONDecodeError:
                continue
            if isinstance(rows, list):
                ids.update(r["id"] for r in rows if isinstance(r, dict) and r.get("id"))
    return frozenset(ids)


_SLUG = re.compile(r"^[a-z0-9-]+$")


def valid_slug(slug: str) -> bool:
    return bool(_SLUG.match(slug))
