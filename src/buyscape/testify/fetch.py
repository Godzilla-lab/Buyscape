"""Widen the Jiji cache beyond the six branded categories, for Testify.

The Phase 0 set is phones, laptops and big appliances. Testify needs the
other three tiers too: small goods with no model number, and material sold by
weight. Jiji's search is literal and returns about twenty adverts per
phrasing, so each kind is asked for in the words the market uses.

Jiji answers a data centre with a bot check, so this runs from an ordinary
connection, the same way fetch-testset always has. It writes under
eval/raw/testify, which is gitignored: photos never leave the machine that
fetched them, and only links and labels go into the benchmark.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import httpx

from ..evalset.jiji import UA, Query, download_media, fetch_category
from .schema import WANTED, Tier

# The words Nigerian sellers use for second-hand. Tokunbo is foreign used.
# Without them a search for a fan is mostly dealers' new stock: the first
# fetch kept 502 brand new adverts out of 700.
SECOND_HAND = ("used", "tokunbo", "fairly used", "uk used")

# (tier, kind in a buyer's words, search phrasings, words a title must carry)
KINDS: tuple[tuple[Tier, str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("small_goods", "rechargeable torchlight", ("rechargeable torchlight", "rechargeable torch light", "led torch"), ("torch",)),
    ("small_goods", "standing fan", ("standing fan", "rechargeable fan"), ("fan",)),
    ("small_goods", "pressing iron", ("pressing iron", "dry iron", "steam iron"), ("iron",)),
    ("small_goods", "electric kettle", ("electric kettle",), ("kettle",)),
    ("small_goods", "blender", ("blender", "blender and grinder"), ("blender",)),
    ("small_goods", "microwave", ("microwave oven", "used microwave"), ("microwave",)),
    ("small_goods", "gas cooker", ("gas cooker", "standing gas cooker"), ("cooker",)),
    ("small_goods", "chest freezer", ("chest freezer", "used freezer"), ("freezer",)),
    ("small_goods", "refrigerator", ("used fridge", "refrigerator"), ("fridge", "refrigerator")),
    ("small_goods", "power bank", ("power bank",), ("power bank", "powerbank")),
    ("small_goods", "UPS", ("ups for computer", "used ups"), ("ups",)),
    ("small_goods", "inverter battery", ("inverter battery", "solar battery"), ("battery",)),
    ("small_goods", "solar panel", ("used solar panel", "solar panel"), ("solar",)),
    ("small_goods", "sewing machine", ("sewing machine",), ("sewing",)),
    ("small_goods", "office chair", ("used office chair", "office chair"), ("chair",)),
    ("small_goods", "2 seater sofa", ("2 seater sofa", "2 seater couch"), ("2 seater", "two seater")),
    ("small_goods", "centre table", ("centre table", "center table"), ("table",)),
    ("small_goods", "plastic water tank", ("water tank", "plastic tank"), ("tank",)),
    ("small_goods", "car battery", ("used car battery", "car battery"), ("battery",)),
    ("small_goods", "speaker", ("bluetooth speaker", "home theatre"), ("speaker", "theatre", "theater")),
    ("material_lot", "scrap metal", ("scrap metal", "scrap iron"), ("scrap",)),
    ("material_lot", "copper wire", ("scrap copper", "copper wire"), ("copper",)),
    ("material_lot", "aluminium", ("scrap aluminium", "aluminium scrap"), ("alumin",)),
    ("material_lot", "car battery scrap", ("scrap battery", "used battery scrap"), ("scrap",)),
    ("material_lot", "carton and paper", ("used carton", "waste paper"), ("carton", "paper")),
    ("material_lot", "plastic", ("plastic scrap", "pet bottles"), ("plastic", "pet")),
)


def _patiently(call, waits: tuple[float, ...] = (15.0, 60.0)):
    """Run a fetch, waiting and retrying when Jiji is slow. None if it never answers.

    A home connection drops a request now and then, and Jiji slows down a
    client that asks too fast. Neither is a reason to lose an hour's fetch.
    """
    for wait in (*waits, None):
        try:
            return call()
        except httpx.HTTPError:
            if wait is None:
                return None
            time.sleep(wait)
    return None


def phrasings(phrases: tuple[str, ...]) -> list[str]:
    """Each phrase as written, then with every second-hand word in front."""
    out: list[str] = []
    for phrase in phrases:
        base = phrase.removeprefix("used ").strip()
        for candidate in (phrase, *(f"{word} {base}" for word in SECOND_HAND)):
            if candidate not in out:
                out.append(candidate)
    return out


def keep(row: dict) -> str | None:
    """Why an advert is left out, or None to keep it."""
    if (row.get("condition") or "").strip().lower() == "brand new":
        return "brand new"
    if WANTED.search(row.get("title") or ""):
        return "buyer, not seller"
    return None


def build(
    out_dir: Path,
    per_phrase: int = 25,
    region: str = "lagos",
    only: tuple[str, ...] = (),
    max_photos: int = 3,
    progress=None,
) -> dict[str, dict[str, int]]:
    """Fetch every kind in every phrasing, keeping second-hand adverts only.

    Adds to what is already cached, so a rerun only grows the set. New stock
    and buyers' adverts are skipped before any photo is downloaded.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, dict[str, int]] = {}
    chosen = [k for k in KINDS if not only or k[1] in only]
    total = sum(len(phrasings(k[2])) for k in chosen)
    done = 0
    with httpx.Client(headers={"User-Agent": UA}, timeout=30.0) as client:
        for tier, kind, phrases, words in chosen:
            path = out_dir / f"{kind.replace(' ', '_')}.json"
            seen: dict[str, dict] = {}
            if path.exists():
                for row in json.loads(path.read_text()):
                    if keep(row) is None:
                        seen[row["id"]] = row
            tally = {"kept": 0, "brand new": 0, "buyer, not seller": 0, "timed out": 0}
            for phrase in phrasings(phrases):
                q = Query(category=kind, query=phrase, must_include=words)
                found = _patiently(lambda: fetch_category(q, per_phrase, region=region, max_pages=3, client=client))
                if found is None:
                    tally["timed out"] += 1
                    continue
                fresh = []
                for listing in found:
                    if listing.id in seen:
                        continue
                    reason = keep(listing.to_json())
                    if reason:
                        tally[reason] += 1
                    else:
                        fresh.append(listing)
                # Three photos tell what an item is and show its condition. Eight
                # cost a slow connection hours for little more.
                for listing in fresh:
                    listing.image_urls = listing.image_urls[:max_photos]
                download_media(fresh, out_dir / "media", client=client)
                for listing in fresh:
                    if listing.media and listing.id not in seen:
                        row = listing.to_json()
                        row["tier"] = tier
                        row["kind"] = kind
                        seen[listing.id] = row
                # Saved after every phrasing, so a stopped run loses one search at most.
                path.write_text(json.dumps(list(seen.values()), indent=1))
                done += 1
                if progress:
                    progress(f"[{done}/{total}] {phrase}: {len(fresh)} new, {len(seen)} {kind} so far")
            path.write_text(json.dumps(list(seen.values()), indent=1))
            tally["kept"] = len(seen)
            counts[kind] = tally
    return counts


def load(out_dir: Path) -> list[dict]:
    """Every cached advert. Other files in the folder, such as Kaggle's
    dataset-metadata.json, are not adverts and are skipped."""
    rows: list[dict] = []
    for path in sorted(out_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            rows.extend(r for r in data if isinstance(r, dict) and "tier" in r and "kind" in r)
    return rows
