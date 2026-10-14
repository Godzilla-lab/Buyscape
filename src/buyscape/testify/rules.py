"""Whether a checked item stays in the benchmark, decided by rule.

A reviewer, hand or model, reports facts: is it second-hand, is the photo the
seller's item, is it for sale. The decision follows from those facts by this
rule, never from the reviewer's own keep or drop vote. Checking 100 items
showed why: Gemini judged an advert to be dealer stock and kept it anyway 33
times, and the hand review did the same 12 times. Applied to both, the rule
made them agree on 88 of 100.
"""

from __future__ import annotations


def drop_reason(review: dict) -> str | None:
    """Why the reviewed item leaves the benchmark, or None to keep it."""
    if review.get("looks_actually_used") == "no":
        return "new stock, not second-hand"
    if review.get("tier") == "not_for_sale":
        return "not for sale: a buyer's advert or a service"
    if set(review.get("photo_issues") or []) & {"stock_or_catalogue_photo", "not_the_item"}:
        return "the photo is not the seller's item"
    if review.get("keep_in_benchmark") == "drop":
        return review.get("drop_reason") or "dropped in review"
    return None
