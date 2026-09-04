"""The local test page runs the same engine as the CLI and says what broke."""

from __future__ import annotations

import base64
import io
import json
import threading
import urllib.request
from pathlib import Path

import pytest
from PIL import Image

from buyscape.ui.server import make_server

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def base_url(tmp_path_factory):
    server = make_server(ROOT, port=0)
    # Fixtures and photos written by the test stay out of the repo.
    server.engine.fixtures = tmp_path_factory.mktemp("fixtures")
    server.engine.inbox = tmp_path_factory.mktemp("inbox")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()
    server.server_close()


def _get(url: str) -> tuple[int, dict | list | bytes]:
    try:
        with urllib.request.urlopen(url) as res:
            body = res.read()
            return res.status, (json.loads(body) if res.headers.get_content_type() == "application/json" else body)
    except urllib.error.HTTPError as err:
        body = err.read()
        return err.code, (json.loads(body) if err.headers.get_content_type() == "application/json" else body)


def _post(url: str, payload: dict) -> tuple[int, dict]:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read())


def _photo() -> str:
    buf = io.BytesIO()
    Image.new("RGB", (64, 48), (90, 120, 150)).save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def test_page_and_meta_load(base_url):
    status, page = _get(base_url + "/")
    assert status == 200 and b"stepWhat" in page
    status, page = _get(base_url + "/bench")
    assert status == 200 and b"test bench" in page
    status, page = _get(base_url + "/office")
    assert status == 200 and b"Sessions" in page
    status, meta = _get(base_url + "/api/meta")
    assert status == 200
    assert any(p["name"] == "balanced" for p in meta["presets"])
    assert "buyscrap_ng" in meta["tenants"]
    assert "phone" in meta["protocols"]


def test_runs_on_disk_are_listed_with_their_gate(base_url):
    status, runs = _get(base_url + "/api/runs")
    assert status == 200 and runs
    finished = [r for r in runs if r["summary"]]
    assert finished, "at least one proof run has a summary"
    assert finished[0]["gate"] and finished[0]["cases"]
    run, case = finished[0]["name"], finished[0]["cases"][0]
    status, body = _get(f"{base_url}/api/runs/{run}/cases/{case}")
    assert status == 200 and body["report"].startswith("# Case ")


def test_files_outside_eval_are_refused(base_url):
    status, _ = _get(base_url + "/files/../pyproject.toml")
    assert status == 404


def test_valuing_dropped_photos_writes_a_folder_and_a_report(base_url):
    status, data = _post(
        base_url + "/api/value",
        {
            "preset": "fake",
            "mode": "record",
            "photos": [{"name": "IMG_1.jpg", "data": _photo()}],
            "text": "old fan, not working",
            "asking": 3000,
            "answers": {"works": "no", "ignored_blank": ""},
            "label": "test bench fan",
        },
    )
    assert status == 200, data
    assert data["report"].startswith("# Case ")
    assert data["quote"]["currency"] == "NGN"
    folder = Path(data["folder"])
    assert (folder / "IMG_1.jpg").exists()
    assert (folder / "seller.txt").read_text() == "old fan, not working\n"
    assert (folder / "answers.yaml").read_text() == "works: 'no'\n"
    assert (folder / "report.md").exists()
    assert data["images"][0].startswith("/files/inbox/")
    status, _ = _get(base_url + data["images"][0])
    assert status == 200


def test_a_cached_case_can_be_rerun(base_url):
    status, cases = _get(base_url + "/api/testset/jiji")
    assert status == 200 and cases
    case = cases[0]
    assert case["answer_key"] and case["images"]
    status, data = _post(
        base_url + "/api/value",
        {"preset": "fake", "mode": "record", "case_id": case["id"], "set": "jiji"},
    )
    assert status == 200, data
    assert data["case_id"] == case["id"]
    assert data["answer_key"]["title"] == case["answer_key"]
    assert data["folder"] is None


def test_bad_input_is_a_loud_400(base_url):
    status, data = _post(base_url + "/api/value", {"preset": "fake", "photos": []})
    assert status == 400 and "no photos" in data["error"]
    status, data = _post(base_url + "/api/value", {"preset": "nope", "photos": [{"name": "a.jpg", "data": _photo()}]})
    assert status == 400 and "unknown preset" in data["error"]


def test_staff_pages_need_the_token_when_one_is_set(base_url, monkeypatch):
    monkeypatch.setenv("BUYSCAPE_OFFICE_TOKEN", "s3cret")
    status, _ = _get(base_url + "/office")
    assert status == 401
    status, _ = _get(base_url + "/api/office/sessions")
    assert status == 401
    status, _ = _get(base_url + "/api/office/sessions?token=s3cret")
    assert status == 200
    status, _ = _get(base_url + "/")
    assert status == 200, "the seller page is never gated"
