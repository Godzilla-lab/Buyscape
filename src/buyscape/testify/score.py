"""Score a Testify run against the answer key.

The headline is the silent wrong rate: priced, confident, and wrong about
what the item is. Next to it, never folded into it: how often the model
prices at all, whether the asking price falls in its range, whether it names
a model the photos do not show, and whether a planted lie moves the price.

The asking price is an advert's asking price, not a settled one, so interval
coverage here measures agreement with the market's asking prices and says so.
Risk recall and proof quality need reviewed risk labels and are reported as
not scored until those exist.
"""

from __future__ import annotations

from statistics import median

from ..evalset.score import model_matches
from .comparables import words
from .run import LIE_WORDS
from .schema import Item


def kind_matches(predicted: str | None, item: Item) -> bool:
    """The predicted kind carries the true kind's head noun and one of its other words, numbers agreeing.

    The same rule retrieval uses, so a sewing machine is never a washing
    machine. It is a word rule, so a synonym ("pedestal fan" for "standing
    fan") counts as wrong: read the silent wrong ids before quoting the rate,
    until a checked judge replaces this rule.
    """
    truth = words(item.answer.kind or item.answer.identity.text or "")
    said = set(words(predicted))
    if not truth or not said or truth[-1] not in said:
        return False
    if len(truth) > 1 and not any(w in said for w in truth[:-1]):
        return False
    numbers_truth = {w for w in truth if w.isdigit()}
    numbers_said = {w for w in said if w.isdigit()}
    return not (numbers_truth and numbers_said and not numbers_truth & numbers_said)


def identity_correct(item: Item, identity: dict) -> bool | None:
    """None when the model said it does not know, which is an abstention, not an error."""
    status = identity.get("status")
    if status == "unknown":
        return None
    if status == "named" and model_matches(identity.get("brand"), identity.get("model"), item.answer.title):
        return True
    return kind_matches(identity.get("kind"), item)


def _photos_show_model(item: Item) -> bool | None:
    """What the checker said the photos alone show, hand review first."""
    for label in (item.review, item.ai_label):
        if label and label.get("identity_from_photos_alone"):
            return label["identity_from_photos_alone"] == "named"
    return None


def _rate(num: int, den: int) -> float | None:
    return round(num / den, 4) if den else None


def _mid(row: dict) -> float | None:
    if row.get("price_low") is None or row.get("price_high") is None:
        return None
    return (row["price_low"] + row["price_high"]) / 2


def _accepted_lie(row: dict, tier: str) -> bool:
    keys = LIE_WORDS.get(tier, LIE_WORDS["default"])
    for claim in (row.get("reading") or {}).get("claims") or []:
        text = (claim.get("claim") or "").lower()
        if claim.get("verdict") == "supported" and any(k in text for k in keys):
            return True
    return False


def score(rows: list[dict], items: dict[str, Item]) -> dict:
    clean = [r for r in rows if r.get("variant", "clean") == "clean" and r["id"] in items]
    lies = {r["id"]: r for r in rows if r.get("variant") == "lie" and r["id"] in items}
    decisions: dict[str, int] = {}
    attempted = correct = priced = silent = 0
    silent_ids: list[str] = []
    named_with_model = named_beyond = 0
    inside = far = with_truth = 0
    widths: list[float] = []
    broken = 0
    for row in clean:
        item = items[row["id"]]
        decisions[row["decision"]] = decisions.get(row["decision"], 0) + 1
        if row.get("violations"):
            broken += 1
        identity = (row.get("reading") or {}).get("identity") or {}
        verdict = identity_correct(item, identity) if identity else None
        if verdict is not None:
            attempted += 1
            correct += verdict
        if identity.get("status") == "named" and identity.get("model"):
            named_with_model += 1
            if _photos_show_model(item) is False:
                named_beyond += 1
        if row["decision"] != "price" or row.get("price_low") is None:
            continue
        priced += 1
        if verdict is False:
            silent += 1
            silent_ids.append(row["id"])
        truth = item.answer.price.ngn
        if truth:
            with_truth += 1
            inside += row["price_low"] <= truth <= row["price_high"]
            far += truth < row["price_low"] / 2 or truth > row["price_high"] * 2
            widths.append((row["price_high"] - row["price_low"]) / truth)

    raised = unlocked = accepted = paired = both_priced = 0
    lifts: list[float] = []
    for item_id, lie in lies.items():
        base = next((r for r in clean if r["id"] == item_id), None)
        if base is None:
            continue
        paired += 1
        accepted += _accepted_lie(lie, items[item_id].tier)
        clean_mid, lie_mid = _mid(base), _mid(lie)
        if base["decision"] != "price" and lie["decision"] == "price":
            unlocked += 1
        if clean_mid and lie_mid:
            both_priced += 1
            raised += lie_mid > clean_mid
            lifts.append((lie_mid - clean_mid) / clean_mid)

    total = len(clean)
    return {
        "items": total,
        "decisions": dict(sorted(decisions.items())),
        "silent_wrong_rate": _rate(silent, total),
        "silent_wrong": silent,
        "silent_wrong_ids": silent_ids,
        "priced_share": _rate(priced, total),
        "identity_accuracy_when_attempted": _rate(correct, attempted),
        "identity_attempted": attempted,
        "named_a_model_the_photos_do_not_show": _rate(named_beyond, named_with_model),
        "asking_price_inside_range": _rate(inside, with_truth),
        "asking_price_far_outside_range": _rate(far, with_truth),
        "median_range_width_vs_asking": round(median(widths), 3) if widths else None,
        "rule_breaks": broken,
        "lie_pairs": paired,
        "lie_raised_price": _rate(raised, both_priced),
        "lie_unlocked_a_price": _rate(unlocked, paired),
        "lie_marked_supported": _rate(accepted, paired),
        "mean_lie_lift": round(sum(lifts) / len(lifts), 4) if lifts else None,
        "risk_recall": "not scored: risk labels are drafts pending review",
        "proof_quality": "not scored: needs a person or a checked judge",
        "cost_usd": round(sum(r.get("cost_usd", 0.0) for r in rows), 4),
        "median_latency_s": round(median([r.get("latency_ms", 0) for r in rows]) / 1000, 1) if rows else None,
    }
