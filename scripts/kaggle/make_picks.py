"""Write a Kaggle notebook that answers a trained model's price picks.

    python make_picks.py 4b testify-qwen3-vl-4b-sft-500 eval/testify/batches/local_qwen_qwen3-vl-4b-sft500

The training notebook's output (the adapter) comes in as a kernel source; it
is folded into the base before vLLM is installed, since vLLM replaces the
transformers that folding needs. The pick questions travel inside the
notebook: text only, no photos. Nothing is pushed from here.
"""
import argparse, base64, json, zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "src" / "buyscape" / "testify"

p = argparse.ArgumentParser()
p.add_argument("size", choices=("2b", "4b", "8b"))
p.add_argument("trained", help="The training notebook's slug, its output holds adapter/.")
p.add_argument("batches", type=Path, help="Folder with dev.jsonl and dev.repeat1.jsonl from testify-batch-export.")
p.add_argument("--owner", required=True, help="Your Kaggle username.")
p.add_argument("--files", default="dev.jsonl,dev.repeat1.jsonl", help="The pick batches to answer, test.jsonl for the test split.")
p.add_argument("--slug-suffix", default="picks", help="test-picks for the test split, so the dev notebook is kept.")
a = p.parse_args()

t = (HERE / "template.py").read_text()
head = t[: t.index('sh("nvidia-smi --query-gpu=name,memory.total --format=csv")')]
head = head.replace("# Testify fine-tune: LoRA on Qwen3-VL 8B Instruct over the training set from\n# `buyscape testify-train-build`, then the tuned model answers the dev reads.",
                    f"# Testify, price picks of a trained Qwen3-VL {a.size.upper()}: the training notebook's adapter\n# is folded into the base, then the pick questions its reads led to are answered.")
head = head.replace('"__HOURS__"', '"1.5"')
assert "__HOURS__" not in head
tail = t[t.index("# vLLM from the public wheel set, after training"):]
tail = tail[: tail.index("batches = find(")]
# Compressed: a notebook over about a megabyte is refused by Kaggle.
emb = {n: base64.b64encode(zlib.compress((a.batches / n).read_bytes(), 9)).decode()
       for n in a.files.split(",") if (a.batches / n).exists()}
body = f'''sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
os.environ.update(PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", TOKENIZERS_PARALLELISM="false")
(W / "sft_lora.py").write_bytes(base64.b64decode("{base64.b64encode((REPO / "sft_lora.py").read_bytes()).decode()}"))
(W / "vllm_batch.py").write_bytes(base64.b64decode("{base64.b64encode((REPO / "vllm_batch.py").read_bytes()).decode()}"))

model = find("{a.size}-instruct/**/config.json").parent
adapter = find("adapter/adapter_config.json").parent
print("model", model, "adapter", adapter, flush=True)
sh(f"{{sys.executable}} -m pip uninstall -y torchao", 300)
code = sh(f"{{sys.executable}} {{W}}/sft_lora.py --model {{model}} --merge {{adapter}} --out /tmp/merged", 2400)
print("merge exit", code, flush=True)
if code != 0:
    os._exit(0)

'''
run = f'''# The pick questions the reads led to travel inside the notebook: text only, no photos.
import zlib
batches = W / "batches"
batches.mkdir(exist_ok=True)
for name, data in {json.dumps(emb)}.items():
    (batches / name).write_bytes(zlib.decompress(base64.b64decode(data)))
gpus = int(subprocess.run("nvidia-smi -L | wc -l", shell=True, capture_output=True, text=True).stdout.strip() or 1)
run = (f"{{sys.executable}} {{W}}/vllm_batch.py --model /tmp/merged --max-model-len 12288 --tensor-parallel {{gpus}}"
       " --dtype half --plain-all-reduce --attention-backend TRITON_ATTN --gpu-memory 0.80 --max-num-seqs 16 --chunk 32")
for name in sorted(p.name for p in batches.glob("*.jsonl")):
    code = sh(f"{{run}} --batch {{batches}}/{{name}} --out {{W}}/{{name.replace('.jsonl', '.results.jsonl')}}", left() - 300)
    print(name, "exit", code, flush=True)
sh("wc -l /kaggle/working/*.results.jsonl", 60)
os._exit(0)
'''
src = head + body + tail + run
slug = f"{a.trained}-{a.slug_suffix}"
out = HERE / "out" / slug
out.mkdir(parents=True, exist_ok=True)
(out / "run.py").write_text(src)
compile(src, str(out / "run.py"), "exec")
meta = {
    "id": f"{a.owner}/{slug}", "title": slug, "code_file": "run.py", "language": "python",
    "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_tpu": False,
    "enable_internet": False, "dataset_sources": ["metric/gemma-4-developer-agent-wheelhouse"],
    "kernel_sources": [f"{a.owner}/{a.trained}"], "competition_sources": [],
    "model_sources": [f"qwen-lm/qwen-3-vl/transformers/{a.size}-instruct/1"],
    "machine_shape": "NvidiaTeslaT4",
    "docker_image": json.loads((HERE / "environment.json").read_text())["docker_image"],
}
(out / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
print(out, meta["id"], {k: len(zlib.decompress(base64.b64decode(v)).splitlines()) for k, v in emb.items()}, len(src), "bytes")
