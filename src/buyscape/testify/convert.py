"""Turn what is already on disk into Testify items, for nothing.

Two sources. The Jiji set's raw cache is gitignored and may be missing, so
those items are rebuilt from the case reports in docs/proof, which carry the
answer key, the claims the engine pulled from the seller's text, and each
model pair's verdict. BuyScrap items come from the cached adverts when they
exist, which also carry the seller's own words.

The listing title stays in the answer and never in the inputs.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import yaml

from ..evalset import buyscrap
from . import fetch as wider
from .rules import drop_reason
from ..protocols.schema import Protocol, load_protocols
from .schema import (
    WANTED,
    Answer,
    Baseline,
    Identity,
    Item,
    Photos,
    PriceTruth,
    RiskSeed,
    split_for,
    tier_for,
)

_ANSWER_KEY = re.compile(r"^## Answer key \(not shown to the engine\)\n`(\{.*\})`", re.M)
_PHOTOS = re.compile(r"^Photos: (\d+)", re.M)
_ANSWERED = re.compile(r"^\*\*Answer: (.+?)\*\*", re.M)
_NOT_IDENTIFIED = re.compile(r"^\*\*Not identified: ([A-Z_]+)\.\*\*", re.M)
_PRICE_FAIL = re.compile(r"^## Price\n\*\*([A-Z_]+)\.\*\*", re.M)
_RANGE = re.compile(r"^\*\*([\d,]+) to ([\d,]+) [A-Z]{3}\*\* \(([^,]+),", re.M)
_CLAIM = re.compile(r"^- \[[a-z_]+\] (.+)$")
_REQUIRED = "Required evidence"
# Contact details are the seller's, not the benchmark's, and are never released.
_PHONE = re.compile(r"(?<!\d)(?:\+?234[\s-]?|0)[789][01](?:[\s-]?\d){8}(?!\d)")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def redact(text: str | None) -> str | None:
    if text is None:
        return None
    return _EMAIL.sub("[email]", _PHONE.sub("[phone]", text))




def _claims(report: str) -> list[str]:
    """The seller's statements, without the engine's own missing-shot notes."""
    section = report.split("## Claims", 1)[-1].split("\n## ", 1)[0]
    out = []
    for line in section.splitlines():
        match = _CLAIM.match(line)
        if match and not match.group(1).startswith(_REQUIRED):
            out.append(match.group(1).strip())
    return out


def baseline_from_report(report: str, rel: str) -> Baseline:
    fail = _NOT_IDENTIFIED.search(report)
    price_fail = _PRICE_FAIL.search(report)
    rng = _RANGE.search(report)
    if fail:
        code = fail.group(1)
        decision = {
            "CANNOT_IDENTIFY": "cannot_identify",
            "FRAUD_SUSPECTED": "fraud_suspected",
            "EVIDENCE_INCOMPLETE": "ask_for_proof",
        }.get(code, "cannot_identify")
    elif price_fail:
        code = price_fail.group(1)
        decision = "fraud_suspected" if code == "FRAUD_SUSPECTED" else "no_price_data"
    else:
        code, decision = None, "price"
    answered = _ANSWERED.search(report)
    return Baseline(
        decision=decision,
        failure_code=code,
        answer=answered.group(1) if answered else None,
        price_low=int(rng.group(1).replace(",", "")) if rng else None,
        price_high=int(rng.group(2).replace(",", "")) if rng else None,
        basis=rng.group(3).strip() if rng else None,
        report=rel,
    )


def risk_seeds(protocol: Protocol) -> list[RiskSeed]:
    """Each protocol claim is a hidden risk, its evidence shots the proof."""
    asks = {shot.id: shot.ask for shot in protocol.shots}
    return [
        RiskSeed(
            risk=claim.id,
            proof=[asks[s] for s in claim.evidence_slots if s in asks],
            worst_case=claim.worst_case,
            pickup_check=claim.pickup_check,
            source=f"protocol:{protocol.category} v{protocol.version}",
        )
        for claim in protocol.claims
    ]


def _verdicts(eval_dir: Path) -> tuple[dict[str, str], set[str]]:
    truths: dict[str, str] = {}
    path = eval_dir / "adjudications.yaml"
    for row in (yaml.safe_load(path.read_text()) if path.exists() else None) or []:
        if row.get("truth"):
            truths[str(row["id"])] = str(row["truth"])
        elif row.get("verdict") == "wrong":
            truths[str(row["id"])] = ""
    must: set[str] = set()
    path = eval_dir / "must_abstain.yaml"
    for row in (yaml.safe_load(path.read_text()) if path.exists() else None) or []:
        must.add(str(row["id"]))
    return truths, must


def _identity(item_id: str, title: str, truths: dict[str, str], must: set[str]) -> Identity:
    if item_id in must:
        return Identity(text=None, source="none", must_abstain=True)
    if item_id in truths:
        truth = truths[item_id]
        return Identity(text=truth or None, source="adjudicated" if truth else "none", must_abstain=not truth)
    return Identity(text=title, source="title")


def _protocol_for(category: str | None, protocols: dict[str, Protocol]) -> Protocol | None:
    return protocols.get(category or "") or protocols.get("generic")


def baselines_by_case(proof_dir: Path, suffix: str = "") -> dict[str, dict[str, Baseline]]:
    """Every recorded model pair's verdict per case, keyed by the run folder."""
    out: dict[str, dict[str, Baseline]] = {}
    for run in sorted(p for p in proof_dir.iterdir() if (p / "cases").is_dir()):
        is_buyscrap = run.name.endswith("__buyscrap")
        if run.name.startswith("fake__") or is_buyscrap != (suffix == "__buyscrap"):
            continue
        pair = run.name.removesuffix("__buyscrap")
        for case in sorted((run / "cases").glob("*.md")):
            rel = str(case.relative_to(proof_dir.parent.parent))
            out.setdefault(case.stem, {})[pair] = baseline_from_report(case.read_text(), rel)
    return out


def jiji_items(root: Path) -> list[Item]:
    """Rebuild Jiji items from the most complete run's case reports."""
    proof = root / "docs" / "proof"
    protocols = load_protocols(root / "protocols")
    truths, must = _verdicts(root / "eval")
    baselines = baselines_by_case(proof)
    reports: dict[str, str] = {}
    for run in sorted(proof.iterdir(), key=lambda p: -len(list((p / "cases").glob("*.md"))) if (p / "cases").is_dir() else 0):
        if run.name.endswith("__buyscrap") or not (run / "cases").is_dir():
            continue
        for case in (run / "cases").glob("*.md"):
            reports.setdefault(case.stem, case.read_text())

    items: list[Item] = []
    for case_id, report in sorted(reports.items()):
        match = _ANSWER_KEY.search(report)
        if not match:
            continue
        key = ast.literal_eval(match.group(1))
        category = key.get("category")
        protocol = _protocol_for(category, protocols)
        photos = _PHOTOS.search(report)
        url = str(key.get("url") or "").split("?")[0]
        items.append(
            Item(
                id=case_id,
                source="jiji",
                url=f"https://jiji.ng{url}" if url.startswith("/") else url,
                split=split_for(case_id),
                tier=tier_for(category),
                photos=Photos(
                    count=int(photos.group(1)) if photos else 0,
                    cache=f"eval/raw/media/{case_id}/",
                    note="Jiji photos, not ours to publish. Refetch with fetch-testset.",
                ),
                seller_text=None,
                seller_claims=_claims(report),
                answer=Answer(
                    title=key["title"],
                    category=category,
                    identity=_identity(case_id, key["title"], truths, must),
                    price=PriceTruth(
                        ngn=key.get("price_ngn"),
                        kind="asking",
                        used=key.get("is_used"),
                        note="" if key.get("is_used") else "new stock asking price, not a used reference",
                    ),
                ),
                risks=risk_seeds(protocol) if protocol else [],
                baselines=baselines.get(case_id, {}),
            )
        )
    return items


def load_labels(root: Path) -> dict[str, dict]:
    path = root / "eval" / "testify" / "labels.yaml"
    return (yaml.safe_load(path.read_text()) if path.exists() else None) or {}


def buyscrap_items(root: Path) -> list[Item]:
    """The tenant's adverts, tiered by hand label rather than by site category.

    The site files a television under E-waste because that is how the tenant
    prices it, which says nothing about what it is. An advert with no label
    falls back to the wanted-post check and to small goods.
    """
    raw = root / "eval" / "raw" / "buyscrap"
    protocols = load_protocols(root / "protocols")
    labels = load_labels(root)
    baselines = baselines_by_case(root / "docs" / "proof", "__buyscrap")
    items: list[Item] = []
    for listing in buyscrap.load(raw):
        label = labels.get(listing.id, {})
        wanted = bool(WANTED.search(listing.title))
        tier = label.get("tier") or ("not_for_sale" if wanted else "small_goods")
        category = label.get("protocol")
        protocol = _protocol_for(category, protocols)
        items.append(
            Item(
                id=listing.id,
                source="buyscrap",
                url=listing.url,
                split=split_for(listing.id),
                tier=tier,
                photos=Photos(
                    count=len(listing.media),
                    cache="eval/raw/buyscrap/media/",
                    note="Seller photos on the tenant's site. Links only in the release.",
                ),
                seller_text=listing.description or None,
                answer=Answer(
                    title=listing.title,
                    category=category,
                    kind=label.get("kind"),
                    identity=Identity(text=listing.title, source="title"),
                    price=PriceTruth(
                        ngn=listing.price_ngn or None,
                        kind="wanted" if tier == "not_for_sale" else "asking",
                        used=True,
                        note=f"site category {listing.category}",
                    ),
                ),
                risks=risk_seeds(protocol) if protocol else [],
                baselines=baselines.get(listing.id, {}),
            )
        )
    return items


def wider_items(root: Path, cache: str = "testify") -> list[Item]:
    """Small goods and material lots fetched by `buyscape testify-fetch`.

    From the testify_new cache, which holds dealers' new stock, every item is
    split `train`: training data for naming an item, never a benchmark item.
    """
    raw = root / "eval" / "raw" / cache
    training = cache != "testify"
    protocols = load_protocols(root / "protocols")
    items: list[Item] = []
    for row in wider.load(raw):
        category = "material_lot" if row["tier"] == "material_lot" else "generic"
        # Most scrap adverts on Jiji are dealers asking to buy, not sellers.
        wanted = bool(WANTED.search(row["title"]))
        protocol = _protocol_for(category, protocols)
        url = str(row.get("url") or "").split("?")[0]
        items.append(
            Item(
                id=row["id"],
                source="jiji",
                url=f"https://jiji.ng{url}" if url.startswith("/") else url,
                split="train" if training else split_for(row["id"]),
                market=row.get("region") or "lagos",
                tier="not_for_sale" if wanted else row["tier"],
                photos=Photos(
                    count=len(row.get("media") or []),
                    cache=f"eval/raw/{cache}/media/{row['id']}/",
                    note="Jiji photos, not ours to publish.",
                ),
                seller_text=row.get("description") or None,
                answer=Answer(
                    title=row["title"],
                    category=category,
                    kind=row["kind"],
                    identity=Identity(text=row["kind"], source="title"),
                    price=PriceTruth(
                        ngn=row.get("price_ngn"),
                        kind="wanted" if wanted else "asking",
                        used=row.get("is_used"),
                        note=row.get("condition") or "",
                    ),
                ),
                risks=risk_seeds(protocol) if protocol else [],
            )
        )
    return items


def train_items(root: Path, previous: Path | None = None) -> list[Item]:
    """The new-stock training pool. Kept from the previous file when the
    cache is not on this machine, like every other source."""
    if wider.load(root / "eval" / "raw" / "testify_new"):
        return sorted(wider_items(root, "testify_new"), key=lambda i: i.id)
    return load_items(previous) if previous else []


def _group(item: Item) -> str:
    if item.source == "buyscrap":
        return "buyscrap"
    if (item.photos.cache or "").startswith("eval/raw/testify/"):
        return "wider"
    return "reports"


def load_items(path: Path) -> list[Item]:
    if not path.exists():
        return []
    return [Item.model_validate_json(line) for line in path.read_text().splitlines() if line.strip()]


def all_items(root: Path, previous: Path | None = None) -> list[Item]:
    """Every source, deduped by id. The first source to name an id wins.

    A source whose cache is not on this machine keeps the items it had in the
    previous file, so converting on a laptop that never fetched BuyScrap does
    not quietly delete the BuyScrap items someone else fetched.
    """
    raw = root / "eval" / "raw"
    fresh = {
        "reports": jiji_items(root),
        "buyscrap": buyscrap_items(root) if (raw / "buyscrap" / "listings.json").exists() else None,
        "wider": wider_items(root) if wider.load(raw / "testify") else None,
    }
    kept = load_items(previous) if previous else []
    out: dict[str, Item] = {}
    for group, items in fresh.items():
        for item in items if items is not None else [i for i in kept if _group(i) == group]:
            out.setdefault(item.id, item)
    apply_reviews(out, root / "eval" / "testify" / "review_dev.yaml")
    apply_ai_labels(out, root / "eval" / "testify" / "labels_ai" / f"{LABELLER}.jsonl")
    return sorted(out.values(), key=lambda i: (i.source, i.id))


def apply_reviews(items: dict[str, Item], path: Path) -> None:
    """Attach each photo review, and stop scoring what the rule drops.

    A dropped item stays in the file with its reason, so the drop can be
    argued with. An advert judged new stock is not a used price, whatever
    the seller's condition tag said.
    """
    if not path.exists():
        return
    for review in yaml.safe_load(path.read_text()) or []:
        item = items.get(str(review.get("id")))
        if item is None:
            continue
        item.review = review
        item.exclude = drop_reason(review)
        if review.get("looks_actually_used") == "no":
            item.answer.price.used = False


# The model whose labels fill in where no hand review exists. It agreed with
# the hand review on 88 of 100 keep or drop decisions once both were put
# through the same rule (docs/research/failure-analysis.md).
LABELLER = "gemini-3.5-flash-lite"


def apply_ai_labels(items: dict[str, Item], path: Path) -> None:
    """A model's photo check, for items no person or reviewer has looked at.

    Its tier and kind replace the ones guessed from the search word, which
    were wrong for most material lots. Where a hand review exists, the hand
    review decides and the model's label is only attached.
    """
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        label = json.loads(line)
        item = items.get(str(label.get("id")))
        if item is None:
            continue
        item.ai_label = label
        if item.split != "train" and label.get("tier") in Item.model_fields["tier"].annotation.__args__:
            item.tier = label["tier"]
        if label.get("kind"):
            item.answer.kind = label["kind"]
        if item.review is None:
            item.exclude = drop_reason(label)
            if label.get("looks_actually_used") == "no":
                item.answer.price.used = False


def write(items: list[Item], out: Path) -> None:
    for item in items:
        item.seller_text = redact(item.seller_text)
        item.seller_claims = [redact(c) or "" for c in item.seller_claims]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(i.model_dump(mode="json"), ensure_ascii=False) + "\n" for i in items))
