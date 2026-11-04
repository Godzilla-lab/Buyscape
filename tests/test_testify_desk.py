"""A person sits the valuation test from the back office, blind to the answer key."""

import json
from pathlib import Path

import pytest

from buyscape.testify import comparables as comps
from buyscape.testify import sitting
from buyscape.testify.answer import IdentityAnswer, Reading
from buyscape.testify.schema import Answer, Item, PriceTruth
from buyscape.ui import testify_desk as desk


def _item(item_id: str) -> Item:
    return Item(
        id=item_id, source="jiji", url=f"https://jiji.ng/x/{item_id}.html", split="dev", tier="small_goods",
        seller_text="Neat chair, Price: 10,000 naira",
        answer=Answer(title="Secret Title Chair", kind="office chair",
                      price=PriceTruth(ngn=10000, used=True, observed_on="2026-10-14")),
    )


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    photo = tmp_path / "00.jpg"
    photo.write_bytes(b"\xff\xd8\xff")
    out = tmp_path / "eval" / "testify" / "sittings" / "human_ada" / "dev"
    pool = comps.build_pool([])
    sitting.export(tmp_path / "fx", [(_item("bent-office-chair"), [photo], ())], pool, out, lies=False)
    return tmp_path


def test_the_page_never_names_the_item_or_shows_the_price(root: Path):
    listed = desk.sittings(root)
    assert listed == [{"who": "human_ada", "part": "dev", "cases": 1, "answered": 0}]
    cases = desk.cases(root, "human_ada", "dev")
    assert "bent-office-chair" not in json.dumps(cases) and "variant" not in json.dumps(cases)
    shown = desk.case(root, "human_ada", "dev", cases[0]["case"])
    text = json.dumps(shown)
    assert "Secret Title" not in text and "10,000" not in text and "bent-office-chair" not in text
    assert shown["photos"] == ["photo_0.jpg"] and shown["task"] == "testify_read"


def test_an_answer_is_checked_against_the_model_schema_before_it_is_kept(root: Path):
    name = desk.cases(root, "human_ada", "dev")[0]["case"]
    with pytest.raises(ValueError, match="decision"):
        desk.save(root, "human_ada", "dev", name, {"observations": [], "identity": {"status": "by_type"}})
    good = Reading(observations=["mesh chair"], identity=IdentityAnswer(status="by_type", kind="office chair"),
                   decision="price", reason="clear").model_dump()
    assert desk.save(root, "human_ada", "dev", name, good) == {"ok": True}
    assert desk.cases(root, "human_ada", "dev")[0]["answered"]
    assert desk.case(root, "human_ada", "dev", name)["answer"]["identity"]["kind"] == "office chair"


def test_names_outside_the_sitting_are_refused(root: Path):
    name = desk.cases(root, "human_ada", "dev")[0]["case"]
    with pytest.raises(ValueError):
        desk.case(root, "..", "dev", name)
    with pytest.raises((ValueError, KeyError)):
        desk.photo(root, "human_ada", "dev", name, "../case.json")
    with pytest.raises(KeyError):
        desk.photo(root, "human_ada", "dev", name, "prompt.md")
    assert desk.photo(root, "human_ada", "dev", name, "photo_0.jpg").name == "photo_0.jpg"


def test_an_untouched_form_is_not_an_answer(root: Path):
    name = desk.cases(root, "human_ada", "dev")[0]["case"]
    blank = Reading(observations=[], identity=IdentityAnswer(status="by_type"), decision="price", reason="").model_dump()
    with pytest.raises(ValueError, match="what the item is"):
        desk.save(root, "human_ada", "dev", name, blank)
    unsure = Reading(observations=["a dark photo"], identity=IdentityAnswer(status="unknown"),
                     decision="cannot_identify", reason="too dark to tell").model_dump()
    assert desk.save(root, "human_ada", "dev", name, unsure) == {"ok": True}
