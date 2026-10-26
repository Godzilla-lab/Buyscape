"""True claims a photo shows and their false twins: both witnesses, the title
and the local OCR, must agree before a fact is planted."""

from pathlib import Path

from buyscape.testify import truths
from buyscape.testify.schema import Answer, Item, PriceTruth


def _item(title: str) -> Item:
    return Item(id="t1", source="jiji", url="https://jiji.ng/x/t1.html", split="dev", tier="branded_electronics",
                answer=Answer(title=title, price=PriceTruth(ngn=100000)))


PHOTOS = [Path("00.jpg"), Path("01.jpg")]


def test_a_code_on_a_photo_and_in_the_title_becomes_a_truth_and_a_raised_false_twin():
    lines = {"00.jpg": ["Nikon"], "01.jpg": ["D3300 VR"]}
    fact = truths.fact(_item("Nikon D3300 with 18-55mm lens"), PHOTOS, lambda p: lines[p.name], truths.rivals())
    assert fact["fact"] == "code" and fact["shown_in"] == 1
    assert fact["truth"] == "The model is D3300." and fact["contra"] == "The model is D3400."


def test_with_no_code_on_a_photo_the_brand_is_the_fact_and_its_rival_the_lie():
    lines = {"00.jpg": ["NIKON"], "01.jpg": []}
    fact = truths.fact(_item("Nikon D3300 with 18-55mm lens"), PHOTOS, lambda p: lines[p.name], truths.rivals())
    assert fact["fact"] == "brand" and fact["truth"] == "The brand is Nikon." and fact["contra"] == "The brand is Canon."


def test_nothing_read_on_a_photo_plants_nothing():
    assert truths.fact(_item("Nikon D3300"), PHOTOS, lambda p: [], truths.rivals()) is None


def test_raising_a_code_moves_its_first_number():
    assert truths.raised("7kg") == "8kg" and truths.raised("D3300") == "D3400" and truths.raised("650D") == "750D"
    assert truths.raised("Pro") is None


def test_uptake_and_catching_are_read_from_the_claims_and_the_identity():
    facts = {"t1": {"token": "d3300", "false_token": "D3400"}}
    truth = {"id": "t1", "variant": "truth", "reading": {
        "claims": [{"claim": "The model is D3300.", "verdict": "supported"}],
        "identity": {"status": "named", "brand": "Nikon", "model": "D3300"}}}
    contra = {"id": "t1", "variant": "contra", "reading": {
        "claims": [{"claim": "The model is D3400.", "verdict": "contradicted"}],
        "identity": {"status": "named", "brand": "Nikon", "model": "D3300"}}}
    result = truths.score([truth, contra], facts)
    assert result["truth_marked_supported"] == 1.0 and result["truth_used_in_identity"] == 1.0
    assert result["contra_caught"] == 1.0 and result["contra_adopted"] == 0.0
