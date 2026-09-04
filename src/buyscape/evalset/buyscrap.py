"""Fetch the tenant's own listings from buyscrap.com.ng into a cached test set.

BuyScrap is a WordPress site running the Classiera classifieds theme. The
WordPress JSON API lists every advert with its title, body and category; the
advert page carries the price, condition, location and the seller's photos.
Robots.txt allows crawling. Nothing here is re-fetched during a run: the cache
on disk is the test set, exactly as with Jiji.

These items are what the tenant actually buys: faulty laptops, scrap lots,
broken appliances. Their titles are not model names, so they are an answer key
for category and for the material path, not for identification.
"""

from __future__ import annotations

import html
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

from .jiji import Listing

SITE = "https://www.buyscrap.com.ng"
USER_AGENT = "Mozilla/5.0 (Macintosh) BuyscapeEval/0.1 (+tenant eval, polite crawl)"
_TAG = re.compile(r"<[^>]+>")
_PRICE = re.compile(r"Sale Price:.*?</li>", re.S)
_CONDITION = re.compile(r"Condition:.*?</li>", re.S)
_LOCATION = re.compile(r"Location.{0,12}?:.*?</li>", re.S)
_IMG = re.compile(r'<img[^>]+class="img-responsive"[^>]*>')
_SRC = re.compile(r'src="([^"]+)"')
_ALT = re.compile(r'alt="([^"]*)"')
_SCRIPTS = re.compile(r"<script.*?</script>|<style.*?</style>", re.S)


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", _TAG.sub(" ", fragment))).strip()


def _field(pattern: re.Pattern[str], page: str, label: str) -> str:
    match = pattern.search(page)
    if not match:
        return ""
    return _text(match.group(0)).replace(label, "", 1).strip()


def _price(page: str) -> int:
    digits = re.sub(r"[^\d]", "", _field(_PRICE, page, "Sale Price:"))
    return int(digits) if digits else 0


def _images(page: str, title: str) -> list[str]:
    """The advert's own photos, not the logo and not the related adverts.

    Classiera gives every photo the advert title as its alt text, and the
    related-ad carousel uses each other advert's title, so the alt is the
    attribution. Thumbnails carry a WIDTHxHEIGHT suffix and are never ours.
    """
    own: list[str] = []
    for tag in _IMG.findall(page):
        src_match = _SRC.search(tag)
        if not src_match:
            continue
        src = src_match.group(1)
        if "Payment-confirmation" in src or re.search(r"-\d+x\d+\.", src):
            continue
        alt_match = _ALT.search(tag)
        alt = html.unescape(alt_match.group(1)).strip().lower() if alt_match else ""
        if alt and alt != title.strip().lower():
            continue
        if src not in own:
            own.append(src)
    return own[:6]


def fetch(out_dir: Path, delay_s: float = 0.8) -> list[Listing]:
    """Pull every advert and its photos into out_dir. Idempotent."""
    out_dir.mkdir(parents=True, exist_ok=True)
    media_dir = out_dir / "media"
    media_dir.mkdir(exist_ok=True)
    client = httpx.Client(timeout=30, headers={"User-Agent": USER_AGENT}, follow_redirects=True)

    categories = {
        c["id"]: c["name"]
        for c in client.get(
            f"{SITE}/wp-json/wp/v2/categories", params={"per_page": 100, "_fields": "id,name"}
        ).json()
    }
    posts: list[dict] = []
    page = 1
    while True:
        resp = client.get(
            f"{SITE}/wp-json/wp/v2/posts",
            params={
                "per_page": 100,
                "page": page,
                "_fields": "id,date,link,slug,title,content,categories",
            },
        )
        if resp.status_code != 200:
            break
        batch = resp.json()
        posts.extend(batch)
        if page >= int(resp.headers.get("x-wp-totalpages", "1")):
            break
        page += 1

    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    listings: list[Listing] = []
    for post in posts:
        time.sleep(delay_s)
        page_html = _SCRIPTS.sub("", client.get(post["link"]).text)
        title = _text(post["title"]["rendered"])
        image_urls = _images(page_html, title)
        media: list[str] = []
        for i, url in enumerate(image_urls):
            suffix = Path(url.split("?")[0]).suffix or ".jpg"
            rel = f"{post['slug']}_{i}{suffix}"
            target = media_dir / rel
            if not target.exists():
                try:
                    data = client.get(url).content
                except httpx.HTTPError:
                    continue
                target.write_bytes(data)
            media.append(rel)
        listings.append(
            Listing(
                id=post["slug"],
                category=", ".join(categories.get(c, str(c)) for c in post["categories"]),
                title=title,
                price_ngn=_price(page_html),
                description=_text(post["content"]["rendered"]),
                condition=_field(_CONDITION, page_html, "Condition:"),
                is_used=True,
                attrs={"location": _field(_LOCATION, page_html, "Location:"), "posted": post["date"][:10]},
                image_urls=image_urls,
                url=post["link"],
                fetched_at=fetched_at,
                media=media,
            )
        )
    (out_dir / "listings.json").write_text(json.dumps([l.to_json() for l in listings], indent=1))
    return listings


def load(out_dir: Path) -> list[Listing]:
    path = out_dir / "listings.json"
    if not path.exists():
        return []
    return [Listing(**row) for row in json.loads(path.read_text())]
