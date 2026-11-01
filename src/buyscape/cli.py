"""Buyscape command line. Everything the proof needs, nothing it does not."""

from __future__ import annotations

import hashlib
import json
import os
import re
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
    if model.startswith(("agent:", "human:", "local:")):
        # A person or an agent who sat the test, or a model run on someone's
        # own GPU: answers come only from the recordings that testify-import
        # or testify-batch-import wrote.
        return RecordingProvider(None, fixtures / _dir_name(model), mode="replay")

    served = model
    if model.startswith("grok"):
        vendor, key = "xai", "XAI_API_KEY"
    elif model.startswith("nvidia:"):
        vendor, key, served = "nvidia", "NVIDIA_API_KEY", model.removeprefix("nvidia:")
    elif model.startswith("kaggle:"):
        vendor, key, served = "kaggle", "MODEL_PROXY_API_KEY", model.removeprefix("kaggle:")
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

            inner = OpenRouterProvider(served, vendor=vendor)
    elif mode != "replay":
        console.print(
            f"[yellow]{key} is not set, so only recorded calls can be replayed "
            f"for {model}.[/yellow]"
        )
    return RecordingProvider(inner, fixtures / _dir_name(model), mode=mode)


def _dir_name(model: str) -> str:
    """A model name as one folder name: openrouter's vendor/model and our prefixes alike."""
    return model.replace("/", "_").replace(":", "_")


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
    from .pricing import shops

    comps = JijiComps(pool, exclude_ids=frozenset(c.id for c in cases), shop_rows=shops.load(ROOT, tenant_config.shops))
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
    from .pricing import shops

    comps = JijiComps(pool, live=lambda key, cat, pages, used=True: [l.to_json() for l in jiji.search_used(key, cat, max_pages=pages, limit=20 * pages, used=used)],
                      shop_rows=shops.load(ROOT, tenant_config.shops))
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


@app.command("fetch-shops")
def fetch_shops(
    tenant: str = typer.Option("buyscrap_ng", help="Whose shops, and whose categories for Jumia."),
    shop: list[str] = typer.Option(None, help="Only these shops. Default: every shop the tenant names."),
    pages: int = typer.Option(5, help="Pages read per Jumia category, 40 products a page."),
    limit: int = typer.Option(0, help="At most this many Slot product pages. 0 for all of them."),
) -> None:
    """Cache new asking prices from the shops a tenant trusts, for the share-of-new route. Free.

    Pointek through its store API, Slot from its sitemap's product pages,
    Jumia by whole categories since its search is closed to crawlers. Every
    price keeps its shop, its product link and the day it was read."""
    from .pricing import shops

    config = load_tenant(ROOT / "tenants" / f"{tenant}.yaml")
    chosen = shop or config.shops
    with shops.client() as client:
        for name in chosen:
            if name not in shops.FETCHERS:
                console.print(f"[red]No fetcher for {name!r}; known: {', '.join(shops.SHOPS)}[/red]")
                continue
            if name == "jumia":
                rows = shops.fetch_jumia(client, config.shop_categories.get("jumia", {}), pages=pages)
            elif name == "slot":
                rows = shops.fetch_slot(client, limit=limit or None)
            else:
                rows = shops.fetch_pointek(client)
            total = shops.save(rows, ROOT / shops.CACHE / f"{name}.json")
            used = sum(r["condition"] != "new" for r in rows)
            console.print(f"  {name}: {len(rows)} prices read ({used} pre-owned, kept apart), {total} cached")


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

    # Training pool: dealers' new stock, for naming items, and second-hand
    # adverts fetched for training. An advert in the benchmark, or a repost
    # of one, is never also a training example.
    pool_path = out.parent / "train_pool.jsonl"
    pool = convert.train_items(ROOT, previous=pool_path)
    repeats = convert.repeats(pool, items, ROOT)
    pool = [i for i in pool if i.id not in repeats]
    convert.write(pool, pool_path)
    console.print(f"{len(pool)} training items written to {pool_path}, {len(repeats)} left out as benchmark adverts")
    for (cache, market), n in sorted(Counter((i.photos.cache.split("/")[2], i.market) for i in pool).items()):
        console.print(f"  {n:4d}  {cache:14s} {market}")
    for kind, n in sorted(Counter(i.answer.kind for i in pool).items(), key=lambda kv: -kv[1])[:10]:
        console.print(f"  {n:4d}  {kind}")


@app.command("testify-construct")
def testify_construct(
    out: Path = typer.Option(ROOT / "eval" / "testify" / "constructed.jsonl"),
) -> None:
    """Items with the proof taken away, and photos that cannot be priced. Free: local OCR only."""
    import json
    from collections import Counter

    from .identify.ocr import default_reader
    from .testify import construct, label
    from .testify.schema import Item

    reader = default_reader()
    if reader is None:
        console.print("[red]The local OCR is not installed, so the plates cannot be found.[/red]")
        raise typer.Exit(1)
    # A person's checks survive a rebuild: an item keeps its verdict while it is built the same way.
    old = {}
    if out.exists():
        old = {(r["id"], r["route"]): r for r in map(json.loads, out.read_text().splitlines())}
    items = [Item.model_validate_json(line) for line in (ROOT / "eval" / "testify" / "items.jsonl").open()]
    images = ROOT / "eval" / "raw" / "testify_constructed"
    rows = []
    for item in items:
        if item.split not in ("dev", "test") or (not item.ai_label and not item.exclude):
            continue
        row = construct.bad_photo(item) if item.exclude else None
        if row is None and not item.exclude:
            photos = label.photos_for(item, ROOT)
            row = construct.construct(item, photos, reader.boxes, images, ROOT) if photos else None
        if row is None:
            continue
        before = old.get((row["id"], row["route"]))
        if before and before.get("photos") == row.get("photos"):
            row["checked"] = before.get("checked")
            if before.get("checked_by"):
                row["checked_by"] = before["checked_by"]
        rows.append(row)
    out.write_text("".join(json.dumps(r) + "\n" for r in rows))
    console.print(f"{len(rows)} constructed items written to {out}")
    for (split, route), n in sorted(Counter((r["split"], r["route"]) for r in rows).items()):
        console.print(f"  {n:4d}  {split:5s} {route}")


@app.command("testify-truths")
def testify_truths(
    out: Path = typer.Option(ROOT / "eval" / "testify" / "truths.jsonl"),
) -> None:
    """True claims a photo shows, and their false twins, for the truth and contra variants. Free: local OCR."""
    import json
    from collections import Counter

    from .identify.ocr import default_reader
    from .providers.base import ImageRef
    from .testify import label, truths
    from .testify.schema import Item

    reader = default_reader()
    if reader is None:
        console.print("[red]The local OCR is not installed, so no fact can be read off a photo.[/red]")
        raise typer.Exit(1)
    old = {}
    if out.exists():
        old = {r["id"]: r for r in map(json.loads, out.read_text().splitlines())}
    rival_of = truths.rivals()
    rows = []
    for line in (ROOT / "eval" / "testify" / "items.jsonl").open():
        item = Item.model_validate_json(line)
        if item.split not in ("dev", "test") or not item.ai_label:
            continue
        row = truths.fact(item, label.photos_for(item, ROOT), lambda p: reader((ImageRef(p),)), rival_of)
        if row is None:
            continue
        before = old.get(row["id"])
        if before and before.get("truth") == row["truth"]:
            row["checked"] = before.get("checked")
        rows.append(row)
    out.write_text("".join(json.dumps(r) + "\n" for r in rows))
    console.print(f"{len(rows)} facts written to {out}")
    for (split, kind), n in sorted(Counter((r["split"], r["fact"]) for r in rows).items()):
        console.print(f"  {n:4d}  {split:5s} {kind}")


@app.command("testify-compare")
def testify_compare(
    split: str = typer.Option("dev"),
    resamples: int = typer.Option(2000, help="Paired bootstrap draws."),
    out: Path = typer.Option(ROOT / "eval" / "testify" / "runs" / "compare.json"),
    tenant: Path = typer.Option(ROOT / "tenants" / "buyscrap_ng.yaml", help="Whose deal costs price the money score."),
    lost_deal: str = typer.Option("2000,5000,10000", help="Lost-deal costs to show while the tenant has set none."),
    proof_dropoff: float = typer.Option(0.5, help="Seller drop-off to show while the tenant has set none."),
) -> None:
    """Every scored model side by side, with paired intervals, the coverage curve and the money score. Free."""
    import json

    from .tenant import load_tenant
    from .testify.schema import Item
    from .testify.stats import COVERAGES, expected_loss, paired_bootstrap, per_item

    items = {}
    for line in (ROOT / "eval" / "testify" / "items.jsonl").open():
        item = Item.model_validate_json(line)
        if item.split == split and not item.exclude and item.ai_label:
            items[item.id] = item
    costs = load_tenant(tenant).deal_costs
    if costs.lost_deal is not None and costs.proof_dropoff is not None:
        settings = [(costs.lost_deal, costs.proof_dropoff, f"{tenant.stem}'s own costs")]
    else:
        settings = [(float(x), proof_dropoff, "not the tenant's: it has set none")
                    for x in lost_deal.split(",") if x.strip()]
    models, money = {}, {}
    for run in sorted((ROOT / "eval" / "testify" / "runs").glob(f"*/{split}.jsonl")):
        rows = [json.loads(line) for line in run.read_text().splitlines()]
        repeat = run.with_name(f"{split}.repeat1.jsonl")
        again = [json.loads(line) for line in repeat.read_text().splitlines()] if repeat.exists() else None
        models[run.parent.name] = per_item(rows, items, again)
        money[run.parent.name] = [
            {"lost_deal": cost, "proof_dropoff": drop, "whose": whose,
             **expected_loss(rows, items, cost, drop, costs.offer)}
            for cost, drop, whose in settings
        ]
    result = paired_bootstrap(models, n=resamples)
    result["split"] = split
    result["expected_loss"] = money
    out.write_text(json.dumps(result, indent=1) + "\n")
    console.print(f"{result['items']} items every model answered, {resamples} paired resamples")
    shown = ["priced_share", "silent_wrong_rate", "identity_accuracy",
             *(f"silent_at_{round(c * 100)}pct" for c in COVERAGES), "silent_area"]
    for name, stats in result["models"].items():
        console.print(f"  {name}")
        for stat in shown:
            point, ci = stats[stat]["point"], stats[stat]["interval"]
            console.print(f"    {stat:22s} {point if point is not None else '-':>8}  {ci or ''}")
    console.print("Expected loss per item, in the tenant's currency:")
    for name, lines in money.items():
        shown_lines = ", ".join(f"{m['loss_per_item']} at a lost deal of {m['lost_deal']:,.0f}" for m in lines)
        console.print(f"  {name}: {shown_lines}; {lines[0]['offers_above_asking']} offers above the asking "
                      f"price, the largest {lines[0]['largest_overpayment']:,}")
    console.print(f"  ({settings[0][2]}; proof drop-off {settings[0][1]})")
    console.print("Differences whose interval excludes zero:")
    for pair, stats in result["pairs"].items():
        for stat, value in stats.items():
            if not value["tie"]:
                console.print(f"  {pair}: {stat} {value['difference']} {value['interval']}")
    console.print(f"Written to {out}")
    tables = _stage_tables(split, items, money)
    out.with_suffix(".md").write_text(tables)
    console.print(f"Read and pick tables written to {out.with_suffix('.md')}")


def _stage_tables(split: str, items: dict, money: dict) -> str:
    """Two tables, not one number: what each model read, and how it priced.

    The read stage is the model alone. The pick stage also depends on the
    comparables our crawler found, so it is reported apart."""
    import json

    from .testify import construct, truths
    from .testify.score import against_repeat, score

    runs = ROOT / "eval" / "testify" / "runs"

    def load(path: Path) -> list[dict]:
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []

    def pct(value) -> str:
        return "-" if value is None else f"{value * 100:.0f}%"

    facts_path = ROOT / "eval" / "testify" / "truths.jsonl"
    facts = {r["id"]: r for r in load(facts_path)}
    built = load(ROOT / "eval" / "testify" / "constructed.jsonl")
    read_rows, pick_rows = [], []
    for run in sorted(runs.glob(f"*/{split}.jsonl")):
        name, rows = run.parent.name, load(run)
        s = score(rows, items)
        noise = against_repeat(rows, load(run.with_name(f"{split}.repeat1.jsonl")), items)
        t = truths.score(load(run.with_name(f"{split}.truth_contra.jsonl")), facts)
        c = construct.score(load(run.with_name(f"{split}.constructed.jsonl")), built, items, rows)
        read_rows.append(f"| {name} | {pct(s['identity_accuracy_when_attempted'])} | "
                         f"{pct(s['identity_accuracy_judged'])} | "
                         f"{pct(s['named_a_model_the_photos_do_not_show'])} | {pct(s['lie_marked_supported'])} | "
                         f"{pct(t.get('truth_marked_supported'))} | {pct(t.get('contra_caught'))} | "
                         f"{pct(c.get('noproof_abstained'))} | {pct(c.get('proof_asked_first'))} | "
                         f"{pct(noise.get('repeat_same_decision'))} |")
        loss = (money.get(name) or [{}])[0]
        pick_rows.append(f"| {name} | {pct(s['priced_share'])} | {s['silent_wrong']} | "
                         f"{pct(s['asking_price_inside_range'])} | {pct(s['priced_above_asking'])} | "
                         f"{pct(s['lie_raised_price'])} ({pct(noise.get('price_raised_on_honest_repeat'))}) | "
                         f"{loss.get('loss_per_item', '-')} |")
    return "\n".join([
        f"# Testify {split}: the read and the pick", "",
        "## The read: the model alone", "",
        "| Model | Identity right | Same thing, judged | Named a model the photos do not show | "
        "Lie marked supported | True claim marked supported | False claim caught | Abstained with the label gone | "
        "Asked for the label first | Same decision asked twice |",
        "|---|---|---|---|---|---|---|---|---|---|", *read_rows, "",
        "Identity right is the word rule; same thing, judged also counts other words for the same thing "
        "(testify/judge.py), and a person's verdict comes first in both.", "",
        "## The pick: the model and our comparables", "",
        "| Model | Gave a price | Silent wrong | Asking price inside the range | Offered above asking | "
        "Lie raised the price (asking again raised it) | Expected loss per item, naira |",
        "|---|---|---|---|---|---|---|", *pick_rows, "",
        "Expected loss is at the first lost-deal cost in compare.json; it is not any business's own number.", "",
    ])


@app.command("testify-adjudicate")
def testify_adjudicate(split: str = typer.Option("dev")) -> None:
    """Add every priced answer a word rule marks wrong to the adjudication file, for a person. Free."""
    import json

    import yaml

    from .testify import adjudicate
    from .testify.schema import Item
    from .testify.score import identity_correct

    items = {}
    for line in (ROOT / "eval" / "testify" / "items.jsonl").open():
        item = Item.model_validate_json(line)
        if item.split == split and not item.exclude and item.ai_label:
            items[item.id] = item
    found = []
    for run in sorted((ROOT / "eval" / "testify" / "runs").glob(f"*/{split}*.jsonl")):
        for row in map(json.loads, run.read_text().splitlines()):
            identity = (row.get("reading") or {}).get("identity") or {}
            if row["id"] in items and row.get("price_low") is not None and identity \
                    and row.get("variant") not in ("noproof", "bad_photo") \
                    and identity_correct(items[row["id"]], identity) is False:
                found.append((f"{run.parent.name}/{run.stem}", row, items[row["id"]]))
    new = adjudicate.pending(found)
    path = adjudicate.PATH
    held = (yaml.safe_load(path.read_text()) or []) if path.exists() else []
    if new:
        path.write_text((path.read_text() if path.exists() else _ADJUDICATION_HEAD)
                        + yaml.safe_dump(new, sort_keys=False, allow_unicode=True, width=110))
    waiting = sum(1 for e in held + new if not e.get("verdict"))
    console.print(f"{len(new)} new answers to read, {waiting} waiting for a person's verdict in {path}")


_ADJUDICATION_HEAD = """# A person's verdict on each priced answer the word rules marked wrong.
#
# Written by `uv run buyscape testify-adjudicate`. For each entry, read the
# item's photos and the answer, then set `verdict` to right, wrong_kind,
# wrong_brand or wrong_version, `by` to your name, and `why` in a line.
# Unsure leaves the rule's call standing and is counted apart.
# `first_reading` is a model's draft and moves no score: only `verdict` does.
# An entry matches every run that gave the same answer to the same item.

"""


@app.command("testify-judge")
def testify_judge(
    split: list[str] = typer.Option(["dev"], help="Splits whose answers to judge: dev, test."),
    model: str = typer.Option("nvidia:minimaxai/minimax-m3.1-flash", help="A judge that sits no Testify table."),
    workers: int = typer.Option(2),
    check: bool = typer.Option(False, help="Only measure the judge: a person's verdicts, and answers swapped between kinds."),
    limit: int = typer.Option(None, help="Judge at most this many new answers."),
) -> None:
    """Judge every answer the word rules mark wrong: the same thing in other words is right. Free on NVIDIA."""
    import random
    import time

    from .testify import adjudicate, judge
    from .testify.schema import Item
    from .testify.score import identity_correct

    items = {}
    for line in (ROOT / "eval" / "testify" / "items.jsonl").open():
        item = Item.model_validate_json(line)
        if not item.exclude and item.ai_label:
            items[item.id] = item
    provider = _provider(model, ROOT / "eval" / "fixtures", "auto")

    def ask(pairs):
        """Verdicts for (item, answer) pairs, judge.BATCH to a call; a failed call leaves its batch unjudged."""
        out = []
        for start in range(0, len(pairs), judge.BATCH):
            chunk = pairs[start:start + judge.BATCH]
            cases = [(item.answer.title, identity, item.answer.kind,
                      (item.review or item.ai_label or {}).get("what_it_is")) for item, identity in chunk]
            out.append((start, chunk, judge.request(cases)))
        said: list = [None] * len(pairs)

        def one(job):
            start, chunk, request = job
            for wait in (30, 60, 120, 0):
                try:
                    batch = provider.structured_call(request)[0]
                    said[start:start + len(chunk)] = judge.read(batch, len(chunk))
                    return
                except Exception as exc:  # never guessed: the batch stays unjudged
                    if "429" not in str(exc) or not wait:
                        console.print(f"[red]batch at {start}: {type(exc).__name__}: {str(exc)[:160]}[/red]")
                        return
                    time.sleep(wait)  # the free tier's rate limit: wait it out

        with ThreadPoolExecutor(max_workers=max(1, workers)) as threads:
            list(threads.map(one, out))
        return said

    def answers(splits, keep):
        out = {}
        for s in splits:
            for run in sorted((ROOT / "eval" / "testify" / "runs").glob(f"*/{s}*.jsonl")):
                for row in map(json.loads, run.read_text().splitlines()):
                    identity = (row.get("reading") or {}).get("identity") or {}
                    item = items.get(row["id"])
                    if item and item.split == s and identity and row.get("variant", "clean") == "clean" \
                            and identity.get("status") != "unknown" and keep(item, identity):
                        out.setdefault(judge.key(item.id, identity), (item, identity))
        return out

    if check:
        # A person's verdicts, then answers the rules call right put on another kind's advert.
        people = {}
        for entry in yaml.safe_load(adjudicate.PATH.read_text()) or []:
            if entry.get("verdict") in ("right", "wrong_kind", "wrong_brand", "wrong_version"):
                people[(entry["item"], re.sub(r"[^a-z0-9]", "", entry["answer"].lower()))] = entry["verdict"]
        found = answers(["dev", "test"], lambda item, identity: adjudicate._key(item.id, identity) in people)
        persons = {}
        for item, identity in found.values():
            persons.setdefault(adjudicate._key(item.id, identity), (item, identity))
        right = answers(["dev"], lambda item, identity: identity_correct(item, identity) is True)
        pool = list(right.values())
        random.Random(1).shuffle(pool)
        head = lambda item: (item.answer.kind or "").lower().split()[-1:]  # noqa: E731
        swapped = []  # (item, someone else's answer, "kind" or "same")
        for (item, _), (donor, identity) in zip(pool, pool[1:] + pool[:1]):
            if sum(w == "kind" for *_, w in swapped) < 40 and head(item) != head(donor) \
                    and identity_correct(item, identity) is False:
                swapped.append((item, identity, "kind"))
        # The harder half: another advert of the same kind, with a model of its own.
        models = [(i, o) for i, o in pool if o.get("status") == "named" and o.get("model")]
        for item, _ in pool:
            donor = next((o for i, o in models if i.answer.kind == item.answer.kind and i.id != item.id
                          and identity_correct(item, o) is False), None)
            if donor and sum(w == "same" for *_, w in swapped) < 40:
                swapped.append((item, donor, "same"))

        # One shuffled list, so no batch is all swaps or all a person's.
        cases = [("person", k, item, identity) for k, (item, identity) in persons.items()] \
            + [("swap", k, item, identity) for k, (item, identity, _) in enumerate(swapped)]
        random.Random(2).shuffle(cases)
        verdicts = ask([(item, identity) for _, _, item, identity in cases])
        said_people = [next(v for (w, k2, *_), v in zip(cases, verdicts) if w == "person" and k2 == k) for k in persons]
        said_swap = [next(v for (w, k2, *_), v in zip(cases, verdicts) if w == "swap" and k2 == k)
                     for k in range(len(swapped))]
        agree = 0
        for (k, (item, identity)), said in zip(persons.items(), said_people):
            truth = people[k]
            ok = said is not None and (said.verdict == "right") == (truth == "right")
            agree += ok
            mark = "" if ok else "  [red]disagrees[/red]"
            console.print(f"person {truth:13s} judge {said.verdict if said else 'none':13s} "
                          f"{item.answer.title.strip()[:50]!r} <- {judge.answer_line(identity)[:60]!r}{mark}")
        caught = {"kind": 0, "same": 0}
        for (item, identity, how), said in zip(swapped, said_swap):
            if said is not None and said.verdict != "right":
                caught[how] += 1
            else:
                console.print(f"swap passed: {item.answer.title.strip()[:50]!r} <- {judge.answer_line(identity)[:60]!r} "
                              f"({said.why if said else 'no answer'})")
        tried = {w: sum(how == w for *_, how in swapped) for w in caught}
        console.print(f"agrees with a person on {agree} of {len(persons)}; calls {caught['kind']} of {tried['kind']} "
                      f"answers moved to another kind's advert wrong, and {caught['same']} of {tried['same']} "
                      "moved to another advert of the same kind")
        return

    held = judge._verdicts(judge.PATH)
    todo = answers(split, lambda item, identity: identity_correct(item, identity) is False
                   and adjudicate.verdict(item.id, identity) is None)
    todo = {k: v for k, v in todo.items() if k not in held}
    if limit:
        todo = dict(list(todo.items())[:limit])
    console.print(f"{len(todo)} answers the word rules mark wrong to judge with {model}")
    pairs, judged_n, tally = list(todo.items()), 0, {}
    step = judge.BATCH * max(1, workers) * 2  # written as it goes, so a stopped run keeps what it judged
    for start in range(0, len(pairs), step):
        part = pairs[start:start + step]
        said = ask([pair for _, pair in part])
        rows = [{"item": k[0], "key": k[1], "answer": judge.answer_line(identity), "title": item.answer.title.strip(),
                 "verdict": v.verdict, "why": v.why, "by": model, "version": judge.JUDGE_VERSION}
                for (k, (item, identity)), v in zip(part, said) if v is not None]
        judge.record(rows)
        judged_n += len(rows)
        for r in rows:
            tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
        console.print(f"{judged_n} of {len(pairs)} judged: {tally}")
    console.print(f"{judged_n} judged, {len(todo) - judged_n} failed: {tally}")


@app.command("testify-label")
def testify_label(
    model: str = typer.Option("gemini-3.8-flash", help="Labelling model. A name with no slash is Google AI Studio."),
    split: str = typer.Option("dev", help="dev, test, all, or train for the training pool."),
    reviewed_only: bool = typer.Option(False, help="Only items the hand review covered, to measure agreement first."),
    market: str = typer.Option("", help="Only items from this city, for example lagos. Empty for all."),
    limit: int = typer.Option(0, help="Stop after this many items; 0 for no limit."),
    budget_usd: float = typer.Option(0.5, help="Stop once list-price spend reaches this."),
    mode: str = typer.Option("auto", help="record | replay | auto"),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
    key_env: str = typer.Option(
        "", help="The variable holding the Google key, for example GEMINI_API_1, to use a second project's free quota."
    ),
) -> None:
    """Check benchmark items photo by photo with a model, and compare it with the hand review.

    --split train checks the training pool the same way, so the fine-tuning set
    keeps a teacher's brand or model only where the benchmark's own photo check
    would. Those labels go to eval/testify/train/, which is never committed.
    """
    import yaml as _yaml

    from .providers.base import QuotaExhausted
    from .testify import label
    from .testify.convert import load_items

    _load_dotenv()
    if key_env:
        if not os.environ.get(key_env):
            raise typer.BadParameter(f"{key_env} is not set", param_hint="--key-env")
        os.environ["GOOGLE_API_KEY"] = os.environ[key_env]
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
    provider = _provider(model, fixtures, mode)
    reviews = {
        str(r["id"]): r
        for r in _yaml.safe_load((ROOT / "eval" / "testify" / "review_dev.yaml").read_text()) or []
    }
    source = "train_pool.jsonl" if split == "train" else "items.jsonl"
    items = [
        i for i in load_items(ROOT / "eval" / "testify" / source)
        if (split in ("all", "train") or i.split == split) and (not reviewed_only or i.id in reviews)
        and (not market or i.market == market)
    ]
    out_path = ROOT / "eval" / "testify" / "labels_ai" / f"{model.replace('/', '_')}.jsonl"
    if split == "train":
        out_path = ROOT / "eval" / "testify" / "train" / f"labels_{_dir_name(model)}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"]: json.loads(l) for l in out_path.read_text().splitlines()} if out_path.exists() else {}
    spend, called, skipped = 0.0, 0, 0
    for item in items:
        if limit and called >= limit:
            break
        if spend >= budget_usd:
            console.print(f"[yellow]Stopped at the {budget_usd} USD budget.[/yellow]")
            break
        photos = label.photos_for(item, ROOT)
        if not photos:
            skipped += 1
            continue
        try:
            answer, meta = provider.structured_call(label.request_for(item, photos))
        except Exception as exc:  # a failed item is reported, never guessed
            console.print(f"[red]{item.id}: {type(exc).__name__}: {str(exc)[:160]}[/red]")
            if isinstance(exc, QuotaExhausted):
                console.print("[yellow]Rerun tomorrow, or with --key-env naming a key from another "
                              "Google project.[/yellow]")
                break
            continue
        called += 1
        spend += 0.0 if meta.replayed else meta.cost_usd
        done[item.id] = {"id": item.id, "model": model, "prompt_version": label.PROMPT_VERSION, **answer.model_dump()}
        out_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sorted(done.values(), key=lambda r: r["id"])))
    console.print(f"{called} items labelled, {skipped} without photos here, list-price spend {spend:.4f} USD")
    for name, row in label.agreement(done, reviews).items():
        console.print(f"  agreement with the hand review, {name}: {row['agree']}/{row['items']} = {row['rate']}")
    ledger = ROOT / "docs" / "proof" / "spend.jsonl"
    with ledger.open("a") as fh:
        fh.write(json.dumps({
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "task": "testify-label",
            "model": model, "mode": mode, "cases": called, "spend_usd": round(spend, 4),
        }) + "\n")


@app.command("testify")
def testify_run(
    model: str = typer.Option(..., help="Model under test. A name with no slash is Google AI Studio."),
    split: str = typer.Option("dev", help="dev or test. Tune on dev only."),
    market: str = typer.Option("", help="Only items from this city, for example lagos. Empty for all."),
    limit: int = typer.Option(0, help="Stop after this many items; 0 for no limit."),
    lies: bool = typer.Option(True, help="Also run each item with a planted lie, to measure lie lift."),
    budget_usd: float = typer.Option(0.5, help="Stop once real spend reaches this."),
    mode: str = typer.Option("auto", help="record | replay | auto"),
    key_env: str = typer.Option("", help="The variable holding the Google key, for example GEMINI_API_1."),
    tag: str = typer.Option(
        "", help="A second run of the same model, such as repeat1: recorded and written apart, to measure run noise."
    ),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
    ids_file: Path = typer.Option(
        None, help="Only the adverts listed, one id per line, such as a second teacher's look at the training "
        "adverts the first read wrong (testify-train-build --wrong-ids). Needs --tag, so it is written apart."
    ),
    reads_only: bool = typer.Option(
        False, help="The read step only, no price pick: a teacher's reads for the training set."
    ),
    constructed: bool = typer.Option(
        False, help="The items with the proof taken away, and photos that cannot be priced (testify-construct)."
    ),
    variants: str = typer.Option(
        "", help="Comma list from clean, lie, truth, contra, pressure, pushback. Empty: clean and lie, "
        "or clean alone with --no-lies. truth and contra need testify-truths first. Score pushback "
        "with lie and pressure with clean in the same list: they replay free."
    ),
    condition: str = typer.Option(
        "read_pick", help="read_pick (read, then pick), witness_judge (photos-only witness, text-only judge) "
        "or joint (one call reads and picks)."
    ),
    frozen_pick: bool = typer.Option(
        False, help="Pick again from one list for every model, the comparables for the item's kind, "
        "on the model's recorded honest reads. Text only."
    ),
) -> None:
    """Score a model on Testify: checked items only, title and price never shown.

    --split train answers the training pool instead, priced only against
    training adverts, for a teacher's reads; it is never a score.
    """
    from .testify import label
    from .testify.run import run_item
    from .testify.score import against_pressure, against_pushback, score

    _load_dotenv()
    if key_env:
        if not os.environ.get(key_env):
            raise typer.BadParameter(f"{key_env} is not set", param_hint="--key-env")
        os.environ["GOOGLE_API_KEY"] = os.environ[key_env]
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
    provider = _provider(model, fixtures / tag if tag else fixtures, mode)
    everything, pool, hashes = _testify_pool(split)
    if reads_only:
        pool = []  # no comparables, so no price pick is asked for
    wanted = set(ids_file.read_text().split()) if ids_file else None
    if wanted is not None and not tag:
        raise typer.BadParameter("give the second look a --tag, so it is written apart", param_hint="--ids-file")
    chosen = [
        i for i in everything
        if i.split == split and not i.exclude and (split == "train" or i.ai_label or i.review)
        and (not market or i.market == market) and (wanted is None or i.id in wanted)
    ]
    out_dir = ROOT / "eval" / "testify" / "runs" / _dir_name(model)
    out_dir.mkdir(parents=True, exist_ok=True)
    from .testify.run import CONDITIONS

    if condition not in CONDITIONS:
        raise typer.BadParameter(f"one of {', '.join(CONDITIONS)}", param_hint="--condition")
    cond = "" if condition == "read_pick" else condition
    if frozen_pick:
        from .testify.run import frozen_pick as pick_again

        reads = {r["id"]: r for r in map(json.loads, (out_dir / f"{split}.jsonl").read_text().splitlines())
                 if r.get("variant", "clean") == "clean"}
        rows = []
        for item in chosen:
            if item.id in reads:
                rows.append(pick_again(provider, item, reads[item.id], pool, tuple(hashes.get(item.id, ()))))
        (out_dir / f"{split}.frozen_pick.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        result = score([{**r, "variant": "clean"} for r in rows], {i.id: i for i in chosen})
        result.update({"model": model, "split": split, "pick": "frozen list for the kind"})
        (out_dir / f"{split}.frozen_pick.summary.json").write_text(json.dumps(result, indent=1) + "\n")
        for key in ("items", "priced_share", "silent_wrong", "asking_price_inside_range", "priced_above_asking"):
            console.print(f"  {key}: {result[key]}")
        return
    if constructed:
        _testify_constructed(provider, everything, pool, hashes, split, out_dir,
                             ".".join(s for s in (tag, cond) if s), budget_usd, model, mode, condition)
        return
    # A run of other variants or another condition is written apart from the main
    # run it would overwrite, but its calls share the main recordings, so a
    # pushback replays the lie read.
    extra = "_".join(v.strip() for v in variants.split(",") if v.strip() not in ("", "clean", "lie"))
    suffix = ".".join(s for s in (tag, cond, extra) if s)
    name = f"{split}{'_' + market if market else ''}{'.' + suffix if suffix else ''}"
    out_path = out_dir / f"{name}.jsonl"
    wanted = [v.strip() for v in variants.split(",") if v.strip()] or (["clean", "lie"] if lies else ["clean"])
    facts: dict[str, dict] = {}
    if {"truth", "contra"} & set(wanted):
        facts_path = ROOT / "eval" / "testify" / "truths.jsonl"
        if not facts_path.exists():
            raise typer.BadParameter("run testify-truths first", param_hint="--variants")
        facts = {r["id"]: r for r in map(json.loads, facts_path.read_text().splitlines())
                 if r.get("checked") is not False}
    rows: list[dict] = []
    spend, done, skipped = 0.0, 0, 0
    for item in chosen:
        if limit and done >= limit:
            break
        if spend >= budget_usd:
            console.print(f"[yellow]Stopped at the {budget_usd} USD budget.[/yellow]")
            break
        photos = label.photos_for(item, ROOT)
        if not photos:
            skipped += 1
            continue
        stop = False
        asked = len(rows)
        for variant in wanted:
            planted = None
            if variant in ("truth", "contra"):
                if item.id not in facts:
                    continue
                planted = facts[item.id][variant]
            row = run_item(provider, item, photos, pool, variant, tuple(hashes.get(item.id, ())), planted, condition)
            spend += row["cost_usd"]
            rows.append(row)
            if "QuotaExhausted" in row.get("error", ""):
                stop = True  # not the model's failure: leave the item out of this score
                rows = [r for r in rows if r["id"] != item.id]
                break
        # An item with nothing to ask (no fact for a truth run) does not count toward --limit.
        done += not stop and len(rows) > asked
        out_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        if stop:
            console.print("[yellow]The free daily quota for this key is used up. Rerun tomorrow; "
                          "recorded items replay free.[/yellow]")
            break
    result = score(rows, {i.id: i for i in chosen})
    if facts:
        from .testify import truths

        result.update(truths.score(rows, facts))
    if "pushback" in wanted:
        result.update(against_pushback(rows, {i.id: i for i in chosen}))
    if "pressure" in wanted:
        result.update(against_pressure(rows, {i.id: i for i in chosen}))
    result.update({"model": model, "split": split, "market": market or "all", "skipped_no_photos": skipped})
    (out_dir / f"{name}.summary.json").write_text(json.dumps(result, indent=1) + "\n")
    for key, value in result.items():
        if key != "silent_wrong_ids":
            console.print(f"  {key}: {value}")
    ledger = ROOT / "docs" / "proof" / "spend.jsonl"
    with ledger.open("a") as fh:
        fh.write(json.dumps({
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "task": "testify",
            "model": model, "mode": mode, "cases": done, "spend_usd": round(spend, 4),
        }) + "\n")


def _testify_constructed(provider, everything, pool, hashes, split, out_dir, tag, budget_usd, model, mode,
                         condition="read_pick") -> None:
    """Run the constructed items for one split and score them against the model's honest run."""
    from .testify import construct, label
    from .testify.run import run_item

    path = ROOT / "eval" / "testify" / "constructed.jsonl"
    if not path.exists():
        raise typer.BadParameter("run testify-construct first", param_hint="--constructed")
    records = [r for r in map(json.loads, path.read_text().splitlines())
               if r["split"] == split and r.get("checked") is not False]
    items = {i.id: i for i in everything}
    name = f"{split}.constructed{'.' + tag if tag else ''}"
    out_path = out_dir / f"{name}.jsonl"
    rows: list[dict] = []
    spend, done = 0.0, 0
    for record in records:
        if spend >= budget_usd:
            console.print(f"[yellow]Stopped at the {budget_usd} USD budget.[/yellow]")
            break
        item = items[record["id"]]
        if record["route"] == "bad_photo":
            photos, variant = label.photos_for(item, ROOT), "bad_photo"
        else:
            photos, variant = [ROOT / p for p in record["photos"]], "noproof"
        if not photos or not all(p.exists() for p in photos):
            continue
        row = run_item(provider, item, photos, pool, "clean", tuple(hashes.get(item.id, ())), condition=condition)
        row["variant"] = variant
        if "QuotaExhausted" in row.get("error", ""):
            console.print("[yellow]The free daily quota for this key is used up. Rerun tomorrow; "
                          "recorded items replay free.[/yellow]")
            break
        spend += row["cost_usd"]
        rows.append(row)
        done += 1
        out_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    honest = out_dir / f"{split}{'.' + condition if condition != 'read_pick' else ''}.jsonl"
    clean = [json.loads(line) for line in honest.read_text().splitlines()] if honest.exists() else None
    result = construct.score(rows, records, items, clean)
    result.update({"model": model, "split": split})
    (out_dir / f"{name}.summary.json").write_text(json.dumps(result, indent=1) + "\n")
    for key, value in result.items():
        console.print(f"  {key}: {value}")
    with (ROOT / "docs" / "proof" / "spend.jsonl").open("a") as fh:
        fh.write(json.dumps({
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "task": "testify-constructed",
            "model": model, "mode": mode, "cases": done, "spend_usd": round(spend, 4),
        }) + "\n")


def _testify_pool(split: str):
    """The items a split draws on, the comparables they are priced against, and photo hashes.

    Training items are priced only against training adverts: a benchmark
    advert's title and asking price inside a training prompt would teach the
    benchmark's answers.
    """
    from .testify import comparables
    from .testify.convert import load_items

    if split == "train":
        items = load_items(ROOT / "eval" / "testify" / "train_pool.jsonl")
        hashes = comparables.photo_hashes(items, ROOT, cache=ROOT / "eval" / "testify" / "train_photo_hashes.json")
    else:
        items = load_items(ROOT / "eval" / "testify" / "items.jsonl")
        hashes = comparables.photo_hashes(items, ROOT)
    return items, comparables.build_pool(items, hashes), hashes


def _testify_cases(split: str, market: str):
    """Checked, scored items with photos here, and the comparables pool, for one split and city."""
    from .testify import label

    everything, pool, hashes = _testify_pool(split)
    cases = []
    for item in everything:
        if item.split != split or item.exclude or not (split == "train" or item.ai_label or item.review):
            continue
        if market and item.market != market:
            continue
        photos = label.photos_for(item, ROOT)
        if photos:
            cases.append((item, photos, tuple(hashes.get(item.id, ()))))
    return cases, pool


@app.command("testify-export")
def testify_export(
    model: str = typer.Option("agent:claude", help="Who sits the test, as agent:<name> or human:<name>."),
    split: str = typer.Option("dev"),
    market: str = typer.Option(""),
    lies: bool = typer.Option(True),
    tag: str = typer.Option("", help="A second sitting, such as repeat1, recorded apart like testify --tag."),
    out: Path = typer.Option(None, help="Defaults to eval/testify/sittings/<name>/<split>_<market>[.<tag>]."),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
) -> None:
    """Write the cases a person or an agent still has to answer, one folder each."""
    from .testify import sitting

    name = _dir_name(model)
    out = out or _sitting_dir(name, split, market, tag)
    cases, pool = _testify_cases(split, market)
    n = sitting.export((fixtures / tag if tag else fixtures) / name, cases, pool, out, lies)
    console.print(f"{n} cases to answer in {out}; the index is {sitting.index_path(out)}")


@app.command("testify-import")
def testify_import(
    model: str = typer.Option("agent:claude"),
    split: str = typer.Option("dev"),
    market: str = typer.Option(""),
    tag: str = typer.Option(""),
    out: Path = typer.Option(None),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
) -> None:
    """Record the answers written in the exported folders, then run testify --mode replay to score them."""
    from .testify import sitting

    name = _dir_name(model)
    out = out or _sitting_dir(name, split, market, tag)
    console.print(sitting.import_answers((fixtures / tag if tag else fixtures) / name, out, model))


@app.command("testify-batch-export")
def testify_batch_export(
    model: str = typer.Option(..., help="The model the batch is for, as local:<vendor>/<model>."),
    split: str = typer.Option("dev"),
    market: str = typer.Option(""),
    lies: bool = typer.Option(True),
    tag: str = typer.Option("", help="A second run, such as repeat1, recorded apart like testify --tag."),
    out: Path = typer.Option(None, help="Defaults to eval/testify/batches/<model>/<split>_<market>[.<tag>].jsonl."),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
) -> None:
    """Write the requests a model run on your own GPU still has to answer, one JSON line each.

    Run them anywhere that speaks the chat format (vLLM, a lab cluster), then
    testify-batch-import the answers. Reads come first; export again for the
    price picks those reads lead to.
    """
    from .testify import sitting

    name = _dir_name(model)
    out = out or _batch_path(name, split, market, tag)
    cases, pool = _testify_cases(split, market)
    n = sitting.export_batch((fixtures / tag if tag else fixtures) / name, cases, pool, out, lies)
    console.print(f"{n} requests to answer in {out}")


@app.command("testify-batch-import")
def testify_batch_import(
    model: str = typer.Option(...),
    results: Path = typer.Option(..., help="One JSON line per answer: custom_id and text."),
    split: str = typer.Option("dev"),
    market: str = typer.Option(""),
    tag: str = typer.Option(""),
    batch: Path = typer.Option(None, help="The exported batch these answer. Defaults to the export's path."),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
) -> None:
    """Record a batch's answers, then run testify --mode replay to score them."""
    from .testify import sitting

    name = _dir_name(model)
    batch = batch or _batch_path(name, split, market, tag)
    console.print(sitting.import_batch((fixtures / tag if tag else fixtures) / name, batch, results, model))


def _batch_path(name: str, split: str, market: str, tag: str) -> Path:
    return ROOT / "eval" / "testify" / "batches" / name / f"{split}{'_' + market if market else ''}{'.' + tag if tag else ''}.jsonl"


@app.command("testify-ocr")
def testify_ocr() -> None:
    """Read the first four photos of every benchmark and training advert once with the local OCR. Free."""
    from .testify.convert import load_items
    from .testify.label import photos_for
    from .testify.ocr_cache import OcrCache

    ocr = OcrCache(ROOT)
    items = load_items(ROOT / "eval" / "testify" / "train_pool.jsonl") + [
        i for i in load_items(ROOT / "eval" / "testify" / "items.jsonl") if i.split in ("dev", "test")]
    for n, item in enumerate(items, 1):
        for photo in photos_for(item, ROOT)[:4]:
            ocr.scored(photo)
        if ocr.added >= 200:
            ocr.save()
            console.print(f"  {n} of {len(items)} adverts read")
    ocr.save()
    console.print(f"{len(ocr.lines_read)} photos read, kept in {ocr.path}")


@app.command("testify-train-build")
def testify_train_build(
    teacher: str = typer.Option(
        "kaggle:google/gemini-3-flash-preview,gemini-3-flash-preview,nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b",
        help="The model whose reads are the targets, or several joined by commas, in order of trust: Gemini "
        "on Kaggle's quota and on Google's free tier, then Nemotron for the adverts no Gemini quota reached "
        "(29 Oct). An advert read by several is taught from the first read that is right about it.",
    ),
    market: str = typer.Option("", help="Only training items from this city. Empty for all."),
    out: Path = typer.Option(None, help="Defaults to eval/testify/train/sft.jsonl, which is never committed."),
    new_per_used: float = typer.Option(1.0, help="Dealers' new-stock adverts kept per second-hand one."),
    pick_teacher: str = typer.Option(
        "kaggle:google/gemini-3-flash-preview,nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b",
        help="Whose recorded picks are the price step's targets, in order of trust. Empty for the "
        "asking-price rule of the second run.",
    ),
    record_picks: str = typer.Option(
        "", help="A model that answers, live, every price step no teacher has answered yet, before the build."
    ),
    workers: int = typer.Option(6, help="Price steps asked at once while recording."),
    wrong_ids: Path = typer.Option(
        None, help="Write the ids of adverts no teacher read right, one per line, for another teacher to read "
        "(testify --ids-file)."
    ),
) -> None:
    """Build the fine-tuning set from a teacher's reads of the training pool.

    Run the teacher first: testify --model <teacher> --split train --no-lies
    --reads-only, and testify-ocr to read the photos once. Only reads right
    about the item are kept, a known item is priced at its worst case, and each
    example gets a lied-to twin; where a photo shows a fact, a true-claim and a
    false-claim twin too, and where a photo carries the label, a twin with it
    taken away that asks for it. A priced example also teaches the price step:
    a teacher's own pick from the training adverts found for it, kept where
    it offers no more than the asking price, and one in six refuses a list
    for another kind. A branded advert with no model named asks for its
    label instead of a price. The pick is text only: --record-picks asks a
    model for every one no teacher has answered, at once, before the build. A
    brand or model on an advert no labeller checked stays only if the local
    OCR found it on a photo. No advert from a seller who is also in the
    benchmark is used, and new stock is capped against second-hand adverts.
    """
    from collections import Counter

    from .testify import train

    out = out or ROOT / "eval" / "testify" / "train" / "sft.jsonl"
    # The pool is training adverts only, so no benchmark price reaches a training prompt.
    cases, pool = _testify_cases("train", market)
    hashes = {item.id: own for item, _, own in cases}
    # Every teacher's reads, in order of trust; a failed read is no read.
    rows = []
    for route in teacher.split(","):
        runs = ROOT / "eval" / "testify" / "runs" / _dir_name(route.strip())
        for path in sorted(runs.glob("train*.jsonl")):
            if ".repeat" in path.name:
                continue
            rows += [row for line in path.read_text().splitlines()
                     if line.strip() and not (row := json.loads(line)).get("error")]
    # The most trusted teacher's name for each advert.
    rows_by_id = {r["id"]: ((r.get("reading") or {}).get("identity") or {}) for r in reversed(rows)}
    # The benchmark's photo check, and the same check run on the training pool.
    labels = {}
    for labels_path in (ROOT / "eval" / "testify" / "labels_ai" / "gemini-3.5-flash-lite.jsonl",
                        *sorted((ROOT / "eval" / "testify" / "train").glob("labels_*.jsonl"))):
        if labels_path.exists():
            labels.update({json.loads(line)["id"]: json.loads(line)
                           for line in labels_path.read_text().splitlines() if line})
    from .identify.ocr import default_reader

    from .protocols.schema import load_protocols
    from .testify import construct, sellers, truths
    from .testify.convert import load_items
    from .testify.label import photos_for
    from .testify.ocr_cache import OcrCache

    if default_reader() is None:
        console.print("[yellow]The OCR engine is not installed: every model name on an advert with no "
                      "photo check is cut to the kind, and no seller, fact or label is read.[/yellow]")
    ocr = OcrCache(ROOT, live=False)

    # No training advert from a seller who is also in the benchmark: Jiji's photo
    # stamp and the phone number in the seller's words name the seller. The
    # stamp is on every photo, so the first one is enough.
    def seller_keys(item, photos):
        return sellers.keys([ocr.scored(p) for p in photos[:1]], item.seller_text)

    held = set()
    for item in load_items(ROOT / "eval" / "testify" / "items.jsonl"):
        if item.split in ("dev", "test"):
            held |= seller_keys(item, photos_for(item, ROOT))
    exact = {k for k in held if k.startswith("phone:")}
    names = [k for k in held if k.startswith("name:")]
    kept, shared = [], 0
    for item, photos, _ in cases:
        mine = seller_keys(item, photos)
        if mine & exact or any(sellers.same(k, n) for k in mine if k.startswith("name:") for n in names):
            shared += 1
            continue
        kept.append((item, photos))
    # New stock is all clean dealer photos and all "price"; unchecked, it was
    # three adverts in four and the first trained model priced everything (29
    # Oct). The ones kept are chosen by id, so a rebuild keeps the same ones.
    used = [c for c in kept if c[0].answer.price.used is not False]
    new = sorted((c for c in kept if c[0].answer.price.used is False),
                 key=lambda c: hashlib.md5(c[0].id.encode()).hexdigest())
    capped = len(new) - min(len(new), round(new_per_used * len(used)))
    kept = used + new[: len(new) - capped]

    rival_of = truths.rivals()
    facts = {item.id: f for item, photos in kept if (f := truths.fact(item, photos, ocr.lines, rival_of))}
    images = ROOT / "eval" / "raw" / "testify_train_constructed"
    # A painted photo is new, so it is read live: the code must be gone from it,
    # and a brand it still shows stays in the answer.
    live = OcrCache(ROOT)
    noproof = {}
    for item, photos in kept:
        tier = (labels.get(item.id) or {}).get("tier")
        if tier == "branded_electronics":
            record = construct.construct(item.model_copy(update={"tier": tier}), photos, live.boxes, images, ROOT)
            if record:
                brand = (rows_by_id.get(item.id) or {}).get("brand") or ""
                record["brand_seen"] = next(
                    (k for k, p in enumerate(record["photos"])
                     if brand and any(construct.carries(re.sub(r"[^a-z0-9]", "", brand.lower()), line)
                                      for line in live.lines(ROOT / p))), None)
                noproof[item.id] = record
    live.save()
    protocols = load_protocols(ROOT / "protocols")

    def ask_for(item):
        protocol = protocols.get(item.answer.category or "") or protocols["generic"]
        shot = next((s for s in protocol.shots if {"model", "model_name", "vin"} & set(s.extract)), None)
        return (shot or next(s for s in protocols["generic"].shots if s.id == "label_or_plate")).ask

    def build(pick_choice, misread=None):
        return train.build(kept, rows, labels, ROOT, ocr=ocr, facts=facts, noproof=noproof, ask_for=ask_for,
                           pool=pool, hashes=hashes, pick_choice=pick_choice, misread=misread)

    from .providers.base import MissingFixture

    fixtures = ROOT / "eval" / "fixtures"
    teachers = [_provider(m.strip(), fixtures, "replay") for m in pick_teacher.split(",") if m.strip()]

    def taught(request):
        for teacher_ in teachers:
            try:
                return teacher_.structured_call(request)[0]
            except MissingFixture:
                continue
        return None

    if record_picks:
        # The price step is text only, so it is asked apart and at once, then the build replays it.
        missing = []

        def wanted(request):
            if taught(request) is None:
                missing.append(request)
            return None

        build(wanted)
        live = _provider(record_picks, fixtures, "auto")

        def ask(request):
            try:
                return live.structured_call(request)[1].cost_usd
            except Exception as exc:  # a failed step is reported, never guessed
                console.print(f"[red]price step: {type(exc).__name__}: {str(exc)[:160]}[/red]")
                return None

        with ThreadPoolExecutor(max_workers=max(1, workers)) as threads:
            costs = list(threads.map(ask, missing))
        answered = [c for c in costs if c is not None]
        console.print(f"{len(answered)} of {len(missing)} price steps answered by {record_picks}")
        with (ROOT / "docs" / "proof" / "spend.jsonl").open("a") as fh:
            fh.write(json.dumps({
                "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "task": "testify-train-picks",
                "model": record_picks, "mode": "auto", "cases": len(answered), "spend_usd": round(sum(answered), 4),
            }) + "\n")
        if record_picks not in pick_teacher.split(","):
            teachers.append(_provider(record_picks, fixtures, "replay"))

    misread: list[str] = []
    examples, tally = build(taught if teachers else None, misread)
    ocr.save()
    if wrong_ids:
        wrong_ids.write_text("".join(f"{i}\n" for i in misread))
        console.print(f"{len(misread)} adverts no teacher read right written to {wrong_ids}")
    tally["seller also in the benchmark, left out"] = shared
    tally["new stock over the cap, left out"] = capped
    train.write(examples, out)
    console.print(f"{len(examples)} examples from {sum(e['variant'] == 'clean' for e in examples)} items "
                  f"written to {out}")
    for why, n in sorted(tally.items(), key=lambda kv: -kv[1]):
        console.print(f"  {n:5d}  {why}")
    for city, n in sorted(Counter(e["market"] for e in examples if e["variant"] == "clean").items()):
        console.print(f"  {n:5d}  items from {city}")


def _sitting_dir(name: str, split: str, market: str, tag: str) -> Path:
    return ROOT / "eval" / "testify" / "sittings" / name / f"{split}{'_' + market if market else ''}{'.' + tag if tag else ''}"


@app.command("testify-score")
def testify_score(
    model: str = typer.Option(..., help="The model whose recorded answers to score."),
    split: str = typer.Option("dev"),
    market: str = typer.Option(""),
    against: str = typer.Option("", help="The tag of an honest repeat, such as repeat1, to measure a lie against noise."),
) -> None:
    """Score a run's recorded answers again, for nothing: no model is called."""
    from .testify.convert import load_items
    from .testify.score import against_repeat, score

    name = f"{split}{'_' + market if market else ''}"
    out_dir = ROOT / "eval" / "testify" / "runs" / _dir_name(model)
    rows = [json.loads(line) for line in (out_dir / f"{name}.jsonl").read_text().splitlines() if line.strip()]
    items = {i.id: i for i in load_items(ROOT / "eval" / "testify" / "items.jsonl")}
    result = score(rows, {r["id"]: items[r["id"]] for r in rows if r["id"] in items})
    if against:
        repeat = [json.loads(line) for line in (out_dir / f"{name}.{against}.jsonl").read_text().splitlines() if line.strip()]
        result.update(against_repeat(rows, repeat, items))
    result.update({"model": model, "split": split, "market": market or "all"})
    (out_dir / f"{name}.summary.json").write_text(json.dumps(result, indent=1) + "\n")
    for key, value in result.items():
        console.print(f"  {key}: {value}")


@app.command("testify-release")
def testify_release(
    out: Path = typer.Option(Path("release/testify-v0.1"), help="Where to write the release files."),
) -> None:
    """Write the public release: links and labels only, checked for anything private first."""
    from .testify import comparables, release
    from .testify.convert import load_items

    items = load_items(ROOT / "eval" / "testify" / "items.jsonl")
    hashes = comparables.photo_hashes(items, ROOT)
    stats = release.build(items, hashes, ROOT, ROOT / out if not out.is_absolute() else out)
    console.print(stats)


@app.command("testify-publish")
def testify_publish(
    repo: str = typer.Option("godzilla1215/testify", help="The Hugging Face dataset to create or update."),
    folder: Path = typer.Option(Path("release/testify-v0.1")),
) -> None:
    """Upload a built release to Hugging Face as a public dataset. Only with the owner's yes."""
    from huggingface_hub import HfApi

    from .testify import release

    _load_dotenv()
    path = folder if folder.is_absolute() else ROOT / folder
    stats = json.loads((path / "stats.json").read_text())
    api = HfApi(token=os.environ.get("HF_TOKEN"))
    api.create_repo(repo, repo_type="dataset", exist_ok=True, private=False)
    api.upload_folder(
        folder_path=str(path), repo_id=repo, repo_type="dataset",
        commit_message=f"Testify v{stats['version']}: {stats['dev']} dev items, {stats['test']} test items",
    )
    console.print(f"published https://huggingface.co/datasets/{repo} (release v{release.VERSION})")


@app.command("testify-crawl")
def testify_crawl(
    region: list[str] = typer.Option(["lagos"], help="Jiji cities, as in its web address: lagos, abuja, rivers, oyo."),
    slug: list[str] = typer.Option(None, help="Jiji category slugs; every one in testify/crawl.py by default."),
    pages: int = typer.Option(100, help="Listing pages per category and city, about two dozen adverts each."),
    keep: int = typer.Option(400, help="New second-hand adverts kept per category and city in one run."),
    max_photos: int = typer.Option(3, help="Photos per advert."),
) -> None:
    """Page through whole Jiji categories for second-hand training adverts. Run from an ordinary connection."""
    from .testify import crawl
    from .testify import fetch as wider

    slugs = slug or list(crawl.CATEGORIES)
    bad = [s for s in slugs if not crawl.valid_slug(s)]
    if bad:
        raise typer.BadParameter(f"not a Jiji category slug: {', '.join(bad)}")
    raw = ROOT / "eval" / "raw"
    avoid = wider.benchmark_ids(raw / "testify")
    held = crawl.held_ids(raw / "testify_train", raw / "testify_new")
    for city in region:
        for s in slugs:
            tally = crawl.crawl(raw / "testify_crawl", city, s, pages=pages, keep=keep, max_photos=max_photos,
                                avoid=avoid, held=held, progress=console.print)
            console.print(f"[bold]{city} {s}[/bold]: {tally}")
    console.print(f"{len(wider.load(raw / 'testify_crawl'))} crawled adverts cached in {raw / 'testify_crawl'}")


@app.command("testify-fetch")
def testify_fetch(
    out: Path = typer.Option(
        None,
        help="Defaults to eval/raw/testify; eval/raw/testify_new with --new-stock; eval/raw/testify_train with --for-training.",
    ),
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
    for_training: bool = typer.Option(
        False,
        help="Fetch second-hand adverts as training data, kept apart from the benchmark. Use it for any new city.",
    ),
    more_words: bool = typer.Option(
        False, help="With --for-training: also search the makers and models the market names, for many more adverts."
    ),
) -> None:
    """Cache Jiji adverts for small goods and material lots. Run from an ordinary connection."""
    from .testify import fetch as wider

    if new_stock and for_training:
        raise typer.BadParameter("--new-stock is already training data; pick one of --new-stock and --for-training")
    if more_words and not for_training:
        raise typer.BadParameter("--more-words is for training data only: add --for-training")
    pool = "new" if new_stock else "used"
    cache = "testify_new" if new_stock else "testify_train" if for_training else "testify"
    out = out or ROOT / "eval" / "raw" / cache
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
        more_words=more_words,
        avoid=wider.benchmark_ids(ROOT / "eval" / "raw" / "testify") if for_training or new_stock else frozenset(),
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
