"""Any item with its own name on its own label can be named, catalogue or not."""

from __future__ import annotations

from pathlib import Path

from buyscape.identify import chain
from buyscape.identify.catalogue import Entry, load_catalogue
from buyscape.providers.base import CostMeter, ImageRef
from buyscape.providers.fake import FakeProvider
from buyscape.providers.tasks import Reading

ROOT = Path(__file__).resolve().parents[1]


class Exploding:
    name = model = "never"

    def structured_call(self, request):
        raise AssertionError("the decider was called for an item its own label names")


def _image() -> Path:
    return next(p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file())


def test_a_plate_the_catalogue_does_not_know_names_the_item():
    read = Reading(brand_text="SUMEC", model_text="MAXI E33KWH", visible_text=["SUMEC", "MAXI E33KWH"])
    hits = [(Entry("generator", "Lutian", "LT3900", "3.5kVA", ()), 0.7)]
    assert chain.label_identity(read, ["SUMEC", "MAXI>", "E33KWH"], "", hits, [e for e, _ in hits]) == ("SUMEC", "MAXI E33KWH")
    # The catalogue knows it: the decider ranks it, with the variant.
    known = [(Entry("generator", "Sumec", "MAXI E33KWH", None, ()), 0.9)]
    assert chain.label_identity(read, ["SUMEC", "E33KWH"], "", known, [e for e, _ in known]) is None
    # No witness that cannot invent: not named.
    assert chain.label_identity(read, [], "", hits, [e for e, _ in hits]) is None
    # A brand no witness produced: not named.
    odd = Reading(brand_text="Lutian", model_text="E33KWH", visible_text=["E33KWH"])
    assert chain.label_identity(odd, ["SUMEC", "E33KWH"], "", hits, []) is None


def test_the_chain_names_it_without_paying_the_decider():
    seen = {"category": "generator", "category_confidence": 0.9, "has_label_or_plate": True,
            "brand_text": "SUMEC", "model_text": "MAXI E33KWH", "brand_source": "SUMEC",
            "model_source": "MAXI E33KWH", "visible_text": ["SUMEC", "MAXI E33KWH", "PORTABLE GENERATOR"]}
    other = dict(seen)
    result = chain.run((ImageRef(_image()),), "5kva maxi generator", load_catalogue(ROOT / "catalogue"),
                       FakeProvider(seen), Exploding(), CostMeter(), corroborator=FakeProvider(other),
                       ocr=lambda images: ["SUMEC", "MAXI>", "E33KWH"])
    assert not result.abstained
    assert result.model_key == "SUMEC MAXI E33KWH"
    assert result.named_from_label
    assert any(l.name == "identify" and l.outcome == "label" for l in result.links)
    strength, why = chain.identification_strength(result)
    assert strength >= chain.MIN_CONFIDENCE
    assert any("catalogue does not list" in w for w in why)


def test_a_label_named_item_still_gets_a_priced_range_from_the_published_band():
    from buyscape.pricing.engine import price
    from buyscape.pricing.sources import Observation

    band = [Observation(source="scrap_index_lagos", kind="scrap_floor", amount=a, currency="NGN", observed_on="2026-09-01")
            for a in (60000.0, 120000.0)]
    quote = price([], band, [], identified=True)
    assert not quote.is_failure and quote.low and quote.high
    assert quote.method == "scrap_band_only"
