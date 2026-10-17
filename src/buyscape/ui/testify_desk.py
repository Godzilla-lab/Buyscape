"""A person sits the Testify test from the back office, one case at a time.

The cases are the folders `buyscape testify-export --model human:<name>`
writes: the exact instructions a model is sent, the seller's words with
money hidden, and the photos. This module only reads those folders and
writes an answer.json in each, checked against the same schema a model's
answer is. `testify-import` then records the answers and the scorer treats
them like any model's.

The page stays blind. It never sends which item a case is, nor whether the
case carries a planted lie, and it shows the cases in a shuffled order fixed
by the sitting's name, so the same advert's two variants never sit together.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pydantic import ValidationError

from ..testify.sitting import SCHEMAS

SAFE = re.compile(r"^[A-Za-z0-9._-]+$")
_COMPARABLE = re.compile(r"^#(\d+): (.+)$")


def _root(root: Path) -> Path:
    return root / "eval" / "testify" / "sittings"


def _safe(*names: str) -> None:
    for name in names:
        if not SAFE.match(name or "") or name in (".", ".."):
            raise ValueError(f"bad name {name!r}")


def _folder(root: Path, who: str, part: str, case: str | None = None) -> Path:
    _safe(who, part, *([case] if case else []))
    folder = _root(root) / who / part
    return folder / case if case else folder


def _index(root: Path, who: str, part: str) -> list[dict]:
    path = _root(root) / who / f"{part}.index.json"
    if not path.exists():
        raise KeyError(f"{who}/{part}")
    return json.loads(path.read_text())


def sittings(root: Path) -> list[dict]:
    """Every exported sitting for a person, with how far it has got."""
    out = []
    base = _root(root)
    if not base.is_dir():
        return out
    for index in sorted(base.glob("human_*/*.index.json")):
        who, part = index.parent.name, index.name.removesuffix(".index.json")
        entries = json.loads(index.read_text())
        done = sum((index.parent / part / e["case"] / "answer.json").exists() for e in entries)
        out.append({"who": who, "part": part, "cases": len(entries), "answered": done})
    return out


def cases(root: Path, who: str, part: str) -> list[dict]:
    """The cases in a fixed shuffled order, with nothing that names the item."""
    entries = _index(root, who, part)
    order = sorted(entries, key=lambda e: hashlib.sha256(f"{who}/{part}/{e['case']}".encode()).hexdigest())
    folder = _folder(root, who, part)
    return [
        {"case": e["case"], "task": e["task"], "answered": (folder / e["case"] / "answer.json").exists()}
        for e in order
    ]


def case(root: Path, who: str, part: str, name: str) -> dict:
    folder = _folder(root, who, part, name)
    data = json.loads((folder / "case.json").read_text())
    comparables = [
        {"n": int(m.group(1)), "text": m.group(2)}
        for line in data["user_text"].splitlines() if (m := _COMPARABLE.match(line))
    ]
    notes = None
    for line in data["user_text"].splitlines():
        if line.startswith("What you wrote: "):
            wrote = json.loads(line.removeprefix("What you wrote: "))
            notes = {"identity": wrote.get("identity"), "observations": wrote.get("observations") or []}
    answer = folder / "answer.json"
    return {
        "case": name,
        "task": data["task"],
        "system": data["system"],
        "request": data["user_text"],
        "photos": data["photos"],
        "comparables": comparables,
        "notes": notes,
        "answer": json.loads(answer.read_text()) if answer.exists() else None,
    }


def save(root: Path, who: str, part: str, name: str, answer: dict) -> dict:
    """Check the answer against the schema a model answers to, then keep it."""
    folder = _folder(root, who, part, name)
    task = json.loads((folder / "case.json").read_text())["task"]
    try:
        SCHEMAS[task].model_validate(answer)
    except ValidationError as exc:
        problems = "; ".join(f"{'.'.join(str(p) for p in e['loc']) or 'answer'}: {e['msg']}" for e in exc.errors())
        raise ValueError(problems) from None
    (folder / "answer.json").write_text(json.dumps(answer, indent=1, ensure_ascii=False) + "\n")
    return {"ok": True}


def photo(root: Path, who: str, part: str, name: str, file: str) -> Path:
    folder = _folder(root, who, part, name)
    _safe(file)
    path = folder / file
    if file not in json.loads((folder / "case.json").read_text())["photos"] or not path.is_file():
        raise KeyError(file)
    return path
