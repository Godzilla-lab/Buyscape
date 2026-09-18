"""A seller's session: photos in, an offer out, and two audiences kept apart."""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path

import pytest
from PIL import Image

from buyscape.ui.server import Engine

ROOT = Path(__file__).resolve().parents[1]


def _jpeg(color=(90, 120, 150), size=(64, 48)) -> str:
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


@pytest.fixture
def engine(tmp_path, monkeypatch):
    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    monkeypatch.setenv("BUYSCAPE_MODE", "record")
    eng = Engine(ROOT)
    eng.fixtures = tmp_path / "fixtures"
    eng.store.dir = tmp_path / "sessions"
    return eng


def test_a_session_is_a_folder_with_the_protocol_shots(engine):
    s = engine.store.create({"category": "E-waste", "text": "old laptops, about 20", "asking": 50000, "contact": "0801"})
    assert len(s["code"]) == 4 and set(s["code"]) <= set("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
    slots = [x["slot"] for x in s["shots"]]
    assert "code_shot" in slots
    code_shot = next(x for x in s["shots"] if x["slot"] == "code_shot")
    assert s["code"] in code_shot["ask"] and "{code}" not in code_shot["ask"]
    assert s["business"] == "BuyScrap Nigeria" and s["currency"] == "NGN"
    assert (engine.store.dir / s["id"] / "session.json").exists()
    assert s["outcome"] is None


def test_not_sure_falls_to_the_generic_protocol(engine):
    s = engine.store.create({"category": None})
    assert engine.store.load(s["id"])["protocol"] == "generic"
    with pytest.raises(ValueError, match="not one of"):
        engine.store.create({"category": "Unicorns"})


def test_photos_land_in_their_slots_and_submit_yields_an_offer(engine):
    store = engine.store
    s = store.create({"category": "Iron", "text": "about 200 kg of iron rods", "asking": 0, "contact": "0802"})
    sid = s["id"]
    s = store.add_photo(sid, {"slot": "code_shot", "name": "IMG_1.jpg", "data": _jpeg()})
    s = store.add_photo(sid, {"slot": "whole_pile", "name": "IMG_2.jpg", "data": _jpeg((10, 200, 10))})
    files = sorted(p.name for p in (store.dir / sid).iterdir())
    assert files == ["code_shot__01.jpg", "session.json", "whole_pile__01.jpg"]
    assert [x["slot"] for x in s["shots"] if x["files"]] == ["code_shot", "whole_pile"]

    s = store.submit(sid, {"answers": {"weight_kg": "200", "blank": " "}, "refused": []})
    assert s["status"] in ("quoted", "needs_more", "no_price")
    out = s["outcome"]
    assert out["headline"]
    assert (store.dir / sid / "report.md").read_text().startswith("# Case ")
    saved = store.load(sid)
    assert saved["answers"] == {"weight_kg": "200"}
    assert saved["result"]["quote"]["currency"] == "NGN"


def test_the_seller_never_sees_model_names_or_scores(engine):
    store = engine.store
    s = store.create({"category": "Laptop" if any(c == "Laptop" for c in store.tenant_view()["categories"]) else "E-waste", "text": "macbook, works", "contact": "0803"})
    sid = s["id"]
    store.add_photo(sid, {"slot": "code_shot", "name": "a.jpg", "data": _jpeg()})
    s = store.submit(sid, {})
    blob = json.dumps(s).lower()
    for banned in ("qwen", "glm", "fake", "confidence", "percent", "candidate", "catalogue", "fraud", "reader", "reasoner", "cost"):
        assert banned not in blob, f"{banned!r} leaked into the seller view"
    office = json.dumps(store.office_view(store.load(sid))).lower()
    assert "reader" in office and "assessment" in office


def test_a_photo_reused_under_another_number_is_flagged_for_review(engine):
    store = engine.store
    first = store.create({"category": "Iron", "contact": "0801"})
    store.add_photo(first["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg((200, 30, 30), (400, 300))})
    store.submit(first["id"], {})

    again = store.create({"category": "Iron", "contact": "0801"})
    store.add_photo(again["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg((200, 30, 30), (400, 300))})
    s = store.submit(again["id"], {})
    assert store.load(s["id"])["duplicates"][0]["same_contact"] is True
    assert s["status"] != "review"

    other = store.create({"category": "Iron", "contact": "0999"})
    store.add_photo(other["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg((200, 30, 30), (400, 300))})
    s = store.submit(other["id"], {})
    assert s["status"] == "review"
    assert s["outcome"]["headline"].startswith("We need to check")
    assert s["outcome"]["low"] is None


def test_settling_writes_a_calibration_row(engine):
    store = engine.store
    s = store.create({"category": "Iron", "contact": "0804", "asking": 40000})
    store.add_photo(s["id"], {"slot": "whole_pile", "name": "a.jpg", "data": _jpeg()})
    store.submit(s["id"], {})
    with pytest.raises(ValueError):
        store.settle(s["id"], {"price": 0})
    view = store.settle(s["id"], {"price": 35000, "note": "lighter than stated"})
    assert view["status"] == "settled" and view["settlement"]["price"] == 35000
    rows = [json.loads(l) for l in (store.dir / "settlements.jsonl").read_text().splitlines()]
    assert rows[-1]["session_id"] == s["id"]
    assert rows[-1]["settled_price"] == 35000 and rows[-1]["asking"] == 40000
    assert "quoted_low" in rows[-1] and rows[-1]["category"] == "Iron"
    listed = next(r for r in store.list() if r["id"] == s["id"])
    assert listed["settled"] == 35000


def test_remove_photo_and_unknown_session(engine):
    store = engine.store
    s = store.create({"category": "Iron"})
    s = store.add_photo(s["id"], {"slot": "extra", "name": "x.png", "data": _jpeg()})
    assert s["extra"] and (store.dir / s["id"] / "extra__01.png").exists()
    s = store.remove_photo(s["id"], "extra__01.png")
    assert s["extra"] == [] and not (store.dir / s["id"] / "extra__01.png").exists()
    with pytest.raises(KeyError):
        store.load("../nope")
    with pytest.raises(ValueError, match="no photos"):
        store.submit(s["id"], {})


def _mp4(seconds: int = 3, fps: int = 10) -> str:
    """A tiny clip, one sharp lettered frame per second, as a data URL."""
    import tempfile

    import cv2
    import numpy as np

    path = Path(tempfile.mkdtemp()) / "clip.mp4"
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), float(fps), (96, 64))
    for i in range(seconds * fps):
        frame = np.full((64, 96, 3), 90, np.uint8)
        if i % fps == fps // 2:
            cv2.putText(frame, f"S{i // fps}", (8, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        writer.write(frame)
    writer.release()
    return "data:video/mp4;base64," + base64.b64encode(path.read_bytes()).decode()


def test_a_clip_becomes_stills_the_engine_reads_and_the_seller_does_not_see(engine):
    store = engine.store
    s = store.create({"category": "E-waste", "text": "old laptop"})
    sid = s["id"]
    s = store.add_photo(sid, {"slot": "extra", "name": "clip.mp4", "data": _mp4()})
    saved = store.load(sid)
    kinds = [p["kind"] for p in saved["photos"]]
    assert kinds.count("clip") == 1 and kinds.count("frame") >= 2
    frames = [p for p in saved["photos"] if p["kind"] == "frame"]
    assert all(p["from"] == "extra__01.mp4" and p["phash"] for p in frames)
    assert all((store.dir / sid / p["file"]).exists() for p in frames)
    # The engine sees the stills, the seller sees only the clip they recorded.
    assert [p.name for p in store._images(saved)] == [p["file"] for p in frames]
    shown = s["extra"]
    assert [f["kind"] for f in shown] == ["clip"]
    assert all(p["kind"] in ("clip", "frame") for p in store.office_view(saved)["photos"])
    # Removing the clip takes its stills with it.
    s = store.remove_photo(sid, "extra__01.mp4")
    assert store.load(sid)["photos"] == []
    assert sorted(p.name for p in (store.dir / sid).iterdir()) == ["session.json"]


def test_submit_returns_at_once_and_the_page_polls_for_the_offer(engine):
    import time

    store = engine.store
    s = store.create({"category": "Iron", "text": "about 50 kg of iron rods"})
    store.add_photo(s["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg()})
    s = store.start_submit(s["id"], {"answers": {"weight_kg": "50"}})
    assert s["status"] == "valuing" and s["valuing"] and s["outcome"] is None
    # Asking again while it runs does not start a second valuation.
    assert store.start_submit(s["id"], {})["valuing"]
    for _ in range(200):
        s = store.seller_view(store.load(s["id"]))
        if not s["valuing"]:
            break
        time.sleep(0.05)
    assert not s["valuing"] and s["error"] is None
    assert s["status"] in ("quoted", "needs_more", "no_price") and s["outcome"]["headline"]


def test_a_valuation_that_breaks_is_a_failed_session_not_a_hung_page(engine):
    import time

    store = engine.store

    def broken(case, tenant):
        raise RuntimeError("provider down")

    store.valuer = broken
    s = store.create({"category": "Iron", "text": "rods"})
    store.add_photo(s["id"], {"slot": "code_shot", "name": "a.jpg", "data": _jpeg()})
    store.start_submit(s["id"], {})
    for _ in range(200):
        s = store.seller_view(store.load(s["id"]))
        if not s["valuing"]:
            break
        time.sleep(0.05)
    assert s["status"] == "failed" and "provider down" in s["error"]


def test_a_phone_photo_is_shrunk_and_kept_the_right_way_up(engine):
    from PIL import Image

    store = engine.store
    s = store.create({"category": "Iron"})
    # A tall photo stored sideways with EXIF orientation 6, the way phones do it.
    im = Image.new("RGB", (4000, 3000), (200, 30, 30))
    im.paste((30, 30, 200), (0, 0, 4000, 300))
    exif = Image.Exif()
    exif[0x0112] = 6
    buf = io.BytesIO()
    im.save(buf, format="JPEG", exif=exif)
    data = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    s = store.add_photo(s["id"], {"slot": "code_shot", "name": "IMG.jpg", "data": data})
    path = store.dir / s["id"] / "code_shot__01.jpg"
    with Image.open(path) as saved:
        from buyscape.ui.sessions import MAX_PHOTO_SIDE

        assert max(saved.size) == MAX_PHOTO_SIDE
        assert saved.size[1] > saved.size[0], "orientation 6 means the photo was taken upright"
        assert saved.getexif().get(0x0112) in (None, 1)


def test_a_blurred_photo_is_flagged_at_upload_and_a_sharp_one_is_not(engine):
    import numpy as np
    from PIL import Image as PILImage

    store = engine.store
    s = store.create({"category": "Iron"})
    # Flat grey: nothing to focus on, scores near zero.
    s = store.add_photo(s["id"], {"slot": "code_shot", "name": "blur.jpg", "data": _jpeg((120, 120, 120), (640, 480))})
    warned = [f for f in s["shots"][0]["files"] if f["warning"]]
    assert warned and "blurred" in warned[0]["warning"]
    # High-contrast text and noise: sharp.
    rng = np.random.default_rng(1)
    noisy = PILImage.fromarray(rng.integers(0, 255, (480, 640, 3), dtype=np.uint8))
    buf = io.BytesIO()
    noisy.save(buf, format="JPEG", quality=90)
    data = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    s = store.add_photo(s["id"], {"slot": "code_shot", "name": "sharp.jpg", "data": data})
    sharp = [f for f in s["shots"][0]["files"] if f["file"] == "code_shot__02.jpg"][0]
    assert sharp["warning"] is None
    assert store.load(s["id"])["photos"][1]["sharpness"] > 25


def test_sessions_can_live_on_a_mounted_disk(tmp_path, monkeypatch):
    from buyscape.ui.server import Engine

    monkeypatch.setenv("BUYSCAPE_PRESET", "fake")
    monkeypatch.setenv("BUYSCAPE_SESSIONS_DIR", str(tmp_path / "disk"))
    eng = Engine(ROOT)
    assert eng.store.dir == tmp_path / "disk"
    s = eng.store.create({"category": "Iron"})
    assert (tmp_path / "disk" / s["id"] / "session.json").exists()
