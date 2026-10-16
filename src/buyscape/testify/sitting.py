"""Let a person or an agent sit the test, with the same inputs a model gets.

`export` writes every request a run still needs, one folder per case: the
exact instructions a model is sent, the seller's words and the photos, under
a plain case number, because some item ids give the title away. Whoever sits
the test writes an `answer.json` in each folder. `import_answers` turns those
into recorded calls, so `buyscape testify --mode replay` scores them exactly
as it scores a model's.

The read step comes first. Once its answers are in, export again: the price
picks those answers now need are the second batch. An answer that does not
match the schema is kept as written and scores as a failed call, the same as
a model's.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from pydantic import ValidationError

from ..providers.base import MissingFixture, ModelRequest, ProviderError
from ..providers.recording import RecordingProvider
from .answer import PriceChoice, Reading
from .run import run_item

SCHEMAS = {"testify_read": Reading, "testify_pick": PriceChoice}

HEADER = (
    "You are sitting a valuation test. Answer from the files in this folder only: "
    "do not open any other file, run any command or search the web. Write your reply, "
    "the JSON object and nothing else, to answer.json in this folder.\n\n"
)


class _Capture:
    """Replays what is recorded and notes every request that is not."""

    def __init__(self, recorder: RecordingProvider) -> None:
        self.recorder = recorder
        self.context: tuple[str, str] = ("", "")
        self.missing: list[tuple[str, str, ModelRequest]] = []

    def structured_call(self, request: ModelRequest):
        try:
            return self.recorder.structured_call(request)
        except MissingFixture:
            self.missing.append((*self.context, request))
            raise ProviderError("not answered yet") from None


def _prompt(request: ModelRequest, photos: list[str]) -> str:
    schema = json.dumps(request.output_schema.model_json_schema())
    lines = [
        HEADER,
        "## Instructions\n",
        request.system,
        "\nReply with a single JSON object and nothing else. It must validate against this JSON Schema:\n",
        schema,
        "\n## The request\n",
        request.user_text,
    ]
    if photos:
        lines += ["\n## Photos\n", *(f"- photo {n}: {name}" for n, name in enumerate(photos))]
    return "\n".join(lines) + "\n"


def export(model_dir: Path, cases: list[tuple], pool, out: Path, lies: bool = True) -> int:
    """Write a folder per unanswered request. `cases` holds (item, photos, own_photo_hashes)."""
    capture = _Capture(RecordingProvider(None, model_dir, mode="replay"))
    for item, photos, own in cases:
        for variant in ("clean", "lie") if lies else ("clean",):
            capture.context = (item.id, variant)
            run_item(capture, item, photos, pool, variant, own)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    index = []
    for n, (item_id, variant, request) in enumerate(capture.missing):
        folder = out / f"case_{n:03d}"
        folder.mkdir()
        names = []
        for i, image in enumerate(request.images):
            name = f"photo_{i}{image.path.suffix.lower()}"
            shutil.copyfile(image.path, folder / name)
            names.append(name)
        (folder / "prompt.md").write_text(_prompt(request, names))
        index.append({"case": folder.name, "task": request.task, "prompt_version": request.prompt_version,
                      "key": request.fixture_key(), "item": item_id, "variant": variant})
    # The index names the items, so it sits beside the cases, never inside them.
    index_path(out).write_text(json.dumps(index, indent=1) + "\n")
    return len(index)


def index_path(out: Path) -> Path:
    return out.parent / f"{out.name}.index.json"


def import_answers(model_dir: Path, out: Path, model: str) -> dict[str, int]:
    """Record each answer.json as a call. Missing answers stay unanswered."""
    counts = {"valid": 0, "invalid": 0, "missing": 0}
    for entry in json.loads(index_path(out).read_text()):
        answer = out / entry["case"] / "answer.json"
        if not answer.exists():
            counts["missing"] += 1
            continue
        text = answer.read_text()
        try:
            response = json.loads(text)
        except json.JSONDecodeError:
            response = {"unparsed": text[:4000]}
        try:
            SCHEMAS[entry["task"]].model_validate(response)
            counts["valid"] += 1
        except ValidationError:
            counts["invalid"] += 1
        path = model_dir / entry["task"] / f"{entry['key']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "task": entry["task"], "prompt_version": entry["prompt_version"], "model": model,
            "response": response,
            "meta": {"provider": "sitting", "model": model, "task": entry["task"], "latency_ms": 0,
                     "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "replayed": False,
                     "fixture_key": entry["key"], "error": None},
        }, indent=2) + "\n")
    return counts
