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
            if self._engine is None:
                import logging

                from rapidocr import RapidOCR

                # It announces every model file it loads at INFO, and resets
                # its own logger level from this setting on construction.
                logging.getLogger("RapidOCR").setLevel(logging.WARNING)
                self._engine = RapidOCR(params={"Global.log_level": "warning"})
            return [line for image in images for line in self._read(image)]

    def _read(self, image: ImageRef) -> list[str]:
        result = self._engine(str(image.path))
        lines: list[str] = []
        for text, score in zip(result.txts or (), result.scores or ()):
            text = str(text).strip()
            if text and float(score) >= MIN_SCORE and text not in lines:
                lines.append(text)
        return lines


def default_reader() -> OcrReader | None:
    """The bundled OCR engine, or None when it is not installed."""
    try:
        import onnxruntime  # noqa: F401
        import rapidocr  # noqa: F401
    except ImportError:
        return None
    return _RapidReader()
