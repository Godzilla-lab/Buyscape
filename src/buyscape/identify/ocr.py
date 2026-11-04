"""A third witness that cannot invent: character level OCR.

The two vision language models are corroborated against each other because
each one, shown half a plate, composes the rest. An OCR model is a different
kind of reader. It recognises glyphs inside boxes it detected on the image and
it has no idea what a generator plate usually says, so it can misread a
character but it cannot finish a specification table. That makes it a useful
tie breaker: a code one language model produced and the OCR also produced was
on the photograph.

It runs locally on the CPU in about a fifth of a second per photo and costs
nothing, so it is on by default and never recorded as a fixture.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Callable

from ..providers.base import ImageRef

# Below this the detector is guessing at noise, a bolt head or a reflection.
MIN_SCORE = 0.6
# The engine sees a copy no larger than this. The detector's memory grows
# with the square of the side: four 1600 pixel frames peaked at 760 MB above
# the loaded model, four 960 pixel frames at 270, and a plate photographed
# up close is still legible at 960. On a 512 MB host this is the difference
# between working and being killed.
OCR_MAX_SIDE = 960

OcrReader = Callable[[tuple[ImageRef, ...]], list[str]]
"""Photos in, legible lines out. Injected so tests never load the model."""


@dataclass
class _RapidReader:
    """Lazy wrapper so importing this module costs nothing."""

    _engine: object | None = None
    # One engine serves every worker thread; a read takes a fifth of a second
    # so taking turns costs nothing and the engine is never entered twice.
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def __call__(self, images: tuple[ImageRef, ...]) -> list[str]:
        with self._lock:
            self._load()
            return [line for image in images for line in self._read(image)]

    def boxes(self, path) -> list[tuple[str, list[tuple[float, float]]]]:
        """Each legible line with the corners of its box, in the photo's own pixels.

        Testify uses this to paint a plate out of a photo, never to read one, so a
        line the engine is unsure of comes back too: half a code is still a code."""
        with self._lock:
            self._load()
            return [(text, corners) for text, _, corners in self._detect(path, min_score=0.0)]

    def _load(self) -> None:
        if self._engine is None:
            import logging

            from rapidocr import RapidOCR

            # It announces every model file it loads at INFO, and resets
            # its own logger level from this setting on construction.
            logging.getLogger("RapidOCR").setLevel(logging.WARNING)
            self._engine = RapidOCR(
                params={
                    "Global.log_level": "warning",
                    "Global.max_side_len": OCR_MAX_SIDE,
                    # Two threads read a plate in well under a second; more
                    # only adds per-thread buffers on a small host.
                    "EngineConfig.onnxruntime.intra_op_num_threads": 2,
                }
            )

    def _read(self, image: ImageRef) -> list[str]:
        lines: list[str] = []
        for text, _, _ in self._detect(image.path):
            if text not in lines:
                lines.append(text)
        return lines

    def _detect(self, path, min_score: float = MIN_SCORE) -> list[tuple[str, float, list[tuple[float, float]]]]:
        import numpy as np
        from PIL import Image

        with Image.open(path) as im:
            width = im.width
            im.thumbnail((OCR_MAX_SIDE, OCR_MAX_SIDE))
            scale = width / im.width
            frame = np.asarray(im.convert("RGB"))[:, :, ::-1].copy()  # the engine wants BGR
        result = self._engine(frame)
        boxes = result.boxes if result.boxes is not None else [None] * len(result.txts or ())
        found = []
        for text, score, box in zip(result.txts or (), result.scores or (), boxes):
            text = str(text).strip()
            if text and float(score) >= min_score:
                corners = [(float(x) * scale, float(y) * scale) for x, y in box] if box is not None else []
                found.append((text, float(score), corners))
        return found


def default_reader() -> OcrReader | None:
    """The bundled OCR engine, or None when it is not installed."""
    try:
        import onnxruntime  # noqa: F401
        import rapidocr  # noqa: F401
    except ImportError:
        return None
    return _RapidReader()
