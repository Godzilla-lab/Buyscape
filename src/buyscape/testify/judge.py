"""Judged identity: whether an answer names the same thing as the advert, in any words.

The word rules mark an answer wrong unless it shares the title's words, so
"mountain bike" for a "Bicycle", "car headlight" for a "Car headlamp" and
"multifunction copier" for an old "Photocopier" all count as wrong. Sellers
name things loosely, in the market's words, and a title can be vaguer than
the photos or plain wrong; an answer that names the same thing, more or
less exactly, is right (the user's rule, 1 Nov): a "PS4" for a PS4 Pro, the
engine of an engine-and-gearbox bundle, as a person ruled on 28 Oct. What
stays wrong is another thing: a gamepad for the console, another maker,
another model or version the advert contradicts.

A judge reads only the title and the answer, never the photos, and is a
model that sits no Testify table, so no answer is judged by its own family.
Its calls are checked against a person's verdicts (`adjudication.yaml`)
before they are used, and a person's verdict always comes first.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from ..providers.base import ModelRequest

PATH = Path(__file__).resolve().parents[3] / "eval" / "testify" / "judged.jsonl"
JUDGE_VERSION = "testify_same_thing.v3"
BATCH = 15  # answers per call: the free tier allows a few calls a minute
VERDICTS = ("right", "wrong_kind", "wrong_brand", "wrong_version", "unsure")

SYSTEM = """You check answers on a Nigerian marketplace benchmark. A seller titled an advert; a model looked at the photos and said what the item is. Decide whether the model named the same thing as the advert. When a line says what the photos were checked to show, it settles what the item is where the title is vague or wrong.

Sellers name things loosely, in local or market words, and a title can be vaguer than the photos or wrong. The answer does not have to use the title's words. It is right when it names the same thing in other words: "mountain bike" for a bicycle, "car headlight" for a car headlamp, "multifunction copier" for a photocopier, "transmission" for a gearbox. It is right when it is more exact than the title ("PS4 Pro" for a Sony game console), and when it is less exact without contradicting it: the line without its tier or edition ("PS4" or "PlayStation 4" for a PS4 Pro), the maker and kind without the model, or the main item of a bundle ("car engine" for an engine sold with its gearbox and wiring).

It is wrong when it names a different thing:
- wrong_kind: another kind of item, or a part or accessory instead of the item (a gamepad for a games console, an engine for a gearbox, a phone case for a phone);
- wrong_brand: the right kind from another maker;
- wrong_version: another model or version of the right line, one the advert contradicts (a PS4 Slim, or "a standard PS4, not a Pro", for a PS4 Pro; a Yamaha PSR-350 for a PSR-550; an iPhone 11 for an iPhone 12).

Use unsure only when the title and the photo check cannot tell. Each numbered case is a different advert and answer: judge each on its own. Reply with JSON: {"verdicts": [{"n": the case number, "verdict": one of right, wrong_kind, wrong_brand, wrong_version, unsure, "why": one short sentence}, one entry per case]}."""


class JudgeVerdict(BaseModel):
    n: int
    verdict: Literal["right", "wrong_kind", "wrong_brand", "wrong_version", "unsure"]
    why: str


class JudgeBatch(BaseModel):
    verdicts: list[JudgeVerdict]


def answer_line(identity: dict) -> str:
    """Everything the answer named, in one line: brand, model and kind."""
    return " | ".join(f"{k}: {identity[k]}" for k in ("brand", "model", "kind") if identity.get(k))


def key(item_id: str, identity: dict) -> tuple[str, str]:
    return item_id, re.sub(r"[^a-z0-9|]", "", answer_line(identity).lower())


Case = tuple[str, dict, "str | None", "str | None"]  # title, answer, the benchmark's kind, what the photo check saw


def request(cases: list[Case]) -> ModelRequest:
    """One call for a batch of answers. The kind and what the photo check saw go in when known."""
    lines = []
    for n, (title, identity, kind, seen) in enumerate(cases, 1):
        lines.append(f"{n}. Advert title: {title.strip()}")
        if kind or seen:
            lines.append("   What the item is, checked against its photos: " + "; ".join(p for p in (kind, seen) if p))
        lines.append(f"   The model's answer: {answer_line(identity)}")
    return ModelRequest(
        task="testify_same_thing",
        prompt_version=JUDGE_VERSION,
        system=SYSTEM,
        user_text="\n".join(lines),
        output_schema=JudgeBatch,
        max_tokens=12000,
    )


def read(batch: JudgeBatch, size: int) -> list[JudgeVerdict | None]:
    """The verdicts in case order; a case the reply skipped or numbered twice is None, never guessed."""
    by_n: dict[int, list[JudgeVerdict]] = {}
    for v in batch.verdicts:
        by_n.setdefault(v.n, []).append(v)
    return [by_n[n][0] if len(by_n.get(n, ())) == 1 else None for n in range(1, size + 1)]


@lru_cache(maxsize=4)
def _verdicts(path: Path = PATH) -> dict[tuple[str, str], str]:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    # Only this prompt's verdicts: a changed prompt judges every answer afresh.
    return {(r["item"], r["key"]): r["verdict"] for r in rows if r.get("version", JUDGE_VERSION) == JUDGE_VERSION}


def judged(item_id: str, identity: dict, path: Path | None = None) -> str | None:
    """The judge's verdict on this answer for this item, or None when it has none."""
    item, k = key(item_id, identity)
    return _verdicts(path or PATH).get((item, k))


def record(rows: list[dict], path: Path | None = None) -> None:
    """Add verdicts, one JSON line each, and forget the cached ones."""
    path = path or PATH
    with path.open("a") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    _verdicts.cache_clear()
