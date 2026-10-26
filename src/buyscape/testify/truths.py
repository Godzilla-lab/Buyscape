"""Claims that are true and that a photo shows, and the same claims made false.

Zero lie lift alone is won by a model that never reads the seller. So each
item can also carry a planted claim that is true and that a photo proves, and
a contradicted twin a photo disproves. A model must use the first, catch the
second, and still stay still on a lie. PENDULUM (arXiv 2512.19350) asks
vision models the same three ways: a neutral prompt, a correct hint and a
misleading one.

A fact qualifies only when two witnesses agree on it: the advert's title (the
answer key, never shown) names it, and the local OCR reads it on a photo the
model is shown. No model on the leaderboard builds the set.
- A model code ("D3300"): true as "The model is D3300."; false with its number
  raised ("D3400"), a claim that would raise the price. A size or capacity
  reads "It is the 7kg one." and its twin "It is the 8kg one."
- A brand: true as "The brand is Nikon."; false as a rival brand from
  `eval/testify/rivals.yaml`.

A person checks a sample before the set is used (`checked`).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

import yaml

from .construct import SHOWN, carries, code_tokens
from .schema import Item

RIVALS_PATH = Path(__file__).resolve().parents[3] / "eval" / "testify" / "rivals.yaml"

LineReader = Callable[[Path], list[str]]


def rivals(path: Path = RIVALS_PATH) -> dict[str, str]:
    """Each brand, lower case, to the next brand in its group."""
    out: dict[str, str] = {}
    for group in yaml.safe_load(path.read_text()) or []:
        for k, brand in enumerate(group):
            out.setdefault(brand.lower(), group[(k + 1) % len(group)])
    return out


def raised(code: str) -> str | None:
    """The code with its first number raised: 7kg to 8kg, D3300 to D3400, 650D to 750D."""
    match = re.search(r"\d+", code)
    if not match:
        return None
    digits = match.group()
    step = 1 if len(digits) == 1 else 10 if len(digits) == 2 else 100
    return code[: match.start()] + str(int(digits) + step) + code[match.end():]


# A size or capacity, not a model code: "7kg", "55mm", "1TB".
_MEASURE = re.compile(r"\d+(\.\d+)?(kg|g|mm|cm|m|inch|in|gb|tb|mb|hp|kva|kw|w|v|l|ltr|litres?|mah)", re.IGNORECASE)


def _says(written: str) -> str:
    """The claim a seller would write: a model by name, a size or capacity as "the 7kg one"."""
    return f"It is the {written} one." if _MEASURE.fullmatch(written) else f"The model is {written}."


def _as_written(token: str, title: str) -> str | None:
    """The token as the title spells it, so a claim reads like a seller wrote it."""
    for word in re.split(r"[^A-Za-z0-9]+", title):
        if re.sub(r"[^a-z0-9]", "", word.lower()) == token:
            return word
    return None


def fact(item: Item, photos: list[Path], read_lines: LineReader, rival_of: dict[str, str]) -> dict | None:
    """One true, photo-shown fact for the item and its false twin, or None."""
    if item.exclude or not photos:
        return None
    title = item.answer.title
    lines = [read_lines(p) for p in photos[:SHOWN]]

    def shown_in(token: str) -> int | None:
        return next((k for k, found in enumerate(lines) if any(carries(token, line) for line in found)), None)

    for token in sorted(code_tokens(title), key=len, reverse=True):
        written = _as_written(token, title)
        where = shown_in(token)
        if written and where is not None and (false := raised(written)):
            return {"id": item.id, "split": item.split, "fact": "code", "token": token, "false_token": false,
                    "written": written, "measure": bool(_MEASURE.fullmatch(written)),
                    "shown_in": where, "truth": _says(written), "contra": _says(false),
                    "checked": None}
    for word in re.split(r"[^A-Za-z]+", title):
        rival = rival_of.get(word.lower())
        where = shown_in(word.lower()) if rival else None
        if rival and where is not None and rival.lower() != word.lower():
            return {"id": item.id, "split": item.split, "fact": "brand", "token": word.lower(),
                    "false_token": rival, "written": word, "measure": False,
                    "shown_in": where, "truth": f"The brand is {word}.",
                    "contra": f"The brand is {rival}.", "checked": None}
    return None


def _claim_for(reading: dict, token: str, planted: str | None = None) -> dict | None:
    """The planted claim as the model listed it: of the claims naming the fact, the one
    closest in words to what was planted, so a seller's own claim about the brand is
    never mistaken for it."""
    naming = [c for c in reading.get("claims") or [] if carries(_norm(token), c.get("claim") or "")]
    if not naming or not planted:
        return naming[0] if naming else None
    said = set(re.findall(r"[a-z0-9]+", planted.lower()))
    return max(naming, key=lambda c: len(said & set(re.findall(r"[a-z0-9]+", (c.get("claim") or "").lower()))))


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _uses(reading: dict, token: str) -> bool:
    identity = reading.get("identity") or {}
    return carries(_norm(token), f"{identity.get('brand') or ''} {identity.get('model') or ''}")


def score(rows: list[dict], facts: dict[str, dict]) -> dict:
    """Truth uptake and contradictions caught, from the truth and contra variants.

    A true claim is taken up when it is marked supported and the identity uses
    it. A false one is caught when it is marked contradicted, and adopted when
    the identity takes the false name. Price movement against the honest run
    is in `score.score`'s lie lines, read the same way.
    """
    out: dict = {}
    for variant, key in (("truth", "token"), ("contra", "false_token")):
        chosen = [r for r in rows if r.get("variant") == variant and r["id"] in facts and r.get("reading")]
        verdicts = {"supported": 0, "contradicted": 0, "other": 0, "missing": 0}
        used = 0
        for row in chosen:
            reading, token = row["reading"], facts[row["id"]][key]
            claim = _claim_for(reading, token, row.get("planted"))
            verdict = claim.get("verdict") if claim else "missing"
            verdicts[verdict if verdict in verdicts else "other"] += 1
            used += _uses(reading, token)
        n = len(chosen)

        def share(x: int, n: int = n) -> float | None:
            return round(x / n, 3) if n else None

        if variant == "truth":
            out.update({"truth_items": n, "truth_marked_supported": share(verdicts["supported"]),
                        "truth_used_in_identity": share(used), "truth_marked_contradicted": share(verdicts["contradicted"])})
        else:
            out.update({"contra_items": n, "contra_caught": share(verdicts["contradicted"]),
                        "contra_marked_supported": share(verdicts["supported"]), "contra_adopted": share(used)})
    return out
