"""Shop prices: each shop's page read right, pre-owned kept apart, and every
price sourced to its shop when the comps source hands it out."""

import json
from pathlib import Path

from buyscape.pricing import shops
from buyscape.pricing.sources import JijiComps


def test_pointek_prices_come_in_kobo_and_only_in_stock_items_count():
    products = [
        {"id": 7, "name": "iPhone Duo 256GB", "permalink": "https://www.pointekonline.com/p/7", "is_in_stock": True,
         "prices": {"price": "380000000", "currency_code": "NGN", "currency_minor_unit": 2}},
        {"id": 8, "name": "Sold out phone", "permalink": "https://www.pointekonline.com/p/8", "is_in_stock": False,
         "prices": {"price": "100000", "currency_code": "NGN", "currency_minor_unit": 2}},
    ]
    rows = shops.pointek_rows(products)
    assert [(r["id"], r["price_ngn"], r["source"]) for r in rows] == [("pointek:7", 3800000, "shop:pointek")]


def _slot_page(condition: str, availability: str = "https://schema.org/InStock") -> str:
    block = {"@type": "Product", "name": "POCO C95 PRO 8GB+256GB",
             "offers": {"@type": "Offer", "priceCurrency": "NGN", "price": 304800,
                        "availability": availability, "itemCondition": f"https://schema.org/{condition}"}}
    return f'<html><script type="application/ld+json">{json.dumps(block)}</script></html>'


def test_slot_reads_the_product_block_and_marks_pre_owned_apart():
    url = "https://slot.ng/products/poco-c95-pro-8gb256gb"
    new = shops.slot_row(url, shops.ld_product(_slot_page("NewCondition")))
    used = shops.slot_row(url, shops.ld_product(_slot_page("UsedCondition")))
    gone = shops.slot_row(url, shops.ld_product(_slot_page("NewCondition", "https://schema.org/OutOfStock")))
    assert new["price_ngn"] == 304800 and new["condition"] == "new" and new["id"] == "slot:poco-c95-pro-8gb256gb"
    assert used["condition"] == "pre_owned" and gone is None


def test_jumia_reads_the_category_page_store_and_skips_what_cannot_be_bought():
    store = {"products": [
        {"sku": "XI1", "name": "Redmi 15C 128GB", "displayName": "XIAOMI Redmi 15C 128GB", "brand": "XIAOMI",
         "prices": {"rawPrice": "174557.00"}, "url": "/xiaomi-redmi-15c-1.html", "isBuyable": True},
        {"sku": "NO2", "name": "Gone", "prices": {"rawPrice": "1000"}, "url": "/gone.html", "isBuyable": False},
    ]}
    page = f"<script>window.__STORE__={json.dumps(store)};</script>"
    rows = shops.jumia_rows(page, "phone")
    assert [(r["title"], r["price_ngn"], r["category"]) for r in rows] == [("XIAOMI Redmi 15C 128GB", 174557, "phone")]
    assert rows[0]["url"] == "https://www.jumia.com.ng/xiaomi-redmi-15c-1.html"


def test_only_the_tenants_shops_and_only_new_prices_reach_the_comps_source(tmp_path: Path):
    new = shops._row("slot", "a", "Samsung Galaxy A07 128GB", 200000, "https://slot.ng/products/a", category="phone")
    used = shops._row("slot", "b", "Samsung Galaxy A07 128GB", 150000, "https://slot.ng/products/b", "pre_owned", "phone")
    shops.save([new, used], tmp_path / shops.CACHE / "slot.json")
    shops.save([shops._row("jumia", "c", "Samsung Galaxy A07 128GB", 210000, "https://www.jumia.com.ng/c.html")],
               tmp_path / shops.CACHE / "jumia.json")
    rows = shops.load(tmp_path, ["slot"])
    assert [r["id"] for r in rows] == ["slot:a"]
    comps = JijiComps(tmp_path / "empty", shop_rows=rows)
    found = comps.fetch("phone", "Samsung Galaxy A07 128GB", new=True)
    assert [(o.source, o.amount, o.url) for o in found] == [("shop:slot", 200000.0, "https://slot.ng/products/a")]


def test_a_product_read_again_keeps_its_newest_price(tmp_path: Path):
    path = tmp_path / "pointek.json"
    shops.save([shops._row("pointek", "1", "Phone", 100, "u")], path)
    assert shops.save([shops._row("pointek", "1", "Phone", 120, "u"), shops._row("pointek", "2", "Other", 5, "v")], path) == 2
    assert {r["id"]: r["price_ngn"] for r in json.loads(path.read_text())} == {"pointek:1": 120, "pointek:2": 5}
