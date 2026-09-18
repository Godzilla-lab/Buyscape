"""When the cache has no price for an identified item, go and get one; when
the market has none either, a person prices it, never the scrap floor."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from buyscape.pricing.engine import price
from buyscape.pricing.sources import JijiComps, Observation, SourceUnavailable
from buyscape.providers.tasks import Reading

ROOT = Path(__file__).resolve().parents[1]


def _row(i: int, title: str, price_ngn: int, category: str = "laptop") -> dict:
    return {"id": f"live{i}", "category": category, "title": title, "price_ngn": price_ngn,
            "is_used": True, "url": "", "fetched_at": "2026-09-18T09:00:00Z"}


def test_a_model_the_cache_lacks_is_fetched_live_once_and_remembered(tmp_path):
    calls: list[tuple[str, str]] = []

    def live(key, category):
        calls.append((key, category))
        return [_row(1, "Apple MacBook Air M2 2022 16GB 256GB", 720000),
                _row(2, "MacBook Air M2 13 inch 2022 used", 650000),
                _row(3, "Brand new MacBook Air M2", 900000) | {"is_used": False}]

    comps = JijiComps(tmp_path, live=live)
    obs = comps.fetch("laptop", "Apple MacBook Air M2 2022")
    assert [o.amount for o in obs] == [720000.0, 650000.0]
    assert calls == [("Apple MacBook Air M2 2022", "laptop")]
    assert len(json.loads((tmp_path / "live.json").read_text())) == 2
    # The next seller of the same model is served from what was learnt.
    comps.fetch("laptop", "Apple MacBook Air M2 2022")
    assert len(calls) == 1
    again = JijiComps(tmp_path)
    assert len(again.fetch("laptop", "Apple MacBook Air M2 2022")) == 2


def test_a_market_outage_is_one_failed_call_not_one_per_case(tmp_path):
    calls = []

    def down(key, category):
        calls.append(key)
        raise ConnectionError("jiji unreachable")

    comps = JijiComps(tmp_path, live=down)
    with pytest.raises(SourceUnavailable):
        comps.fetch("laptop", "Apple MacBook Air M2 2022")
    with pytest.raises(SourceUnavailable):
        comps.fetch("laptop", "HP EliteBook 840 G6")
    assert calls == ["Apple MacBook Air M2 2022"]


def test_an_identified_item_with_only_a_floor_goes_to_a_person_not_to_the_floor():
    floor = [Observation(source="scrap_index_lagos", kind="scrap_floor", amount=5000.0, currency="NGN", observed_on="2026-09-01")]
    quote = price([], floor, [], identified=True)
    assert quote.failure_code == "NO_PRICE_DATA"
    assert quote.floor == 5000.0 and "5,000" in quote.reason
    # A real band with width still prices the whole unit.
    band = [Observation(source="scrap_index_lagos", kind="scrap_floor", amount=a, currency="NGN", observed_on="2026-09-01") for a in (60000.0, 120000.0)]
    assert price([], band, [], identified=True).method == "scrap_band_only"


def test_a_screen_showing_its_own_serial_is_testimony_not_a_gallery():
    from buyscape.identify import chain
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider

    image = next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())
    about = {"category": "laptop", "category_confidence": 1.0, "has_label_or_plate": True,
             "screenshot_of_gallery": True, "serial_text": "GN4F7G654M", "model_text": "MacBook Air",
             "model_source": "MacBook Air", "visible_text": ["MacBook Air", "M2, 2022", "GN4F7G654M"]}
    result = chain.run((ImageRef(image),), "macbook air m2", load_catalogue(ROOT / "catalogue"),
                       FakeProvider(about), FakeProvider(), CostMeter(), corroborator=FakeProvider(about))
    assert not any("gallery" in f for f in result.fraud_flags)
    gallery = dict(about, serial_text=None)
    result = chain.run((ImageRef(image),), "macbook air m2", load_catalogue(ROOT / "catalogue"),
                       FakeProvider(gallery), FakeProvider(), CostMeter(), corroborator=FakeProvider(gallery))
    assert any("gallery" in f for f in result.fraud_flags)


def test_the_seller_is_told_what_it_is_and_that_a_person_prices_it(tmp_path, monkeypatch):
    from buyscape.ui.server import Engine

    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    eng = Engine(ROOT)
    store = eng.store
    store.dir = tmp_path / "sessions"
    s = store.create({"category": "E-waste", "text": "macbook air m2"})
    session = store.load(s["id"])
    session["result"] = {"model_key": "Apple MacBook Air M2 2022", "asks": [], "claims": [], "answer_notes": [],
                         "quote": {"failure_code": "NO_PRICE_DATA", "reason": "r", "low": None, "high": None,
                                   "currency": "NGN", "floor": 5000.0, "weight_conditional": False, "conditions": []}}
    session["status"] = "no_price"
    out = store.seller_view(session)["outcome"]
    assert "person" in out["headline"].lower()
    assert "Apple MacBook Air M2 2022" in out["detail"] and "5,000" in out["detail"]


def test_a_thin_cache_is_topped_up_from_the_live_market_and_dedupes(tmp_path):
    (tmp_path / "laptop.json").write_text(json.dumps([_row(1, "Apple MacBook Air M2 2022 8GB", 800000)]))
    calls = []

    def live(key, category):
        calls.append(key)
        return [_row(1, "Apple MacBook Air M2 2022 8GB", 800000), _row(9, "MacBook Air M2 2022 16GB", 950000)]

    comps = JijiComps(tmp_path, live=live)
    obs = comps.fetch("laptop", "Apple MacBook Air M2 2022")
    assert sorted(o.amount for o in obs) == [800000.0, 950000.0]
    assert calls == ["Apple MacBook Air M2 2022"]
    # Six or more on hand: the market is not asked.
    many = tmp_path / "many"
    many.mkdir()
    (many / "laptop.json").write_text(json.dumps([_row(i, "Apple MacBook Air M2 2022", 700000 + i) for i in range(6)]))
    calls.clear()
    JijiComps(many, live=live).fetch("laptop", "Apple MacBook Air M2 2022")
    assert calls == []
