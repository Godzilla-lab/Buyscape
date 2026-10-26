"""Adapter for any OpenAI-compatible chat endpoint.

OpenRouter and xAI speak the same protocol, so they share one implementation
and differ only in base URL and price table. Adding another such vendor is a
new entry in ENDPOINTS, not a new file.
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
XAI_URL = "https://api.x.ai/v1/chat/completions"

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
    # Cheap thinking vision models, OpenRouter catalogue 2026-09-04.
    "z-ai/glm-5.3-flash": (0.070, 0.250),
    "openai/gpt-5.6-luna": (0.200, 1.200),
    "qwen/qwen3.8-27b": (0.420, 3.000),
    "google/gemini-3.5-flash-lite": (0.300, 2.500),
    "anthropic/claude-sonnet-5": (2.000, 10.000),
    "anthropic/claude-opus-5": (5.000, 25.000),
    "anthropic/claude-fable-5.1": (10.000, 50.000),
    # xAI, list prices fetched 2026-09-03, under the 200k prompt tier.
    "grok-4.6": (2.000, 6.000),
    "grok-4.5": (2.000, 6.000),
    "grok-4.3": (1.250, 2.500),
}

# Models that think before answering. Their thoughts count against max_tokens
# and are billed as output, so they get a low effort setting and headroom.
REASONING_MODELS = {
    "z-ai/glm-5.3-flash",
    "openai/gpt-5.6-luna",
    "qwen/qwen3.8-27b",
    "google/gemini-3.8-flash",
    "google/gemini-3.5-flash-lite",
}
# High effort on purpose: these models are cheap enough that thinking hard
# costs a fraction of a cent, and the decider must be right, not just cheap.
REASONING_EFFORT = "high"
REASONING_HEADROOM = 4096

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def content(request: ModelRequest) -> list[dict]:
    """The user turn: the request's text, then each photo after its label."""
    parts: list[dict] = [{"type": "text", "text": request.user_text}]
    for img in request.images:
        if img.label:
            parts.append({"type": "text", "text": f"[{img.label}]"})
        parts.append({"type": "image_url", "image_url": {"url": img.data_url(request.image_max_side)}})
    return parts


def system_text(request: ModelRequest) -> str:
    """The system turn: the task's instructions, then the answer's JSON Schema."""
    schema = request.output_schema.model_json_schema()
    return (
        f"{request.system}\n\n"
        "Reply with a single JSON object and nothing else. It must validate "
        f"against this JSON Schema:\n{json.dumps(schema)}"
    )


def chat_body(request: ModelRequest) -> dict:
    """The chat request every OpenAI-style server is sent, less the model name.

    A batch run on someone's own GPU is sent the same body, so a model scores
    the same wherever it runs.
    """
    messages = [
        {"role": "system", "content": system_text(request)},
        {"role": "user", "content": content(request)},
    ]
    for reply, said in request.turns:
        messages += [{"role": "assistant", "content": reply}, {"role": "user", "content": said}]
    return {
        "messages": messages,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "response_format": {"type": "json_object"},
    }


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

    #: vendor -> (base url, env var holding the key)
    ENDPOINTS: dict[str, tuple[str, str]] = {
        "openrouter": (API_URL, "OPENROUTER_API_KEY"),
        "xai": (XAI_URL, "XAI_API_KEY"),
        # NVIDIA's API catalogue serves open vision models on a free developer tier.
        "nvidia": ("https://integrate.api.nvidia.com/v1/chat/completions", "NVIDIA_API_KEY"),
        # Kaggle Benchmarks' model proxy: frontier models on a free daily quota.
        # Its address and a two-hour key come from `kaggle benchmarks auth`.
        "kaggle": ("", "MODEL_PROXY_API_KEY"),
    }

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        timeout: float = 180.0,
        max_retries: int = 2,
        client: httpx.Client | None = None,
        vendor: str = "openrouter",
        network_retries: int = 5,
    ) -> None:
        if vendor not in self.ENDPOINTS:
            raise ProviderError(f"unknown vendor {vendor!r}")
        self.model = model
        self.vendor = vendor
        self.name = f"{vendor}:{model}"
        self._url, env_var = self.ENDPOINTS[vendor]
        if vendor == "kaggle":
            self._url = os.environ.get("MODEL_PROXY_URL", "").rstrip("/") + "/openapi/chat/completions"
        self._key = api_key or os.environ.get(env_var, "")
        if not self._key:
            raise ProviderError(f"{env_var} is not set")
        self._timeout = timeout
        self._max_retries = max_retries
        self._network_retries = network_retries
        self._client = client or httpx.Client(timeout=timeout)
        self._sleep = time.sleep

    def _content(self, request: ModelRequest) -> list[dict]:
        return content(request)

    def _cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        rate_in, rate_out = PRICES.get(self.model, (0.0, 0.0))
        return round(
            prompt_tokens / 1e6 * rate_in + completion_tokens / 1e6 * rate_out, 6
        )

    def structured_call(self, request: ModelRequest) -> tuple[BaseModel, CallMeta]:
        body = {"model": self.model, **chat_body(request)}
        if self._url == API_URL:
            # OpenRouter returns the amount it actually billed. That number,
            # not the list table, is what a spending cap must be measured on.
            body["usage"] = {"include": True}
            if self.model in REASONING_MODELS:
                body["reasoning"] = {"effort": REASONING_EFFORT, "exclude": True}
                body["max_tokens"] = request.max_tokens + REASONING_HEADROOM
        if self.vendor == "kaggle":
            # The proxy refuses JSON mode, and Claude refuses a temperature;
            # the system prompt still asks for the JSON object alone.
            body.pop("response_format")
            if self.model.startswith("anthropic/"):
                body.pop("temperature")
        headers = {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
            "X-Title": "Buyscape valuation eval",
        }

        last: Exception | None = None
        spent = 0.0  # every attempt is billed, including the ones that fail validation
        failures = 0  # the model or the gateway answered badly
        outages = 0  # the network itself failed: DNS, refused, timed out
        while True:
            started = time.perf_counter()
            try:
                resp = self._client.post(self._url, json=body, headers=headers)
                if resp.status_code >= 500 or resp.status_code == 429:
                    raise ProviderError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                if resp.status_code != 200:
                    raise ProviderError(f"HTTP {resp.status_code}: {resp.text[:300]}")
                payload = resp.json()
                text = payload["choices"][0]["message"]["content"] or ""
                usage = payload.get("usage") or {}
                prompt_tokens = int(usage.get("prompt_tokens") or 0)
                completion_tokens = int(usage.get("completion_tokens") or 0)
                billed = usage.get("cost")
                if isinstance(billed, dict):
                    # Kaggle's proxy reports its quota spent in nanodollars.
                    billed = sum(float(v) for v in billed.values()) / 1e9
                spent += (
                    round(float(billed), 6)
                    if billed is not None
                    else self._cost(prompt_tokens, completion_tokens)
                )
                cost = round(spent, 6)
                parsed = request.output_schema.model_validate(_extract_json(text))
                meta = CallMeta(
                    provider=self.name,
                    model=self.model,
                    task=request.task,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    cost_usd=cost,
                    fixture_key=request.fixture_key(),
                )
                return parsed, meta
            except httpx.TransportError as exc:
                # The network is down, not the model. A DNS blip lasts minutes,
                # so wait it out: two seconds doubling to half a minute. Giving
                # up here turns a whole run into PROVIDER_ERROR reports.
                last = exc
                outages += 1
                if outages > self._network_retries:
                    break
                self._sleep(min(2.0 * 2 ** (outages - 1), 32.0))
            except (httpx.HTTPError, ProviderError, KeyError, ValidationError) as exc:
                last = exc
                failures += 1
                if failures > self._max_retries:
                    break
                self._sleep(1.5 * failures)
        raise ProviderError(f"{self.name} failed after retries: {last}")
