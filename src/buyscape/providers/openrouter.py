"""OpenRouter adapter: one key reaches Qwen, Gemini and Claude.

Production will add direct adapters for Alibaba Model Studio, Google AI and
Anthropic. Nothing outside this file changes when that happens.
"""

from __future__ import annotations

import json
import os
import re
import time

import httpx
from pydantic import BaseModel, ValidationError

from .base import CallMeta, ModelRequest, ProviderError

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# USD per million tokens, list prices fetched 2026-09-03. Used only to report
# cost per job; billing is whatever the provider actually charges.
PRICES: dict[str, tuple[float, float]] = {
    "qwen/qwen3-vl-8b-instruct": (0.117, 0.455),
    "qwen/qwen3-vl-32b-instruct": (0.104, 0.416),
    "qwen/qwen3-vl-30b-a3b-instruct": (0.150, 0.600),
    "qwen/qwen3-vl-235b-a22b-instruct": (0.210, 1.900),
    "qwen/qwen2.5-vl-72b-instruct": (0.800, 1.000),
    "google/gemini-2.5-flash-lite": (0.100, 0.400),
    "google/gemini-3.1-flash-lite": (0.250, 1.500),
    "google/gemini-3.5-flash-lite": (0.300, 2.500),
    "google/gemini-3.5-flash": (1.500, 9.000),
    "google/gemini-3.8-flash": (0.750, 3.750),
    "google/gemini-3.1-pro-preview": (2.000, 12.000),
    "anthropic/claude-haiku-4.5": (1.000, 5.000),
    "anthropic/claude-sonnet-5": (2.000, 10.000),
    "anthropic/claude-opus-5": (5.000, 25.000),
    "anthropic/claude-fable-5.1": (10.000, 50.000),
}

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def _extract_json(text: str) -> dict:
    """Models wrap JSON in prose or fences more often than they should."""
    text = text.strip()
    fenced = _FENCE.search(text)
    if fenced:
        text = fenced.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start, depth = None, 0
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            depth += 1
        elif ch == "}" and start is not None:
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    start, depth = None, 0
    raise ProviderError(f"no JSON object in response: {text[:200]}")


class OpenRouterProvider:
    """Calls one model and validates the reply against the requested schema."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        timeout: float = 120.0,
        max_retries: int = 2,
        client: httpx.Client | None = None,
    ) -> None:
        self.model = model
        self.name = f"openrouter:{model}"
        self._key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        if not self._key:
            raise ProviderError("OPENROUTER_API_KEY is not set")
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = client or httpx.Client(timeout=timeout)

    def _content(self, request: ModelRequest) -> list[dict]:
        parts: list[dict] = [{"type": "text", "text": request.user_text}]
        for img in request.images:
            if img.label:
                parts.append({"type": "text", "text": f"[{img.label}]"})
            parts.append({"type": "image_url", "image_url": {"url": img.data_url()}})
        return parts

    def _cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        rate_in, rate_out = PRICES.get(self.model, (0.0, 0.0))
        return round(
            prompt_tokens / 1e6 * rate_in + completion_tokens / 1e6 * rate_out, 6
        )

    def structured_call(self, request: ModelRequest) -> tuple[BaseModel, CallMeta]:
        schema = request.output_schema.model_json_schema()
        system = (
            f"{request.system}\n\n"
            "Reply with a single JSON object and nothing else. It must validate "
            f"against this JSON Schema:\n{json.dumps(schema)}"
        )
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": self._content(request)},
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
            "X-Title": "Buyscape valuation eval",
        }

        last: Exception | None = None
        for attempt in range(self._max_retries + 1):
            started = time.perf_counter()
            try:
                resp = self._client.post(API_URL, json=body, headers=headers)
                if resp.status_code >= 500 or resp.status_code == 429:
                    raise ProviderError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                if resp.status_code != 200:
                    raise ProviderError(f"HTTP {resp.status_code}: {resp.text[:300]}")
                payload = resp.json()
                text = payload["choices"][0]["message"]["content"] or ""
                usage = payload.get("usage") or {}
                prompt_tokens = int(usage.get("prompt_tokens") or 0)
                completion_tokens = int(usage.get("completion_tokens") or 0)
                parsed = request.output_schema.model_validate(_extract_json(text))
                meta = CallMeta(
                    provider=self.name,
                    model=self.model,
                    task=request.task,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    cost_usd=self._cost(prompt_tokens, completion_tokens),
                    fixture_key=request.fixture_key(),
                )
                return parsed, meta
            except (httpx.HTTPError, ProviderError, KeyError, ValidationError) as exc:
                last = exc
                if attempt < self._max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise ProviderError(f"{self.name} failed after retries: {last}")
