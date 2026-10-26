"""Honest numbers: paired intervals, and one coverage curve instead of two columns.

Every model sits the same items, so a difference between two models is
measured by resampling items, not answers: each resample draws the same items
for every model (a paired bootstrap). A difference whose interval crosses
zero is a tie, however the point estimates rank.

"Priced 40% with 3 wrong" and "priced 19% with 2 wrong" cannot be read side
by side. LLP (arXiv 2510.09347) reports adoption at matched coverage instead.
Here each model's priced answers are ordered by a structural confidence and
cut at the same coverage for every model: the silent-wrong rate among the
answers kept is read at 10%, 20% and 40% of all items. The confidence is
never the model's own word: it is whether two honest runs agreed, how many
comparables there were, and how tight they sat.
"""

from __future__ import annotations

import random
from collections.abc import Callable

from .schema import Item
from .score import identity_correct, outcome

COVERAGES = (0.1, 0.2, 0.4)


def per_item(rows: list[dict], items: dict[str, Item], repeat: list[dict] | None = None) -> dict[str, dict]:
    """What each honest answer was: priced, silently wrong, named right, and how sure the structure is."""
    again = {r["id"]: r for r in repeat or [] if r.get("variant", "clean") == "clean"}
    out: dict[str, dict] = {}
    for row in rows:
        if row.get("variant", "clean") != "clean" or row["id"] not in items:
            continue
        identity = (row.get("reading") or {}).get("identity") or {}
        verdict = identity_correct(items[row["id"]], identity) if identity else None
        priced = row["decision"] == "price" and row.get("price_low") is not None
        out[row["id"]] = {
            "priced": priced,
            "silent": priced and verdict is False,
            "attempted": verdict is not None,
            "correct": verdict is True,
            "error": outcome(row) in ("error", "broke_schema"),
            "confidence": confidence(row, again.get(row["id"])),
        }
    return out


def confidence(row: dict, repeat: dict | None) -> tuple:
    """A sort key, highest first: the honest repeat agreed, then more comparables, then a tighter spread."""
    agreed = repeat is not None and repeat["decision"] == row["decision"] and _same_name(row, repeat)
    found = [c["price_ngn"] for c in row.get("comparables") or []]
    spread = max(found) / min(found) if found and min(found) > 0 else float("inf")
    return (agreed, min(len(found), 12), -spread)


def _same_name(a: dict, b: dict) -> bool:
    def name(row: dict) -> tuple:
        identity = (row.get("reading") or {}).get("identity") or {}
        return tuple((identity.get(k) or "").lower() for k in ("brand", "model", "kind"))
    return name(a) == name(b)


def silent_at(answers: dict[str, dict], ids: list[str], coverage: float) -> float | None:
    """Silent wrongs among the most confident priced answers that cover this share of the items.

    None when the model priced fewer items than that: its curve ends sooner."""
    k = round(coverage * len(ids))
    priced = sorted((i for i in ids if answers[i]["priced"]), key=lambda i: answers[i]["confidence"], reverse=True)
    if k == 0 or len(priced) < k:
        return None
    return sum(answers[i]["silent"] for i in priced[:k]) / k


def area(answers: dict[str, dict], ids: list[str], up_to: float) -> float | None:
    """Mean silent-wrong rate over every coverage from one item up to `up_to`: the area under the curve."""
    points = [silent_at(answers, ids, k / len(ids)) for k in range(1, round(up_to * len(ids)) + 1)]
    points = [p for p in points if p is not None]
    return sum(points) / len(points) if points else None


STATS: dict[str, Callable[[dict[str, dict], list[str]], float | None]] = {
    "priced_share": lambda a, ids: sum(a[i]["priced"] for i in ids) / len(ids),
    "silent_wrong_rate": lambda a, ids: sum(a[i]["silent"] for i in ids) / len(ids),
    "identity_accuracy": lambda a, ids: (sum(a[i]["correct"] for i in ids) / n
                                         if (n := sum(a[i]["attempted"] for i in ids)) else None),
    **{f"silent_at_{round(c * 100)}pct": (lambda a, ids, c=c: silent_at(a, ids, c)) for c in COVERAGES},
}


def paired_bootstrap(models: dict[str, dict[str, dict]], n: int = 2000, seed: int = 0, level: float = 0.95) -> dict:
    """Each statistic for each model, and each pair's difference, with intervals from paired resamples.

    Only items every model answered are used, so each model is measured on the same items."""
    shared = sorted(set.intersection(*(set(a) for a in models.values()))) if models else []
    rng = random.Random(seed)
    draws = [[rng.choice(shared) for _ in shared] for _ in range(n)] if shared else []
    # The area is read up to the coverage every pricing model reaches. A model
    # that prices nothing has no curve and does not shorten the others'.
    reached = [sum(a[i]["priced"] for i in shared) / len(shared) for a in models.values()]
    common = min((r for r in reached if r > 0), default=0.0)
    stats = {**STATS, "silent_area": lambda a, ids: area(a, ids, common)}
    lo_q, hi_q = (1 - level) / 2, 1 - (1 - level) / 2

    def interval(values: list[float]) -> tuple[float, float] | None:
        values = sorted(v for v in values if v is not None)
        if not values:
            return None
        return round(values[int(lo_q * (len(values) - 1))], 4), round(values[int(hi_q * (len(values) - 1))], 4)

    out: dict = {"items": len(shared), "resamples": n, "common_coverage": round(common, 4), "models": {}, "pairs": {}}
    for name, answers in models.items():
        out["models"][name] = {
            stat: {"point": _round(fn(answers, shared)), "interval": interval([fn(answers, d) for d in draws])}
            for stat, fn in stats.items()
        }
    names = list(models)
    for x, a in enumerate(names):
        for b in names[x + 1:]:
            pair = {}
            for stat, fn in stats.items():
                point_a, point_b = fn(models[a], shared), fn(models[b], shared)
                diffs = []
                for d in draws:
                    va, vb = fn(models[a], d), fn(models[b], d)
                    diffs.append(None if va is None or vb is None else va - vb)
                ci = interval(diffs)
                pair[stat] = {
                    "difference": _round(None if point_a is None or point_b is None else point_a - point_b),
                    "interval": ci,
                    "tie": ci is None or ci[0] <= 0 <= ci[1],
                }
            out["pairs"][f"{a} - {b}"] = pair
    return out


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 4)
