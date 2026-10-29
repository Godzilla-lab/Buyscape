"""New prices from shops, for the thin markets where a used price is a share of the new one.

Rule 4 allows it: a dealer's new asking price times the tenant's own
`resale_fraction` is still retrieval. Every row keeps the shop, the product
link and the day it was read. Each shop is read the way its own rules allow
(robots files checked on 28 October 2026):

- **Pointek** (pointekonline.com) publishes its catalogue through the
  standard WooCommerce store API, read a page of products at a time.
- **Slot** (slot.ng) lists every product in its sitemap, and each product
  page carries a schema.org Product block with its price, stock and
  condition. Its search API refuses requests that lack its own site's
  headers, so it is not used. Slot also sells pre-owned phones: those rows
  are kept, marked `pre_owned`, and never used as a new price.
- **Jumia** (jumia.com.ng) closes its search to crawlers (`/catalog/` is
  disallowed), so the categories a tenant names are read whole, a page at a
  time, from the product list each category page carries.

Rows are cached like Jiji's adverts, one JSON file per shop in
`eval/raw/shops/` (a folder of its own: the engine reads every JSON file at
the top of `eval/raw` as adverts), and never fetched during a run. A tenant names the shops
it trusts in its own YAML (`shops`), and the comps source reads only those.
"""

from __future__ import annotations

import html
import json
import re
import time
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from pathlib import Path

import httpx

USER_AGENT = "Mozilla/5.0 (Macintosh) BuyscapeEval/0.1 (+price research, polite crawl)"
# Seconds between two requests to the same shop.
PAUSE = 1.5
SHOPS = ("pointek", "slot", "jumia")

Row = dict


# A shop's own data can call a pre-owned phone new: Slot's product blocks say
# NewCondition for titles that begin "PRE-OWNED" (29 Oct). The title decides.
_PRE_OWNED = re.compile(r"\b(pre[- ]?owned|refurb\w*|renewed|uk[- ]used|used|open[- ]box|second[- ]hand)\b", re.IGNORECASE)


def condition_of(title: str, stated: str = "new") -> str:
    return "pre_owned" if stated != "new" or _PRE_OWNED.search(title or "") else "new"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _row(shop: str, key: str, title: str, price: float, url: str, condition: str = "new",
         category: str | None = None) -> Row:
    """One shop price in the cached advert format, so the comps source reads it like Jiji's."""
    title = re.sub(r"\s+", " ", html.unescape(title)).strip()
    return {
        "id": f"{shop}:{key}",
        "category": category,
        "title": title,
        "price_ngn": int(round(price)),
        "description": "",
        "condition": condition_of(title, condition),
        "is_used": False,
        "attrs": {},
        "image_urls": [],
        "url": url,
        "fetched_at": _now(),
        "media": [],
        "source": f"shop:{shop}",
    }


def _get(client: httpx.Client, url: str, **params) -> httpx.Response | None:
    """One polite request, retried twice on a timeout or a server error; None when the shop stays silent."""
    for attempt in range(3):
        try:
            resp = client.get(url, params=params or None)
            if resp.status_code < 500:
                return resp
        except httpx.TransportError:
            pass
        time.sleep(PAUSE * (attempt + 2))
    return None


# Pointek: the WooCommerce store API.

def pointek_rows(products: list[dict]) -> list[Row]:
    """Store API products to rows: in stock, with a price. Prices come in the
    currency's minor unit (kobo), with the unit's size alongside."""
    out: list[Row] = []
    for p in products:
        prices = p.get("prices") or {}
        if not p.get("is_in_stock") or not prices.get("price") or prices.get("currency_code") != "NGN":
            continue
        price = int(prices["price"]) / 10 ** int(prices.get("currency_minor_unit") or 0)
        out.append(_row("pointek", str(p["id"]), p.get("name") or "", price, p.get("permalink") or ""))
    return out


def fetch_pointek(client: httpx.Client, max_pages: int = 60) -> list[Row]:
    rows: list[Row] = []
    for page in range(1, max_pages + 1):
        resp = _get(client, "https://www.pointekonline.com/wp-json/wc/store/v1/products", page=page, per_page=100)
        if resp is None or resp.status_code != 200:
            break
        products = resp.json()
        if not products:
            break
        rows += pointek_rows(products)
        if page >= int(resp.headers.get("X-WP-TotalPages") or page):
            break
        time.sleep(PAUSE)
    return rows


# Slot: the sitemap, then each product page's schema.org Product block.

_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def ld_product(page: str) -> dict | None:
    """The schema.org Product block of a product page, or None."""
    for block in _LD.findall(page):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for item in data if isinstance(data, list) else [data]:
            if isinstance(item, dict) and item.get("@type") == "Product":
                return item
    return None


def slot_row(url: str, product: dict) -> Row | None:
    offer = product.get("offers") or {}
    if isinstance(offer, list):
        offer = offer[0] if offer else {}
    if offer.get("priceCurrency") != "NGN" or not offer.get("price") or "InStock" not in str(offer.get("availability")):
        return None
    condition = "new" if "NewCondition" in str(offer.get("itemCondition", "NewCondition")) else "pre_owned"
    return _row("slot", url.rstrip("/").rsplit("/", 1)[-1], product.get("name") or "", float(offer["price"]), url, condition)


def fetch_slot(client: httpx.Client, limit: int | None = None) -> list[Row]:
    resp = _get(client, "https://slot.ng/sitemap.xml")
    if resp is None or resp.status_code != 200:
        return []
    urls = re.findall(r"<loc>(https://slot\.ng/products/[^<]+)</loc>", resp.text)[:limit]
    rows: list[Row] = []
    for url in urls:
        time.sleep(PAUSE)
        page = _get(client, url)
        product = ld_product(page.text) if page is not None and page.status_code == 200 else None
        row = slot_row(url, product) if product else None
        if row:
            rows.append(row)
    return rows


# Jumia: whole categories, a page at a time.

_STORE = re.compile(r"window\.__STORE__\s*=\s*(\{.*?\});</script>", re.S)


def jumia_rows(page: str, category: str | None) -> list[Row]:
    """The products a Jumia category page carries, buyable and priced."""
    match = _STORE.search(page)
    if not match:
        return []
    out: list[Row] = []
    for p in json.loads(match.group(1)).get("products") or []:
        price = (p.get("prices") or {}).get("rawPrice")
        if not price or p.get("isBuyable") is False:
            continue
        # The display name is the name the page shows, brand first.
        title = p.get("displayName") or p.get("name") or ""
        out.append(_row("jumia", str(p.get("sku")), title, float(price),
                        "https://www.jumia.com.ng" + str(p.get("url") or ""), category=category))
    return out


def fetch_jumia(client: httpx.Client, categories: dict[str, str | None], pages: int = 5) -> list[Row]:
    """`categories` maps a Jumia category slug to the tenant's category for it."""
    rows: list[Row] = []
    for slug, category in categories.items():
        for page in range(1, pages + 1):
            resp = _get(client, f"https://www.jumia.com.ng/{slug}/", page=page)
            if resp is None or resp.status_code != 200:
                break
            found = jumia_rows(resp.text, category)
            if not found:
                break
            rows += found
            time.sleep(PAUSE)
    return rows


def save(rows: list[Row], path: Path) -> int:
    """Merge into the shop's cache: a product read again keeps its newest price."""
    known: dict[str, Row] = {}
    if path.exists():
        known = {r["id"]: r for r in json.loads(path.read_text())}
    for r in rows:
        known[r["id"]] = r
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(known.values(), key=lambda r: r["id"]), ensure_ascii=False, indent=0))
    return len(known)


CACHE = Path("eval") / "raw" / "shops"


def load(root: Path, shops: Iterable[str]) -> list[Row]:
    """The new-price rows of the shops a tenant trusts. Pre-owned rows are a dealer's
    used price, a different market, and are left out."""
    rows: list[Row] = []
    for shop in shops:
        path = root / CACHE / f"{shop}.json"
        if path.exists():
            rows += [r for r in json.loads(path.read_text()) if condition_of(r.get("title", ""), r.get("condition", "new")) == "new"]
    return rows


FETCHERS: dict[str, Callable[..., list[Row]]] = {"pointek": fetch_pointek, "slot": fetch_slot, "jumia": fetch_jumia}


def client() -> httpx.Client:
    return httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=60, follow_redirects=True)
