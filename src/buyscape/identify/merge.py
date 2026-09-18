"""One reading from many: each photo is read on its own, then combined.

A reader call takes about fifteen seconds per photo and the photos do not
depend on each other, so each is read in its own call and all of them run at
once. A seller with six photos then waits for one, not six. The readings are
combined here by rules that never invent: text is the union of what was
transcribed, a judgement comes from the photo that was surest of it, and a
fraud signal from one photo counts.
"""

from __future__ import annotations

import re
from collections import Counter

from ..providers.tasks import Reading


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _first(readings: list[Reading], name: str) -> tuple[str | None, str | None]:
    """The first photo that read the field, label photos first, with its source line."""
    ordered = sorted(readings, key=lambda r: not r.has_label_or_plate)
    for r in ordered:
        value = getattr(r, name)
        if value:
            return value, getattr(r, name.replace("_text", "_source"), None)
    return None, None


def merge_readings(readings: list[Reading]) -> Reading:
    if not readings:
        return Reading()
    if len(readings) == 1:
        return readings[0]

    surest = max(readings, key=lambda r: (r.category_confidence, -readings.index(r)))
    heaviest = max(readings, key=lambda r: (r.weight_confidence, -readings.index(r)))
    presentation = Counter(r.presentation for r in readings).most_common(1)[0][0]

    seen: set[str] = set()
    lines: list[str] = []
    for r in readings:
        for line in r.visible_text:
            key = _norm(line)
            if key and key not in seen:
                seen.add(key)
                lines.append(line)
    notes: list[str] = []
    for r in readings:
        for n in r.condition_notes:
            if n not in notes:
                notes.append(n)

    merged = Reading(
        presentation=presentation,
        materials=list((heaviest if heaviest.materials else next((r for r in readings if r.materials), heaviest)).materials),
        estimated_weight_kg=heaviest.estimated_weight_kg,
        weight_confidence=heaviest.weight_confidence,
        category=surest.category,
        category_confidence=surest.category_confidence,
        visible_text=lines,
        has_label_or_plate=any(r.has_label_or_plate for r in readings),
        is_screenshot=any(r.is_screenshot for r in readings),
        condition_notes=notes,
        # One photo of a heap is a heap. One photo with a stray cup in it is
        # not "several items", so that needs most of the photos to agree.
        multiple_items=sum(r.multiple_items for r in readings) * 2 > len(readings),
        stock_photo_suspected=any(r.stock_photo_suspected for r in readings),
        screenshot_of_gallery=any(r.screenshot_of_gallery for r in readings),
    )
    for name in ("brand_text", "model_text", "rating_text", "serial_text"):
        value, source = _first(readings, name)
        setattr(merged, name, value)
        if name != "serial_text":
            setattr(merged, name.replace("_text", "_source"), source)
    return merged
