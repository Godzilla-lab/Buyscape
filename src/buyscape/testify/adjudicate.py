"""Adjudicated identity: a person's call on every answer a word rule marks wrong.

In round three, ten of fifteen "silent wrong" answers were the rules' mistakes,
found only by reading. The rules stay as a first pass; every priced answer
they mark wrong is written to `eval/testify/adjudication.yaml` with a first
reading, and counts only once a person has set its `verdict`. The first
reading is drafted by a model, and models sit this benchmark, so a draft
never moves a score.

Wrong is split three ways, because they are different failures:
- kind: the wrong thing ("sofa" for a 3 and 2 seater set, an engine for a gearbox);
- brand: the wrong maker;
- version: the right line, the wrong model ("PS4" for a PS4 Pro).

A person who reads it and cannot tell marks it unsure. The rule's call then
stands, and the answer is counted apart as unsure, so a reader sees how many
of the silent wrongs nobody could settle.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import yaml

from .schema import Item

PATH = Path(__file__).resolve().parents[3] / "eval" / "testify" / "adjudication.yaml"
VERDICTS = ("right", "wrong_kind", "wrong_brand", "wrong_version", "unsure")


def answer_text(identity: dict) -> str:
    """The answer as one line: brand and model when named, else the kind."""
    named = " ".join(p for p in (identity.get("brand"), identity.get("model")) if p)
    return named if identity.get("status") == "named" and named else identity.get("kind") or ""


def _key(item_id: str, identity: dict) -> tuple[str, str]:
    return item_id, re.sub(r"[^a-z0-9]", "", answer_text(identity).lower())


@lru_cache(maxsize=4)
def _entries(path: Path = PATH) -> tuple[dict, ...]:
    return tuple(yaml.safe_load(path.read_text()) or []) if path.exists() else ()


def verdict(item_id: str, identity: dict, path: Path | None = None) -> str | None:
    """A person's verdict on this answer for this item, or None when none has been given."""
    key = _key(item_id, identity)
    for entry in _entries(path or PATH):
        if entry.get("verdict") in VERDICTS and (entry["item"], re.sub(r"[^a-z0-9]", "", entry["answer"].lower())) == key:
            return entry["verdict"]
    return None


def wrong_how(item: Item, identity: dict) -> str:
    """A first guess at how a wrong answer is wrong, for the reader to confirm."""
    from .score import kind_matches

    if identity.get("kind") and not kind_matches(identity.get("kind"), item):
        return "wrong_kind"
    brand = (identity.get("brand") or "").lower()
    if brand and not any(w in item.answer.title.lower() for w in re.split(r"\W+", brand) if len(w) > 2):
        return "wrong_brand"
    return "wrong_version"


def pending(found: list[tuple[str, dict, Item]], path: Path | None = None) -> list[dict]:
    """Entries for answers the rules marked wrong that the file does not hold yet.

    `found` is (run name, row, item) for each priced answer a rule marked wrong."""
    held = {(e["item"], re.sub(r"[^a-z0-9]", "", e["answer"].lower())) for e in _entries(path or PATH)}
    out: dict[tuple[str, str], dict] = {}
    for run, row, item in found:
        identity = (row.get("reading") or {}).get("identity") or {}
        key = _key(item.id, identity)
        if key in held:
            continue
        entry = out.setdefault(key, {
            "item": item.id, "title": item.answer.title, "answer": answer_text(identity), "runs": [],
            "rule": "wrong", "first_reading": wrong_how(item, identity), "why": "a guess from the word rules",
            "verdict": None, "by": None,
        })
        entry["runs"].append(run)
    return list(out.values())
