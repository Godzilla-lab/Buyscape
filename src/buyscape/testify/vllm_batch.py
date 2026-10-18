"""Answer a Testify batch with an open model on your own GPU, through vLLM.

Standalone: it needs vLLM and the standard library, not buyscape, so it runs
as it is on a Kaggle notebook or a lab machine.

    python vllm_batch.py --model /path/to/Qwen3-VL-8B-Instruct \\
        --batch dev.jsonl --out dev.results.jsonl

Each batch line holds the chat body an API model is sent (`buyscape
testify-batch-export` writes it). Each answer goes out as one line,
{"custom_id", "text", "input_tokens", "output_tokens", "latency_ms",
"error"}, for `buyscape testify-batch-import`. Answers are written as they
finish, and a rerun skips every request already answered, so a run cut off
by a time limit loses one chunk at most.

The body's own settings are kept: its temperature (zero, so the most likely
answer), its token cap, and JSON mode, which only forces syntactically valid
JSON, as `response_format: json_object` does on an API.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def _requests(batches: list[Path], done: set[str], limit: int) -> list[dict]:
    out, seen = [], set(done)
    for path in batches:
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row["custom_id"] in seen:
                continue
            seen.add(row["custom_id"])
            out.append(row)
    return out[:limit] if limit else out


def _json_mode():
    """JSON mode in whichever form this vLLM version spells it."""
    try:
        from vllm.sampling_params import StructuredOutputsParams

        return {"structured_outputs": StructuredOutputsParams(json_object=True)}
    except ImportError:
        from vllm.sampling_params import GuidedDecodingParams

        return {"guided_decoding": GuidedDecodingParams(json_object=True)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--model", required=True, help="A local folder or a Hugging Face name.")
    parser.add_argument("--batch", type=Path, nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-model-len", type=int, default=20000)
    parser.add_argument("--gpu-memory", type=float, default=0.92)
    parser.add_argument("--tensor-parallel", type=int, default=1)
    parser.add_argument("--max-images", type=int, default=4)
    parser.add_argument("--chunk", type=int, default=48, help="Requests sent together; answers are saved after each.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--quantization", default=None, help="For example fp8, to make room on a small card.")
    parser.add_argument("--dtype", default="auto", help="half on a card without bfloat16, such as a T4.")
    parser.add_argument(
        "--attention-backend", default=None,
        help="TRITON_ATTN on a card FlashInfer has no prebuilt kernels for, such as a T4.",
    )
    parser.add_argument(
        "--plain-all-reduce", action="store_true",
        help="Split across cards with NCCL alone, for pairs without a direct link such as two T4s.",
    )
    args = parser.parse_args()

    done: set[str] = set()
    if args.out.exists():
        for line in args.out.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get("text") or not row.get("error"):
                    done.add(row["custom_id"])
    todo = _requests(args.batch, done, args.limit)
    print(f"{len(done)} answered before, {len(todo)} to answer", flush=True)
    if not todo:
        return

    from vllm import LLM, SamplingParams

    extra = {"attention_backend": args.attention_backend} if args.attention_backend else {}
    llm = LLM(
        **extra,
        model=args.model,
        max_model_len=args.max_model_len,
        gpu_memory_utilization=args.gpu_memory,
        tensor_parallel_size=args.tensor_parallel,
        limit_mm_per_prompt={"image": args.max_images},
        quantization=args.quantization,
        dtype=args.dtype,
        disable_custom_all_reduce=args.plain_all_reduce,
        seed=0,
    )
    mode = _json_mode()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    for start in range(0, len(todo), args.chunk):
        chunk = todo[start : start + args.chunk]
        params = [
            SamplingParams(
                temperature=float(r["body"].get("temperature") or 0.0),
                max_tokens=int(r["body"].get("max_tokens") or 1500),
                seed=0,
                **mode,
            )
            for r in chunk
        ]
        began = time.perf_counter()
        rows = []
        try:
            outputs = llm.chat([r["body"]["messages"] for r in chunk], sampling_params=params, use_tqdm=False)
            each = int((time.perf_counter() - began) * 1000 / max(len(chunk), 1))
            for r, o in zip(chunk, outputs, strict=True):
                answer = o.outputs[0]
                rows.append({
                    "custom_id": r["custom_id"],
                    "text": answer.text,
                    "input_tokens": len(o.prompt_token_ids or []),
                    "output_tokens": len(answer.token_ids or []),
                    "latency_ms": each,
                    "finish_reason": answer.finish_reason,
                    "error": None,
                })
        except Exception as exc:  # noqa: BLE001 - a failed chunk is recorded, the run goes on
            rows = [{"custom_id": r["custom_id"], "text": "", "error": f"{type(exc).__name__}: {exc}"[:500]}
                    for r in chunk]
        with args.out.open("a") as fh:
            fh.writelines(json.dumps(row) + "\n" for row in rows)
        print(f"[{start + len(chunk)}/{len(todo)}] {time.perf_counter() - began:.0f}s", flush=True)


if __name__ == "__main__":
    main()
