"""Fetch a held-out test set of real Lagos listings from Jiji.

Read-only. Runs once, caches to disk, and is never called during an eval run.
The listing title supplies ground-truth brand and model; the asking price is
the pricing reference.

Nigerian appliance and generator listings are dominated by dealers selling new
stock: a sample of 60 washing machine adverts had 59 marked "Brand New". So the
set keeps every listing that carries photos and records its condition, and the
eval uses the split deliberately. Identification is scored on all of them, since
a photo of a washing machine is a photo of a washing machine either way. Pricing
is scored only on the used subset, because a dealer's new-stock asking price is
not evidence about what a second-hand unit fetches.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

BASE = "https://jiji.ng/api_web/v1/listing"
UA = (
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124 Mobile Safari/537.36"
)
USED_VALUES = {"used", "foreign used", "nigerian used", "refurbished"}
MIN_PHOTOS = 1


@dataclass(frozen=True)
class Query:
    """One slice of the test set."""

    category: str
    slug: str | None = None
    query: str | None = None
    must_include: tuple[str, ...] = ()
    filters: dict[str, str] = field(default_factory=dict)

    def params(self, page: int, region: str) -> dict[str, str]:
        p = {"region_slug": region, "page": str(page)}
        if self.slug:
            p["slug"] = self.slug
        if self.query:
            p["query"] = self.query
        p.update(self.filters)
        return p


# A bare "generator" query 301-redirects to this category plus type filter, so
# the filter is applied directly.
QUERIES: tuple[Query, ...] = (
    Query("phone", slug="mobile-phones"),
    Query(
        "generator",
        slug="power-equipments",
        must_include=("generator", "kva", "gen set", "genset"),
        filters={"filter_attr_1483_type": "Generators"},
    ),
    Query(
        "split_ac",
        query="split air conditioner",
        must_include=("air condition", "aircondition", " ac ", "hp split", "split"),
    ),
    Query(
        "washing_machine",
        query="washing machine",
        must_include=("washing machine", "washer", "wash and dry"),
    ),
    # The tenant's own adverts are mostly laptops, and Jiji titles here carry
    # brand, model, RAM and processor, which makes them a strong answer key.
    Query("laptop", slug="computers-and-laptops", must_include=("laptop", "macbook", "notebook")),
)


@dataclass
class Listing:
    """One cached advert, trimmed to the fields the eval needs."""

    id: str
    category: str
    title: str
    price_ngn: int
    description: str
    condition: str
    is_used: bool
    attrs: dict[str, str]
    image_urls: list[str]
    url: str
    fetched_at: str
    media: list[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "price_ngn": self.price_ngn,
            "description": self.description,
            "condition": self.condition,
            "is_used": self.is_used,
            "attrs": self.attrs,
            "image_urls": self.image_urls,
            "url": self.url,
            "fetched_at": self.fetched_at,
            "media": self.media,
        }


def _attrs(advert: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for a in advert.get("attrs") or []:
        name = a.get("name")
        value = a.get("value")
        if name and value:
            out[str(name)] = str(value)
    return out


def _image_urls(advert: dict) -> list[str]:
    urls: list[str] = []
    for img in advert.get("images") or []:
        if isinstance(img, dict):
            url = img.get("url") or img.get("full") or img.get("origin")
            if url:
                urls.append(str(url))
        elif isinstance(img, str):
            urls.append(img)
    main = (advert.get("image_obj") or {}).get("url")
    if main and main not in urls:
        urls.insert(0, str(main))
    return urls


def _is_used(attrs: dict[str, str]) -> bool:
    """True when the seller marked the item second-hand.

    Only these listings are valid price references; everything with photos is
    still a valid identification case.
    """
    return (attrs.get("Condition") or "").strip().lower() in USED_VALUES


def _matches(title: str, q: Query) -> bool:
    if not q.must_include:
        return True
    hay = f" {title.lower()} "
    return any(token in hay for token in q.must_include)


def fetch_category(
    q: Query,
    want: int,
    region: str = "lagos",
    max_pages: int = 25,
    client: httpx.Client | None = None,
) -> list[Listing]:
    """Page through Jiji until `want` used listings with photos are collected."""
    own = client is None
    client = client or httpx.Client(headers={"User-Agent": UA}, timeout=25.0)
    kept: list[Listing] = []
    try:
        for page in range(1, max_pages + 1):
            if len(kept) >= want:
                break
            r = client.get(BASE, params=q.params(page, region))
            if r.status_code != 200:
                break
            adverts = (r.json().get("adverts_list") or {}).get("adverts") or []
            if not adverts:
                break
            for advert in adverts:
                attrs = _attrs(advert)
                title = str(advert.get("title") or "")
                images = _image_urls(advert)
                if len(images) < MIN_PHOTOS or not _matches(title, q):
                    continue
                price = (advert.get("price_obj") or {}).get("value")
                if not isinstance(price, (int, float)) or price <= 0:
                    continue
                kept.append(
                    Listing(
                        id=str(advert.get("guid") or advert.get("id")),
                        category=q.category,
                        title=title,
                        price_ngn=int(price),
                        description=str(advert.get("details") or advert.get("short_description") or ""),
                        condition=attrs.get("Condition", ""),
                        is_used=_is_used(attrs),
                        attrs=attrs,
                        image_urls=images[:8],
                        url=str(advert.get("url") or ""),
                        fetched_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    )
                )
                if len(kept) >= want:
                    break
            time.sleep(0.7)
    finally:
        if own:
            client.close()
    return kept


def download_media(listings: list[Listing], root: Path, client: httpx.Client | None = None) -> None:
    """Save each listing's photos under root/<id>/ and record relative paths."""
    own = client is None
    client = client or httpx.Client(headers={"User-Agent": UA}, timeout=30.0)
    try:
        for listing in listings:
            folder = root / listing.id
            folder.mkdir(parents=True, exist_ok=True)
            saved: list[str] = []
            for i, url in enumerate(listing.image_urls):
                dest = folder / f"{i:02d}.jpg"
                if not dest.exists():
                    try:
                        resp = client.get(url)
                        if resp.status_code != 200 or not resp.content:
                            continue
                        dest.write_bytes(resp.content)
                    except httpx.HTTPError:
                        continue
                saved.append(str(dest.relative_to(root)))
            listing.media = saved
    finally:
        if own:
            client.close()


def build(
    out_dir: Path,
    per_category: int = 40,
    region: str = "lagos",
    only: tuple[str, ...] = (),
) -> dict[str, int]:
    """Fetch and cache the whole test set with photos. Returns counts per category.

    `only` restricts the fetch to named categories, so adding one category
    never re-downloads and re-writes the ones already cached.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    media_root = out_dir / "media"
    counts: dict[str, int] = {}
    with httpx.Client(headers={"User-Agent": UA}, timeout=30.0) as client:
        for q in QUERIES:
            if only and q.category not in only:
                continue
            listings = fetch_category(q, per_category, region=region, client=client)
            download_media(listings, media_root, client=client)
            listings = [l for l in listings if l.media]
            path = out_dir / f"{q.category}.json"
            path.write_text(json.dumps([l.to_json() for l in listings], indent=2))
            counts[q.category] = len(listings)
    return counts


def build_price_pool(
    out_dir: Path,
    per_category: int = 400,
    region: str = "lagos",
    max_pages: int = 60,
    only: tuple[str, ...] = (),
) -> dict[str, int]:
    """Cache a large pool of used listings for use as comparable prices only.

    This is the price database a real deployment maintains, and it is separate
    from the test set: no photos are downloaded, and only second-hand listings
    are kept, because a dealer's new-stock price is not a used-price comp.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    with httpx.Client(headers={"User-Agent": UA}, timeout=30.0) as client:
        for q in QUERIES:
            if only and q.category not in only:
                continue
            kept: list[Listing] = []
            seen: set[str] = set()
            for page in range(1, max_pages + 1):
                if len(kept) >= per_category:
                    break
                r = client.get(BASE, params=q.params(page, region))
                if r.status_code != 200:
                    break
                adverts = (r.json().get("adverts_list") or {}).get("adverts") or []
                if not adverts:
                    break
                for advert in adverts:
                    attrs = _attrs(advert)
                    if not _is_used(attrs):
                        continue
                    title = str(advert.get("title") or "")
                    if not _matches(title, q):
                        continue
                    price = (advert.get("price_obj") or {}).get("value")
                    if not isinstance(price, (int, float)) or price <= 0:
                        continue
                    advert_id = str(advert.get("guid") or advert.get("id"))
                    if advert_id in seen:
                        continue
                    seen.add(advert_id)
                    kept.append(
                        Listing(
                            id=advert_id,
                            category=q.category,
                            title=title,
                            price_ngn=int(price),
                            description="",
                            condition=attrs.get("Condition", ""),
                            is_used=True,
                            attrs=attrs,
                            image_urls=[],
                            url=str(advert.get("url") or ""),
                            fetched_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        )
                    )
                time.sleep(0.6)
            (out_dir / f"{q.category}.json").write_text(
                json.dumps([l.to_json() for l in kept], indent=2)
            )
            counts[q.category] = len(kept)
    return counts


def load(out_dir: Path) -> list[Listing]:
    """Read the cached test set back."""
    listings: list[Listing] = []
    for q in QUERIES:
        path = out_dir / f"{q.category}.json"
        if not path.exists():
            continue
        for row in json.loads(path.read_text()):
            listings.append(Listing(**row))
    return listings
