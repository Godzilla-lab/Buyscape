"""Every advert we hold, in one folder: the private data pack, and a public one built from it.

Our data sits in several caches, one per way it was gathered: the benchmark's
searches, the tenant's own adverts, the training searches, the category crawl,
dealers' new stock and shop prices. The pack puts them together, one row per
advert, each saying where and when it came from and what it is used for, with
its photos, the photo checks and the teachers' reads beside it, and a
datasheet that counts what is inside. It stays private: the photos and the
sellers' own words are not ours to share.

`public_rows` builds the shareable version from the same rows: the link, facts
anyone can read at the link, and our own labels. Never a photo, never a
seller's words, and no answer for the benchmark's test split. It is checked
the way the Testify release is before anything is written.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from collections import Counter
from pathlib import Path

from .convert import _EMAIL, _PHONE, redact
from .release import _LOCAL, CHECK_FIELDS
from .select import BAND_NAMES, band

VERSION = "1"

# Cache folder under eval/raw: (what it is used for, how it was gathered). In
# priority order: an advert held by two caches takes the first one's role.
SOURCES: dict[str, tuple[str, str]] = {
    "testify": ("benchmark", "Jiji search, one phrasing list per kind, the benchmark's cities"),
    "buyscrap": ("tenant", "the tenant's own adverts on buyscrap.com.ng"),
    "testify_train": ("training", "Jiji search in more cities and with more phrasings, training only"),
    "testify_crawl": ("training", "Jiji category listings paged at random, training only"),
    "testify_new": ("new stock", "dealers' new stock on Jiji, for the share-of-new price route"),
    "shops": ("shop price", "new prices from the tenant's shops (Jumia, Slot, Pointek)"),
}

PUBLIC_FIELDS = ("id", "role", "split", "source", "url", "city", "area", "site_category", "kind", "price_ngn",
                 "condition",
                 "is_used", "fetched_at", "photo_count", "photo_hashes")
# What the benchmark's test split never shows: its answer.
TEST_HIDDEN = ("kind", "price_ngn", "site_category", "condition", "is_used")


def _url(url: str, cache: str) -> str:
    if url.startswith("/"):
        return "https://jiji.ng" + url
    return url


def _area(url: str) -> str | None:
    """The place in a Jiji link: a state ("lagos") or a district within one ("ikeja")."""
    if "jiji.ng/" in url:
        return url.split("jiji.ng/", 1)[1].split("/", 1)[0] or None
    return None


def _city(row: dict, url: str) -> str | None:
    """The state the advert was fetched for; a link's place only when it names no district."""
    return row.get("region") or None


def _source(row: dict, cache: str) -> str:
    if cache == "shops":
        return str(row.get("source") or "shop").removeprefix("shop:")
    return "buyscrap" if cache == "buyscrap" else "jiji"


def benchmark_index(items_path: Path) -> dict[str, dict]:
    """The benchmark's items keyed by the advert they came from: by photo folder, and by link."""
    index: dict[str, dict] = {}
    if not items_path.exists():
        return index
    for line in items_path.read_text().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        entry = {"benchmark_id": item["id"], "split": item.get("split"), "left_out": item.get("exclude"),
                 "market": item.get("market"),
                 "photo_check": item.get("review") or item.get("ai_label")}
        folder = Path((item.get("photos") or {}).get("cache") or "").name
        if folder and folder != "media":
            index[folder] = entry
        if item.get("url"):
            index[item["url"]] = entry
    return index


def gather(raw: Path, bench: dict[str, dict]) -> list[dict]:
    """One row per advert across every cache, the first cache in SOURCES taking it."""
    rows: dict[str, dict] = {}
    for cache, (role, _) in SOURCES.items():
        for path in sorted((raw / cache).glob("*.json")):
            try:
                adverts = json.loads(path.read_text())
            except json.JSONDecodeError:
                continue
            if not isinstance(adverts, list):
                continue
            for advert in adverts:
                if not isinstance(advert, dict) or not advert.get("id"):
                    continue
                key = str(advert["id"])
                if key in rows:
                    if cache not in rows[key]["also_in"] and cache != rows[key]["cache"]:
                        rows[key]["also_in"].append(cache)
                    continue
                url = _url(str(advert.get("url") or ""), cache)
                hit = bench.get(key) or bench.get(url) or {}
                rows[key] = {
                    "id": key,
                    # A benchmark search's advert that never became an item (a buyer, no photo), or that
                    # the photo check left out, is held back; it keeps its split so it is never trained on.
                    "role": ("benchmark" if hit and not hit.get("left_out") else
                             "held back" if hit or role == "benchmark" else role),
                    "split": hit.get("split") or ("train" if role == "training" else None),
                    "benchmark_id": hit.get("benchmark_id"),
                    "left_out": hit.get("left_out"),
                    "source": _source(advert, cache),
                    "cache": cache,
                    "also_in": [],
                    "url": url,
                    "city": (hit.get("market") or _city(advert, url)) if cache != "shops" else "online",
                    "area": _area(url),
                    # What it is: our search kind, the crawl's site category, a shop's or the tenant's category.
                    "kind": advert.get("kind") or advert.get("category"),
                    "site_category": advert.get("site_category"),
                    "protocol": advert.get("protocol"),
                    "tier": advert.get("tier"),
                    "title": advert.get("title"),
                    "price_ngn": advert.get("price_ngn"),
                    "condition": advert.get("condition") or None,
                    "is_used": advert.get("is_used"),
                    "attrs": advert.get("attrs") or {},
                    # Item fields only: a phone number or an email in the seller's text is never kept.
                    "description": redact(advert.get("description")),
                    "fetched_at": advert.get("fetched_at"),
                    "media": [str(m) for m in advert.get("media") or []],
                    "photo_check": hit.get("photo_check"),
                }
    return list(rows.values())


def _place(src: Path, dst: Path, copy: bool) -> bool:
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return True
    if not copy:
        try:
            os.link(src, dst)
            return True
        except OSError:
            pass
    shutil.copy2(src, dst)
    return True


def place_photos(rows: list[dict], raw: Path, out: Path, copy: bool = False) -> tuple[int, int, int]:
    """Each advert's photos under photos/<id>/, linked rather than copied when the disk allows.

    Returns (photos placed, photos missing, bytes)."""
    placed = missing = size = 0
    for row in rows:
        paths = []
        for media in row.pop("media"):
            src = raw / row["cache"] / "media" / media
            dst = out / "photos" / row["id"] / Path(media).name
            if _place(src, dst, copy):
                paths.append(f"photos/{row['id']}/{dst.name}")
                placed += 1
                size += dst.stat().st_size
            else:
                missing += 1
        row["photos"] = paths
    return placed, missing, size


def _jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def annotations(root: Path, ids: set[str]) -> tuple[list[dict], list[dict], dict[str, list[str]]]:
    """The photo checks, the teachers' reads and the photo hashes for the adverts in the pack."""
    checks = [r for r in _jsonl(root / "eval" / "testify" / "train" / "labels_gemini-3.5-flash-lite.jsonl")
              if r.get("id") in ids]
    reads: dict[tuple[str, str], dict] = {}
    for path in sorted((root / "eval" / "testify" / "runs").glob("*/train*.jsonl")):
        for row in _jsonl(path):
            if row.get("id") in ids and row.get("reading") and not row.get("error"):
                reads[(row["id"], path.parent.name)] = {"id": row["id"], "model": path.parent.name,
                                                         "reading": row["reading"]}
    hashes: dict[str, list[str]] = {}
    for name in ("photo_hashes.json", "train_photo_hashes.json"):
        path = root / "eval" / "testify" / name
        if path.exists():
            hashes.update(json.loads(path.read_text()))
    return checks, list(reads.values()), hashes


def condition_of(row: dict) -> str:
    condition = (row.get("condition") or "").strip().lower()
    if condition == "brand new" or row["role"] in ("new stock", "shop price"):
        return "new"
    if row.get("is_used") or condition:
        return "used, by the site's field"
    return "used, by the seller's words" if row["role"] == "training" else "not stated"


def stats(rows: list[dict], photos: tuple[int, int, int], checks: list[dict], reads: list[dict]) -> dict:
    priced = [r for r in rows if isinstance(r.get("price_ngn"), (int, float)) and r["price_ngn"] > 0]
    dates = sorted(r["fetched_at"][:10] for r in rows if r.get("fetched_at"))
    return {
        "version": VERSION,
        "adverts": len(rows),
        "photos": photos[0],
        "photos_missing": photos[1],
        "photo_megabytes": round(photos[2] / 1e6),
        "first_fetched": dates[0] if dates else None,
        "last_fetched": dates[-1] if dates else None,
        "by_role": dict(Counter(r["role"] for r in rows).most_common()),
        "by_split": dict(Counter(r["split"] or "none" for r in rows).most_common()),
        "by_source": dict(Counter(r["source"] for r in rows).most_common()),
        "by_city": dict(Counter(r["city"] or f"not stated ({r['role']})" for r in rows).most_common()),
        # Shop prices are new prices across whole ranges; the kinds count what sellers list.
        "by_kind": dict(Counter((r["kind"] or "not stated").lower() for r in rows
                                if r["role"] != "shop price").most_common()),
        "by_price_band": {BAND_NAMES[b]: n for b, n in sorted(Counter(band(int(r["price_ngn"])) for r in priced).items())},
        "by_condition": dict(Counter(condition_of(r) for r in rows).most_common()),
        "photo_checks": len(checks),
        "reads_by_model": dict(Counter(r["model"] for r in reads).most_common()),
    }


def _table(title: str, counts: dict, limit: int | None = None) -> str:
    items = list(counts.items())
    shown = items[:limit] if limit else items
    lines = [f"| {title} | Adverts |", "|---|---|"] + [f"| {k} | {v:,} |" for k, v in shown]
    if limit and len(items) > limit:
        lines.append(f"| {len(items) - limit} more | {sum(v for _, v in items[limit:]):,} |")
    return "\n".join(lines)


def datasheet(s: dict, public: bool = False) -> str:
    """A README for the pack: what is inside, where it came from, how it was chosen and what may be shared."""
    sources = "\n".join(f"| `{cache}` | {role} | {how} |" for cache, (role, how) in SOURCES.items())
    reads = "\n".join(f"| {m} | {n:,} |" for m, n in s["reads_by_model"].items()) or "| none yet | 0 |"
    if public:
        intro = "This is the public version: links and labels only, no photos and no seller's words."
        files = """| `adverts.jsonl` | One row per advert: id, role, split, source, link, city, category, kind, price, condition, date, photo count, photo hashes, and our photo check where there is one. The benchmark's test split shows only its link |"""
    else:
        intro = ("This is the private pack. It holds photos and sellers' own words, which are not ours to share;\n"
                 "`public/` holds the shareable version.")
        files = """| `adverts.jsonl` | One row per advert: id, role, split, source, link, city, category, kind, title, price, condition, details, date, photo paths |
| `photos/<id>/` | The advert's photos as the site served them |
| `annotations/photo_checks.jsonl` | A model's check of each training advert's photos: what it shows, whether the title matches, any text on the item |
| `annotations/reads.jsonl` | A teacher model's full read of an advert, the training target for the small model |
| `manifest.json` | Counts, sizes and checksums of this version |"""
    return f"""# Buyscape market data, version {s['version']}

Second-hand goods for sale in Nigeria: {s['adverts']:,} adverts with {s['photos']:,} photos
({s['photo_megabytes']:,} MB), fetched from {s['first_fetched']} to {s['last_fetched']}. Every
advert has a link, a price in naira and the date it was read. The city is the state it was fetched
for; the area is the place its link names, a state or a district.
{intro}

## What is inside

| File | What it holds |
|---|---|
{files}

## Where it came from

| Cache | Role | How it was gathered |
|---|---|---|
{sources}

- **benchmark**: the Testify items. The `test` split is never used for training or tuning.
- **held back**: found by a benchmark search but left out of it (a buyer's advert, no photo, or the
  photo check could not tell what it is). It keeps its split, so it is never trained on.
- **training**: adverts for teaching the small model. Never in the benchmark.
- **tenant**: the first business's own adverts.
- **new stock** and **shop price**: new prices, used only for the share-of-new price route.

{_table("Role", s['by_role'])}

{_table("Source", s['by_source'])}

## What it covers

{_table("City", s['by_city'], 20)}

{_table("What it is (shop prices left out)", s['by_kind'], 40)}

{_table("Price band, naira", s['by_price_band'])}

{_table("Condition", s['by_condition'])}

## Labels

{s['photo_checks']:,} training adverts have a photo check. Teacher reads by model:

| Model | Reads |
|---|---|
{reads}

## How adverts were chosen

- Sellers only: a buyer's advert ("we buy used laptops") is left out.
- Second-hand only for training: the site's condition field says used, or the seller's own
  words do ("fairly used", "tokunbo", "faulty", "for parts"). Brand new stock is kept apart.
- Pages are visited in a random order across a whole category, not only its first pages,
  which are mostly dealers' promotions.
- Phone numbers and email addresses are removed from every seller's text before it is stored.
- An advert in the benchmark is never fetched again for training.

## What may be shared

The photos and the sellers' words belong to the sellers and the site. The public version
carries the link, facts anyone can read at the link (price, city, condition, date), our own
labels and photo hashes for finding duplicates; never a photo, a title or a seller's words,
and nothing that answers the benchmark's test split. Jiji's terms are being checked with
Jiji before anything is published.

## Rebuild

`uv run buyscape data-pack` from the Buyscape repository rebuilds this folder from the caches.
"""


def public_rows(rows: list[dict], checks: dict[str, dict]) -> list[dict]:
    out = []
    for row in rows:
        public = {k: row.get(k) for k in PUBLIC_FIELDS if k not in ("photo_count", "photo_hashes")}
        public["photo_count"] = len(row.get("photos") or [])
        public["photo_hashes"] = row.get("photo_hashes") or []
        check = checks.get(row["id"]) or row.get("photo_check")
        if check and row.get("split") != "test":
            public["photo_check"] = {k: check.get(k) for k in CHECK_FIELDS}
        if row.get("split") == "test":
            for key in TEST_HIDDEN:
                public.pop(key, None)
        out.append(public)
    return out


def check_public(public: list[dict], private: list[dict]) -> list[str]:
    """Everything private found in the public rows. Empty means they may be shared."""
    text = "\n".join(json.dumps(r, ensure_ascii=False) for r in public)
    found = []
    for name, pattern in (("a phone number", _PHONE), ("an email address", _EMAIL), ("a local path", _LOCAL)):
        hit = pattern.search(text)
        if hit:
            found.append(f"{name}: {hit.group(0)!r}")
    flat = " ".join(text.split()).lower()
    for row in private:
        for words in (row.get("title"), row.get("description")):
            words = " ".join((words or "").split()).lower()
            # Long enough to be the seller's own sentence, not a phrase a link shares.
            if len(words) >= 40 and words[:40] in flat:
                found.append(f"the seller's own words for {row['id']}")
                break
    test = {r["id"] for r in private if r.get("split") == "test"}
    for row in public:
        if row["id"] in test and any(k in row for k in TEST_HIDDEN + ("photo_check",)):
            found.append(f"an answer for test advert {row['id']}")
    return found


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def build(root: Path, out: Path, copy: bool = False) -> dict:
    """Write the private pack and its public version (`out/public`). Returns the counts."""
    raw = root / "eval" / "raw"
    rows = gather(raw, benchmark_index(root / "eval" / "testify" / "items.jsonl"))
    checks, reads, hashes = annotations(root, {r["id"] for r in rows})
    by_bench = {r["benchmark_id"]: r["id"] for r in rows if r.get("benchmark_id")}
    for key, value in list(hashes.items()):
        if key in by_bench:
            hashes[by_bench[key]] = value
    for row in rows:
        row["photo_hashes"] = hashes.get(row["id"], [])
    out.mkdir(parents=True, exist_ok=True)
    photos = place_photos(rows, raw, out, copy)
    counts = stats(rows, photos, checks, reads)
    public = public_rows(rows, {c["id"]: c for c in checks})
    problems = check_public(public, rows)
    if problems:
        raise ValueError("public version not written, private data found: " + "; ".join(problems[:5]))
    _write_jsonl(out / "adverts.jsonl", rows)
    _write_jsonl(out / "annotations" / "photo_checks.jsonl", checks)
    _write_jsonl(out / "annotations" / "reads.jsonl", reads)
    (out / "README.md").write_text(datasheet(counts))
    _write_jsonl(out / "public" / "adverts.jsonl", public)
    (out / "public" / "README.md").write_text(datasheet(counts, public=True))
    files = {p.relative_to(out).as_posix(): _sha(p) for p in sorted(out.rglob("*.jsonl"))}
    (out / "manifest.json").write_text(json.dumps({**counts, "sha256": files}, indent=1) + "\n")
    return counts
