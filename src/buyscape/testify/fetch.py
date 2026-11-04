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

from ..evalset.jiji import UA, Query, _url_width, download_media, fetch_category, page_photos, photo_number
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


# More search phrasings per kind, for training data only (--more-words). Jiji's
# search is literal and gives about twenty adverts a phrasing, so a kind asked
# for two ways stops at about forty adverts a city; the makers and models the
# market names find different adverts. Each must carry a word the kind's
# titles carry, or every advert it finds is dropped. Never a benchmark fetch.
MORE_WORDS: dict[str, tuple[str, ...]] = {
    "rechargeable torchlight": ("solar torch", "torchlight", "police torch", "led torchlight", "searchlight torch",
                                "head torch", "zoom torch", "rechargeable torch"),
    "standing fan": ("binatone standing fan", "ox standing fan", "qlink standing fan", "lontor standing fan",
                     "thermocool standing fan", "pedestal fan", "solar standing fan", "rechargeable standing fan"),
    "pressing iron": ("philips pressing iron", "binatone pressing iron", "electric iron", "industrial pressing iron",
                      "steam pressing iron", "sonik iron", "silver crest iron", "industrial dry iron"),
    "electric kettle": ("binatone kettle", "kenwood kettle", "philips kettle", "stainless kettle", "cordless kettle",
                        "silver crest kettle", "kettle for sale"),
    "blender": ("binatone blender", "kenwood blender", "philips blender", "silver crest blender", "industrial blender",
                "nutribullet blender", "qlink blender", "master chef blender"),
    "microwave": ("lg microwave", "samsung microwave", "hisense microwave", "scanfrost microwave", "kenwood microwave",
                  "midea microwave", "sharp microwave", "panasonic microwave"),
    "gas cooker": ("4 burner gas cooker", "5 burner gas cooker", "maxi gas cooker", "nexus gas cooker",
                   "scanfrost gas cooker", "thermocool gas cooker", "table top gas cooker", "polystar gas cooker",
                   "gas cooker with oven"),
    "chest freezer": ("haier thermocool freezer", "hisense freezer", "lg freezer", "nexus freezer", "scanfrost freezer",
                      "polystar freezer", "midea freezer", "deep freezer", "display freezer", "restpoint freezer"),
    "refrigerator": ("lg fridge", "samsung fridge", "hisense fridge", "haier thermocool fridge", "nexus fridge",
                     "scanfrost fridge", "double door fridge", "side by side fridge", "small fridge", "midea fridge",
                     "polystar fridge"),
    "power bank": ("oraimo power bank", "new age power bank", "anker power bank", "xiaomi power bank",
                   "20000mah power bank", "30000mah power bank", "solar power bank"),
    "UPS": ("apc ups", "mercury ups", "eaton ups", "1000va ups", "1500va ups", "online ups", "ups for sale"),
    "inverter battery": ("tubular battery", "lithium battery", "200ah battery", "220ah battery", "luminous battery",
                         "quanta battery", "felicity battery", "deep cycle battery", "gel battery", "100ah battery"),
    "solar panel": ("mono solar panel", "poly solar panel", "300w solar panel", "450w solar panel", "550w solar panel",
                    "jinko solar panel", "canadian solar panel", "200w solar panel"),
    "sewing machine": ("butterfly sewing machine", "singer sewing machine", "brother sewing machine",
                       "janome sewing machine", "electric sewing machine", "manual sewing machine"),
    "office chair": ("executive office chair", "swivel chair", "mesh office chair", "gaming chair", "visitor chair",
                     "boss chair", "conference chair"),
    "2 seater sofa": ("2 seater leather sofa", "2 seater fabric sofa", "two seater sofa", "2 seater sofa chair",
                      "2 seater recliner", "2 seater settee"),
    "centre table": ("glass centre table", "wooden centre table", "marble centre table", "coffee table",
                     "mirror centre table", "center table set"),
    "plastic water tank": ("geepee tank", "1000 litres tank", "2000 litres tank", "5000 litres tank",
                           "500 litres tank", "overhead tank", "water storage tank"),
    "car battery": ("exide battery", "varta battery", "bosch car battery", "75ah car battery", "100ah car battery",
                    "tokunbo car battery", "amaron battery"),
    "speaker": ("jbl speaker", "sony speaker", "lg home theatre", "samsung home theatre", "pa speaker",
                "active speaker", "bose speaker", "rechargeable speaker", "sony home theatre"),
    "scrap metal": ("metal scrap", "heavy metal scrap", "steel scrap", "scrap for sale", "scrap iron rods"),
    "copper wire": ("copper scrap", "copper cable", "armoured copper cable", "copper coil", "pure copper"),
    "aluminium": ("aluminium cans", "aluminium profile scrap", "aluminium wire", "aluminium sheet"),
    "car battery scrap": ("battery scrap", "dead battery scrap", "scrap batteries", "lead acid battery scrap"),
    "carton and paper": ("waste carton", "carton scrap", "paper scrap", "old newspaper", "used cartons"),
    "plastic": ("plastic waste", "pet bottle flakes", "hdpe plastic scrap", "plastic bottles", "waste plastic"),
    "car engine": ("toyota engine", "honda engine", "lexus engine", "camry engine", "corolla engine", "benz engine",
                   "tokunbo engine", "v6 engine", "hyundai engine", "nissan engine", "ford engine", "kia engine"),
    "gearbox": ("toyota gearbox", "honda gearbox", "lexus gearbox", "camry gear box", "corolla gearbox",
                "automatic gearbox", "manual gearbox", "benz gearbox", "tokunbo gearbox"),
    "car headlamp": ("toyota headlamp", "camry headlight", "corolla headlamp", "lexus headlight", "honda headlamp",
                     "benz headlamp", "highlander headlight", "tokunbo headlamp", "headlight"),
    "car alternator": ("toyota alternator", "honda alternator", "lexus alternator", "benz alternator",
                       "camry alternator", "tokunbo alternator"),
    "tyres": ("michelin tyres", "bridgestone tyres", "dunlop tyres", "tokunbo tyres", "17 inch tyres",
              "16 inch tyres", "car tyres", "jeep tyres", "continental tyres"),
    "game console": ("ps4 pro", "ps4 slim", "ps5 slim", "playstation 4", "playstation 5", "xbox series x",
                     "xbox series s", "xbox 360", "hacked ps4"),
    "camera": ("sony camera", "canon 5d", "nikon d750", "mirrorless camera", "video camera", "canon 80d",
               "nikon d3500", "fujifilm camera"),
    "drilling machine": ("dewalt drill", "bosch drill", "makita drill", "impact drill", "cordless drill",
                         "hammer drill", "electric drill", "magnetic drill"),
    "welding machine": ("inverter welding machine", "arc welding machine", "co2 welding machine",
                        "argon welding machine", "mig welding machine", "lincoln welding machine"),
    "bicycle": ("mountain bike", "children bicycle", "kids bicycle", "bmx bicycle", "sport bicycle", "road bike",
                "folding bicycle", "adult bicycle"),
    "motorcycle": ("bajaj boxer", "honda motorcycle", "suzuki motorcycle", "tvs motorcycle", "qlink motorcycle",
                   "haojue motorcycle", "jincheng motorcycle", "bajaj motorcycle", "power bike motorcycle"),
    "wardrobe": ("wooden wardrobe", "3 door wardrobe", "4 door wardrobe", "2 door wardrobe", "sliding wardrobe",
                 "mirror wardrobe"),
    "bed frame": ("6 by 6 bed", "4 by 6 bed", "upholstered bed", "wooden bed", "bunk bed", "king size bed",
                  "queen size bed", "double decker bed"),
    "dining table": ("6 seater dining", "4 seater dining", "8 seater dining", "glass dining table",
                     "wooden dining table", "marble dining table"),
    "office desk": ("executive office table", "office workstation table", "computer desk", "study desk",
                    "executive desk", "reception table", "conference table"),
    "filing cabinet": ("4 drawer filing cabinet", "metal cabinet", "office cabinet", "file cabinet",
                       "steel filing cabinet", "storage cabinet"),
    "salon equipment": ("salon hair dryer", "hood dryer", "standing hair dryer", "salon wash basin",
                        "salon trolley", "salon steamer"),
    "industrial sewing machine": ("juki sewing machine", "industrial straight sewing machine",
                                  "overlocking sewing machine", "brother industrial sewing machine",
                                  "jack sewing machine", "embroidery machine for sale"),
    "printer": ("hp printer", "canon printer", "epson printer", "laserjet printer", "konica minolta photocopier",
                "sharp photocopier", "kyocera photocopier", "ricoh copier", "large format printer"),
    "keyboard instrument": ("yamaha psr keyboard", "casio keyboard", "korg keyboard", "roland keyboard",
                            "digital piano", "yamaha piano", "61 keys keyboard", "workstation keyboard"),
    "plastic drum": ("250 litres drum", "25 litres drum", "plastic drums", "blue drum", "chemical drum",
                     "150 litres drum"),
    "gas cylinder": ("12.5kg gas cylinder", "6kg gas cylinder", "25kg gas cylinder", "50kg gas cylinder",
                     "empty gas cylinder", "3kg gas cylinder"),
    "used clothes bale": ("okrika bales", "first grade okrika", "bale of jeans", "bale of shoes", "uk bale",
                          "bale for sale"),
    "pallets": ("plastic pallets", "pallet for sale", "used pallets", "euro pallets", "pallet wood"),
    "scrap tyres": ("tyre scrap", "old tyres", "tire scrap", "used tyres scrap"),
    "used books": ("school books", "university textbooks", "law books", "medical textbooks", "children books",
                   "story books"),
}

# Kinds for training only, asked with --more-words: what BuyScrap buys and the
# benchmark's kinds miss. Faulty and broken goods are a large part of its
# trade, and its own adverts are mostly e-waste, glass, circuit boards and
# scrap cars. (tier, kind, search phrasings, words a title must carry), as in
# KINDS; a buyer's advert ("we buy faulty laptops") is dropped as in KINDS.
TRAIN_KINDS: tuple[tuple[Tier, str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("branded_electronics", "faulty television", ("faulty tv", "spoilt tv", "bad tv", "broken tv screen",
                                                  "tv for parts", "scrap tv", "cracked tv screen"), ("tv", "television")),
    ("branded_electronics", "faulty laptop", ("faulty laptop", "spoilt laptop", "broken laptop", "laptop for parts",
                                              "bad laptop", "cracked laptop screen", "dead laptop"),
     ("laptop", "macbook", "notebook")),
    ("branded_electronics", "faulty phone", ("faulty phone", "spoilt phone", "broken phone", "cracked screen phone",
                                             "phone for parts", "faulty iphone", "faulty samsung", "bad iphone"),
     ("phone", "iphone", "samsung", "tecno", "infinix", "itel", "galaxy")),
    ("small_goods", "faulty air conditioner", ("faulty ac", "spoilt ac", "scrap ac", "bad air conditioner",
                                               "faulty split unit", "scrap split ac", "ac compressor"),
     (" ac", "a/c", "air condition", "split unit", "compressor")),
    ("small_goods", "faulty refrigerator", ("faulty fridge", "spoilt fridge", "scrap fridge", "faulty freezer",
                                            "spoilt freezer", "scrap freezer", "bad fridge"),
     ("fridge", "freezer", "refrigerator")),
    ("small_goods", "faulty washing machine", ("faulty washing machine", "spoilt washing machine",
                                               "scrap washing machine", "washing machine for parts"), ("washing",)),
    ("small_goods", "faulty generator", ("faulty generator", "spoilt generator", "scrap generator",
                                         "generator for parts", "bad generator"), ("generator",)),
    ("small_goods", "faulty inverter", ("faulty inverter", "spoilt inverter", "scrap inverter", "faulty ups",
                                        "bad inverter"), ("inverter", "ups")),
    ("branded_electronics", "computer monitor", ("computer monitor", "lg monitor", "dell monitor", "hp monitor",
                                                 "samsung monitor", "faulty monitor"), ("monitor",)),
    ("branded_electronics", "desktop computer", ("system unit", "desktop computer", "all in one computer",
                                                 "hp desktop", "dell desktop"),
     ("system unit", "desktop", "all in one", "computer")),
    ("material_lot", "circuit boards", ("circuit boards", "scrap motherboard", "e waste", "ewaste", "computer scrap",
                                        "scrap pcb", "scrap ram", "electronic waste"),
     ("board", "e-waste", "e waste", "ewaste", "pcb", "electronic", "scrap", "ram")),
    ("material_lot", "glass bottles", ("glass bottles", "empty bottles", "empty glass bottles", "used bottles",
                                       "scrap glass", "broken glass", "glass cullet"), ("bottle", "glass")),
    ("material_lot", "scrap car", ("scrap car", "accidented car", "car for scrap", "scrap vehicle", "accident car",
                                   "rickety car", "car scrap"), ("scrap", "accident", "rickety")),
    ("small_goods", "industrial machine", ("grinding machine", "pure water machine", "block making machine",
                                           "industrial mixer", "milling machine", "popcorn machine",
                                           "industrial machine"), ("machine", "mixer")),
)

# The evidence protocol a training kind is asked under, where one fits it.
TRAIN_PROTOCOL = {"faulty laptop": "laptop", "faulty phone": "phone", "faulty air conditioner": "split_ac",
                  "faulty washing machine": "washing_machine", "faulty generator": "generator"}

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


def _variants(phrases: tuple[str, ...], pool: str, more: tuple[str, ...] = ()) -> list[tuple[str, str | None]]:
    """Each phrasing with the word put in front of it, or None for the phrase as written.

    `more` are asked as written only: the words in front find nothing new."""
    out: list[tuple[str, str | None]] = []
    seen: set[str] = set()
    words = SECOND_HAND if pool == "used" else ("brand new",)
    for phrase in more:
        if phrase not in seen:
            seen.add(phrase)
            out.append((phrase, None))
    for phrase in phrases:
        base = phrase.removeprefix("used ").strip()
        for candidate, word in ((phrase, None), *((f"{w} {base}", w) for w in words)):
            if candidate not in seen:
                seen.add(candidate)
                out.append((candidate, word))
    return out


def _from_page(listing, client: httpx.Client) -> list[str]:
    """The advert's photos read from its own page, or [] if the page fails."""
    first = photo_number(listing.image_urls[0]) if listing.image_urls else None
    try:
        response = client.get("https://jiji.ng" + listing.url.split("?")[0] if listing.url.startswith("/") else listing.url)
    except httpx.HTTPError:
        return []
    time.sleep(0.7)
    return page_photos(response.text, first) if response.status_code == 200 else []


def _thumbnails_only(row: dict) -> bool:
    """Cached before the advert pages were read: every photo 300 pixels or less."""
    widths = [_url_width(u) for u in row.get("image_urls") or []]
    return bool(widths) and max(widths) <= 300


def _sharper(new: list[str], old: list[str]) -> bool:
    """Whether an advert now lists a bigger first photo than the cached one."""
    return bool(new and old) and _url_width(new[0]) > max(_url_width(old[0]), 0) and _url_width(old[0]) > 0


def _forget_photos(media: Path, row: dict) -> None:
    for rel in row.get("media") or []:
        (media / rel).unlink(missing_ok=True)


def _done(out_dir: Path, kind: str, region: str) -> bool:
    """Whether this kind was fetched for this city. Each city shows different
    adverts, so Lagos being done says nothing about Abuja. Lagos runs from
    before cities were tracked left only the kind's file behind."""
    slug = kind.replace(" ", "_")
    if (out_dir / ".done" / region / slug).exists():
        return True
    # Only the benchmark's own cache had Lagos runs from before cities were
    # tracked; in a training cache the kind's file is other cities' adverts.
    return region == "lagos" and out_dir.name == "testify" and (out_dir / f"{slug}.json").exists()


def _mark_done(out_dir: Path, kind: str, region: str) -> None:
    marker = out_dir / ".done" / region / kind.replace(" ", "_")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()


def phrasings(phrases: tuple[str, ...], pool: str = "used", more: tuple[str, ...] = ()) -> list[str]:
    """Each phrase as written, then with every second-hand word in front.

    The new-stock pool asks plainly and as "brand new", which is how dealers
    title their adverts. `more` (MORE_WORDS) go first, as written.
    """
    return [candidate for candidate, _ in _variants(phrases, pool, more)]

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
    more_words: bool = False,
    avoid: frozenset[str] = frozenset(),
) -> dict[str, dict[str, int]]:
    """Fetch every kind in every phrasing, keeping second-hand adverts only.

    Adds to what is already cached, so a rerun only grows the set. New stock
    and buyers' adverts are skipped before any photo is downloaded.
    `more_words` also asks MORE_WORDS and the TRAIN_KINDS, for training data;
    it is marked done apart, so a city fetched before is asked again. Adverts
    in `avoid` (the benchmark's) are passed over before any photo is fetched.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, dict[str, int]] = {}
    mark = (lambda kind: f"{kind} more") if more_words else (lambda kind: kind)  # noqa: E731
    more = (lambda kind: MORE_WORDS.get(kind, ())) if more_words else (lambda kind: ())  # noqa: E731
    kinds = KINDS + TRAIN_KINDS if more_words else KINDS
    chosen = [k for k in kinds if (not only or k[1] in only) and not (skip_done and _done(out_dir, mark(k[1]), region))]
    total = sum(len(phrasings(k[2], pool, more(k[1]))) for k in chosen)
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
            tally = {"kept": 0, "brand new": 0, "second-hand": 0, "buyer, not seller": 0, "timed out": 0, "sharper photos": 0,
                     "in the benchmark": 0}
            for phrase, word in _variants(phrases, pool, more(kind)):
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
                    if listing.id in avoid:
                        tally["in the benchmark"] += 1
                        continue
                    if listing.id in seen:
                        # Fetched before with thumbnails: take the bigger photos now offered.
                        old = seen[listing.id]
                        if listing.url and _thumbnails_only(old):
                            listing.image_urls = _from_page(listing, client) or listing.image_urls
                        if _sharper(listing.image_urls, old.get("image_urls") or []):
                            _forget_photos(out_dir / "media", old)
                            listing.image_urls = listing.image_urls[:max_photos]
                            download_media([listing], out_dir / "media", client=client)
                            if listing.media:
                                old["image_urls"], old["media"] = listing.image_urls, listing.media
                                tally["sharper photos"] += 1
                        continue
                    reason = keep(listing.to_json(), pool)
                    if reason:
                        tally[reason] += 1
                    else:
                        fresh.append(listing)
                # The advert's own page has all its photos, and a bigger first one.
                for listing in fresh:
                    bigger = _from_page(listing, client) if listing.url else []
                    listing.image_urls = (bigger or listing.image_urls)[:max_photos]
                # Three photos tell what an item is and show its condition. Eight
                # cost a slow connection hours for little more.
                download_media(fresh, out_dir / "media", client=client)
                for listing in fresh:
                    if listing.media and listing.id not in seen:
                        row = listing.to_json()
                        row["tier"] = tier
                        row["kind"] = kind
                        row["region"] = region
                        if kind in TRAIN_PROTOCOL:
                            row["protocol"] = TRAIN_PROTOCOL[kind]
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
            _mark_done(out_dir, mark(kind), region)
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


def benchmark_ids(cache: Path) -> frozenset[str]:
    """Every advert id the benchmark's cache holds, so training never fetches one again."""
    ids: set[str] = set()
    for path in cache.glob("*.json"):
        rows = json.loads(path.read_text())
        if isinstance(rows, list):
            ids.update(r["id"] for r in rows if isinstance(r, dict) and r.get("id"))
    return frozenset(ids)
