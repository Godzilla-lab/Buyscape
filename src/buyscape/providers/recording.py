"""Record real calls once, replay them for ever after.

Every eval run and every test goes through this. In replay mode a call that was
never recorded raises rather than silently reaching the network, so a changed
prompt version fails loudly instead of quietly costing money.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .base import CallMeta, MissingFixture, ModelRequest, VisionProvider

Mode = Literal["record", "replay", "auto"]


class RecordingProvider:
    """Wraps any provider. Same interface, so callers cannot tell."""

    def __init__(
        self,
        inner: VisionProvider | None,
        fixture_dir: Path,
        mode: Mode = "auto",
    ) -> None:
        self._inner = inner
        self._dir = fixture_dir
        self._mode: Mode = mode
        self.name = inner.name if inner else "replay-only"
        self.model = inner.model if inner else "replay-only"

    def _path(self, request: ModelRequest) -> Path:
        return self._dir / request.task / f"{request.fixture_key()}.json"

    def structured_call(self, request: ModelRequest) -> tuple[BaseModel, CallMeta]:
        path = self._path(request)
        if self._mode in ("replay", "auto") and path.exists():
            saved = json.loads(path.read_text())
            parsed = request.output_schema.model_validate(saved["response"])
            meta = CallMeta(**saved["meta"])
            meta.replayed = True
            return parsed, meta
        if self._mode == "replay":
            raise MissingFixture(
                f"no fixture for task={request.task} key={request.fixture_key()} "
                f"(model={self.model}); record it before replaying"
            )
        if self._inner is None:
            raise MissingFixture("replay-only provider has no fixture for this call")

        parsed, meta = self._inner.structured_call(request)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "task": request.task,
                    "prompt_version": request.prompt_version,
                    "model": self.model,
                    "response": parsed.model_dump(mode="json"),
                    "meta": meta.__dict__,
                },
                indent=2,
            )
        )
        return parsed, meta
