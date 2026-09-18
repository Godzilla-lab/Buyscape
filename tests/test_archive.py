"""A finished session is copied off the machine, and comes back on restart."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from buyscape.ui.archive import from_env
from buyscape.ui.server import Engine

ROOT = Path(__file__).resolve().parents[1]


class FakeArchive:
    repo_id = "fake/sessions"

    def __init__(self):
        self.uploads: list[tuple[str, str | None]] = []

    def upload_later(self, session_dir: Path, extra: Path | None = None):
        self.uploads.append((session_dir.name, extra.name if extra else None))


def _jpeg() -> str:
    import base64
    import io

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (64, 48), (90, 120, 150)).save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def test_a_valued_and_a_settled_session_are_backed_up(tmp_path, monkeypatch):
    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    monkeypatch.setenv("BUYSCAPE_MODE", "record")
    eng = Engine(ROOT)
    eng.fixtures = tmp_path / "fx"
    store = eng.store
    store.dir = tmp_path / "sessions"
    store.archive = FakeArchive()
    s = store.create({"category": "Iron", "text": "rods"})
    store.add_photo(s["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg()})
    store.start_submit(s["id"], {"answers": {"weight_kg": "50"}})
    for _ in range(200):
        if store.load(s["id"])["status"] != "valuing":
            break
        time.sleep(0.05)
    # Once for the photo, once when valuing starts, once when it finishes.
    assert store.archive.uploads == [(s["id"], None)] * 3
    store.settle(s["id"], {"price": 12000})
    assert store.archive.uploads[-1] == (s["id"], "settlements.jsonl")


def test_no_archive_without_the_environment():
    assert from_env({}) is None
    assert from_env({"BUYSCAPE_ARCHIVE_REPO": "x/y"}) is None
    assert from_env({"BUYSCAPE_ARCHIVE_REPO": "x/y", "HF_TOKEN": "t"}).repo_id == "x/y"


def test_a_session_is_backed_up_as_soon_as_it_has_a_photo_and_when_valuing_starts(tmp_path, monkeypatch):
    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    monkeypatch.setenv("BUYSCAPE_MODE", "record")
    eng = Engine(ROOT)
    eng.fixtures = tmp_path / "fx"
    store = eng.store
    store.dir = tmp_path / "sessions"
    store.archive = FakeArchive()
    s = store.create({"category": "Iron", "text": "rods"})
    store.add_photo(s["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg()})
    assert store.archive.uploads == [(s["id"], None)], "the photo is the first thing worth keeping"
    store.start_submit(s["id"], {})
    assert store.archive.uploads[1] == (s["id"], None)


def test_a_valuation_cut_off_by_a_restart_is_marked_to_retry(tmp_path, monkeypatch):
    import json

    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    eng = Engine(ROOT)
    store = eng.store
    store.dir = tmp_path / "sessions"
    s = store.create({"category": "Iron"})
    path = store.dir / s["id"] / "session.json"
    data = json.loads(path.read_text())
    data["status"] = "valuing"
    path.write_text(json.dumps(data))
    assert store.recover_interrupted() == 1
    view = store.seller_view(store.load(s["id"]))
    assert view["status"] == "failed" and "restarted" in view["error"] and not view["valuing"]
