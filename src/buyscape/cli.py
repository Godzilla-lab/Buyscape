"""Buyscape command line. Everything the proof needs, nothing it does not."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .evalset import jiji, score
from .identify.catalogue import load_catalogue
from .pricing.sources import JijiComps, MaterialsFloor, ScrapIndex
from .protocols.schema import load_protocols
from .providers.base import VisionProvider
from .providers.fake import FakeProvider
from .providers.recording import RecordingProvider
from .runner import Case, report_markdown, run_case

app = typer.Typer(add_completion=False, help="Remote valuation engine for second-hand goods.")
console = Console()

ROOT = Path.cwd()
DEFAULT_READER = "qwen/qwen3-vl-32b-instruct"
DEFAULT_REASONER = "google/gemini-3.8-flash"


def _provider(model: str, fixtures: Path, mode: str) -> VisionProvider:
    """Build a provider from the model name.

    A name with no slash is a Google AI Studio model, anything else goes to
    OpenRouter. Callers never see the difference.
    """
    if model == "fake":
        return RecordingProvider(FakeProvider(), fixtures / "fake", mode="record")

    inner = None
    is_google = "/" not in model
    key = "GOOGLE_API_KEY" if is_google else "OPENROUTER_API_KEY"
    if os.environ.get(key):
        if is_google:
            from .providers.google import GoogleProvider

            inner = GoogleProvider(model)
        else:
            from .providers.openrouter import OpenRouterProvider

            inner = OpenRouterProvider(model)
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
) -> None:
    """Pull a held-out set of real Lagos listings from Jiji. Run once."""
    counts = jiji.build(out, per_category=per_category)
    for category, n in counts.items():
        console.print(f"{category:18s} {n}")


def _load_cases(raw: Path, limit: int | None, categories: list[str] | None) -> list[Case]:
    cases: list[Case] = []
    for listing in jiji.load(raw):
        if categories and listing.category not in categories:
            continue
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
) -> None:
    """Cache a large pool of used asking prices. No photos, comps only."""
    counts = jiji.build_price_pool(out, per_category=per_category)
    for category, n in counts.items():
        console.print(f"{category:18s} {n}")


@app.command("run")
def run(
    raw: Path = typer.Option(Path("eval/raw"), help="Cached test set."),
    prices: Path = typer.Option(Path("eval/prices"), help="Cached comparable prices."),
    out: Path = typer.Option(Path("docs/proof"), help="Where reports are written."),
    reader: str = typer.Option(DEFAULT_READER, help="Tier 1 model, or 'fake'."),
    reasoner: str = typer.Option(DEFAULT_REASONER, help="Tier 2 model, or 'fake'."),
    mode: str = typer.Option("auto", help="record | replay | auto"),
    limit: int = typer.Option(0, help="Cap the number of cases. 0 means all."),
    category: list[str] = typer.Option(None, help="Restrict to these categories."),
    workers: int = typer.Option(6, help="Cases to run at once. Cases are independent."),
    fixtures: Path = typer.Option(Path("eval/fixtures")),
) -> None:
    """Run the engine over the test set and write the reports and the gate."""
    protocols = load_protocols(ROOT / "protocols")
    catalogue = load_catalogue(ROOT / "catalogue")
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

    run_dir = out / f"{reader.replace('/', '_')}__{reasoner.replace('/', '_')}"
    (run_dir / "cases").mkdir(parents=True, exist_ok=True)

    def one(case: Case):
        result = run_case(
            case, protocols, catalogue, comps, scrap, reader_p, reasoner_p, materials
        )
        (run_dir / "cases" / f"{case.id}.md").write_text(report_markdown(case, result))
        return case, result

    pairs = []
    done = 0
    with console.status(f"Running {len(cases)} cases") as status:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            for case, result in pool.map(one, cases):
                done += 1
                status.update(f"[{done}/{len(cases)}] {case.id}")
                pairs.append((case, result))

    metrics = score.score(pairs)
    summary = metrics.summary()
    summary["reader"] = reader
    summary["reasoner"] = reasoner
    score.write_summary(run_dir / "summary.json", summary)

    table = Table(title=f"Buyscape proof: reader {reader}, reasoner {reasoner}")
    table.add_column("metric")
    table.add_column("value", justify="right")
    for key, value in summary.items():
        if key in ("failure_codes", "reader", "reasoner"):
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
    console.print(f"Reports: {run_dir / 'cases'}")
    console.print("[green]GATE PASSED[/green]" if all_pass else "[red]GATE NOT PASSED[/red]")


@app.command("protocols")
def check_protocols() -> None:
    """Validate every protocol file."""
    protocols = load_protocols(ROOT / "protocols")
    for name, p in protocols.items():
        opening = ", ".join(s.id for s in p.opening_shots) or "none"
        console.print(
            f"{name:18s} v{p.version} shots={len(p.shots)} "
            f"required={len(p.required_shots)} opens={opening} claims={len(p.claims)}"
        )


if __name__ == "__main__":
    app()
