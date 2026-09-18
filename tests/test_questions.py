"""Questions the business writes are data, priced like any claim, never generated."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import pytest

from buyscape.protocols.schema import load_protocols
from buyscape.tenant import TenantQuestion, load_questions, load_tenant, save_questions

ROOT = Path(__file__).resolve().parents[1]


def test_a_question_without_a_worst_case_or_a_pickup_check_is_refused():
    with pytest.raises(ValueError, match="worst"):
        TenantQuestion(ask="Does it work?", worst_case="", pickup_check="Agent switches it on")
    with pytest.raises(ValueError, match="pickup|worst"):
        TenantQuestion(ask="Does it work?", worst_case="assumed dead", pickup_check=" ")
    with pytest.raises(ValueError, match="options"):
        TenantQuestion(ask="Screen?", kind="choice", options=["fine"], worst_case="cracked", pickup_check="Agent looks")
    q = TenantQuestion(ask="Does it switch on and stay on?", worst_case="assumed dead, priced as e-waste",
                       pickup_check="Agent plugs it in for ten minutes")
    assert q.id == "does_it_switch_on_and_stay"
    assert q.as_claim().penalty == 0.9 and q.as_question().claim == q.id


def test_staff_questions_join_the_protocol_for_their_category_only(tmp_path):
    protocols = load_protocols(ROOT / "protocols")
    tenant = load_tenant(ROOT / "tenants" / "buyscrap_ng.yaml")
    tenant.questions = [
        TenantQuestion(category="E-waste", ask="Does it switch on?", worst_case="assumed dead", pickup_check="Agent tries it"),
        TenantQuestion(category="*", ask="How long have you had it?", kind="number", unit="years",
                       worst_case="assumed older than stated", pickup_check="Agent reads the date code"),
    ]
    ewaste = tenant.with_questions(tenant.protocol_for(protocols, "E-waste"), "E-waste")
    iron = tenant.with_questions(tenant.protocol_for(protocols, "Iron"), "Iron")
    assert {q.id for q in ewaste.questions} >= {"does_it_switch_on", "how_long_have_you_had_it"}
    assert "does_it_switch_on" not in {q.id for q in iron.questions}
    assert "how_long_have_you_had_it" in {q.id for q in iron.questions}
    assert ewaste.claim_for("does_it_switch_on", "condition").pickup_check == "Agent tries it"
    # Round trip through the file staff edits.
    path = tmp_path / "t.questions.yaml"
    save_questions(path, tenant.questions)
    assert [q.id for q in load_questions(path)] == ["does_it_switch_on", "how_long_have_you_had_it"]


def test_an_answer_to_a_staff_question_is_priced_at_the_worst_case(tmp_path, monkeypatch):
    from buyscape.ui.server import Engine

    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    monkeypatch.setenv("BUYSCAPE_MODE", "record")
    eng = Engine(ROOT)
    eng.fixtures = tmp_path / "fixtures"
    store = eng.store
    store.dir = tmp_path / "sessions"
    store.questions_path = tmp_path / "q.yaml"
    store.tenant.questions = []
    store.save_question({"category": "E-waste", "ask": "Does it switch on?", "kind": "yesno",
                         "worst_case": "assumed dead, priced as e-waste", "pickup_check": "Agent plugs it in",
                         "penalty": "0.6", "options": ""})
    assert store.questions_path.exists()
    s = store.create({"category": "E-waste", "text": "old hp laptop", "asking": 20000, "contact": "0801"})
    assert any(q["id"] == "does_it_switch_on" for q in s["questions"])
    other = store.create({"category": "Iron", "text": "rods"})
    assert not any(q["id"] == "does_it_switch_on" for q in other["questions"])

    import base64
    import io

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (64, 48), (90, 120, 150)).save(buf, format="JPEG")
    jpeg = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    store.add_photo(s["id"], {"slot": "code_shot", "name": "a.jpg", "data": jpeg})
    s = store.submit(s["id"], {"answers": {"does_it_switch_on": "no", "weight_kg": "2"}})
    saved = store.load(s["id"])
    mine = [c for c in saved["result"]["claims"] if "Does it switch on" in c["text"]]
    assert mine and "plugs it in" in (mine[0]["pickup_check"] or "")
    assert mine[0]["worst_case"] == "assumed dead, priced as e-waste"
    assert mine[0]["status"] != "supported", "an answer is never proven remotely"
    assert any("Does it switch on" in c for c in saved["result"]["quote"]["conditions"])

    store.remove_question({"category": "E-waste", "id": "does_it_switch_on"})
    assert store.tenant.questions == []


def test_the_office_serves_and_saves_questions(tmp_path, monkeypatch):
    import threading

    from buyscape.ui.server import make_server

    monkeypatch.setenv("BUYSCAPE_OFFICE_TOKEN", "secret")
    server = make_server(ROOT, port=0)
    server.engine.store.questions_path = tmp_path / "q.yaml"
    server.engine.store.tenant.questions = []
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        def call(path, body=None, token="secret"):
            req = urllib.request.Request(
                base + path, data=json.dumps(body).encode() if body else None,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
                method="POST" if body else "GET",
            )
            try:
                with urllib.request.urlopen(req) as res:
                    return res.status, json.loads(res.read())
            except urllib.error.HTTPError as err:
                return err.code, json.loads(err.read())

        assert call("/api/office/questions", token="wrong")[0] == 401
        status, view = call("/api/office/questions")
        assert status == 200 and "E-waste" in view["categories"] and view["questions"] == []
        status, view = call("/api/office/questions", {"action": "save", "question": {
            "category": "*", "ask": "Any water damage?", "kind": "yesno",
            "worst_case": "assumed water damaged", "pickup_check": "Agent opens it and looks for corrosion"}})
        assert status == 200 and view["questions"][0]["id"] == "any_water_damage"
        status, err = call("/api/office/questions", {"action": "save", "question": {"ask": "Nice?", "worst_case": "", "pickup_check": ""}})
        assert status == 400 and "unproven" in err["error"]
        with urllib.request.urlopen(base + "/office/questions?token=secret") as res:
            assert b"Questions we ask sellers" in res.read()
    finally:
        server.shutdown()
        server.server_close()
