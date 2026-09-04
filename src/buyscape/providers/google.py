"""Google AI Studio adapter.

Worth its own adapter rather than going through an aggregator: the free tier
serves the same Gemini Flash models that are the production tier 2 candidate,
so the cheap path and the real path are the same model.
"""

from __future__ import annotations

import base64
import json
import os
import time

import httpx
from pydantic import BaseModel, ValidationError

from .base import CallMeta, ModelRequest, ProviderError
from .openrouter import _extract_json

BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# USD per million tokens, list prices fetched 2026-09-03. The free tier bills
# nothing; these are kept so a run reports what the same work would cost paid.
PRICES: dict[str, tuple[float, float]] = {
    "gemini-3.8-flash": (0.75, 3.75),
    "gemini-3.7-flash": (0.75, 3.75),
    "gemini-3.6-flash": (0.75, 3.75),
    "gemini-3.5-flash": (1.50, 9.00),
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "gemini-3.1-flash-lite": (0.25, 1.50),
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.5-flash-lite": (0.10, 0.40),
    "gemini-2.5-pro": (1.25, 10.00),
}


class GoogleProvider:
    """Calls one Gemini model with a response schema and validates the reply."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        timeout: float = 180.0,
        max_retries: int = 4,
        client: httpx.Client | None = None,
    ) -> None:
        self.model = model
        self.name = f"google:{model}"
        self._key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        if not self._key:
            raise ProviderError("GOOGLE_API_KEY is not set")
        self._max_retries = max_retries
        self._client = client or httpx.Client(timeout=timeout)

    def _parts(self, request: ModelRequest) -> list[dict]:
        parts: list[dict] = [{"text": request.user_text}]
        for img in request.images:
            if img.label:
                parts.append({"text": f"[{img.label}]"})
            mime, data = img.encoded(request.image_max_side)
            parts.append(
                {"inline_data": {"mime_type": mime, "data": base64.b64encode(data).decode()}}
            )
        return parts

    def _cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        rate_in, rate_out = PRICES.get(self.model, (0.0, 0.0))
        return round(prompt_tokens / 1e6 * rate_in + completion_tokens / 1e6 * rate_out, 6)

    def structured_call(self, request: ModelRequest) -> tuple[BaseModel, CallMeta]:
        schema = request.output_schema.model_json_schema()
        body = {
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            f"{request.system}\n\nReply with a single JSON object "
                            f"matching this schema:\n{json.dumps(schema)}"
                        )
                    }
                ]
            },
            "contents": [{"role": "user", "parts": self._parts(request)}],
            "generationConfig": {
                "temperature": request.temperature,
                # Gemini 3.x thinks before it answers and the thoughts count
                # against the output cap. Keep thinking low and leave room for
                # it, or the JSON arrives truncated and the call is retried.
                "maxOutputTokens": request.max_tokens + 4096,
                "thinkingConfig": {"thinkingLevel": "high"},
                "responseMimeType": "application/json",
            },
        }
        url = f"{BASE}/{self.model}:generateContent"
        headers = {"x-goog-api-key": self._key, "Content-Type": "application/json"}

        last: Exception | None = None
        spent = 0.0
        for attempt in range(self._max_retries + 1):
            started = time.perf_counter()
            try:
                resp = self._client.post(url, json=body, headers=headers)
                if resp.status_code in (429, 503):
                    # The free tier meters requests per minute and sheds load
                    # under demand. Both pass with patience, not with money.
                    time.sleep(12.0 * (attempt + 1))
                    raise ProviderError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                if resp.status_code != 200:
                    raise ProviderError(f"HTTP {resp.status_code}: {resp.text[:300]}")
                payload = resp.json()
                candidates = payload.get("candidates") or []
                if not candidates:
                    raise ProviderError(f"no candidates: {json.dumps(payload)[:300]}")
                text = "".join(
                    part.get("text", "")
                    for part in (candidates[0].get("content") or {}).get("parts") or []
                )
                usage = payload.get("usageMetadata") or {}
                prompt_tokens = int(usage.get("promptTokenCount") or 0)
                completion_tokens = int(usage.get("candidatesTokenCount") or 0) + int(
                    usage.get("thoughtsTokenCount") or 0
                )  # thoughts are billed as output on the paid tier
                spent += self._cost(prompt_tokens, completion_tokens)
                parsed = request.output_schema.model_validate(_extract_json(text))
                return parsed, CallMeta(
                    provider=self.name,
                    model=self.model,
                    task=request.task,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    cost_usd=round(spent, 6),
                    fixture_key=request.fixture_key(),
                )
            except (httpx.HTTPError, ProviderError, KeyError, ValidationError) as exc:
                last = exc
                if attempt < self._max_retries:
                    time.sleep(2.0 * (attempt + 1))
        raise ProviderError(f"{self.name} failed after retries: {last}")
