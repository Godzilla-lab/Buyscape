# Testify fine-tune: LoRA on Qwen3-VL 8B Instruct over the training set from
# `buyscape testify-train-build`, then the tuned model answers the dev reads.
#
# Every step has a time limit and the notebook always exits: on 17 Oct a
# failed engine start left a session hanging for eleven GPU hours.
import base64, glob, importlib, json, os, signal, subprocess, sys, time
from pathlib import Path

STARTED = time.time()
BUDGET_S = int(float(os.environ.get("BUDGET_HOURS", "__HOURS__")) * 3600)
W = Path("/kaggle/working")


def sh(cmd, limit_s=None):
    """Run a command in its own process group, and leave nothing of it behind."""
    print("$", cmd, flush=True)
    proc = subprocess.Popen(cmd, shell=True, start_new_session=True)
    try:
        code = proc.wait(timeout=limit_s)
    except subprocess.TimeoutExpired:
        print(f"timed out after {limit_s}s, stopping it", flush=True)
        code = 124
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()
    gpus_free()
    return code


def gpus_free(limit_s=180):
    end = time.time() + limit_s
    out = []
    while time.time() < end:
        out = subprocess.run("nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits",
                             shell=True, capture_output=True, text=True).stdout.split()
        if out and all(int(x) < 1024 for x in out if x.isdigit()):
            return
        time.sleep(5)
    print("GPU memory still in use:", out, flush=True)


def left():
    return int(BUDGET_S - (time.time() - STARTED))


def find(pattern):
    hits = sorted(glob.glob("/kaggle/input/**/" + pattern, recursive=True))
    if not hits:
        print(f"missing input: {pattern}", flush=True)
        os._exit(2)
    return Path(hits[0])


def done():
    sh("ls -la /kaggle/working; tail -3 /kaggle/working/adapter/log.jsonl", 60)
    os._exit(0)


sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
os.environ.update(PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True", TOKENIZERS_PARALLELISM="false")
(W / "sft_lora.py").write_bytes(base64.b64decode("__SFT__"))
(W / "vllm_batch.py").write_bytes(base64.b64decode("__VLLM__"))

model = find("8b-instruct/**/config.json").parent
data = find("sft_2400.jsonl")
photos = find("testify_train/media").parent.parent
root = Path("/tmp/root")
(root / "eval").mkdir(parents=True, exist_ok=True)
if not (root / "eval" / "raw").exists():
    os.symlink(photos, root / "eval" / "raw")
print("model", model, "data", data, "photos", photos, flush=True)
train = f"{sys.executable} {W}/sft_lora.py --model {model} --data {data} --root {root}"
# The image's torchao 0.10 is older than peft 0.19 accepts, and peft refuses
# to build adapters while it is installed. LoRA here never uses it.
sh(f"{sys.executable} -m pip uninstall -y torchao", 300)
sh(f"{sys.executable} -c 'import peft, transformers, torch; print(\"peft\", peft.__version__, \"transformers\", transformers.__version__, \"torch\", torch.__version__)'", 300)

# A dozen chats first, within 25 minutes, so a setup fault costs little. If
# the cards run out of memory, once more with smaller photos and shorter chats.
small = ""
# On 24 Oct the defaults ran out of memory on the second card; these fitted.
for settings in ("--image-tokens 320 --max-len 4096", "--image-tokens 256 --max-len 3072"):
    sh("rm -rf /tmp/check", 60)
    code = sh(f"{train} --out /tmp/check --limit 12 --epochs 1 --accumulate 4 --held-out 0.2 --hours 0.3 {settings}", 1500)
    print("check exit", code, "with", settings or "the default settings", flush=True)
    if code == 0 and Path("/tmp/check/adapter_config.json").exists():
        small = settings
        break
else:
    print("the check failed: stopping", flush=True)
    done()

# The check trained 8 chats in two steps: if each took over half a minute,
# the full run would teach almost nothing in the time left, so stop here.
events = [json.loads(line) for line in Path("/tmp/check/log.jsonl").read_text().splitlines() if line.strip()]
first = next(e for e in events if e["event"] == "start")["minutes"]
last = max(e["minutes"] for e in events if e["event"] == "step")
per_chat = (last - first) * 60 / 8
print(f"check speed: {per_chat:.1f} seconds per chat", flush=True)
if per_chat > 30:
    print("too slow to be worth the GPU hours: stopping", flush=True)
    done()

# Leave time to fold the adapter in and answer the dev reads.
hours = max(0.5, (left() - __EVAL_S__) / 3600)
code = sh(f"{train} --out {W}/adapter --hours {hours:.2f} {small} __TRAIN_ARGS__", int(hours * 3600) + 1200)
print("train exit", code, flush=True)
if not (W / "adapter" / "adapter_config.json").exists():
    done()

code = sh(f"{sys.executable} {W}/sft_lora.py --model {model} --merge {W}/adapter --out /tmp/merged", 2400)
print("merge exit", code, flush=True)
if code != 0 or left() < 1800:
    done()

# vLLM from the public wheel set, after training: it replaces transformers.
wheelhouse = find("vllm-*.whl").parent
tmp = Path("/tmp/wheelhouse")
tmp.mkdir(exist_ok=True)
for w in wheelhouse.glob("*.whl"):
    if "cutlass" in w.name.lower():
        continue
    target = tmp / (w.name.replace("cu128", "+cu128") if ("cu128" in w.name and "+" not in w.name) else w.name)
    if not target.exists():
        os.symlink(w, target)
for pth in glob.glob("/usr/local/lib/python*/dist-packages/*cutlass*.pth"):
    os.unlink(pth)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "--force-reinstall",
                *sorted(str(w) for w in tmp.glob("*.whl"))], check=True)
importlib.invalidate_caches()
os.environ.update(VLLM_USE_FLASHINFER_SAMPLER="0", VLLM_NO_USAGE_STATS="1", VLLM_WORKER_MULTIPROC_METHOD="spawn")
libdirs = {str(Path(p).parent) for pat in ("/usr/lib*/**/libcuda.so*", "/usr/local/**/libcuda.so*")
           for p in glob.glob(pat, recursive=True)}
os.environ["LIBRARY_PATH"] = ":".join(sorted(libdirs) + [os.environ.get("LIBRARY_PATH", "")]).strip(":")

batches = find("dev.repeat1.jsonl").parent
gpus = int(subprocess.run("nvidia-smi -L | wc -l", shell=True, capture_output=True, text=True).stdout.strip() or 1)
run = (f"{sys.executable} {W}/vllm_batch.py --model /tmp/merged --max-model-len 12288 --tensor-parallel {gpus}"
       " --dtype half --plain-all-reduce --attention-backend TRITON_ATTN --gpu-memory 0.80 --max-num-seqs 16 --chunk 32")
code = sh(f"{run} --batch {batches}/dev.jsonl --out {W}/dev.results.jsonl", left() - 600)
print("dev exit", code, flush=True)
if left() > 2400:
    code = sh(f"{run} --batch {batches}/dev.repeat1.jsonl --out {W}/dev.repeat1.results.jsonl", left() - 600)
    print("repeat exit", code, flush=True)
done()
