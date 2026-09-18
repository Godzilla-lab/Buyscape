"""A clip is stored for staff and read by the engine as its sharpest stills."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from buyscape.media.frames import sample_frames, sharpness


def _clip(path: Path, seconds: int = 6, fps: int = 10) -> Path:
    """A flat grey clip with one sharp lettered frame in each second."""
    import cv2

    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), float(fps), (96, 64))
    assert writer.isOpened()
    for i in range(seconds * fps):
        frame = np.full((64, 96, 3), 90, np.uint8)
        if i % fps == fps // 2:
            cv2.putText(frame, f"S{i // fps}", (8, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        writer.write(frame)
    writer.release()
    return path


def test_the_sharpest_frame_of_each_stretch_is_kept_in_time_order(tmp_path):
    clip = _clip(tmp_path / "walk.mp4")
    frames = sample_frames(clip, tmp_path / "frames", "walk", keep=3)
    assert [p.name for p in frames] == ["walk_f1.jpg", "walk_f2.jpg", "walk_f3.jpg"]
    import cv2

    for p in frames:
        assert sharpness(cv2.imread(str(p))) > 50, "a flat grey frame was chosen over a lettered one"


def test_an_unreadable_clip_yields_nothing_rather_than_an_error(tmp_path):
    bad = tmp_path / "bad.mp4"
    bad.write_bytes(b"not a video")
    assert sample_frames(bad, tmp_path / "frames", "bad") == []
