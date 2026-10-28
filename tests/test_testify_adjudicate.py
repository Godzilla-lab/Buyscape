"""A person's verdict overrules the word rules, a model's draft never does,
and silent wrongs are told apart by how they are wrong."""

from buyscape.testify import adjudicate
from buyscape.testify.schema import Answer, Item, PriceTruth
from buyscape.testify.score import identity_correct, score

ITEM = Item(id="e1", source="jiji", url="https://jiji.ng/x/e1.html", split="dev", tier="small_goods",
            answer=Answer(title="2GR,Toyota Complete Engine", kind="car engine", price=PriceTruth(ngn=900000)))
V6 = {"status": "by_type", "kind": "V6 engine"}


def _file(tmp_path, monkeypatch, verdict, first="right"):
    path = tmp_path / "adjudication.yaml"
    path.write_text(f"- item: e1\n  answer: V6 engine\n  first_reading: {first}\n  verdict: {verdict}\n")
    monkeypatch.setattr(adjudicate, "PATH", path)
    adjudicate._entries.cache_clear()
    return path


def test_a_draft_moves_nothing_and_a_verdict_decides(tmp_path, monkeypatch):
    _file(tmp_path, monkeypatch, "null")
    rule = identity_correct(ITEM, V6)
    _file(tmp_path, monkeypatch, "right")
    assert identity_correct(ITEM, V6) is True
    _file(tmp_path, monkeypatch, "wrong_kind")
    assert identity_correct(ITEM, V6) is False
    adjudicate._entries.cache_clear()
    assert rule in (True, False)


def test_a_silent_wrong_is_counted_by_how_it_is_wrong(tmp_path, monkeypatch):
    _file(tmp_path, monkeypatch, "wrong_kind")
    row = {"id": "e1", "variant": "clean", "decision": "price", "price_low": 800000, "price_high": 950000,
           "reading": {"identity": V6}}
    result = score([row], {"e1": ITEM})
    assert result["silent_wrong"] == 1 and result["silent_wrong_how"] == {"wrong_kind": 1}
    adjudicate._entries.cache_clear()


def test_unsure_leaves_the_rule_standing_and_is_counted_apart(tmp_path, monkeypatch):
    _file(tmp_path, monkeypatch, "unsure", first="wrong_kind")
    row = {"id": "e1", "variant": "clean", "decision": "price", "price_low": 800000, "price_high": 950000,
           "reading": {"identity": V6}}
    assert identity_correct(ITEM, V6) is False
    assert score([row], {"e1": ITEM})["silent_wrong_how"] == {"unsure": 1}
    adjudicate._entries.cache_clear()


def test_new_answers_are_listed_once_with_every_run_that_gave_them(tmp_path, monkeypatch):
    _file(tmp_path, monkeypatch, "null")
    row = {"reading": {"identity": {"status": "named", "brand": "Toyota", "model": "V6"}}}
    out = adjudicate.pending([("a/dev", row, ITEM), ("b/dev", row, ITEM)])
    assert len(out) == 1 and out[0]["runs"] == ["a/dev", "b/dev"] and out[0]["verdict"] is None
    adjudicate._entries.cache_clear()
