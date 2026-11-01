"""Training on a rented Vast.ai GPU, in turns with free Kaggle sessions.

The run is the same `sft_lora.py --resumable` everywhere. Its save points go
to a private Hugging Face repo, so a Vast machine picks up where Kaggle
stopped and the other way round. Money is guarded three ways: the training's
own time limit is set from the credit, this module's watcher saves nothing
and destroys the machine once the job says it is done or the credit falls to
the reserve, and nothing is rented without `--yes` after the cost is shown.

Datacenter machines only by default: most cheap offers are someone's home
computer, and the training photos would sit on it.
"""

from __future__ import annotations

import json
import os
import shlex
from dataclasses import dataclass

import httpx

API = "https://console.vast.ai/api/v0"
# CUDA 12.8 and PyTorch 2.7 or later: the RTX 5090 (Blackwell) runs nothing older; A100s run it too.
IMAGE = "pytorch/pytorch:2.7.1-cuda12.8-cudnn9-devel"
# A Vast machine's own minutes for downloading the base, the data and the last save.
SETUP_HOURS = 0.5


@dataclass(frozen=True)
class Offer:
    id: int
    gpu: str
    gpu_gb: float
    dollars_per_hour: float
    datacenter: bool
    reliability: float
    down_mbps: float

    def line(self) -> str:
        where = "datacenter" if self.datacenter else "someone's machine"
        return (f"#{self.id}: {self.gpu} {self.gpu_gb:.0f} GB, ${self.dollars_per_hour:.2f} an hour, {where}, "
                f"reliability {self.reliability:.3f}, {self.down_mbps:.0f} Mbps down")


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
                          reliability=float(o.get("reliability2") or 0), down_mbps=float(o.get("inet_down") or 0))
            if offer.gpu_gb >= min_gb and (offer.datacenter or not datacenter_only):
                found.append(offer)
    return sorted(found, key=lambda o: o.dollars_per_hour)


def training_hours(credit_left: float, dollars_per_hour: float, reserve: float = 1.0) -> float:
    """Hours the training may run so the machine is gone before the credit falls to the reserve."""
    usable = max(0.0, credit_left - reserve) / dollars_per_hour - SETUP_HOURS
    return round(max(0.0, usable), 2)


def onstart(data_repo: str, run_repo: str, data_file: str, train_args: str, hours: float) -> str:
    """The machine's start script: tools, data and save point in, train, adapter out, then a done mark.

    The token arrives as HF_TRAIN_TOKEN, a Hugging Face token for these two repos only."""
    q = shlex.quote
    return "\n".join([
        "set -x",
        "cd /workspace",
        "pip install -q 'transformers>=4.57' peft accelerate safetensors pillow huggingface_hub",
        f"hf download {q(data_repo)} --repo-type dataset --local-dir data --token \"$HF_TRAIN_TOKEN\"",
        f"python data/sft_lora.py --model Qwen/Qwen3-VL-2B-Instruct --data data/{q(data_file)} --root data "
        f"--out out --resumable --hub-repo {q(run_repo)} --hours {hours} {train_args} > train.log 2>&1",
        f"hf upload {q(run_repo)} out adapter --private --token \"$HF_TRAIN_TOKEN\"",
        f"hf upload {q(run_repo)} train.log logs/train.log --private --token \"$HF_TRAIN_TOKEN\"",
        "echo done > DONE",
        f"hf upload {q(run_repo)} DONE DONE --private --token \"$HF_TRAIN_TOKEN\"",
    ])


def request_body(script: str, token: str, disk_gb: int = 80) -> dict:
    """The machine runs the script as its only command, so it stops itself when the script ends:
    the GPU is not paid for while nobody is watching."""
    return {"client_id": "me", "image": IMAGE, "disk": disk_gb, "label": "testify-train",
            "env": {"HF_TRAIN_TOKEN": token}, "runtype": "args", "args": ["bash", "-c", script]}


def create(offer: Offer, script: str, token: str, disk_gb: int = 80, client: httpx.Client | None = None) -> int:
    """Rent the machine. The caller has shown the cost and been told yes."""
    client = client or httpx.Client(timeout=60)
    r = client.put(f"{API}/asks/{offer.id}/", headers=_headers(), json=request_body(script, token, disk_gb))
    r.raise_for_status()
    return int(r.json()["new_contract"])


def instances(client: httpx.Client | None = None) -> list[dict]:
    client = client or httpx.Client(timeout=30)
    r = client.get(f"{API}/instances/", params={"owner": "me"}, headers=_headers())
    r.raise_for_status()
    return r.json().get("instances", [])


def destroy(instance_id: int, client: httpx.Client | None = None) -> None:
    client = client or httpx.Client(timeout=30)
    client.delete(f"{API}/instances/{instance_id}/", headers=_headers()).raise_for_status()
