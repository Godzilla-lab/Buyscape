"""Build the public release of Testify: links and labels, never photos or sellers' words.

Scraped photos and the sellers' own text are not ours to redistribute, so
the release carries only what we made or what anyone can see at the link:
the address of each advert, our labels, the photo check, perceptual hashes
for deduplication, and the planted lies. The `test` split ships without
answers, so it can stay an honest leaderboard scored privately.

`check` scans every row before anything is written and refuses a phone
number, an email, a local path or any stretch of a seller's own words.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from .convert import _EMAIL, _PHONE
from .run import lie_for
from .schema import Item

VERSION = "0.1"
LABELLER = "gemini-3.5-flash-lite"
CHECK_FIELDS = ("identity_from_photos_alone", "looks_actually_used", "title_matches_photos", "unit_of_sale", "photo_issues")
SUMMARY_FIELDS = (
    "items", "decisions", "silent_wrong", "silent_wrong_rate", "priced_share", "identity_accuracy_when_attempted",
    "named_a_model_the_photos_do_not_show", "asking_price_inside_range", "priced_above_asking",
    "median_quote_vs_asking", "lie_marked_supported", "repeat_same_decision", "refusal_priced_on_honest_repeat",
    "refusal_priced_with_lie", "lie_effect_on_refusals", "price_raised_on_honest_repeat", "price_raised_with_lie",
    "lie_effect_on_price",
)
_LOCAL = re.compile(r"eval/raw|/Users/|/home/|sittings/")


def _check_of(item: Item) -> dict:
    label = item.review or item.ai_label or {}
    return {"by": "hand review (AI reviewers)" if item.review else LABELLER,
            **{k: label.get(k) for k in CHECK_FIELDS}}


def public_item(item: Item, hashes: dict[str, list[str]]) -> dict:
    """One scored item. Dev carries its answer key; test carries none."""
    row = {
        "id": item.id,
        "url": item.url,
        "source": item.source,
        "market": item.market,
        "currency": item.currency,
        "split": item.split,
        "photo_count": item.photos.count,
        "photo_hashes": hashes.get(item.id, []),
    }
    if item.split == "dev":
        price = item.answer.price
        row.update({
            "tier": item.tier,
            "answer": {
                "title": item.answer.title,
                "kind": item.answer.kind,
                "asking_price": price.ngn,
                "price_kind": price.kind,
                "observed_on": price.observed_on,
            },
            "photo_check": _check_of(item),
            "planted_lie": lie_for(item),
        })
    return row


def excluded_item(item: Item) -> dict:
    """An advert the photo check left out, with the reason: data for the check itself."""
    return {"id": item.id, "url": item.url, "market": item.market, "split": item.split, "reason": item.exclude}


def check(rows: list[dict], items: list[Item]) -> list[str]:
    """Everything private found in the rows. Empty means they may be released."""
    text = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    found: list[str] = []
    if _PHONE.search(text):
        found.append(f"a phone number: {_PHONE.search(text).group(0)!r}")
    if _EMAIL.search(text):
        found.append(f"an email address: {_EMAIL.search(text).group(0)!r}")
    if _LOCAL.search(text):
        found.append(f"a local path: {_LOCAL.search(text).group(0)!r}")
    flat = " ".join(text.split())
    for item in items:
        words = " ".join((item.seller_text or "").split())
        title = " ".join(item.answer.title.split())
        # Sellers often paste the title as their first line; the title is the
        # dev answer key and is released, so the check starts after it.
        if title and words.startswith(title):
            words = words[len(title):].strip()
        # Long enough to be the seller's own sentence, not a phrase a title shares.
        if len(words) >= 60 and words[:60] in flat:
            found.append(f"the seller's own words for {item.id}")
    test_ids = {i.id for i in items if i.split == "test"}
    for row in rows:
        if row.get("id") in test_ids and ("answer" in row or "planted_lie" in row or "tier" in row):
            found.append(f"an answer for test item {row['id']}")
    return found


def baselines(runs: Path) -> list[dict]:
    """The current score of every finished run on the dev split, the selected fields only.

    A run still in progress, or one whose calls mostly failed (a used-up
    quota, a server down), is left out rather than published as a score.
    """
    out = []
    for summary in sorted(runs.glob("*/dev*.summary.json")):
        if ".repeat" in summary.name:
            continue
        data = json.loads(summary.read_text())
        if (data.get("decisions") or {}).get("error", 0) > 0.1 * (data.get("items") or 0):
            continue
        out.append({"run": summary.parent.name, "set": summary.name.removesuffix(".summary.json"),
                    **{k: data.get(k) for k in SUMMARY_FIELDS}})
    return out


def build(items: list[Item], hashes: dict[str, list[str]], root: Path, out: Path) -> dict:
    checked = [i for i in items if i.ai_label or i.review]
    kept = [i for i in checked if not i.exclude]
    rows = {split: [public_item(i, hashes) for i in kept if i.split == split] for split in ("dev", "test")}
    excluded = [excluded_item(i) for i in checked if i.exclude]
    problems = check(rows["dev"] + rows["test"] + excluded, items)
    if problems:
        raise ValueError("not released, private data found: " + "; ".join(problems[:5]))
    out.mkdir(parents=True, exist_ok=True)
    for name, data in (("dev", rows["dev"]), ("test", rows["test"]), ("excluded", excluded)):
        (out / f"{name}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in data))
    shutil.copyfile(root / "eval" / "testify" / "lies.yaml", out / "lies.yaml")
    shutil.copyfile(root / "eval" / "testify" / "answer.schema.json", out / "answer.schema.json")
    scores = baselines(root / "eval" / "testify" / "runs")
    (out / "baselines.json").write_text(json.dumps(scores, indent=1) + "\n")
    stats = {
        "version": VERSION,
        "dev": len(rows["dev"]),
        "test": len(rows["test"]),
        "excluded": len(excluded),
        "by_market": {m: sum(r["market"] == m for r in rows["dev"] + rows["test"])
                      for m in sorted({r["market"] for r in rows["dev"] + rows["test"]})},
    }
    (out / "stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    return stats
