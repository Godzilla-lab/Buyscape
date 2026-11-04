"""Training on a rented Vast.ai GPU, in turns with free Kaggle sessions.

The run is the same `sft_lora.py --resumable` everywhere. Its save points go
to a private Hugging Face repo, so a Vast machine picks up where Kaggle
stopped and the other way round. Money is guarded three ways: the training's
own time limit is set from the credit, this module's watcher saves nothing
and destroys the machine once the job says it is done or the credit falls to
the reserve, and nothing is rented without `--yes` after the cost is shown.

Datacenter machines only by default: most cheap offers are someone's home
computer, and the training photos would sit on it.

The machine gets its Hugging Face token from the Vast account's own
environment variables (HF_TRAIN_TOKEN, a token for the two private repos
only), so the token never passes through here.

The same machines also read for the training set: `read_onstart` serves an open
vision model with vLLM beside the adverts and runs the teacher's reads against
it, many at once, then sends the answers and recordings back.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path

import httpx

API = "https://console.vast.ai/api/v0"
# CUDA 12.8 and PyTorch 2.7 or later: the RTX 5090 (Blackwell) runs nothing older; A100s run it too.
IMAGE = "pytorch/pytorch:2.7.1-cuda12.8-cudnn9-devel"
# A Vast machine's own minutes for downloading the base, the data and the last save.
SETUP_HOURS = 0.5
# The teacher on a rented GPU: the engine's own default reader, open weights, FP8 to fit one 80 GB card.
READER = "Qwen/Qwen3-VL-32B-Instruct-FP8"
VLLM = "vllm==0.32.0"
# Its torch 2.13 wheels need a driver that runs CUDA 13.
READ_CUDA = 13.0
# Minutes a reading machine spends before its first read: tools, the model's 36 GB, loading it.
READ_SETUP_MINUTES = 20
# What a reading machine downloads before its first read: the model and vLLM's software.
READ_SETUP_GB = 46
TOKEN_VAR = "HF_TRAIN_TOKEN"
# Vast gives each machine its own id and a key that can manage only that machine.
SELF_STOP = ("python -c \"import os, urllib.request as u; u.urlopen(u.Request("
             "'https://console.vast.ai/api/v0/instances/' + os.environ['CONTAINER_ID'] + '/', "
             "data=b'{\\\"state\\\": \\\"stopped\\\"}', method='PUT', headers={'Authorization': 'Bearer ' + "
             "os.environ['CONTAINER_API_KEY'], 'Content-Type': 'application/json'}), timeout=30)\" || true")


@dataclass(frozen=True)
class Offer:
    id: int
    gpu: str
    gpu_gb: float
    dollars_per_hour: float
    datacenter: bool
    reliability: float
    down_mbps: float
    cuda: float = 0.0
    # Hosts charge for downloads too: on 3 Nov one charged $26.67 a TB, so the reader's 46 GB of
    # model and software cost more than its first half hour of GPU.
    down_per_tb: float = 0.0

    def setup_dollars(self, gigabytes: float) -> float:
        return gigabytes / 1000 * self.down_per_tb

    def line(self) -> str:
        where = "datacenter" if self.datacenter else "someone's machine"
        return (f"#{self.id}: {self.gpu} {self.gpu_gb:.0f} GB, ${self.dollars_per_hour:.2f} an hour, "
                f"downloads ${self.down_per_tb:.2f} a TB, {where}, reliability {self.reliability:.3f}, "
                f"{self.down_mbps:.0f} Mbps down")


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {os.environ['VAST_API_KEY']}"}


def credit(client: httpx.Client | None = None) -> float:
    client = client or httpx.Client(timeout=30)
    r = client.get(f"{API}/users/current/", headers=_headers())
    r.raise_for_status()
    return float(r.json().get("credit") or 0.0)


def offers(gpus: tuple[str, ...], min_gb: float = 24, datacenter_only: bool = True,
           client: httpx.Client | None = None) -> list[Offer]:
    """Rentable single-GPU machines, cheapest first."""
    client = client or httpx.Client(timeout=40)
    found: list[Offer] = []
    for gpu in gpus:
        q = {"gpu_name": {"eq": gpu}, "num_gpus": {"eq": 1}, "rentable": {"eq": True}, "verified": {"eq": True},
             "reliability2": {"gte": 0.98}, "inet_down": {"gte": 200}, "disk_space": {"gte": 80},
             "order": [["dph_total", "asc"]], "limit": 30}
        r = client.get(f"{API}/bundles/", params={"q": json.dumps(q)}, headers=_headers())
        if r.status_code != 200:
            continue
        for o in r.json().get("offers", []):
            offer = Offer(id=int(o["id"]), gpu=str(o.get("gpu_name")), gpu_gb=float(o.get("gpu_ram") or 0) / 1024,
                          dollars_per_hour=float(o.get("dph_total") or 0), datacenter=bool(o.get("hosting_type") == 1
                                                                                            or o.get("datacenter")),
                          reliability=float(o.get("reliability2") or 0), down_mbps=float(o.get("inet_down") or 0),
                          cuda=float(o.get("cuda_max_good") or 0),
                          down_per_tb=float(o.get("internet_down_cost_per_tb") or o.get("inet_down_cost", 0) * 1024 or 0))
            if offer.gpu_gb >= min_gb and (offer.datacenter or not datacenter_only):
                found.append(offer)
    return sorted(found, key=lambda o: o.dollars_per_hour)


def training_hours(credit_left: float, dollars_per_hour: float, reserve: float = 1.0) -> float:
    """Hours the training may run so the machine is gone before the credit falls to the reserve."""
    usable = max(0.0, credit_left - reserve) / dollars_per_hour - SETUP_HOURS
    return round(max(0.0, usable), 2)


def onstart(data_repo: str, run_repo: str, data_file: str, train_args: str, hours: float, folder: str = "") -> str:
    """The machine's start script: tools, data and save point in, train, adapter out, then a done mark.

    The token arrives as HF_TRAIN_TOKEN, a Hugging Face token for these two repos only."""
    q = shlex.quote
    return "\n".join([
        # The token goes to the hf tool as HF_TOKEN, set before the commands are echoed, so no log carries it.
        f'export HF_TOKEN="${TOKEN_VAR}"',
        "set -x",
        "cd /workspace",
        # Vast starts the script again whenever it ends. A second start trains nothing: it asks Vast
        # to stop this machine, and waits to be stopped or destroyed, rather than paying to start over.
        f"if [ -f /workspace/.ran ]; then {SELF_STOP}; sleep 3600; exit 0; fi; touch /workspace/.ran",
        # The versions the 2B trained with on Kaggle (run 5, 1 Nov), not whatever is newest today.
        "pip install -q torch==2.10.0 torchvision==0.25.0 --index-url https://download.pytorch.org/whl/cu128",
        "pip install -q transformers==5.0.0 peft==0.19.1 accelerate safetensors pillow 'huggingface_hub>=1.0'",
        # Only the training folder: every gigabyte a host sends is paid for. One pattern: a second
        # one is read as a file name, and then the tool ignores the pattern altogether.
        (f"hf download {q(data_repo)} --repo-type dataset --local-dir data"
         + (f" --include {q(folder + '/*')}" if folder else "")),
        # Photos travel as one archive per cache, far fewer files than one upload each.
        f"for t in data/{folder}/*.tar; do [ -f \"$t\" ] && tar xf \"$t\" -C data/{folder}; done",
        (f"python data/{folder + '/' if folder else ''}sft_lora.py --model Qwen/Qwen3-VL-2B-Instruct "
         f"--data data/{folder + '/' if folder else ''}{q(data_file)} --root data/{folder} "
         f"--out out --resumable --hub-repo {q(run_repo)} --hours {hours} {train_args} > train.log 2>&1"),
        "code=$?",
        f"hf upload {q(run_repo)} train.log logs/train.log --private",
        # The done mark only for a run that ended well, so a failed run is never taken for a finished one.
        (f"[ $code -eq 0 ] && hf upload {q(run_repo)} out adapter --private && echo done > DONE "
         f"&& hf upload {q(run_repo)} DONE DONE --private"),
        SELF_STOP,
    ])


def request_body(script: str, token: str | None = None, disk_gb: int = 80, label: str = "testify-train") -> dict:
    """The machine runs the script as its only command, so it stops itself when the script ends:
    the GPU is not paid for while nobody is watching. With no token given, the machine takes
    HF_TRAIN_TOKEN from the Vast account's own variables."""
    return {"client_id": "me", "image": IMAGE, "disk": disk_gb, "label": label,
            "env": {TOKEN_VAR: token} if token else {}, "runtype": "args", "args": ["bash", "-c", script]}


def create(offer: Offer, script: str, token: str | None = None, disk_gb: int = 80, label: str = "testify-train",
           client: httpx.Client | None = None) -> int:
    """Rent the machine. The caller has shown the cost and been told yes."""
    client = client or httpx.Client(timeout=60)
    r = client.put(f"{API}/asks/{offer.id}/", headers=_headers(), json=request_body(script, token, disk_gb, label))
    r.raise_for_status()
    return int(r.json()["new_contract"])


def account_has(name: str, client: httpx.Client | None = None) -> bool:
    """Whether the Vast account holds an environment variable by this name. Names only: no value is read out."""
    client = client or httpx.Client(timeout=30)
    r = client.get(f"{API}/secrets/", headers=_headers())
    r.raise_for_status()
    data = r.json()
    names = data.get("secrets", data) if isinstance(data, dict) else {}
    return name in names


# Tracked files a reading machine needs: the engine, its protocols and the training pool.
BUNDLE_PATHS = ("src", "protocols", "catalogue", "tenants", "pyproject.toml", "uv.lock", "README.md", "LICENSE",
                "eval/testify/answer.schema.json", "eval/testify/lies.yaml", "eval/testify/train_lies.yaml")
BUNDLE_FILES = ("eval/testify/train_pool.jsonl", "eval/testify/train_photo_hashes.json")


def bundle(root: Path, ids: list[str], out: Path) -> dict[str, int]:
    """What a reading machine downloads: the code, the training pool, the ids and their photos.

    The pool and hashes are taken as they stand here, so adverts converted since
    the last commit are included. Returns counts for the plan."""
    from .convert import load_items

    out.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.run(["git", "ls-files", "--", *BUNDLE_PATHS], cwd=root, capture_output=True, text=True,
                             check=True).stdout.split()
    with tarfile.open(out / "code.tar.gz", "w:gz") as tar:
        for rel in [*tracked, *BUNDLE_FILES]:
            if (root / rel).is_file():
                tar.add(root / rel, arcname=rel)
    wanted = set(ids)
    items = [i for i in load_items(root / "eval" / "testify" / "train_pool.jsonl") if i.id in wanted]
    photos = 0
    with tarfile.open(out / "photos.tar", "w") as tar:
        for item in items:
            folder = root / (item.photos.cache or "")
            if item.photos.cache and folder.is_dir():
                for photo in sorted(folder.iterdir()):
                    if photo.is_file():
                        tar.add(photo, arcname=photo.relative_to(root).as_posix())
                        photos += 1
    (out / "ids.txt").write_text("".join(f"{i.id}\n" for i in items))
    return {"adverts": len(items), "not in the pool": len(wanted) - len(items), "photos": photos,
            "megabytes": round(sum(p.stat().st_size for p in out.iterdir()) / 1e6)}


def read_onstart(data_repo: str, run_repo: str, job: str, minutes: int, model: str = READER,
                 parallel: int = 16) -> str:
    """The reading machine's script: the model served by vLLM, the reads run against it in parallel parts,
    then the answers, recordings and logs sent back whatever happened, under a hard time limit."""
    q = shlex.quote
    work = "\n".join([
        "set -x",
        "cd /workspace && pip install -q uv 'huggingface_hub>=1.0'",
        f"hf download {q(data_repo)} --repo-type dataset --include {q(job + '/*')} --local-dir in",
        f"mkdir -p job && tar xzf in/{job}/code.tar.gz -C job && tar xf in/{job}/photos.tar -C job",
        f"cp in/{job}/ids.txt job/ids.txt && mkdir -p job/docs/proof",
        "uv venv -q -p 3.12 /workspace/venv && . /workspace/venv/bin/activate",
        f"uv pip install -q {q(VLLM)} -e job",
        (f"vllm serve {q(model)} --api-key local --max-model-len 16384 --limit-mm-per-prompt '{{\"image\": 4}}' "
         f"--gpu-memory-utilization 0.92 --max-num-seqs {parallel * 2} > job/vllm.log 2>&1 &"),
        # The image has no curl: python asks the server, and the reads start the moment it answers.
        ("for i in $(seq 1 120); do python -c \"import urllib.request as u; u.urlopen(u.Request("
         "'http://localhost:8000/v1/models', headers={'Authorization': 'Bearer local'}), timeout=5)\" "
         "2>/dev/null && break; sleep 10; done"),
        f"cd job && split -n l/{parallel} -d ids.txt part_ && export VLLM_API_KEY=local",
        # Wait for the readers only: a bare wait would also wait for the model server, which never ends.
        (f"pids=''; for p in part_*; do buyscape testify --model vllm:{model} --split train --ids-file $p "
         f"--tag {job}_$p --no-lies --reads-only --budget-usd 9 > $p.log 2>&1 & pids=\"$pids $!\"; done; "
         "wait $pids"),
    ])
    send = ("mkdir -p /workspace/out && cd /workspace/out && "
            "cp -r /workspace/job/eval/testify/runs . 2>/dev/null; cp -r /workspace/job/eval/fixtures . 2>/dev/null; "
            f"cp /workspace/job/*.log . 2>/dev/null; hf upload {q(run_repo)} /workspace/out reads/{job} >/dev/null 2>&1")
    return "\n".join([
        # The token goes to the hf tool as HF_TOKEN, before any command is echoed, so no log carries it.
        f'test -n "${TOKEN_VAR}" || {{ echo "{TOKEN_VAR} is not on the Vast account"; exit 3; }}',
        f"if [ -f /workspace/.ran ]; then {SELF_STOP}; sleep 3600; exit 0; fi; touch /workspace/.ran",
        f'export HF_TOKEN="${TOKEN_VAR}"',
        # What is read so far goes back every half hour, so a machine lost midway loses half an hour at most.
        f"(while sleep 1800; do {send}; done) & keeper=$!",
        f"timeout {int(minutes)}m bash -c {q(work)}",
        'code=$?',
        "kill $keeper 2>/dev/null",
        f"{send}",
        "echo \"$code\" > /workspace/out/EXIT",
        f"hf upload {q(run_repo)} /workspace/out reads/{job}",
        # The model server outlives the reads and keeps the machine running, and billed, until it is stopped.
        "pkill -f 'vllm serve'; pkill -f vllm; sleep 5",
        SELF_STOP,
    ])


def instances(client: httpx.Client | None = None) -> list[dict]:
    client = client or httpx.Client(timeout=30)
    r = client.get(f"{API}/instances/", params={"owner": "me"}, headers=_headers())
    r.raise_for_status()
    return r.json().get("instances", [])


def destroy(instance_id: int, client: httpx.Client | None = None) -> None:
    client = client or httpx.Client(timeout=30)
    client.delete(f"{API}/instances/{instance_id}/", headers=_headers()).raise_for_status()
