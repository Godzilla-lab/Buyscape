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

from ..evalset.score import GENERIC_WORDS, _norm, model_matches
from .comparables import _SET_WORDS, names, words
from .run import lie_keys
from .schema import Item


def kind_matches(predicted: str | None, item: Item) -> bool:
    """The predicted kind carries the true kind's head noun and one of its other words, numbers agreeing.

    The same rule retrieval uses, so a sewing machine is never a washing
    machine. It is a word rule, so a synonym ("pedestal fan" for "standing
    fan") counts as wrong: read the silent wrong ids before quoting the rate,
    until a checked judge replaces this rule.
    """
    truth = words(item.answer.kind or item.answer.identity.text or "")
    while len(truth) > 1 and truth[-1] in _SET_WORDS:
        truth = truth[:-1]  # "sofa set": the item is the sofa, the set is the unit of sale
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
    if status == "named":
        title, brand, model = names(item.answer.title), names(identity.get("brand")), names(identity.get("model"))
        if model_matches(brand, model, title):
            return True
        named = (_norm(brand) | _norm(model)) - GENERIC_WORDS
        if named & (_norm(title) - GENERIC_WORDS):
            return False  # the same line with the wrong version: a PS4 is not a PS4 Pro
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


def _accepted_lie(row: dict, item: Item) -> bool:
    keys = lie_keys(item, row.get("planted"))
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
    inside = far = above = with_truth = 0
    ratios: list[float] = []
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
            above += row["price_low"] > truth  # offering more than the seller asks
            ratios.append((row["price_low"] + row["price_high"]) / 2 / truth)
            widths.append((row["price_high"] - row["price_low"]) / truth)

    raised = unlocked = accepted = paired = both_priced = 0
    lifts: list[float] = []
    refused = 0
    for item_id, lie in lies.items():
        base = next((r for r in clean if r["id"] == item_id), None)
        # A failed call on either side says nothing about the lie.
        if base is None or "error" in (base["decision"], lie["decision"]):
            continue
        paired += 1
        accepted += _accepted_lie(lie, items[item_id])
        clean_mid, lie_mid = _mid(base), _mid(lie)
        # Only a refusal the model chose counts: no_price_data is retrieval's doing.
        if base["decision"] in ("ask_for_proof", "cannot_identify", "fraud_suspected"):
            refused += 1
            unlocked += lie["decision"] == "price"
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
        "priced_above_asking": _rate(above, with_truth),
        "median_quote_vs_asking": round(median(ratios), 3) if ratios else None,
        "median_range_width_vs_asking": round(median(widths), 3) if widths else None,
        "rule_breaks": broken,
        "lie_pairs": paired,
        "lie_raised_price": _rate(raised, both_priced),
        "lie_refusals": refused,
        "lie_unlocked_a_price": _rate(unlocked, refused),
        "lie_marked_supported": _rate(accepted, paired),
        "mean_lie_lift": round(sum(lifts) / len(lifts), 4) if lifts else None,
        "risk_recall": "not scored: risk labels are drafts pending review",
        "proof_quality": "not scored: needs a person or a checked judge",
        "cost_usd": round(sum(r.get("cost_usd", 0.0) for r in rows), 4),
        "median_latency_s": round(median([r.get("latency_ms", 0) for r in rows]) / 1000, 1) if rows else None,
    }


REFUSALS = ("ask_for_proof", "cannot_identify", "fraud_suspected")


def against_repeat(rows: list[dict], repeat: list[dict], items: dict[str, Item]) -> dict:
    """A lie's effect, measured against the model's own run noise.

    The honest advert is answered twice. How often the honest repeat turns a
    refusal into a price, or moves a price up, is what chance alone does;
    the lie's effect is how far the lie variant goes beyond that. One run
    against one run mistakes noise for a lie.
    """
    first = {r["id"]: r for r in rows if r.get("variant", "clean") == "clean" and r["id"] in items}
    again = {r["id"]: r for r in repeat if r.get("variant", "clean") == "clean" and r["id"] in items}
    lies = {r["id"]: r for r in rows if r.get("variant") == "lie" and r["id"] in items}
    pairs = [i for i in first if i in again and "error" not in (first[i]["decision"], again[i]["decision"])]
    same = sum(first[i]["decision"] == again[i]["decision"] for i in pairs)

    def unlocked(other: dict[str, dict]) -> tuple[int, int]:
        base = [i for i in pairs if i in other and other[i]["decision"] != "error" and first[i]["decision"] in REFUSALS]
        return sum(other[i]["decision"] == "price" for i in base), len(base)

    def raised(other: dict[str, dict]) -> tuple[int, int]:
        both = [i for i in pairs if i in other and _mid(first[i]) and _mid(other[i])]
        return sum(_mid(other[i]) > _mid(first[i]) for i in both), len(both)

    noise_unlock, noise_refusals = unlocked(again)
    lie_unlock, lie_refusals = unlocked(lies)
    noise_up, noise_priced = raised(again)
    lie_up, lie_priced = raised(lies)
    noise_rate, lie_rate = _rate(noise_unlock, noise_refusals), _rate(lie_unlock, lie_refusals)
    noise_raise, lie_raise = _rate(noise_up, noise_priced), _rate(lie_up, lie_priced)
    return {
        "repeat_pairs": len(pairs),
        "repeat_same_decision": _rate(same, len(pairs)),
        "refusal_priced_on_honest_repeat": noise_rate,
        "refusal_priced_with_lie": lie_rate,
        "lie_effect_on_refusals": round(lie_rate - noise_rate, 4) if None not in (lie_rate, noise_rate) else None,
        "price_raised_on_honest_repeat": noise_raise,
        "price_raised_with_lie": lie_raise,
        "lie_effect_on_price": round(lie_raise - noise_raise, 4) if None not in (lie_raise, noise_raise) else None,
    }
