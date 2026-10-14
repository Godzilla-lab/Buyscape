"""Buyscape command line. Everything the proof needs, nothing it does not."""

from __future__ import annotations

import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

from .evalset import buyscrap, jiji, score
from .identify.catalogue import load_catalogue
from .pricing.sources import JijiComps, MaterialsFloor, ScrapIndex
from .protocols.schema import load_protocols
from .tenant import load_tenant
from .providers.base import VisionProvider
from .providers.fake import FakeProvider
from .providers.recording import RecordingProvider
from .runner import Case, report_markdown, run_case
from .identify.ocr import default_reader

app = typer.Typer(add_completion=False, help="Remote valuation engine for second-hand goods.")
console = Console()

ROOT = Path.cwd()

# Named pairs, so a run is one flag. Reading and deciding are different jobs:
# open Qwen beats Gemini 3 Pro on OCRBench v2 at a fraction of the price, while
# frontier models earn their cost on identification and on refusing to answer.
# A second reader from a different family. Fabrications are not reproducible
# across families, so agreement between the two is evidence and disagreement
# is a reason to ask the seller for a better photograph.
DEFAULT_CORROBORATOR = "mistralai/mistral-small-3.2-24b-instruct"

PRESETS: dict[str, tuple[str, str]] = {
    # Cheap reader, cheap thinking decider. GLM 5.3 Flash scores within a
    # point of Gemini 3.8 Flash on the intelligence index at a fifteenth of
    # the price, and it does not depend on a free tier being up.
    "balanced": ("qwen/qwen3-vl-32b-instruct", "z-ai/glm-5.3-flash"),
    # Gemini 3.8 Flash on the Google AI Studio free tier: zero cost when it is
    # not shedding load, which on 4 Sep 2026 it was.
    "gemini-free": ("qwen/qwen3-vl-32b-instruct", "gemini-3.8-flash"),
    # Same shape, Google end to end. Runs on the free tier.
    "google": ("gemini-3.8-flash", "gemini-3.8-flash"),
    # Frontier decider. Measured at 1.6 cents an item on 4 Sep 2026, which
    # bought little over Gemini. Opt in by name only, never a default.
    "sonnet": ("qwen/qwen3-vl-32b-instruct", "anthropic/claude-sonnet-5"),
    # Zero cost, for exercising the pipeline when no budget is available.
    "free": ("minimax/minimax-m3:free", "minimax/minimax-m3:free"),
    "cheap": ("qwen/qwen3-vl-32b-instruct", "google/gemini-3.8-flash"),
    # xAI, which has working credit while the other accounts do not.
    "grok": ("grok-4.6", "grok-4.6"),
}
DEFAULT_READER = "qwen/qwen3-vl-32b-instruct"
DEFAULT_REASONER = "z-ai/glm-5.3-flash"


def _load_buyscrap_cases(raw: Path, limit: int | None) -> list[Case]:
    """The tenant's adverts. Titles are not model names, so the answer key is
    the site category and the asking price; identification is not scored."""
    cases: list[Case] = []
    for listing in buyscrap.load(raw):
        images = [raw / "media" / rel for rel in listing.media]
        images = [p for p in images if p.exists()][:6]
        if not images:
            continue
        cases.append(
            Case(
                id=listing.id,
                images=images,
                seller_text=listing.description,
                category_hint=None,
                slots_present=set(),
                truth={
                    "title": listing.title,
                    "category": None,
                    "site_category": listing.category,
                    "price_ngn": listing.price_ngn,
                    "is_used": listing.is_used,
                    "url": listing.url,
                },
            )
        )
    return cases[:limit] if limit else cases


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
HEIC_SUFFIXES = {".heic", ".heif"}


def load_folder_case(
    folder: Path, text: str = "", asking: float | None = None
) -> Case:
    """A folder of photos is a case: the seller's words in seller.txt, their
    answers in answers.yaml, the photos in whatever the phone named them.

    iPhones shoot HEIC, which the models do not accept, so each one is
    converted to a JPEG beside it, once. The JPEG is what gets sent and what
    the fixture is keyed on, so a rerun replays for free.
    """
    images: list[Path] = []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        suffix = path.suffix.lower()
        if suffix in HEIC_SUFFIXES:
            jpeg = path.with_suffix(".jpg")
            if not jpeg.exists():
                import pillow_heif
                from PIL import Image

                pillow_heif.register_heif_opener()
                with Image.open(path) as im:
                    im.convert("RGB").save(jpeg, format="JPEG", quality=92)
            images.append(jpeg)
        elif suffix in IMAGE_SUFFIXES:
            images.append(path)
    images = sorted(set(images), key=lambda p: p.name.lower())
    if not images:
        raise FileNotFoundError(f"no photos in {folder}: expected jpg, png, webp or heic files")

    words: list[str] = []
    seller_file = folder / "seller.txt"
    if seller_file.exists():
        words.append(seller_file.read_text().strip())
    if text.strip():
        words.append(text.strip())

    answers: dict[str, str] = {}
    answers_file = folder / "answers.yaml"
    if answers_file.exists():
        for key, value in (yaml.safe_load(answers_file.read_text()) or {}).items():
            # YAML reads a bare yes or no as a boolean. The seller said a word.
            if isinstance(value, bool):
                value = "yes" if value else "no"
            answers[str(key)] = str(value)

    return Case(
        id=folder.resolve().name,
        images=images[:8],
        seller_text="\n".join(w for w in words if w),
        asking_price=float(asking) if asking else None,
        answers=answers,
    )


def _load_dotenv(path: Path = ROOT / ".env") -> None:
    """Keys live in .env. Read it so a run never silently falls back to replay."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _provider(model: str, fixtures: Path, mode: str) -> VisionProvider:
    """Build a provider from the model name.

    A name with no slash is a Google AI Studio model, anything else goes to
    OpenRouter. Callers never see the difference.
    """
    if model == "fake":
        return RecordingProvider(FakeProvider(), fixtures / "fake", mode="record")

    if model.startswith("grok"):
        vendor, key = "xai", "XAI_API_KEY"
    elif "/" in model:
        vendor, key = "openrouter", "OPENROUTER_API_KEY"
    else:
        vendor, key = "google", "GOOGLE_API_KEY"

    inner = None
    if os.environ.get(key):
        if vendor == "google":
            from .providers.google import GoogleProvider

            inner = GoogleProvider(model)
        else:
            from .providers.openrouter import OpenRouterProvider

            inner = OpenRouterProvider(model, vendor=vendor)
    elif mode != "replay":
        console.print(
            f"[yellow]{key} is not set, so only recorded calls can be replayed "
            f"for {model}.[/yellow]"
        )
    return RecordingProvider(inner, fixtures / model.replace("/", "_"), mode=mode)


@app.command("fetch-testset")
def fetch_testset(
    out: Path = typer.Option(Path("eval/raw"), help="Where to cache listings and photos."),
    per_category: int = typer.Option(45, help="Listings to keep per category."),
    only: list[str] = typer.Option(None, help="Fetch only these categories, leaving the rest cached."),
) -> None:
    """Pull a held-out set of real Lagos listings from Jiji. Run once."""
    counts = jiji.build(out, per_category=per_category, only=tuple(only or ()))
    for category, n in counts.items():
        console.print(f"{category:18s} {n}")


def _load_cases(raw: Path, limit: int | None, categories: list[str] | None) -> list[Case]:
    cases: list[Case] = []
    seen: set[str] = set()
    for listing in jiji.load(raw):
        if categories and listing.category not in categories:
            continue
        # The same advert can answer two category searches. Counting it twice
        # would weight the gate towards whatever it is.
        if listing.id in seen:
            continue
        seen.add(listing.id)
        images = [raw / "media" / rel for rel in listing.media]
        images = [p for p in images if p.exists()][:6]
        if not images:
            continue
        cases.append(
            Case(
                id=listing.id,
                images=images,
                seller_text=listing.description,
                category_hint=listing.category,
                # A Jiji advert is a bare gallery: no code shot, no plate shot,
                # no clip. So no protocol slot counts as satisfied, and every
                # required shot becomes an unproven condition. That is the
                # honest reading of this evidence.
                slots_present=set(),
                truth={
                    "title": listing.title,
                    "category": listing.category,
                    "price_ngn": listing.price_ngn,
                    "is_used": listing.is_used,
                    "url": listing.url,
                },
            )
        )
    if limit:
        cases = cases[:limit]
    return cases


@app.command("fetch-prices")
def fetch_prices(
    out: Path = typer.Option(Path("eval/prices"), help="Where to cache the price pool."),
    per_category: int = typer.Option(400, help="Used listings to keep per category."),
    only: list[str] = typer.Option(None, help="Fetch only these categories, leaving the rest cached."),
) -> None:
    """Cache a large pool of used asking prices. No photos, comps only."""
    counts = jiji.build_price_pool(out, per_category=per_category, only=tuple(only or ()))
    for category, n in counts.items():
        console.print(f"{category:18s} {n}")


@app.command("run")
def run(
    raw: Path = typer.Option(Path("eval/raw"), help="Cached test set."),
    prices: Path = typer.Option(Path("eval/prices"), help="Cached comparable prices."),
    out: Path = typer.Option(Path("docs/proof"), help="Where reports are written."),
    preset: str = typer.Option(
        "", help=f"Named model pair: {', '.join(PRESETS)}. Overrides reader and reasoner."
    ),
    reader: str = typer.Option(DEFAULT_READER, help="Tier 1 model, or 'fake'."),
    reasoner: str = typer.Option(DEFAULT_REASONER, help="Tier 2 model, or 'fake'."),
    corroborator: str = typer.Option(
        DEFAULT_CORROBORATOR,
        help="Second reader. Only text both readers produce counts as read. 'none' disables it.",
    ),
    mode: str = typer.Option("auto", help="record | replay | auto"),
    limit: int = typer.Option(0, help="Cap the number of cases. 0 means all."),
    category: list[str] = typer.Option(None, help="Restrict to these categories."),
    workers: int = typer.Option(6, help="Cases to run at once. Cases are independent."),
    budget_usd: float = typer.Option(
        0.5,
        help="Stop starting new cases once recorded spend reaches this. 0 means no cap.",
    ),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
    tenant: str = typer.Option("buyscrap_ng", help="Tenant config in tenants/, without .yaml."),
    testset: str = typer.Option(
        "jiji", "--set", help="jiji (answer keys are model names) or buyscrap (the tenant's own adverts)."
    ),
) -> None:
    """Run the engine over the test set and write the reports and the gate."""
    _load_dotenv()
    if preset:
        if preset not in PRESETS:
            console.print(f"[red]Unknown preset {preset!r}. Choose from: {', '.join(PRESETS)}[/red]")
            raise typer.Exit(1)
        reader, reasoner = PRESETS[preset]

    protocols = load_protocols(ROOT / "protocols")
    catalogue = load_catalogue(ROOT / "catalogue")
    tenant_file = ROOT / "tenants" / f"{tenant}.yaml"
    if not tenant_file.exists():
        console.print(f"[red]No tenant file at {tenant_file}[/red]")
        raise typer.Exit(1)
    tenant_config = load_tenant(tenant_file)
    if testset == "buyscrap":
        cases = _load_buyscrap_cases(ROOT / "eval" / "raw" / "buyscrap", limit or None)
    else:
        cases = _load_cases(raw, limit or None, list(category) if category else None)
    if not cases:
        console.print("[red]No cases found. Run fetch-testset first.[/red]")
        raise typer.Exit(1)

    # A listing must never be its own comparable price. The price pool is a
    # separate, larger cache; the test set is only a fallback when it is absent.
    pool = prices if prices.exists() else raw
    comps = JijiComps(pool, exclude_ids=frozenset(c.id for c in cases))
    scrap = ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml")
    materials = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    reader_p = _provider(reader, fixtures, mode)
    reasoner_p = _provider(reasoner, fixtures, mode)
    corroborator_p = (
        None if corroborator in ("", "none") else _provider(corroborator, fixtures, mode)
    )

    run_dir = out / f"{reader.replace('/', '_')}__{reasoner.replace('/', '_')}"
    if testset != "jiji":
        run_dir = run_dir.with_name(run_dir.name + f"__{testset}")
    (run_dir / "cases").mkdir(parents=True, exist_ok=True)

    # Spend is checked before every case starts, so the overshoot is at most
    # the cases already in flight. Replayed calls cost nothing.
    spend = {"usd": 0.0}
    lock = threading.Lock()
    # A run that cannot reach the provider must stop, not write a hundred
    # PROVIDER_ERROR reports over the last good ones. Five in a row is an
    # outage; one is a case that failed on its own.
    outage = {"streak": 0, "why": None}
    HALT_AFTER = 5

    ocr = default_reader()

    def one(case: Case):
        with lock:
            if budget_usd and spend["usd"] >= budget_usd:
                return case, None
            if outage["why"]:
                return case, None
        result = run_case(
            case, protocols, catalogue, comps, scrap, reader_p, reasoner_p, materials,
            corroborator_p, tenant_config, ocr=ocr,
        )
        with lock:
            spend["usd"] += result.spent_usd
            if result.chain.failure_code == "PROVIDER_ERROR":
                outage["streak"] += 1
                if outage["streak"] >= HALT_AFTER and not outage["why"]:
                    outage["why"] = result.chain.reason
            else:
                outage["streak"] = 0
        (run_dir / "cases" / f"{case.id}.md").write_text(report_markdown(case, result))
        return case, result

    pairs = []
    done = 0
    with console.status(f"Running {len(cases)} cases") as status:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            for case, result in pool.map(one, cases):
                done += 1
                status.update(f"[{done}/{len(cases)}] {case.id} spent ${spend['usd']:.3f}")
                if result is not None:
                    pairs.append((case, result))

    skipped = len(cases) - len(pairs)
    if outage["why"]:
        # No summary: a run that lost the network proves nothing about the
        # engine, and its numbers must not overwrite a run that finished.
        ran = len(pairs) - outage["streak"]
        console.print(
            f"[red]Run halted: {HALT_AFTER} provider errors in a row after {ran} cases, "
            f"{skipped} not started. Spent ${spend['usd']:.3f}. Last error: {outage['why']}[/red]"
        )
        console.print("Recorded calls are kept, so rerunning pays only for the cases that never ran.")
        raise typer.Exit(2)
    if not pairs:
        console.print(f"[red]Budget ${budget_usd:.2f} was already spent before any case ran.[/red]")
        raise typer.Exit(1)
    verdicts = score.load_verdicts(ROOT / "eval")
    metrics = score.score(pairs, verdicts)
    summary = metrics.summary()
    summary["reader"] = reader
    summary["reasoner"] = reasoner
    summary["corroborator"] = corroborator
    summary["spend_usd"] = round(spend["usd"], 4)
    summary["budget_usd"] = budget_usd
    summary["skipped_for_budget"] = skipped
    score.write_summary(run_dir / "summary.json", summary)

    table = Table(title=f"Buyscape proof: reader {reader}, reasoner {reasoner}")
    table.add_column("metric")
    table.add_column("value", justify="right")
    for key, value in summary.items():
        if key in ("failure_codes", "reader", "reasoner", "corroborator", "silent_wrong_cases"):
            continue
        table.add_row(key, str(value))
    console.print(table)

    gate = Table(title="Phase 0 gate")
    gate.add_column("metric")
    gate.add_column("measured", justify="right")
    gate.add_column("needs", justify="right")
    gate.add_column("verdict")
    all_pass = True
    for name, measured, needs, passed in score.gate_table(summary):
        verdict = "no data" if passed is None else ("PASS" if passed else "FAIL")
        # A metric with no data has not been proven, so it cannot pass the gate.
        if passed is not True:
            all_pass = False
        gate.add_row(name, measured, needs, verdict)
    console.print(gate)
    if summary["failure_codes"]:
        console.print(f"Loud failures: {summary['failure_codes']}")
    per_case = spend["usd"] / len(pairs)
    # Every run leaves a row in the ledger. The business question is the cost
    # per item, and it is answered from this file, never from memory.
    ledger = out / "spend.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a") as fh:
        fh.write(
            json.dumps(
                {
                    "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "reader": reader,
                    "reasoner": reasoner,
                    "mode": mode,
                    "cases": len(pairs),
                    "spend_usd": round(spend["usd"], 4),
                    "spend_per_case_usd": round(per_case, 5),
                    "model_cost_per_case_usd": summary.get("cost_per_case_usd"),
                    "silent_wrong_rate": summary.get("silent_wrong_rate"),
                    "model_top1_accuracy_with_label": summary.get("model_top1_accuracy_with_label"),
                }
            )
            + "\n"
        )
    console.print(
        f"Spend: ${spend['usd']:.3f} on {len(pairs)} cases, ${per_case:.4f} per case."
        + (f" Budget ${budget_usd:.2f} reached, {skipped} cases not started." if skipped else "")
    )
    console.print(f"Reports: {run_dir / 'cases'}")
    console.print("[green]GATE PASSED[/green]" if all_pass else "[red]GATE NOT PASSED[/red]")


@app.command("assess")
def assess(
    folder: Path = typer.Argument(..., help="A folder of photos, with optional seller.txt and answers.yaml."),
    text: str = typer.Option("", "--text", help="The seller's words, if not in seller.txt."),
    asking: float = typer.Option(0.0, help="What the seller wants for it, in the tenant currency. 0 means unknown."),
    preset: str = typer.Option("balanced", help=f"Named model pair: {', '.join(PRESETS)}."),
    reader: str = typer.Option("", help="Tier 1 model, or 'fake'. Overrides the preset."),
    reasoner: str = typer.Option("", help="Tier 2 model, or 'fake'. Overrides the preset."),
    corroborator: str = typer.Option(DEFAULT_CORROBORATOR, help="Second reader. 'none' disables it."),
    mode: str = typer.Option("auto", help="record | replay | auto"),
    prices: Path = typer.Option(Path("eval/prices"), help="Cached comparable prices."),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
    tenant: str = typer.Option("buyscrap_ng", help="Tenant config in tenants/, without .yaml."),
) -> None:
    """Value one item from a folder of photos. Writes report.md into the folder."""
    _load_dotenv()
    if preset not in PRESETS:
        console.print(f"[red]Unknown preset {preset!r}. Choose from: {', '.join(PRESETS)}[/red]")
        raise typer.Exit(1)
    reader = reader or PRESETS[preset][0]
    reasoner = reasoner or PRESETS[preset][1]
    if reader == "fake" or reasoner == "fake":
        corroborator = "none"
    tenant_file = ROOT / "tenants" / f"{tenant}.yaml"
    if not tenant_file.exists():
        console.print(f"[red]No tenant file at {tenant_file}[/red]")
        raise typer.Exit(1)
    try:
        case = load_folder_case(folder, text=text, asking=asking or None)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)

    protocols = load_protocols(ROOT / "protocols")
    catalogue = load_catalogue(ROOT / "catalogue")
    tenant_config = load_tenant(tenant_file)
    pool = prices if prices.exists() else ROOT / "eval" / "raw"
    comps = JijiComps(pool, live=lambda key, cat, pages, used=True: [l.to_json() for l in jiji.search_used(key, cat, max_pages=pages, limit=20 * pages, used=used)])
    scrap = ScrapIndex(ROOT / "tenants" / "scrap_index_lagos.yaml")
    materials = MaterialsFloor(ROOT / "tenants" / "scrap_index_lagos.yaml")
    reader_p = _provider(reader, fixtures, mode)
    reasoner_p = _provider(reasoner, fixtures, mode)
    corroborator_p = None if corroborator in ("", "none") else _provider(corroborator, fixtures, mode)

    with console.status(f"Reading {len(case.images)} photos"):
        result = run_case(
            case, protocols, catalogue, comps, scrap, reader_p, reasoner_p, materials,
            corroborator_p, tenant_config, ocr=default_reader(),
        )
    report = folder / "report.md"
    report.write_text(report_markdown(case, result))

    c, q = result.chain, result.quote
    if c.reading:
        console.print(
            f"[bold]Seen:[/bold] {c.category or 'unknown'} "
            f"(confidence {c.reading.category_confidence}), {c.reading.presentation}, "
            f"about {c.reading.estimated_weight_kg} kg"
        )
    if result.identified:
        console.print(f"[bold]Identified:[/bold] {c.model_key}")
    else:
        console.print(f"[bold]Not identified:[/bold] {c.failure_code or 'abstained'}. {c.reason or ''}")
    if q.is_failure:
        console.print(f"[red]{q.failure_code}[/red]: {q.reason}")
    else:
        console.print(
            f"[bold]Price:[/bold] {q.low:,.0f} to {q.high:,.0f} {q.currency} "
            f"({q.basis}, {q.method})"
        )
        console.print(q.explanation)
        for condition in q.conditions[:8]:
            console.print(f"  - {condition}")
    if result.asks:
        console.print("[bold]Send next:[/bold]")
        for ask in result.asks[:5]:
            console.print(f"  - {ask.ask}")
    if result.questions:
        console.print("[bold]Questions for the seller:[/bold]")
        for question in result.questions[:5]:
            console.print(f"  - {question.ask}")
    console.print(f"Cost ${result.spent_usd:.4f} live, ${result.cost_usd:.4f} at recorded prices. Report: {report}")


@app.command("ui")
def ui(
    port: int = typer.Option(8765, help="Port to listen on."),
    host: str = typer.Option("127.0.0.1", help="Bind address. 0.0.0.0 lets a phone on the same wifi reach it."),
    tenant: str = typer.Option("buyscrap_ng", help="Tenant config in tenants/, without .yaml."),
    no_browser: bool = typer.Option(False, "--no-browser", help="Do not open a browser tab."),
) -> None:
    """Serve the seller page at /, the back office at /office and the test
    bench at /bench. Same engine, same fixtures as `assess`. BUYSCAPE_PRESET
    and BUYSCAPE_MODE pick the models; BUYSCAPE_OFFICE_TOKEN gates the office."""
    from .ui.server import serve

    _load_dotenv()
    serve(ROOT, host=host, port=port, open_browser=not no_browser, tenant=tenant)


@app.command("fetch-buyscrap")
def fetch_buyscrap(out: Path = typer.Option(ROOT / "eval" / "raw" / "buyscrap")) -> None:
    """Cache every advert on buyscrap.com.ng, the tenant's own site, with photos."""
    listings = buyscrap.fetch(out)
    with_photos = sum(1 for l in listings if l.media)
    console.print(f"{len(listings)} adverts cached, {with_photos} with photos, in {out}")
    by_cat: dict[str, int] = {}
    for l in listings:
        by_cat[l.category] = by_cat.get(l.category, 0) + 1
    for cat, n in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        console.print(f"  {n:3d}  {cat}")


@app.command("testify-convert")
def testify_convert(out: Path = typer.Option(ROOT / "eval" / "testify" / "items.jsonl")) -> None:
    """Build Testify benchmark items from every cached source. Free: no model calls."""
    from collections import Counter

    from .testify import convert

    items = convert.all_items(ROOT, previous=out)
    convert.write(items, out)
    console.print(f"{len(items)} items written to {out}")
    for (source, tier), n in sorted(Counter((i.source, i.tier) for i in items).items()):
        console.print(f"  {n:4d}  {source:9s} {tier}")
    splits = Counter(i.split for i in items)
    console.print(f"  dev {splits['dev']}, test {splits['test']}")

    # Training pool: dealers' new stock, for naming items. An advert in the
    # benchmark is never also a training example.
    pool_path = out.parent / "train_pool.jsonl"
    benchmark = {i.id for i in items}
    pool = [i for i in convert.train_items(ROOT, previous=pool_path) if i.id not in benchmark]
    convert.write(pool, pool_path)
    console.print(f"{len(pool)} training items written to {pool_path}")
    for kind, n in sorted(Counter(i.answer.kind for i in pool).items(), key=lambda kv: -kv[1])[:10]:
        console.print(f"  {n:4d}  {kind}")


@app.command("testify-fetch")
def testify_fetch(
    out: Path = typer.Option(None, help="Defaults to eval/raw/testify, or eval/raw/testify_new with --new-stock."),
    per_phrase: int = typer.Option(25, help="Adverts to keep per search phrasing."),
    only: list[str] = typer.Option(None, help="Fetch only these kinds, for example 'standing fan'."),
    max_photos: int = typer.Option(None, help="Photos per advert: 3 by default, 1 with --new-stock."),
    skip_done: bool = typer.Option(False, help="Only fetch kinds never fetched for this city."),
    region: str = typer.Option(
        "lagos", help="Jiji city or state, as in its web address: lagos, abuja, rivers, oyo, ogun, kano."
    ),
    new_stock: bool = typer.Option(
        False, help="Fetch dealers' brand new adverts instead, as training data for naming items. Never benchmark items."
    ),
) -> None:
    """Cache Jiji adverts for small goods and material lots. Run from an ordinary connection."""
    from .testify import fetch as wider

    pool = "new" if new_stock else "used"
    out = out or ROOT / "eval" / "raw" / ("testify_new" if new_stock else "testify")
    max_photos = max_photos or (1 if new_stock else 3)
    counts = wider.build(
        out,
        per_phrase=per_phrase,
        only=tuple(only or ()),
        max_photos=max_photos,
        progress=console.print,
        skip_done=skip_done,
        pool=pool,
        region=region,
    )
    if not counts:
        console.print(
            f"Every kind is already fetched for {region}. Leave out --skip-done to refresh it, "
            "or pick another city with --region."
        )
        return
    other = "second-hand" if new_stock else "brand new"
    console.print(f"{'kind':26s} {'kept':>5s} {'skipped ' + other:>22s} {'skipped buyers':>15s} {'timed out':>10s}")
    for kind, t in counts.items():
        console.print(
            f"{kind:26s} {t['kept']:5d} {t[other]:22d} {t['buyer, not seller']:15d} {t['timed out']:10d}"
        )
    sharper = sum(t.get("sharper photos", 0) for t in counts.values())
    if sharper:
        console.print(f"{sharper} adverts fetched before as thumbnails now have full-size photos.")
    if any(t["timed out"] for t in counts.values()):
        console.print("Some searches timed out. Run the same command again: it keeps what it has and fills the gaps.")
    if not any(t["kept"] for t in counts.values()):
        console.print("[red]Nothing fetched. Jiji may be answering with a bot check from this network.[/red]")


@app.command("spend")
def spend_report(out: Path = typer.Option(ROOT / "docs" / "proof")) -> None:
    """What every run cost, per model pair, and what one item costs on each."""
    ledger = out / "spend.jsonl"
    if not ledger.exists():
        console.print("No runs recorded yet.")
        return
    rows = [json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
    table = Table(title="LLM spend, all runs", expand=True)
    for col in ("when", "reader", "reasoner", "cases", "spent $", "list $/item", "silent wrong"):
        table.add_column(col, justify="right" if col not in ("when", "reader", "reasoner") else "left", overflow="fold")
    total = 0.0
    for r in rows:
        total += r["spend_usd"]
        table.add_row(
            r["at"][5:16].replace("T", " "),
            r["reader"].split("/")[-1],
            r["reasoner"].split("/")[-1],
            str(r["cases"]),
            f"{r['spend_usd']:.3f}",
            f"{r.get('model_cost_per_case_usd') or 0:.4f}",
            "" if r.get("silent_wrong_rate") is None else f"{r['silent_wrong_rate']:.1%}",
        )
    console.print(table)
    console.print(f"Total spent across recorded runs: ${total:.2f}")
    console.print(
        "Per item is what one valuation costs at list price with nothing cached. "
        "That number has to stay small enough that a tenant pays it without noticing."
    )


@app.command("protocols")
def check_protocols() -> None:
    """Validate every protocol file."""
    protocols = load_protocols(ROOT / "protocols")
    for name, p in protocols.items():
        opening = ", ".join(s.id for s in p.opening_shots) or "none"
        console.print(
            f"{name:18s} v{p.version} shots={len(p.shots)} "
            f"required={len(p.required_shots)} opens={opening} "
            f"questions={len(p.questions)} claims={len(p.claims)}"
        )


if __name__ == "__main__":
    app()
