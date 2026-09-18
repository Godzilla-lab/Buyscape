"""Turn a seller's clip into the still frames the readers can look at.

A thirty second walk around the item is hundreds of frames, and the readers
only need the handful where the camera was still and the writing sharp. The
clip is cut into equal stretches of time, every frame in each stretch is
scored for sharpness by the variance of its Laplacian, and the sharpest one
per stretch is written out as a JPEG. Spreading the picks over the whole clip
matters more than raw sharpness: the plate is at one end of the walk and the
serial sticker at the other.

Plain OpenCV on the CPU. No model, no spend, no network.
"""

from __future__ import annotations

from pathlib import Path

# How many stills a clip becomes. Enough for a plate, a screen and the sides.
DEFAULT_KEEP = 6


def sharpness(frame) -> float:
    """Variance of the Laplacian: high on crisp edges, near zero on blur."""
    import cv2

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(grey, cv2.CV_64F).var())


def sample_frames(clip: Path, out_dir: Path, stem: str, keep: int = DEFAULT_KEEP) -> list[Path]:
    """The sharpest frame from each of `keep` equal stretches of the clip.

    Returns the JPEGs written, in time order. An unreadable clip returns an
    empty list rather than raising, so a bad upload never blocks a session.
    """
    import cv2

    cap = cv2.VideoCapture(str(clip))
    if not cap.isOpened():
        return []
    best: dict[int, tuple[float, object]] = {}
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        # Without a frame count the clip is treated as one stretch and the
        # single sharpest frame is kept.
        stretch = min(keep - 1, index * keep // total) if total > 0 else 0
        score = sharpness(frame)
        if stretch not in best or score > best[stretch][0]:
            best[stretch] = (score, frame)
        index += 1
    cap.release()

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for stretch in sorted(best):
        path = out_dir / f"{stem}_f{stretch + 1}.jpg"
        cv2.imwrite(str(path), best[stretch][1], [cv2.IMWRITE_JPEG_QUALITY, 90])
        written.append(path)
    return written
