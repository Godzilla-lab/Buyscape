"""The local OCR's reading of every advert photo, read once and kept.

The seller check, the items with the proof taken away and the true claims
all need the text on the same photos, and the OCR takes a second or two a
photo. So each photo is read once, every line with its confidence and its
box, into `eval/raw/testify_ocr/cache.json`. It sits beside the photos it
was read from and, like them, is never committed: a stamp carries a seller's
name and a photo can carry a phone number. It has a folder of its own because
the engine reads every JSON file at the top of `eval/raw` as cached adverts.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..identify.ocr import MIN_SCORE, default_reader
from ..providers.base import ImageRef

CACHE = Path("eval") / "raw" / "testify_ocr" / "cache.json"


class OcrCache:
    """Read photos through the cache; a photo not in it is read now and kept."""

    def __init__(self, root: Path, reader=None, live: bool = True) -> None:
        self.root, self.path = root, root / CACHE
        self.lines_read: dict[str, list] = json.loads(self.path.read_text()) if self.path.exists() else {}
        self._reader = reader
        # A build reads only what `testify-ocr` read, so it is quick and the same every time.
        self.live = live
        self.added = 0

    def scored(self, path: Path) -> list[tuple[str, float, list]]:
        key = self._key(path)
        if key not in self.lines_read:
            if not self.live:
                return []
            reader = self._reader or default_reader()
            if reader is None:
                return []
            self._reader = reader
            with reader._lock:
                reader._load()
                self.lines_read[key] = [[t, round(s, 3), [list(c) for c in corners]]
                                        for t, s, corners in reader._detect(path, min_score=0.0)]
            self.added += 1
        return [(t, s, c) for t, s, c in self.lines_read[key]]

    def boxes(self, path: Path) -> list[tuple[str, list]]:
        """Every line with its box, sure or not: for painting a code out."""
        return [(t, c) for t, _, c in self.scored(path)]

    def lines(self, path: Path) -> list[str]:
        """The lines the OCR is sure of: for checking a name or a code."""
        out: list[str] = []
        for t, s, _ in self.scored(path):
            if s >= MIN_SCORE and t not in out:
                out.append(t)
        return out

    def __call__(self, images: tuple[ImageRef, ...]) -> list[str]:
        """The engine's OCR reader interface: photos in, sure lines out."""
        return [line for image in images for line in self.lines(image.path)]

    def save(self) -> None:
        if self.added:
            self.path.write_text(json.dumps(self.lines_read))
            self.added = 0

    def _key(self, path: Path) -> str:
        try:
            return str(Path(path).resolve().relative_to(self.root.resolve()))
        except ValueError:
            return str(path)
