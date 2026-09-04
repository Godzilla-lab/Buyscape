"""A deterministic provider for tests and for wiring the pipeline without a key.

It reads nothing from the images. It exists to prove the plumbing, and it is
deliberately unable to identify anything, so any eval run against it should
report a near total abstention rate. If a fake run ever shows good accuracy,
the harness is measuring itself rather than a model.
"""

from __future__ import annotations

import time

from pydantic import BaseModel

from .base import CallMeta, ModelRequest


class FakeProvider:
    name = "fake"
    model = "fake"

    def __init__(self, reading_overrides: dict | None = None) -> None:
        self._overrides = reading_overrides or {}

    def structured_call(self, request: ModelRequest) -> tuple[BaseModel, CallMeta]:
        started = time.perf_counter()
        if request.task == "read_evidence":
            payload = {
                "category": None,
                "category_confidence": 0.0,
                "visible_text": [],
                "has_label_or_plate": False,
                **self._overrides,
            }
        elif request.task == "identify":
            payload = {
                "candidates": [],
                "cannot_identify": True,
                "reason_if_cannot": "fake provider never identifies",
            }
        elif request.task == "extract_claims":
            payload = {"claims": []}
        else:
            payload = {}
        parsed = request.output_schema.model_validate(payload)
        meta = CallMeta(
            provider=self.name,
            model=self.model,
            task=request.task,
            latency_ms=int((time.perf_counter() - started) * 1000),
            fixture_key=request.fixture_key(),
        )
        return parsed, meta
