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
    ("material_lot", "plastic", ("plastic scrap", "pet bottles"), ("plastic", " pet ")),
    # Where Nigeria's second-hand trade actually is. The first fetch found no
    # used fans, blenders or fridges on Jiji at all: those go through WhatsApp
    # and scrap buyers. Tokunbo parts, tools, furniture and work equipment do
    # trade used in public, so these kinds were added after it.
    ("small_goods", "car engine", ("car engine", "engine for sale"), ("engine",)),
    ("small_goods", "gearbox", ("gearbox", "gear box"), ("gearbox", "gear box")),
    ("small_goods", "car headlamp", ("headlamp", "head light"), ("headlamp", "head lamp", "headlight", "head light")),
    ("small_goods", "car alternator", ("alternator",), ("alternator",)),
    ("small_goods", "tyres", ("tyres", "tires"), ("tyre", "tire")),
    ("small_goods", "game console", ("ps4", "ps5", "xbox one"), ("ps4", "ps5", "playstation", "xbox")),
    ("small_goods", "camera", ("dslr camera", "canon camera", "nikon camera"), ("camera", "canon", "nikon")),
    ("small_goods", "drilling machine", ("drilling machine", "hand drill"), ("drill",)),
    ("small_goods", "welding machine", ("welding machine",), ("welding",)),
    ("small_goods", "bicycle", ("bicycle", "bike for sale"), ("bicycle", "bike")),
    ("small_goods", "motorcycle", ("motorcycle", "okada bike"), ("motorcycle", "okada", "bajaj", "motor bike")),
    ("small_goods", "wardrobe", ("wardrobe",), ("wardrobe",)),
    ("small_goods", "bed frame", ("bed frame", "bed for sale"), ("bed",)),
    ("small_goods", "dining table", ("dining table", "dining set"), ("dining",)),
    ("small_goods", "office desk", ("office desk", "office table"), ("desk", "table")),
    ("small_goods", "filing cabinet", ("filing cabinet", "steel cabinet"), ("cabinet",)),
    ("small_goods", "salon equipment", ("salon chair", "hair dryer salon"), ("salon", "dryer")),
    ("small_goods", "industrial sewing machine", ("industrial sewing machine", "embroidery machine"), ("sewing", "embroidery")),
    ("small_goods", "printer", ("printer", "photocopier"), ("printer", "photocopier", "copier")),
    ("small_goods", "keyboard instrument", ("yamaha keyboard", "piano keyboard"), ("keyboard", "piano")),
    ("small_goods", "plastic drum", ("plastic drum", "200 litres drum"), ("drum",)),
    ("small_goods", "gas cylinder", ("gas cylinder", "cooking gas cylinder"), ("cylinder",)),
    ("material_lot", "used clothes bale", ("okrika bale", "bale of clothes"), ("bale", "okrika")),
    ("material_lot", "pallets", ("wooden pallets", "pallets"), ("pallet",)),
    ("material_lot", "scrap tyres", ("scrap tyres", "waste tyres"), ("tyre", "tire")),
    ("material_lot", "used books", ("used books", "textbooks"), ("book",)),
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


# A word in front of a search is dropped for the rest of a run once it has
# found nothing new this many times in a row. On the first city runs "used",
# "tokunbo", "fairly used" and "UK used" found nothing on hundreds of
# searches: Jiji answers them with the adverts the plain phrase already got.
DRY_LIMIT = 8


def _variants(phrases: tuple[str, ...], pool: str) -> list[tuple[str, str | None]]:
    """Each phrasing with the word put in front of it, or None for the phrase as written."""
    out: list[tuple[str, str | None]] = []
    seen: set[str] = set()
    words = SECOND_HAND if pool == "used" else ("brand new",)
    for phrase in phrases:
        base = phrase.removeprefix("used ").strip()
        for candidate, word in ((phrase, None), *((f"{w} {base}", w) for w in words)):
            if candidate not in seen:
                seen.add(candidate)
                out.append((candidate, word))
    return out


def _done(out_dir: Path, kind: str, region: str) -> bool:
    """Whether this kind was fetched for this city. Each city shows different
    adverts, so Lagos being done says nothing about Abuja. Lagos runs from
    before cities were tracked left only the kind's file behind."""
    slug = kind.replace(" ", "_")
    if (out_dir / ".done" / region / slug).exists():
        return True
    return region == "lagos" and (out_dir / f"{slug}.json").exists()


def _mark_done(out_dir: Path, kind: str, region: str) -> None:
    marker = out_dir / ".done" / region / kind.replace(" ", "_")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()


def phrasings(phrases: tuple[str, ...], pool: str = "used") -> list[str]:
    """Each phrase as written, then with every second-hand word in front.

    The new-stock pool asks plainly and as "brand new", which is how dealers
    title their adverts.
    """
    return [candidate for candidate, _ in _variants(phrases, pool)]

def keep(row: dict, pool: str = "used") -> str | None:
    """Why an advert is left out of a pool, or None to keep it.

    The used pool is the benchmark: second-hand adverts only. The new pool is
    training data for naming an item, and takes dealers' new stock only, so
    the two never share an advert.
    """
    if WANTED.search(row.get("title") or ""):
        return "buyer, not seller"
    is_new = (row.get("condition") or "").strip().lower() == "brand new"
    if pool == "used" and is_new:
        return "brand new"
    if pool == "new" and not is_new:
        return "second-hand"
    return None


def build(
    out_dir: Path,
    per_phrase: int = 25,
    region: str = "lagos",
    only: tuple[str, ...] = (),
    max_photos: int = 3,
    progress=None,
    skip_done: bool = False,
    pool: str = "used",
) -> dict[str, dict[str, int]]:
    """Fetch every kind in every phrasing, keeping second-hand adverts only.

    Adds to what is already cached, so a rerun only grows the set. New stock
    and buyers' adverts are skipped before any photo is downloaded.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, dict[str, int]] = {}
    chosen = [k for k in KINDS if (not only or k[1] in only) and not (skip_done and _done(out_dir, k[1], region))]
    total = sum(len(phrasings(k[2], pool)) for k in chosen)
    done = 0
    dry: dict[str, int] = {}
    with httpx.Client(headers={"User-Agent": UA}, timeout=30.0) as client:
        for tier, kind, phrases, words in chosen:
            path = out_dir / f"{kind.replace(' ', '_')}.json"
            seen: dict[str, dict] = {}
            if path.exists():
                for row in json.loads(path.read_text()):
                    if keep(row, pool) is None:
                        seen[row["id"]] = row
            tally = {"kept": 0, "brand new": 0, "second-hand": 0, "buyer, not seller": 0, "timed out": 0}
            for phrase, word in _variants(phrases, pool):
                if word and dry.get(word, 0) >= DRY_LIMIT:
                    done += 1
                    continue
                q = Query(category=kind, query=phrase, must_include=words)
                found = _patiently(lambda: fetch_category(q, per_phrase, region=region, max_pages=3, client=client))
                if found is None:
                    tally["timed out"] += 1
                    continue
                fresh = []
                for listing in found:
                    if listing.id in seen:
                        continue
                    reason = keep(listing.to_json(), pool)
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
                        row["region"] = region
                        seen[listing.id] = row
                # Saved after every phrasing, so a stopped run loses one search at most.
                path.write_text(json.dumps(list(seen.values()), indent=1))
                done += 1
                if word:
                    dry[word] = 0 if fresh else dry.get(word, 0) + 1
                    if dry[word] == DRY_LIMIT and progress:
                        progress(f"'{word}' found nothing new {DRY_LIMIT} times running; dropped for the rest of this run")
                if progress:
                    progress(f"[{done}/{total}] {phrase}: {len(fresh)} new, {len(seen)} {kind} so far")
            path.write_text(json.dumps(list(seen.values()), indent=1))
            _mark_done(out_dir, kind, region)
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
