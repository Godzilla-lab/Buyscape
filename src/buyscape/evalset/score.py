"""Score a run against the answer key and print the Phase 0 gate.

The gate exists because the previous attempts at this product failed on silent
wrong answers, not on missing features. So the metric that matters most is the
silent-wrong rate: confident, wrong, and not flagged.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import re

from ..identify.catalogue import tokens
from ..runner import Case, CaseResult


_SPLIT_UNITS = re.compile(r"(\d+)\s*(gb|tb|mb|kva|kg|hp|kw|w)\b", re.I)


def _norm(text: str | None) -> set[str]:
    """Tokenise, splitting a number from its unit so 512gb equals 512 gb."""
    normalised = _SPLIT_UNITS.sub(r"\1 \2", (text or "").lower())
    return set(tokens(normalised))


def brand_matches(predicted: str | None, truth_title: str) -> bool:
    p = _norm(predicted)
    return bool(p) and p.issubset(_norm(truth_title))


def model_matches(brand: str | None, model: str | None, truth_title: str) -> bool:
    """Did the engine name the same product the seller was listing?

    A listing title is a seller's shorthand, not a spec sheet, so extra detail
    the engine read off the item is not an error: "Senci SC30000" against a
    title of "Senci Petrol Generator 20kva" is a plate code the title never
    carried. What is an error is contradicting the title, and numbers are where
    that shows, because an iPhone 14 priced as an iPhone 13 costs real money.

    So the rule is: the answer must share a word with the title, and where both
    carry numbers at least one must agree. Detail the title simply omits passes.
    """
    predicted = _norm(brand) | _norm(model)
    if not predicted:
        return False
    truth = _norm(truth_title)

    pred_numbers = {t for t in predicted if any(c.isdigit() for c in t)}
    truth_numbers = {t for t in truth if any(c.isdigit() for c in t)}
    pred_words = predicted - pred_numbers
    truth_words = truth - truth_numbers

    # Naming a different product entirely.
    if not (pred_words & truth_words):
        return False
    # Both sides quote numbers and none agree: a wrong generation or capacity.
    if pred_numbers and truth_numbers and not (pred_numbers & truth_numbers):
        return False
    return True


@dataclass
class Metrics:
    total: int = 0
    category_scored: int = 0
    category_correct: int = 0
    id_attempted: int = 0
    id_correct: int = 0
    id_wrong: int = 0
    brand_correct: int = 0
    abstained: int = 0
    with_label: int = 0
    with_label_correct: int = 0
    with_label_attempted: int = 0
    silent_wrong: int = 0
    priced: int = 0
    price_failures: int = 0
    ask_within_range: int = 0
    ask_scored: int = 0
    widths: list[float] = field(default_factory=list)
    cost_usd: float = 0.0
    latency_ms: int = 0
    failures: dict[str, int] = field(default_factory=dict)

    def rate(self, num: int, den: int) -> float | None:
        return round(num / den, 4) if den else None

    def summary(self) -> dict:
        widths = sorted(self.widths)
        median_width = widths[len(widths) // 2] if widths else None
        return {
            "cases": self.total,
            "category_accuracy": self.rate(self.category_correct, self.category_scored),
            "model_top1_accuracy_with_label": self.rate(
                self.with_label_correct, self.with_label_attempted
            ),
            "model_top1_accuracy_all_attempts": self.rate(self.id_correct, self.id_attempted),
            "brand_accuracy_when_answered": self.rate(self.brand_correct, self.id_attempted),
            "abstention_rate": self.rate(self.abstained, self.total),
            "silent_wrong_rate": self.rate(self.silent_wrong, self.total),
            "priced": self.priced,
            "price_failures": self.price_failures,
            "asking_price_at_or_above_range": self.rate(self.ask_within_range, self.ask_scored),
            "median_range_width": median_width,
            "cost_per_case_usd": round(self.cost_usd / self.total, 5) if self.total else None,
            "latency_per_case_ms": round(self.latency_ms / self.total) if self.total else None,
            "failure_codes": self.failures,
        }


GATE = {
    "category_accuracy": 0.90,
    "model_top1_accuracy_with_label": 0.80,
    "silent_wrong_rate": 0.05,
    "asking_price_at_or_above_range": 0.80,
}


def score(pairs: list[tuple[Case, CaseResult]]) -> Metrics:
    m = Metrics()
    for case, result in pairs:
        m.total += 1
        m.cost_usd += result.cost_usd
        m.latency_ms += result.latency_ms
        truth = case.truth
        title = str(truth.get("title", ""))

        # One case yields at most one failure code: the chain's if it stopped
        # there, otherwise the quote's. Counting both double-counts the case.
        case_failure = result.chain.failure_code or result.quote.failure_code
        if case_failure:
            m.failures[case_failure] = m.failures.get(case_failure, 0) + 1

        true_category = truth.get("category")
        if true_category and result.chain.category:
            m.category_scored += 1
            predicted = result.chain.category.lower().replace(" ", "_")
            expected = str(true_category).lower()
            aliases = {
                "phone": {"phone", "mobile_phone", "smartphone", "mobile"},
                "generator": {"generator", "petrol_generator", "diesel_generator", "generator_set"},
                "split_ac": {"split_ac", "air_conditioner", "split_air_conditioner", "ac", "aircon"},
                "washing_machine": {"washing_machine", "washer", "washing_machine_dryer"},
            }
            if predicted in aliases.get(expected, {expected}) or expected in predicted:
                m.category_correct += 1

        used_label = result.chain.used_label
        if used_label:
            m.with_label += 1

        if result.identified:
            m.id_attempted += 1
            if brand_matches(result.chain.brand, title):
                m.brand_correct += 1
            correct = model_matches(result.chain.brand, result.chain.model, title)
            if correct:
                m.id_correct += 1
            else:
                m.id_wrong += 1
                m.silent_wrong += 1  # confident, wrong, unflagged
            if used_label:
                m.with_label_attempted += 1
                if correct:
                    m.with_label_correct += 1
        else:
            m.abstained += 1

        q = result.quote
        if q.is_failure:
            m.price_failures += 1
        elif q.low is not None and q.high is not None:
            m.priced += 1
            if q.width_ratio is not None:
                m.widths.append(q.width_ratio)
            ask = truth.get("price_ngn")
            # A buyback pays below the asking price, so a sound range sits at or
            # below what the seller is asking. Above it means we would overpay.
            if ask and truth.get("is_used"):
                m.ask_scored += 1
                if q.high <= float(ask):
                    m.ask_within_range += 1
    return m


def gate_table(summary: dict) -> list[tuple[str, str, str, bool | None]]:
    rows: list[tuple[str, str, str, bool | None]] = []
    for key, threshold in GATE.items():
        value = summary.get(key)
        if value is None:
            rows.append((key, "no data", f"{threshold}", None))
            continue
        passed = value <= threshold if "wrong" in key else value >= threshold
        comparator = "<=" if "wrong" in key else ">="
        rows.append((key, f"{value}", f"{comparator} {threshold}", passed))
    return rows


def write_summary(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2))
