"""Two readers, and only what they both saw is treated as read.

A vision model shown half a legible plate will invent the rest, write the
invented line into its own transcript, and then cite that line as its source.
Asking it to be honest does not fix this and neither does asking it to show
its work, because the fabrication is self consistent. It was measured on this
project: the same generator photographed once was read as SY6500 on one run
and GP-1000 on the next, each time with a confident source line.

What fabrications do not do is agree with each other. Two models from
different families, shown the same photograph, converge on text that is
really there and diverge on text that is not. So a plate code survives here
only when both readers produce it. Anything only one of them saw is dropped,
the disagreement is recorded, and the engine asks the seller for a clearer
photograph rather than pricing a guess.

This is the same rule the claims ledger runs on, applied one layer earlier:
records that should agree must agree, and an unproven fact is worth nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..providers.tasks import Reading

# Fields that name the item and therefore set its price. These are the ones
# worth paying a second read for. Judgements like category or material are not
# checked this way: two readers can honestly describe the same thing in
# different words, and being wrong about them costs far less.
CORROBORATED = ("brand_text", "model_text", "rating_text", "serial_text")

# Where fabrication actually lives. A model composes an alphanumeric code
# character by character, so a code only one reader produced is dropped.
# A brand is different: it is a word from a small set, read off a logo, and
# two readers rarely invent the same wrong one. So a brand that one reader
# read and the other simply left blank survives, marked as uncorroborated.
# A blank is absence of evidence. Two readers naming different brands is a
# contradiction, and that is still dropped.
INVENTABLE_CODES = ("model_text", "rating_text", "serial_text")


@dataclass
class Corroboration:
    reading: Reading
    agreed: list[str] = field(default_factory=list)
    disputed: list[str] = field(default_factory=list)
    only_one_saw: list[str] = field(default_factory=list)
    uncorroborated: list[str] = field(default_factory=list)
    # Fields one language model produced that the OCR engine also produced.
    # OCR reads glyphs and cannot compose a plate, so this is agreement.
    confirmed_by_ocr: list[str] = field(default_factory=list)

    @property
    def notes(self) -> list[str]:
        out = [f"{f} agreed by both readers" for f in self.agreed]
        out += [f"{f} was read by one reader and confirmed by OCR" for f in self.confirmed_by_ocr]
        out += [f"{f} differed between the two readers, so it is treated as unread" for f in self.disputed]
        out += [f"{f} was seen by only one reader, so it is treated as unread" for f in self.only_one_saw]
        out += [
            f"{f} was read by only one reader, so it is kept but not confirmed"
            for f in self.uncorroborated
        ]
        return out


def _norm(value: str | None) -> str:
    """Compare on letters and digits only: 'SPG-3000' and 'spg 3000' agree."""
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def _agree(a: str | None, b: str | None) -> bool:
    x, y = _norm(a), _norm(b)
    if not x or not y:
        return False
    # One reader reading more of the same plate than the other is agreement,
    # not conflict: 'SPG3000' and 'FIRMANSPG3000' are the same machine.
    return x == y or x in y or y in x


def _in_ocr(value: str | None, ocr_lines: list[str]) -> bool:
    """The OCR engine produced this value, or most of it.

    Short strings are not evidence on either side: a line reading '2' is a
    substring of 'HSC-12000I' and confirmed an invented spec sheet that way.
    So both sides need four characters, and a partial OCR line must cover at
    least half of the value it is said to confirm.
    """
    x = _norm(value)
    if len(x) < 4:
        return False
    for line in ocr_lines:
        y = _norm(line)
        if len(y) < 4:
            continue
        if x == y or x in y or (y in x and 2 * len(y) >= len(x)):
            return True
    return False


def _cite(reading: Reading, name: str) -> None:
    """Point a surviving field at the transcript line it came from."""
    value = getattr(reading, f"{name}_text")
    if not value:
        setattr(reading, f"{name}_source", None)
        return
    needle = value.lower().strip()
    line = next((l for l in reading.visible_text if needle in l.lower()), None)
    if line is None:
        # Two witnesses produced the value but no single line contains it as
        # written, for example 'SPG-3000' against a line reading 'SPG 3000'.
        # The value itself is then the line, since it was read twice.
        reading.visible_text.append(value)
        line = value
    setattr(reading, f"{name}_source", line)


def corroborate(
    first: Reading, second: Reading | None, ocr_lines: list[str] | None = None
) -> Corroboration:
    """Keep only the identifying text two witnesses produced.

    The witnesses are the two language models and, when it ran, the OCR
    engine. OCR is different in kind: it cannot invent a code, so a code one
    model produced and the OCR also produced counts as corroborated. OCR
    never adds a fact on its own, because a misread character would then be
    a fact too.

    With no second reader and no OCR this is a pass through, so a single
    reader setup still runs. It is then honest about being uncorroborated
    rather than silently pretending two models looked.
    """
    ocr = ocr_lines or []
    if second is None and not ocr:
        return Corroboration(reading=first)

    merged = first.model_copy(deep=True)
    out = Corroboration(reading=merged)

    if second is None:
        for field_name in CORROBORATED:
            if _in_ocr(getattr(first, field_name), ocr):
                out.confirmed_by_ocr.append(field_name)
        return out

    for field_name in CORROBORATED:
        mine = getattr(first, field_name)
        theirs = getattr(second, field_name)
        if not mine and not theirs:
            continue
        if _agree(mine, theirs):
            # Keep the longer reading: it carries the most of the plate.
            setattr(merged, field_name, max([mine, theirs], key=lambda v: len(v or "")))
            out.agreed.append(field_name)
            continue
        # The readers did not agree with each other. The OCR engine can still
        # side with one of them, and its word settles it, because it has no
        # way to compose the code it is agreeing with.
        backed = [v for v in (mine, theirs) if v and _in_ocr(v, ocr)]
        if len(backed) == 1:
            setattr(merged, field_name, backed[0])
            out.confirmed_by_ocr.append(field_name)
        elif mine and theirs:
            # They read different things off the same photograph. One of them
            # is wrong and nothing here says which, so neither survives.
            setattr(merged, field_name, None)
            out.disputed.append(field_name)
        elif field_name in INVENTABLE_CODES:
            setattr(merged, field_name, None)
            out.only_one_saw.append(field_name)
        else:
            setattr(merged, field_name, mine or theirs)
            out.uncorroborated.append(field_name)

    # A label is only legible if both readers could read something off it.
    merged.has_label_or_plate = first.has_label_or_plate and second.has_label_or_plate
    # The transcript is evidence too, and it is where fabrication actually
    # lives: a model that invents a plate code writes the whole line into its
    # own transcript and then cites it. Keeping one reader's uncorroborated
    # lines would hand that invention straight to the decider through
    # retrieval, so only lines two witnesses produced survive. The OCR engine
    # is a witness for a line just as it is for a field.
    shared = [
        line
        for line in first.visible_text
        if any(_agree(line, o) for o in second.visible_text) or _in_ocr(line, ocr)
    ]
    dropped = len(first.visible_text) - len(shared)
    merged.visible_text = shared
    merged.corroborated_lines = len(shared)
    if dropped:
        out.only_one_saw.append(f"{dropped} transcribed lines")
    # Each surviving field is re-cited from the surviving transcript. The
    # grounding rule downstream drops any field without a line behind it, and
    # a field two witnesses produced has earned its line. This used to blank
    # the sources instead, and the grounding rule then dropped every
    # corroborated model, in all fifteen recorded cases where both readers
    # had agreed.
    for name in ("brand", "model", "rating"):
        _cite(merged, name)

    # Either reader spotting a fraud signal or a second item is enough.
    merged.multiple_items = first.multiple_items or second.multiple_items
    merged.stock_photo_suspected = first.stock_photo_suspected or second.stock_photo_suspected
    merged.screenshot_of_gallery = first.screenshot_of_gallery or second.screenshot_of_gallery
    return out
