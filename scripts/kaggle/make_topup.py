"""Write a Kaggle notebook that tops up a finished run: a short set taught on
from that run's adapter (sft_lora --init-adapter), so the result is one adapter.

    python make_topup.py 2b sft_r7top testify-run7 --owner yourname --sources yourname/testify-run7,yourname/testify-run6b --hours 5.5

The dataset holds the short set and init/, the finished run's adapter.
Built from make_resume.py.

The dataset holds the chats file, the photo archives (eval/raw paths inside)
and savepoint/ from the machine that trained before. The notebook unpacks the
photos, puts the save point where sft_lora.py --resumable looks for it, checks
a dozen chats with the run's own settings, trains on from the save point, and
only when the plan's last step is done folds the adapter in and answers the
dev reads, as the training notebooks before it. A session that ends first
leaves its own save point in the output for the next one. Nothing is pushed
from here.
"""
import argparse, base64, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "src" / "buyscape" / "testify"

p = argparse.ArgumentParser()
p.add_argument("size", choices=("2b", "4b"))
p.add_argument("data", help="The chats file's stem, as in the save point's recipe: sft_r6")
p.add_argument("dataset", help="The Kaggle dataset slug holding the chats, photo archives and savepoint/")
p.add_argument("--owner", required=True, help="Your Kaggle username.")
p.add_argument("--hours", type=float, default=11.5)
p.add_argument("--eval-minutes", type=int, default=100)
p.add_argument("--settings", default="--image-tokens 320 --max-len 4096", help="Must match the save point's recipe.")
p.add_argument("--suffix", default="topup")
p.add_argument("--lr", default="5e-5", help="Lower than the run's own: it goes on from a trained adapter.")
p.add_argument("--sources", default="", help="Comma-separated datasets in place of the default pair, owner/slug each.")
a = p.parse_args()

t = (HERE / "template.py").read_text()
subs = {
    "__HOURS__": str(a.hours),
    "__SFT__": base64.b64encode((REPO / "sft_lora.py").read_bytes()).decode(),
    "__VLLM__": base64.b64encode((REPO / "vllm_batch.py").read_bytes()).decode(),
    "__EVAL_S__": str(a.eval_minutes * 60),
    "__TRAIN_ARGS__": f"--resumable --epochs 1 --lr {a.lr} --init-adapter {{init}}",
    "# Testify fine-tune: LoRA on Qwen3-VL 8B Instruct": f"# Testify fine-tune, resumed: LoRA on Qwen3-VL {a.size.upper()} Instruct",
    'find("8b-instruct/**/config.json")': f'find("{a.size}-instruct/**/config.json")',
    'find("sft_2400.jsonl")': f'find("{a.data}.jsonl")',
}
for k, v in subs.items():
    assert k in t, k
    t = t.replace(k, v)

old = '''def find(pattern):
    hits = sorted(glob.glob("/kaggle/input/**/" + pattern, recursive=True))
    if not hits:
'''
new = '''INPUTS, RAW = [], []


def walk():
    """Every input file once, without entering a photo folder (eval/raw/<cache>)."""
    for top, dirs, files in os.walk("/kaggle/input", followlinks=True):
        if top.endswith("/eval/raw"):
            RAW.extend(os.path.join(top, d) for d in dirs)
            dirs[:] = []
            continue
        INPUTS.extend(os.path.join(top, f) for f in files)


def find(pattern):
    # On 3 Nov a recursive glob walked every photo Kaggle had unpacked and took 48 minutes.
    if not INPUTS:
        walk()
    hits = sorted(p for p in INPUTS if fnmatch.fnmatch(p, "*/" + pattern))
    if not hits:
'''
assert t.count(old) == 1, "find"
t = t.replace(old, new)
t = t.replace("import base64, glob, importlib,", "import base64, fnmatch, glob, importlib,", 1)

old = '''photos = find("testify_train/media").parent.parent
root = Path("/tmp/root")
(root / "eval").mkdir(parents=True, exist_ok=True)
if not (root / "eval" / "raw").exists():
    os.symlink(photos, root / "eval" / "raw")
'''
new = '''# The photos travel as tar archives named .photos, whose paths start at
# eval/raw: Kaggle unpacks a .tar on upload into thousands of files. Any
# folders it did unpack are linked in as they are.
root = Path("/tmp/root")
photos = root / "eval" / "raw"
photos.mkdir(parents=True, exist_ok=True)
find("sft_*.jsonl")
for archive in sorted(p for p in INPUTS if p.endswith(".photos")):
    sh(f"tar xf {archive} -C {root}", 1800)
for folder in RAW:
    if not (photos / Path(folder).name).exists():
        os.symlink(folder, photos / Path(folder).name)
print("photo caches", sorted(p.name for p in photos.iterdir()), flush=True)
if not any(photos.iterdir()):
    print("missing input: photos", flush=True)
    os._exit(2)
# The finished run's adapter the top-up goes on from.
init = find("init/adapter_model.safetensors").parent
print("going on from", init, flush=True)
'''
assert t.count(old) == 1, "photos block"
t = t.replace(old, new)

old = '''for settings in ("--image-tokens 320 --max-len 4096", "--image-tokens 256 --max-len 3072"):'''
new = f'''# Only the run's own settings: the save point refuses any other recipe.
for settings in ("{a.settings}",):'''
assert t.count(old) == 1, "settings"
t = t.replace(old, new)

old = '''print("train exit", code, flush=True)
if not (W / "adapter" / "adapter_config.json").exists():
    done()
'''
new = '''print("train exit", code, flush=True)
if not (W / "adapter" / "adapter_config.json").exists():
    done()
# Folded in and asked only when the plan's last step is done; otherwise the next session resumes.
state = json.loads((W / "adapter" / "savepoint" / "state.json").read_text())
print("reached step", state["step"], "of", state["plan_steps"], flush=True)
if state["step"] < state["plan_steps"]:
    done()
'''
assert t.count(old) == 1, "after train"
t = t.replace(old, new)

out = HERE / "out" / f"{a.size}_{a.data}_{a.suffix}"
out.mkdir(parents=True, exist_ok=True)
(out / "run.py").write_text(t)
slug = f"testify-qwen3-vl-{a.size}-{a.data.replace('_', '-')}-{a.suffix}"
meta = {
    "id": f"{a.owner}/{slug}", "title": slug, "code_file": "run.py", "language": "python",
    "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_tpu": False,
    "enable_internet": False,
    "dataset_sources": ([s.strip() for s in a.sources.split(",") if s.strip()] if a.sources else
                        [f"godzilla1215/{a.dataset}", "godzilla1215/testify-batches"])
                       + ["metric/gemma-4-developer-agent-wheelhouse"],
    "kernel_sources": [], "competition_sources": [],
    "model_sources": [f"qwen-lm/qwen-3-vl/transformers/{a.size}-instruct/1"],
    "machine_shape": "NvidiaTeslaT4",
    "docker_image": json.loads((HERE / "environment.json").read_text())["docker_image"],
}
(out / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
compile(t, str(out / "run.py"), "exec")
print(out, meta["id"])
