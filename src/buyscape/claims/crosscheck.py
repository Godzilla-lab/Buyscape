"""Authenticity is structural, not a detector.

No vision model can tell a clone from a genuine unit, or a replaced screen from
an original one, from a seller's photograph. The large trade-in programmes that
tried to detect fakes from the picture all failed the same way, so this engine
never asks a model that question. Instead the item testifies: the Settings
screen, the *#06# IMEI dialogue, the box label, the rating plate, the maker's
own parts history screen, the scale at pickup. Each of those is easy to read
and hard to fake in combination. This module checks that the testimony agrees
with itself, with the identity the chain chose, and with the catalogue. Two
records that should agree and do not is FRAUD_SUSPECTED, a first-class output
that stops the price. Nothing here calls a model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..identify.catalogue import Entry, tokens

# A measured value may differ from the catalogue by this much before it counts
# as a different item. A clone iPhone is typically ten percent off the spec
# weight; a swapped battery is closer to two.
NUMERIC_TOLERANCE = 0.05

# Testimony keys that carry the maker's own verdict on replaced parts, and the
# claim specs that verdict contradicts when it is anything but clean.
PARTS_KEYS: dict[str, tuple[str, ...]] = {
    "non_genuine_parts": ("screen_original", "genuine_parts", "battery_original"),
}
_CLEAN = {"", "none", "no", "genuine", "original", "allgenuine", "nonefound", "ok"}
_NUMBER = re.compile(r"[-+]?\d+(?:\.\d+)?")


@dataclass(frozen=True)
class Testimony:
    """Values read off one protocol shot, keyed by that shot's extract names."""

    slot: str
    values: dict[str, str]


@dataclass
class CrossCheck:
    fraud_flags: list[str] = field(default_factory=list)
    contradicted: list[str] = field(default_factory=list)  # claim spec ids
    refused: list[str] = field(default_factory=list)  # shot ids the seller declined
    notes: list[str] = field(default_factory=list)

    @property
    def fraud_suspected(self) -> bool:
        return bool(self.fraud_flags)


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def _number(value: str) -> float | None:
    match = _NUMBER.search(str(value or ""))
    return float(match.group()) if match else None


def crosscheck(
    testimony: list[Testimony],
    entry: Entry | None,
    chosen_model: str | None,
    refused_slots: set[str] | None = None,
) -> CrossCheck:
    """Compare every record the item gave against every other one.

    Three comparisons, all mechanical. The same fact read from two shots must
    agree. A shot that names the model must name the model the chain chose. A
    value the catalogue knows for that model must match what was measured.
    """
    out = CrossCheck(refused=sorted(refused_slots or ()))

    by_key: dict[str, list[tuple[str, str]]] = {}
    for record in testimony:
        for key, value in record.values.items():
            if value is not None and str(value).strip():
                by_key.setdefault(key, []).append((record.slot, str(value)))

    # 1. The same fact from two records.
    for key, records in by_key.items():
        if key in PARTS_KEYS:
            continue
        first_slot, first = records[0]
        for slot, value in records[1:]:
            if _norm(value) != _norm(first):
                out.fraud_flags.append(
                    f"{key} on {slot} ({value}) does not match {key} on {first_slot} ({first})"
                )
            else:
                out.notes.append(f"{key} agrees on {first_slot} and {slot}")

    # 2. What the item calls itself against what the chain decided it is. A
    # Settings screen says 'iPhone 14 Pro', never 'Apple iPhone 14 Pro', so
    # the leading brand token is the one word allowed to be missing.
    if chosen_model:
        want = tokens(chosen_model)
        for slot, value in by_key.get("model_name", []):
            have = set(tokens(value))
            missing = [t for t in want if t not in have]
            if missing and missing != want[:1]:
                out.fraud_flags.append(
                    f"{slot} names the item '{value}', not the {chosen_model} that was identified"
                )
            else:
                out.notes.append(f"{slot} agrees with the identification")

    # 3. What was measured against what the catalogue knows about that model.
    if entry is not None:
        for key, records in by_key.items():
            spec = entry.attrs.get(key)
            if spec is None or key in PARTS_KEYS:
                continue
            spec_number = _number(spec)
            for slot, value in records:
                measured = _number(value)
                if spec_number is not None and measured is not None:
                    off = abs(measured - spec_number) > NUMERIC_TOLERANCE * abs(spec_number)
                else:
                    off = _norm(value) != _norm(spec)
                if off:
                    out.fraud_flags.append(
                        f"{key} read from {slot} is {value}, but the catalogue says "
                        f"{entry.key} is {spec}"
                    )
                else:
                    out.notes.append(f"{key} from {slot} matches the catalogue for {entry.key}")

    # 4. The maker's own diagnostics on replaced parts.
    for key, claim_ids in PARTS_KEYS.items():
        for slot, value in by_key.get(key, []):
            if _norm(value) not in _CLEAN:
                out.contradicted.extend(c for c in claim_ids if c not in out.contradicted)
                out.notes.append(f"{slot} reports replaced or non genuine parts: {value}")

    return out
