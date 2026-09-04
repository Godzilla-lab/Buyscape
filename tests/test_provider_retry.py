"""A network outage must not be mistaken for a model failure.

On 4 Sep 2026 a DNS blip lasting a few minutes turned 103 of 178 cases into
PROVIDER_ERROR because every case gave up after two short sleeps. The model was
fine; the machine could not resolve the host. So transport errors back off
long enough for the network to come back, and application errors do not.
"""

from __future__ import annotations

import httpx
import pytest
from pydantic import BaseModel

from buyscape.providers.base import ModelRequest, ProviderError
from buyscape.providers.openrouter import OpenRouterProvider


class Answer(BaseModel):
    word: str


def _request() -> ModelRequest:
    return ModelRequest(
        task="t", prompt_version="t.v1", system="s", user_text="u", output_schema=Answer
    )


class _Response:
    status_code = 200
    text = '{"word": "ok"}'

    def json(self) -> dict:
        return {
            "choices": [{"message": {"content": self.text}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "cost": 0.000001},
        }


class _FlakyClient:
    """Fails with a connection error `outages` times, then answers."""

    def __init__(self, outages: int) -> None:
        self.outages = outages
        self.calls = 0

    def post(self, *args, **kwargs):
        self.calls += 1
        if self.calls <= self.outages:
            raise httpx.ConnectError("[Errno 8] nodename nor servname provided, or not known")
        return _Response()


def _provider(client, **kwargs) -> tuple[OpenRouterProvider, list[float]]:
    provider = OpenRouterProvider("qwen/test", api_key="k", client=client, **kwargs)
    slept: list[float] = []
    provider._sleep = slept.append
    return provider, slept


def test_outage_is_waited_out_with_doubling_backoff():
    client = _FlakyClient(outages=4)
    provider, slept = _provider(client)
    parsed, meta = provider.structured_call(_request())
    assert parsed.word == "ok"
    assert client.calls == 5
    assert slept == [2.0, 4.0, 8.0, 16.0]


def test_outage_longer_than_the_budget_is_a_loud_failure():
    client = _FlakyClient(outages=99)
    provider, slept = _provider(client, network_retries=5)
    with pytest.raises(ProviderError, match="nodename"):
        provider.structured_call(_request())
    assert client.calls == 6
    assert slept == [2.0, 4.0, 8.0, 16.0, 32.0]


def test_application_errors_keep_the_short_retry():
    class _Bad:
        status_code = 500
        text = "upstream"

    class _Client:
        calls = 0

        def post(self, *args, **kwargs):
            self.calls += 1
            return _Bad()

    client = _Client()
    provider, slept = _provider(client, max_retries=2)
    with pytest.raises(ProviderError, match="HTTP 500"):
        provider.structured_call(_request())
    assert client.calls == 3
    assert slept == [1.5, 3.0]
