"""The same thing in other words is right: a judge's verdict lifts the judged
rate only, and a person's verdict always comes first."""

from buyscape.testify import adjudicate, judge
from buyscape.testify.schema import Answer, Item, PriceTruth
from buyscape.testify.score import identity_correct, score

ITEM = Item(id="h1", source="jiji", url="https://jiji.ng/x/h1.html", split="dev", tier="small_goods",
            answer=Answer(title="Toyota Corolla Headlamp", kind="car headlamp", price=PriceTruth(ngn=40000)))
LIGHT = {"status": "by_type", "kind": "car headlight"}
ROW = {"id": "h1", "variant": "clean", "decision": "price", "price_low": 30000, "price_high": 45000,
       "reading": {"identity": LIGHT}}


def _judged(tmp_path, monkeypatch, verdict):
    path = tmp_path / "judged.jsonl"
    item, key = judge.key("h1", LIGHT)
    judge.record([{"item": item, "key": key, "verdict": verdict}], path)
    monkeypatch.setattr(judge, "PATH", path)
    judge._verdicts.cache_clear()


def _person(tmp_path, monkeypatch, verdict):
    path = tmp_path / "adjudication.yaml"
    path.write_text(f"- item: h1\n  answer: car headlight\n  verdict: {verdict}\n")
    monkeypatch.setattr(adjudicate, "PATH", path)
    adjudicate._entries.cache_clear()


def test_the_judge_lifts_the_judged_rate_and_leaves_the_strict_one(tmp_path, monkeypatch):
    _person(tmp_path, monkeypatch, "null")
    assert identity_correct(ITEM, LIGHT) is False  # the word rule: a headlight is not a headlamp
    _judged(tmp_path, monkeypatch, "right")
    result = score([ROW], {"h1": ITEM})
    assert result["identity_accuracy_when_attempted"] == 0 and result["identity_accuracy_judged"] == 1
    _judged(tmp_path, monkeypatch, "wrong_kind")
    assert score([ROW], {"h1": ITEM})["identity_accuracy_judged"] == 0
    judge._verdicts.cache_clear()
    adjudicate._entries.cache_clear()


def test_a_persons_verdict_comes_before_the_judge(tmp_path, monkeypatch):
    _judged(tmp_path, monkeypatch, "right")
    _person(tmp_path, monkeypatch, "unsure")
    assert score([ROW], {"h1": ITEM})["identity_accuracy_judged"] == 0
    judge._verdicts.cache_clear()
    adjudicate._entries.cache_clear()


def test_the_judge_reads_the_title_the_checked_kind_and_the_whole_answer():
    named = {"status": "named", "brand": "Sony", "model": "PS4", "kind": "game console"}
    request = judge.request([(" Ps4 Pro + 2 Pads ", named, "game console", "a games console and two pads"),
                             ("Bicycle", LIGHT, None, None)])
    assert "1. Advert title: Ps4 Pro + 2 Pads\n" in request.user_text
    assert "game console; a games console and two pads" in request.user_text
    assert "   The model's answer: brand: Sony | model: PS4 | kind: game console\n2. " in request.user_text
    assert request.user_text.count("photos") == 1  # nothing checked for the bicycle, so nothing said
    assert judge.key("x", named) == judge.key("x", {**named, "model": "P.S.4"})


def test_a_skipped_or_doubled_case_is_left_unjudged():
    v = lambda n, verdict="right": judge.JudgeVerdict(n=n, verdict=verdict, why="")  # noqa: E731
    said = judge.read(judge.JudgeBatch(verdicts=[v(1), v(3, "wrong_kind"), v(3), v(4, "wrong_brand")]), 4)
    assert [s.verdict if s else None for s in said] == ["right", None, None, "wrong_brand"]
