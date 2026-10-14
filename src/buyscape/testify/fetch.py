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


def build(out_dir: Path, per_phrase: int = 25, region: str = "lagos", only: tuple[str, ...] = ()) -> dict[str, dict[str, int]]:
    """Fetch every kind in every phrasing, keeping second-hand adverts only.

    Adds to what is already cached, so a rerun only grows the set. New stock
    and buyers' adverts are skipped before any photo is downloaded.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, dict[str, int]] = {}
    with httpx.Client(headers={"User-Agent": UA}, timeout=30.0) as client:
        for tier, kind, phrases, words in KINDS:
            if only and kind not in only:
                continue
            path = out_dir / f"{kind.replace(' ', '_')}.json"
            seen: dict[str, dict] = {}
            if path.exists():
                for row in json.loads(path.read_text()):
                    if keep(row) is None:
                        seen[row["id"]] = row
            tally = {"kept": 0, "brand new": 0, "buyer, not seller": 0}
            for phrase in phrasings(phrases):
                q = Query(category=kind, query=phrase, must_include=words)
                fresh = []
                for listing in fetch_category(q, per_phrase, region=region, max_pages=3, client=client):
                    if listing.id in seen:
                        continue
                    reason = keep(listing.to_json())
                    if reason:
                        tally[reason] += 1
                    else:
                        fresh.append(listing)
                download_media(fresh, out_dir / "media", client=client)
                for listing in fresh:
                    if listing.media and listing.id not in seen:
                        row = listing.to_json()
                        row["tier"] = tier
                        row["kind"] = kind
                        seen[listing.id] = row
            path.write_text(json.dumps(list(seen.values()), indent=1))
            tally["kept"] = len(seen)
            counts[kind] = tally
    return counts


def load(out_dir: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(out_dir.glob("*.json")):
        rows.extend(json.loads(path.read_text()))
    return rows
