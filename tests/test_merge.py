"""Each photo is read on its own, at once, and the readings are combined by rules."""

from __future__ import annotations

from pathlib import Path

from buyscape.identify.merge import merge_readings
from buyscape.providers.tasks import MaterialShare, Reading

ROOT = Path(__file__).resolve().parents[1]


def test_text_is_the_union_and_judgements_come_from_the_surest_photo():
    overview = Reading(category="laptop", category_confidence=0.95, presentation="single_unit",
                       materials=[MaterialShare(material="aluminium", fraction=0.8)], estimated_weight_kg=1.3,
                       weight_confidence=0.8, visible_text=["Apple"], condition_notes=["scuffed lid"])
    label = Reading(category="notebook", category_confidence=0.7, has_label_or_plate=True,
                    brand_text="Apple", brand_source="Apple", model_text="MacBook Air", model_source="MacBook Air",
                    serial_text="GN4F7G654M", visible_text=["MacBook Air", "M2, 2022", "GN4F7G654M", "apple"],
                    weight_confidence=0.2, condition_notes=["scuffed lid", "one key missing"])
    code = Reading(category="laptop", category_confidence=0.9, multiple_items=True, visible_text=["UUXD"])
    m = merge_readings([overview, label, code])
    assert m.category == "laptop" and m.category_confidence == 0.95
    assert m.estimated_weight_kg == 1.3 and m.materials[0].material == "aluminium"
    assert m.visible_text == ["Apple", "MacBook Air", "M2, 2022", "GN4F7G654M", "UUXD"]
    assert m.brand_text == "Apple" and m.model_text == "MacBook Air" and m.serial_text == "GN4F7G654M"
    assert m.model_source == "MacBook Air" and m.has_label_or_plate
    assert m.condition_notes == ["scuffed lid", "one key missing"]
    assert not m.multiple_items, "one photo with a stray object in it is not several items"
    assert merge_readings([code, Reading(multiple_items=True)]).multiple_items


def test_a_fraud_signal_from_any_photo_counts_and_one_reading_passes_through():
    plain = Reading(category="phone", category_confidence=0.9)
    assert merge_readings([plain]) is plain
    assert merge_readings([plain, Reading(stock_photo_suspected=True)]).stock_photo_suspected


def test_the_chain_reads_every_photo_in_its_own_call_at_once():
    import time

    from buyscape.identify import chain
    from buyscape.identify.catalogue import load_catalogue
    from buyscape.providers.base import CostMeter, ImageRef
    from buyscape.providers.fake import FakeProvider

    class Counting(FakeProvider):
        calls: list[int] = []

        def structured_call(self, request):
            if request.task == "read_evidence":
                Counting.calls.append(len(request.images))
                time.sleep(0.3)
            return super().structured_call(request)

    media = [p for p in (ROOT / "eval" / "raw" / "media").rglob("*") if p.is_file()][:4]
    seen = {"category": "generator", "category_confidence": 0.9, "visible_text": ["FIRMAN"]}
    started = time.perf_counter()
    result = chain.run(tuple(ImageRef(p) for p in media), "gen", load_catalogue(ROOT / "catalogue"),
                       Counting(seen), FakeProvider(), CostMeter(), corroborator=Counting(seen))
    elapsed = time.perf_counter() - started
    assert Counting.calls == [1] * 8, "four photos and two readers is eight single-photo calls"
    assert elapsed < 1.2, f"eight 0.3 s calls took {elapsed:.2f} s: they did not overlap"
    assert result.reading.visible_text == ["FIRMAN"]
