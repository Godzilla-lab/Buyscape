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

import yaml

from ..identify.catalogue import tokens
from ..runner import Case, CaseResult


@dataclass
class Verdicts:
    """Decisions a person made by looking at the photos.

    The listing title is the answer key, and outside phones it lies: sellers
    title a generator by an inflated kVA while the plate reads otherwise. An
    adjudication says what the plate actually showed and outranks the title.
    The must-abstain set is ten cases nobody could identify from the photos,
    and the engine must abstain on every one of them, every run.
    """

    adjudicated: dict[str, str] = field(default_factory=dict)  # case id -> correct | wrong
    # What the plate actually reads, where the adjudicator could say. An
    # answer is then judged against this rather than by a fixed verdict, so
    # a case once answered wrongly and later answered rightly scores rightly.
    truths: dict[str, str] = field(default_factory=dict)
    must_abstain: set[str] = field(default_factory=set)


def load_verdicts(eval_dir: Path) -> Verdicts:
    """Read eval/adjudications.yaml and eval/must_abstain.yaml if they exist."""
    verdicts = Verdicts()
    adjudications = eval_dir / "adjudications.yaml"
    if adjudications.exists():
        for row in yaml.safe_load(adjudications.read_text()) or []:
            verdict = str(row["verdict"]).lower()
            if verdict not in ("correct", "wrong"):
                raise ValueError(f"adjudication for {row['id']} must be correct or wrong, not {verdict!r}")
            verdicts.adjudicated[str(row["id"])] = verdict
            if row.get("truth"):
                verdicts.truths[str(row["id"])] = str(row["truth"])
    must_abstain = eval_dir / "must_abstain.yaml"
    if must_abstain.exists():
        for row in yaml.safe_load(must_abstain.read_text()) or []:
            verdicts.must_abstain.add(str(row["id"]))
    return verdicts


_SPLIT_UNITS = re.compile(r"(\d+)\s*(gb|tb|mb|kva|kg|hp|kw|w)\b", re.I)


# Words that make a different product at a different price: an iPhone 13 Pro
# Max is not an iPhone 13. Titles carry these reliably, so a mismatch is real.
TIER_WORDS = {"pro", "max", "plus", "ultra", "mini", "lite", "fe", "neo", "prime", "air"}

# Words that say what kind of thing this is and how big it is, never which
# product it is. A match has to rest on a name or a plate code: two adverts
# that share only "hp" and a capacity, or only "top" and "loader", are not the
# same product, and letting those words carry a match scored a wrong brand as
# the right answer.
GENERIC_WORDS = {
    # units
    "hp", "kva", "kw", "kwh", "kg", "gb", "tb", "mb", "w", "v", "hz",
    "inch", "inches", "litre", "litres", "liter", "liters", "l", "ml",
    # form factor
    "top", "front", "loader", "loading", "load", "tub", "twin", "split",
    "inverter", "automatic", "manual", "portable", "standing", "window",
    # category nouns
    "generator", "generators", "gen", "genset", "machine", "machines",
    "washing", "washer", "dryer", "conditioner", "conditioners", "air",
    "ac", "laptop", "laptops", "notebook", "computer", "phone", "phones",
    "smartphone", "unit", "units", "set", "series",
    # fuel and material
    "petrol", "diesel", "gasoline", "solar", "copper", "coil", "wire",
    "gas", "electric",
}


# "Air Conditioner" names a category, not a tier. Without this, the tier rule
# below fires on every split AC listing in the set and scores them all wrong.
_CATEGORY_PHRASE = re.compile(r"\bair[ -]?condition(?:er|ers|ing)?\b", re.I)

_DECIMAL = re.compile(r"(\d)\.(\d)")
_LETTER_PREFIX = re.compile(r"^[a-z]+(?=\d)")
_LETTER_SUFFIX = re.compile(r"^(\d+)[a-z]+$")


def _norm(text: str | None) -> set[str]:
    """Tokenise so the same number written two ways still meets.

    512gb equals 512 gb; 4.5kva stays one number rather than a 4 and a 5;
    KM5000i also answers to 5000i, because a plate code and a seller's
    shorthand differ by exactly that prefix.
    """
    lowered = _CATEGORY_PHRASE.sub(" ", (text or "").lower()).replace("+", " plus ")
    # CL7800E-2R is CL7800E2R, but XT-LITE is also XT Lite: keep both forms.
    lowered = lowered + " " + re.sub(r"(?<=[a-z0-9])-(?=[a-z0-9])", "", lowered)
    lowered = _DECIMAL.sub(r"\1\2", lowered)
    normalised = _SPLIT_UNITS.sub(r"\1 \2", lowered)
    out = set(tokens(normalised))
    for t in list(out):
        stripped = _LETTER_PREFIX.sub("", t)
        if stripped != t:
            out.add(stripped)
        digits = _LETTER_SUFFIX.match(stripped)
        if digits:
            out.add(digits.group(1))  # 350a and 5000i both answer to their number
    return out


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

    # Naming a different product entirely. Units are stripped from this test
    # so that a shared "hp" or "kg" cannot stand in for a shared identity.
    if not ((pred_words - GENERIC_WORDS) & (truth_words - GENERIC_WORDS)):
        return False
    # Both sides quote numbers and none agree: a wrong generation or capacity.
    if pred_numbers and truth_numbers and not (pred_numbers & truth_numbers):
        return False
    # Pro, Max, Plus, Ultra: same generation, different product, different price.
    if (pred_words & TIER_WORDS) != (truth_words & TIER_WORDS):
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
    # Which cases, so a change can be judged case by case, not by the rate.
    silent_wrong_ids: list[str] = field(default_factory=list)
    adjudicated: int = 0
    must_abstain_listed: int = 0
    must_abstain_held: int = 0
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
            "silent_wrong_cases": list(self.silent_wrong_ids),
            "adjudicated": self.adjudicated,
            "must_abstain_held": self.rate(self.must_abstain_held, self.must_abstain_listed),
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
    # Every hand-picked unidentifiable case must come back as an abstention.
    "must_abstain_held": 1.0,
}


def score(pairs: list[tuple[Case, CaseResult]], verdicts: Verdicts | None = None) -> Metrics:
    m = Metrics()
    verdicts = verdicts or Verdicts()
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
                "laptop": {"laptop", "notebook", "macbook", "laptop_computer"},
            }
            if predicted in aliases.get(expected, {expected}) or expected in predicted:
                m.category_correct += 1

        used_label = result.chain.used_label
        if used_label:
            m.with_label += 1

        if case.id in verdicts.must_abstain:
            m.must_abstain_listed += 1
            # A provider error is not an abstention: nothing was decided.
            if not result.identified and case_failure not in ("PROVIDER_ERROR", "NO_FIXTURE"):
                m.must_abstain_held += 1

        if result.identified:
            m.id_attempted += 1
            if brand_matches(result.chain.brand, title):
                m.brand_correct += 1
            # The variant is part of the answer: 'Galaxy S23' with variant
            # 'Ultra' is an S23 Ultra, and is priced as one.
            answered = " ".join(filter(None, [result.chain.model, result.chain.variant]))
            if result.chain.named_type:
                # The answer is a kind of thing, '2 seater sofa', and the
                # title is held to the same rule: a shared word, and where
                # both carry a number the numbers must agree.
                answered = result.chain.type_name or ""
            correct = model_matches(result.chain.brand, answered, title)
            verdict = verdicts.adjudicated.get(case.id)
            if case.id in verdicts.truths:
                # A person read the plate and wrote down what it says. The
                # answer is held to that, by the same rule as a title.
                correct = model_matches(result.chain.brand, answered, verdicts.truths[case.id])
                m.adjudicated += 1
            elif verdict:
                # A person looked at the plate. Their word beats the title.
                correct = verdict == "correct"
                m.adjudicated += 1
            if correct:
                m.id_correct += 1
            else:
                m.id_wrong += 1
                m.silent_wrong += 1  # confident, wrong, unflagged
                m.silent_wrong_ids.append(case.id)
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
