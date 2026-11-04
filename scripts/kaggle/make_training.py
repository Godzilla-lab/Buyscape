"""Write one Kaggle training notebook per size-curve point, from template.py.

    python make_training.py 4b sft_500 --hours 3          the notebook in out/4b_sft_500
    python make_training.py 4b sft_500 --check-only       stop after the speed check

The runner and trainer are taken from the repo at the time of writing, so the
notebook carries the code it was built with. Nothing is pushed from here.
"""
import argparse, base64, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "src" / "buyscape" / "testify"

p = argparse.ArgumentParser()
p.add_argument("size", choices=("2b", "4b", "8b"))
p.add_argument("data", help="sft_500, sft_1500 or sft")
p.add_argument("--hours", type=float, default=3.0, help="The whole session: training, folding in, answering.")
p.add_argument("--eval-minutes", type=int, default=100, help="Kept back from training to fold in and answer the dev reads.")
p.add_argument("--epochs", type=float, default=1.0, help="Passes over the set; 1 fits a Kaggle session for the smaller sets.")
p.add_argument("--check-only", action="store_true")
p.add_argument("--owner", required=True, help="Your Kaggle username.")
p.add_argument("--suffix", default="", help="Added to the notebook name, so a rerun keeps the last run's output.")
a = p.parse_args()

t = (HERE / "template.py").read_text()
subs = {
    "__HOURS__": str(a.hours),
    "__SFT__": base64.b64encode((REPO / "sft_lora.py").read_bytes()).decode(),
    "__VLLM__": base64.b64encode((REPO / "vllm_batch.py").read_bytes()).decode(),
    "__EVAL_S__": str(a.eval_minutes * 60),
    "__TRAIN_ARGS__": f"--epochs {a.epochs:g}",
    "# Testify fine-tune: LoRA on Qwen3-VL 8B Instruct": f"# Testify fine-tune: LoRA on Qwen3-VL {a.size.upper()} Instruct",
    'find("8b-instruct/**/config.json")': f'find("{a.size}-instruct/**/config.json")',
    'find("sft_2400.jsonl")': f'find("{a.data}.jsonl")',
}
for k, v in subs.items():
    assert k in t, k
    t = t.replace(k, v)
old = '''root = Path("/tmp/root")
(root / "eval").mkdir(parents=True, exist_ok=True)
if not (root / "eval" / "raw").exists():
    os.symlink(photos, root / "eval" / "raw")
'''
new = '''extra = find("extra_photos/testify_train_constructed").parent
root = Path("/tmp/root")
raw = root / "eval" / "raw"
if not raw.exists():
    # The photo dataset, then the training set's own photos laid over it:
    # painted copies and ones the photo dataset lacks. Links, not copies.
    raw.mkdir(parents=True)
    sh(f"cp -rsf {photos}/. {raw}/", 1800)
    sh(f"cp -rsf {extra}/. {raw}/", 600)
'''
assert t.count(old) == 1
t = t.replace(old, new)
if a.check_only:
    old = 'if per_chat > 30:'
    assert t.count(old) == 1
    t = t.replace(old, 'print("speed check only: stopping", flush=True)\ndone()\nif per_chat > 30:')
out = HERE / "out" / f"{a.size}_{a.data}{'_check' if a.check_only else ''}{'_' + a.suffix if a.suffix else ''}"
out.mkdir(parents=True, exist_ok=True)
(out / "run.py").write_text(t)
slug = f"testify-qwen3-vl-{a.size}-{a.data.replace('_', '-')}{'-check' if a.check_only else ''}{'-' + a.suffix if a.suffix else ''}"
meta = {
    "id": f"{a.owner}/{slug}", "title": slug, "code_file": "run.py", "language": "python",
    "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_tpu": False,
    "enable_internet": False,
    "dataset_sources": ["godzilla1215/testify-sft", "godzilla1215/buyscape-testify-jiji",
                        "godzilla1215/testify-batches", "metric/gemma-4-developer-agent-wheelhouse"],
    "kernel_sources": [], "competition_sources": [],
    "model_sources": [f"qwen-lm/qwen-3-vl/transformers/{a.size}-instruct/1"],
    "machine_shape": "NvidiaTeslaT4",
    "docker_image": json.loads((HERE / "environment.json").read_text())["docker_image"],
}
(out / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
compile(t, str(out / "run.py"), "exec")
print(out, meta["id"])
