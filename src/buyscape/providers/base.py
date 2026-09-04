"""The one interface every vision model call goes through.

Callers never import a vendor SDK. They build a ModelRequest, hand it to a
provider, and get back a validated pydantic object plus a CallMeta recording
what the call cost. Swapping Qwen for Gemini for Claude is a config change.
"""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ProviderError(RuntimeError):
    """The provider could not answer. Callers decide whether to fail over."""


class MissingFixture(RuntimeError):
    """Replay mode was asked for a call that was never recorded."""


@dataclass(frozen=True)
class ImageRef:
    """One image, addressed by content so fixtures survive a move on disk."""

    path: Path
    label: str | None = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    @property
    def mime(self) -> str:
        return mimetypes.guess_type(self.path.name)[0] or "image/jpeg"

    def data_url(self) -> str:
        b64 = base64.b64encode(self.path.read_bytes()).decode()
        return f"data:{self.mime};base64,{b64}"


@dataclass(frozen=True)
class ModelRequest:
    """Everything a call needs. Hashable, so it doubles as the fixture key."""

    task: str
    prompt_version: str
    system: str
    user_text: str
    output_schema: type[BaseModel]
    images: tuple[ImageRef, ...] = ()
    max_tokens: int = 1500
    temperature: float = 0.0

    def fixture_key(self) -> str:
        payload = {
            "task": self.task,
            "prompt_version": self.prompt_version,
            "system": self.system,
            "user_text": self.user_text,
            "schema": self.output_schema.model_json_schema(),
            "images": [img.sha256 for img in self.images],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        blob = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(blob).hexdigest()[:32]


@dataclass
class CallMeta:
    """What the call cost and where it went. Written to every case report."""

    provider: str
    model: str
    task: str
    latency_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    replayed: bool = False
    fixture_key: str = ""
    error: str | None = None


class VisionProvider(Protocol):
    """Implemented by every adapter, the recorder, and the fake."""

    name: str
    model: str

    def structured_call(self, request: ModelRequest) -> tuple[BaseModel, CallMeta]:
        """Return a validated instance of request.output_schema, plus metering."""
        ...


@dataclass
class CostMeter:
    """Running spend for one case, so the report can show cost per job."""

    calls: list[CallMeta] = field(default_factory=list)

    def record(self, meta: CallMeta) -> CallMeta:
        self.calls.append(meta)
        return meta

    @property
    def total_usd(self) -> float:
        return round(sum(c.cost_usd for c in self.calls), 6)

    @property
    def total_ms(self) -> int:
        return sum(c.latency_ms for c in self.calls)

    def by_task(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for c in self.calls:
            out[c.task] = round(out.get(c.task, 0.0) + c.cost_usd, 6)
        return out
