"""Testify items: stable splits, honest baselines, nothing private released."""

from pathlib import Path

import yaml

from buyscape.testify.convert import baseline_from_report, redact, risk_seeds
from buyscape.testify.schema import Item, split_for
from buyscape.protocols.schema import load_protocols

ROOT = Path(__file__).resolve().parents[1]

ABSTAINED = """## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** nothing legible

## Price
**5,000 to 5,000 NGN** (priced as material, width 0.0, method material_floor, 0 comparable prices)
"""

ANSWERED = """## Identification
**Answer: Samsung Galaxy S22** (margin 0.6)

## Price
**180,000 to 240,000 NGN** (priced as a working item, width 0.3, method comps, 9 comparable prices)
"""

NO_DATA = """**Answer: Nexus 7kg** (margin 0.5)

## Price
**NO_PRICE_DATA.** nothing dated
"""


def test_split_is_stable_and_roughly_a_quarter_dev():
    assert split_for("abc") == split_for("abc")
    ids = [f"item-{n}" for n in range(2000)]
    dev = sum(split_for(i) == "dev" for i in ids)
    assert 400 < dev < 600


def test_baseline_reads_abstention_answer_and_missing_price():
    abstained = baseline_from_report(ABSTAINED, "a.md")
    assert abstained.decision == "cannot_identify"
    assert abstained.answer is None
    assert (abstained.price_low, abstained.basis) == (5000, "priced as material")

    answered = baseline_from_report(ANSWERED, "b.md")
    assert answered.decision == "price"
    assert answered.answer == "Samsung Galaxy S22"
    assert (answered.price_low, answered.price_high) == (180000, 240000)

    assert baseline_from_report(NO_DATA, "c.md").decision == "no_price_data"


def test_contact_details_never_survive():
    text = "Call 08012345678 or +234 801 234 5678, mail seller@example.com"
    clean = redact(text)
    assert "0801" not in clean and "example.com" not in clean
    assert clean.count("[phone]") == 2 and "[email]" in clean


def test_every_protocol_claim_becomes_a_risk_with_its_proof():
    laptop = load_protocols(ROOT / "protocols")["laptop"]
    seeds = risk_seeds(laptop)
    assert [s.risk for s in seeds] == [c.id for c in laptop.claims]
    assert all(s.proof for s in seeds if s.risk == "ram_gb")
    assert all(not s.reviewed for s in seeds)


def test_hand_labels_name_real_tiers_and_protocols():
    labels = yaml.safe_load((ROOT / "eval" / "testify" / "labels.yaml").read_text())
    protocols = load_protocols(ROOT / "protocols")
    tiers = set(Item.model_fields["tier"].annotation.__args__)
    for item_id, label in labels.items():
        assert label["tier"] in tiers, item_id
        assert label["protocol"] in protocols, item_id


def test_released_items_hold_links_not_photos():
    path = ROOT / "eval" / "testify" / "items.jsonl"
    for line in path.read_text().splitlines():
        item = Item.model_validate_json(line)
        assert item.photos.public is False
        assert item.url.startswith("https://")
        assert redact(item.seller_text) == item.seller_text


def test_a_source_missing_here_keeps_its_previous_items(tmp_path):
    from buyscape.testify.convert import all_items, write

    root = tmp_path / "repo"
    (root / "eval").mkdir(parents=True)
    for name in ("protocols", "docs", "tenants"):
        (root / name).symlink_to(ROOT / name)
    (root / "eval" / "adjudications.yaml").symlink_to(ROOT / "eval" / "adjudications.yaml")
    previous = tmp_path / "items.jsonl"
    old = Item.model_validate_json((ROOT / "eval" / "testify" / "items.jsonl").read_text().splitlines()[0])
    kept = old.model_copy(update={"id": "only-on-another-machine", "source": "buyscrap"})
    write([kept], previous)

    items = all_items(root, previous=previous)
    ids = {i.id for i in items}
    assert "only-on-another-machine" in ids
    assert sum(i.source == "jiji" for i in items) == 178


def test_fetch_asks_in_nigerian_second_hand_words_and_skips_new_and_buyers():
    from buyscape.testify.fetch import keep, phrasings

    assert phrasings(("used freezer",)) == [
        "used freezer", "tokunbo freezer", "fairly used freezer", "uk used freezer",
    ]
    assert keep({"condition": "Brand New", "title": "Standing fan"}) == "brand new"
    assert keep({"condition": "Used", "title": "We Buy Scrap Batteries"}) == "buyer, not seller"
    assert keep({"condition": "Used", "title": "Scrap Buyer, Convert Your Scrap To Cash"}) == "buyer, not seller"
    assert keep({"condition": "Used", "title": "Tokunbo standing fan"}) is None


def test_a_kaggle_metadata_file_beside_the_adverts_is_not_an_advert(tmp_path):
    import json

    from buyscape.testify.fetch import load

    (tmp_path / "dataset-metadata.json").write_text(json.dumps({"title": "x", "id": "u/x"}))
    (tmp_path / "fan.json").write_text(json.dumps([{"id": "a", "tier": "small_goods", "kind": "fan", "title": "Fan"}]))
    (tmp_path / "broken.json").write_text("{not json")
    assert [r["id"] for r in load(tmp_path)] == ["a"]


def test_a_slow_jiji_is_retried_and_then_skipped_not_fatal():
    import httpx

    from buyscape.testify.fetch import _patiently

    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise httpx.ReadTimeout("slow")
        return ["ok"]

    assert _patiently(flaky, waits=(0, 0)) == ["ok"]

    def dead():
        raise httpx.ReadTimeout("slow")

    assert _patiently(dead, waits=(0, 0)) is None
