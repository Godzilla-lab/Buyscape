"""Fine-tune Qwen3-VL on the Testify training set with LoRA, on free GPUs.

Standalone: it needs torch, transformers and peft (bitsandbytes too for
--bits 4), not buyscape, so it runs as it is on a Kaggle notebook.

    python sft_lora.py --model /path/to/Qwen3-VL-8B-Instruct \\
        --data sft.jsonl --root <folder the photo paths start from> --out adapter/

The recipe is steps 7 and 8 of docs/research/fine-tuning-research.md:

- Only small adapters are trained, on every linear layer of the language
  part. The vision part is frozen, so the model reads photos as it did.
- By default the base stays in 16 bits, split across the cards: the 8B
  takes 16 GB, which a pair of T4s holds with room to train, and the adapter
  then fits the very weights vLLM serves. --bits 4 is QLoRA, for one card.
- Loss is counted on the answer only, never on the prompt or the photos,
  and only the answer's scores over the vocabulary are ever made: for a
  6,000 token chat the full set would take nearly 4 GB on its own.
- Each photo is shrunk to at most 576 image tokens, the cap the Qwen
  fine-tuning example uses. Photos are the biggest memory cost.
- The two twins of one advert, honest and lied-to, are never split between
  training and the held-out check, so the check cannot be passed by memory.

It stops on a time limit and always saves what it has, because a Kaggle
session that runs over loses everything.

With --resumable the whole plan is trained over as many sessions as it
takes, on any machine: a save point (the adapter, the optimiser, the place in
the data) every --save-minutes, and each session starts from the last one.
With --hub-repo the save points also go to a private Hugging Face repo, so a
rented GPU and a free Kaggle session can take turns on one run.

    python sft_lora.py --model <base> --merge adapter/ --out merged/

folds the adapter into the 16 bit base, a plain model folder vLLM serves
with `vllm_batch.py` as it served the untuned one.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import shutil
import time
from pathlib import Path

# Qwen3-VL turns each 32 by 32 pixel square into one image token.
PIXELS_PER_TOKEN = 32 * 32
LANGUAGE_LINEAR = r".*language_model.*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def held_out(example: dict, share: float) -> bool:
    """Fixed by the advert's id, so both twins of an advert land on the same side."""
    return int(hashlib.sha256(example["id"].encode()).hexdigest(), 16) % 1000 < share * 1000


def shrink(image, max_tokens: int):
    """The photo at no more than `max_tokens` image tokens, its shape kept."""
    w, h = image.size
    scale = math.sqrt(max_tokens * PIXELS_PER_TOKEN / (w * h))
    if scale < 1:
        image = image.resize((max(32, int(w * scale)), max(32, int(h * scale))))
    return image


def encode(example: dict, processor, root: Path, max_tokens: int, max_len: int) -> tuple[dict, int] | None:
    """The model inputs for one chat and how many tokens at its end are the answer.
    None when it is too long."""
    from PIL import Image

    messages, images = [], []
    for turn in example["messages"]:
        if isinstance(turn["content"], str):
            messages.append(turn)
            continue
        parts = []
        for part in turn["content"]:
            if part["type"] == "image":
                # A photo missing on this machine skips the chat, counted, instead of ending hours of training.
                if not (root / part["image"]).is_file():
                    return None
                with Image.open(root / part["image"]) as im:
                    images.append(shrink(im.convert("RGB"), max_tokens))
                parts.append({"type": "image"})
            else:
                parts.append(part)
        messages.append({**turn, "content": parts})
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    prompt = processor.apply_chat_template(messages[:-1], tokenize=False, add_generation_prompt=True)
    if not text.startswith(prompt):
        raise ValueError("the chat template does not put the answer after the prompt")
    batch = processor(text=[text], images=images or None, return_tensors="pt")
    ids = batch["input_ids"][0]
    if len(ids) > max_len:
        return None
    n_prompt = len(processor(text=[prompt], images=images or None, return_tensors="pt")["input_ids"][0])
    return dict(batch), len(ids) - n_prompt


# A save point is only resumed with the recipe it was made with.
RECIPE = ("model", "rank", "alpha", "lr", "epochs", "accumulate", "image_tokens", "max_len", "held_out", "limit", "data")


def recipe(args, model: str) -> dict:
    """What must not change between the sessions of one run. `model` is the base's own
    signature and the data goes by file name, since each machine keeps them in its own folder."""
    out = {k: getattr(args, k) for k in RECIPE if k not in ("model", "data")}
    out["model"] = model
    out["data"] = Path(str(args.data)).name
    return out


def model_signature(config) -> str:
    """The base by what it is, not where it sits: Kaggle mounts a model under a version number."""
    text = getattr(config, "text_config", config)
    return f"{config.model_type}:{text.hidden_size}x{text.num_hidden_layers}:{text.vocab_size}"


def recipe_changes(saved: dict, now: dict) -> list[str]:
    return [f"{k}: {saved.get(k)!r} then, {now.get(k)!r} now" for k in RECIPE if saved.get(k) != now.get(k)]


def epoch_order(train: list[dict], epoch: int) -> list[dict]:
    """The chats of one pass in an order fixed by the pass's number, so a resumed run sees the rest of it."""
    order = train[:]
    random.Random(f"epoch {epoch}").shuffle(order)
    return order


def read_state(save: Path) -> dict | None:
    path = save / "state.json"
    return json.loads(path.read_text()) if path.exists() else None


def swap_in(fresh: Path, save: Path) -> None:
    """Put a finished save point in place of the last one, so a stop mid-save never leaves half of one."""
    old = save.with_name(save.name + ".old")
    shutil.rmtree(old, ignore_errors=True)
    if save.exists():
        save.rename(old)
    fresh.rename(save)
    shutil.rmtree(old, ignore_errors=True)


def hub_pull(repo: str, token: str, save: Path) -> bool:
    """Take the hub's save point when it is further on than this machine's. True when taken."""
    from huggingface_hub import snapshot_download
    from huggingface_hub.utils import RepositoryNotFoundError

    landing = save.with_name(save.name + ".hub")
    shutil.rmtree(landing, ignore_errors=True)
    try:
        snapshot_download(repo, allow_patterns=["savepoint/*"], local_dir=landing, token=token)
    except RepositoryNotFoundError:
        return False
    theirs, mine = read_state(landing / "savepoint"), read_state(save)
    if theirs and (not mine or theirs["step"] > mine["step"]):
        swap_in(landing / "savepoint", save)
        shutil.rmtree(landing, ignore_errors=True)
        return True
    shutil.rmtree(landing, ignore_errors=True)
    return False


def hub_push(repo: str, token: str, save: Path, step: int) -> None:
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    api.create_repo(repo, private=True, exist_ok=True)
    api.upload_folder(folder_path=save, repo_id=repo, path_in_repo="savepoint",
                      commit_message=f"save point at step {step}")


def work_dtype():
    """bfloat16 only on a card built for it. torch.cuda.is_bf16_supported() also
    says yes on a T4, which only emulates it: on 24 Oct that ran ten times slow."""
    import torch

    if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8:
        return torch.bfloat16
    return torch.float16


def merge(base: str, adapter: Path, out: Path) -> None:
    """The base with the adapter folded in, saved in 16 bits with its processor."""
    import torch
    from peft import PeftModel
    from transformers import AutoModelForImageTextToText, AutoProcessor

    # On the cards, not in memory: the 8B at 16 bits plus the merge did not fit
    # a Kaggle machine's 30 GB on 24 Oct.
    where = "auto" if torch.cuda.is_available() else "cpu"
    model = AutoModelForImageTextToText.from_pretrained(base, dtype=work_dtype(), device_map=where)
    model = PeftModel.from_pretrained(model, adapter).merge_and_unload()
    model.save_pretrained(out)
    AutoProcessor.from_pretrained(base).save_pretrained(out)
    print(f"merged model saved to {out}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--model", required=True, help="A local folder or a Hugging Face name.")
    parser.add_argument("--data", type=Path, help="sft.jsonl from buyscape testify-train-build.")
    parser.add_argument("--root", type=Path, help="The folder the photo paths are relative to.")
    parser.add_argument("--out", type=Path, required=True, help="Where the adapter, or the merged model, is saved.")
    parser.add_argument("--merge", type=Path, help="An adapter to fold into the base instead of training.")
    parser.add_argument("--rank", type=int, default=16)
    parser.add_argument("--alpha", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--accumulate", type=int, default=8, help="Chats per optimiser step.")
    parser.add_argument("--image-tokens", type=int, default=576, help="The most image tokens one photo may take.")
    parser.add_argument("--max-len", type=int, default=6144, help="Longer chats are skipped and counted.")
    parser.add_argument("--held-out", type=float, default=0.05, help="Share of adverts kept back to check the loss.")
    parser.add_argument("--hours", type=float, default=4.0, help="Stop and save after this long.")
    parser.add_argument("--limit", type=int, default=0, help="Use only this many chats, for a quick check.")
    parser.add_argument("--bits", type=int, choices=(16, 4), default=16, help="4 is QLoRA, for a single card.")
    parser.add_argument("--card-gb", type=float, default=12.0, help="Weights per card at 16 bits; the rest trains.")
    parser.add_argument("--resumable", action="store_true",
                        help="Train the whole plan over many sessions, from save points, on any machine.")
    parser.add_argument("--save-minutes", type=float, default=30.0, help="How often a resumable run saves its place.")
    parser.add_argument("--hub-repo", help="A private Hugging Face repo the save points go to and come from.")
    parser.add_argument("--hub-token-env", default="HF_TRAIN_TOKEN",
                        help="The variable holding a token that can write that one repo.")
    args = parser.parse_args()
    if args.merge:
        merge(args.model, args.merge, args.out)
        return
    if not (args.data and args.root):
        parser.error("--data and --root are needed to train")
    started = time.time()

    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForImageTextToText, AutoProcessor

    examples = load(args.data)
    if args.limit:
        examples = examples[: args.limit]
    train = [e for e in examples if not held_out(e, args.held_out)]
    # Forty chats are enough to see the loss move, and a long check eats the time limit.
    check = [e for e in examples if held_out(e, args.held_out)][:40]
    print(f"{len(train)} chats to train on, {len(check)} held out", flush=True)

    # A T4 has no bfloat16, so the work is done in float16 with a loss scaler.
    half = work_dtype()
    if args.bits == 4:
        from transformers import BitsAndBytesConfig

        placement = {"device_map": {"": 0}, "quantization_config": BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=half, llm_int8_skip_modules=["visual", "lm_head"],
        )}
    else:
        cards = {i: f"{args.card_gb}GiB" for i in range(torch.cuda.device_count())}
        placement = {"device_map": "auto", "max_memory": cards}
    processor = AutoProcessor.from_pretrained(args.model)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=half, **placement)
    # Not prepare_model_for_kbit_training: it turns the vision part and the
    # output layer to float32, three to five GB a T4 does not have.
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    for param in model.parameters():
        param.requires_grad_(False)
    model = get_peft_model(model, LoraConfig(
        r=args.rank, lora_alpha=args.alpha, lora_dropout=0.05, target_modules=LANGUAGE_LINEAR, task_type="CAUSAL_LM",
    ))
    signature = model_signature(model.config)
    save = args.out / "savepoint"
    token = os.environ.get(args.hub_token_env) if args.hub_repo else None
    if args.hub_repo and not token:
        parser.error(f"--hub-repo needs a token in ${args.hub_token_env}")
    if args.resumable and token and hub_pull(args.hub_repo, token, save):
        print(f"took the save point from {args.hub_repo}", flush=True)
    state = read_state(save) if args.resumable else None
    if state:
        changed = recipe_changes(state["recipe"], recipe(args, signature))
        if changed:
            parser.error("the save point was made with another recipe: " + "; ".join(changed))
        from peft import set_peft_model_state_dict
        from safetensors.torch import load_file

        set_peft_model_state_dict(model, load_file(str(save / "adapter_model.safetensors")))
    trainable = [p for p in model.parameters() if p.requires_grad]
    for param in trainable:
        # The scaler can only unscale float32 gradients.
        param.data = param.data.float()
    model.print_trainable_parameters()
    optimiser = torch.optim.AdamW(trainable, lr=args.lr, weight_decay=0.0)
    # Planned from the epochs, then cut to what the time limit allows once
    # the first steps show the speed, so the learning rate still ends low.
    plan = {"steps": state["plan_steps"] if state else max(1, int(len(train) * args.epochs / args.accumulate))}
    warmup = max(1, plan["steps"] // 20)

    def rate(step: int) -> float:
        if step < warmup:
            return (step + 1) / warmup
        return 0.5 * (1 + math.cos(math.pi * (step - warmup) / max(1, plan["steps"] - warmup)))

    schedule = torch.optim.lr_scheduler.LambdaLR(optimiser, rate)
    scaler = torch.amp.GradScaler("cuda", enabled=half == torch.float16)
    if state:
        kept = torch.load(save / "trainer.pt", map_location="cpu", weights_only=False)
        optimiser.load_state_dict(kept["optimiser"])
        schedule.load_state_dict(kept["schedule"])
        if kept.get("dtype") == str(half) and kept.get("scaler"):
            scaler.load_state_dict(kept["scaler"])  # a card of the other kind starts its own scaler

    def loss_of(example: dict):
        encoded = encode(example, processor, args.root, args.image_tokens, args.max_len)
        if encoded is None:
            return None
        batch, n_answer = encoded
        batch = {k: v.to(model.device) for k, v in batch.items()}
        with torch.autocast("cuda", dtype=half):
            logits = model(**batch, logits_to_keep=n_answer + 1).logits
        # The score at each place predicts the next token, so the last
        # n_answer + 1 places, less the final one, predict the answer.
        target = batch["input_ids"][0, -n_answer:].to(logits.device)
        return torch.nn.functional.cross_entropy(logits[0, :-1].float(), target)

    def check_loss() -> float:
        model.eval()
        losses = []
        with torch.no_grad():
            for example in check:
                loss = loss_of(example)
                if loss is not None:
                    losses.append(float(loss))
        model.train()
        return sum(losses) / max(1, len(losses))

    log = args.out / "log.jsonl"
    args.out.mkdir(parents=True, exist_ok=True)

    def note(**row) -> None:
        row["minutes"] = round((time.time() - started) / 60, 1)
        print(json.dumps(row), flush=True)
        with log.open("a") as fh:
            fh.write(json.dumps(row) + "\n")

    def save_point(at: tuple[int, int], step: int, skipped: int) -> None:
        """The adapter, the optimiser and the place in the data, swapped in whole."""
        fresh = save.with_name(save.name + ".new")
        shutil.rmtree(fresh, ignore_errors=True)
        model.save_pretrained(fresh)
        torch.save({"optimiser": optimiser.state_dict(), "schedule": schedule.state_dict(),
                    "scaler": scaler.state_dict() if scaler.is_enabled() else None, "dtype": str(half)},
                   fresh / "trainer.pt")
        (fresh / "state.json").write_text(json.dumps({
            "step": step, "plan_steps": plan["steps"], "epoch": at[0], "index": at[1], "skipped": skipped,
            "recipe": recipe(args, signature), "saved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }, indent=1))
        swap_in(fresh, save)
        note(event="save point", step=step, epoch=at[0], index=at[1])
        if token:
            hub_push(args.hub_repo, token, save, step)
            note(event="save point on the hub", step=step)

    note(event="resumed" if state else "start", step=state["step"] if state else 0, steps=plan["steps"],
         check_loss=round(check_loss(), 4) if check else None)
    model.train()
    trained_from = time.time()
    step = state["step"] if state else 0
    skipped = state["skipped"] if state else 0
    epoch, index = (state["epoch"], state["index"]) if state else (0, 0)
    boundary = (epoch, index)  # where the last optimiser step left the data
    seen, session_steps, running = 0, 0, []
    last_save = time.time()
    # A resumable run keeps a quarter of an hour for the last save and its upload.
    limit = args.hours * 3600 - (900 if args.resumable else 0)
    stop = False
    while step < plan["steps"] and not stop:
        order = epoch_order(train, epoch)
        for i in range(index, len(order)):
            if time.time() - started > limit:
                note(event="time limit", step=step)
                stop = True
                break
            loss = loss_of(order[i])
            if loss is None:
                skipped += 1
                continue
            scaler.scale(loss / args.accumulate).backward()
            running.append(float(loss))
            seen += 1
            if seen % args.accumulate:
                continue
            scaler.unscale_(optimiser)
            torch.nn.utils.clip_grad_norm_(trainable, 1.0)
            scaler.step(optimiser)
            scaler.update()
            optimiser.zero_grad(set_to_none=True)
            schedule.step()
            step += 1
            session_steps += 1
            boundary = (epoch, i + 1)
            if session_steps == 3 and not args.resumable:
                # Leave a quarter of an hour for the last check and the save.
                per_chat = (time.time() - trained_from) / seen
                left = args.hours * 3600 - (time.time() - started) - 900
                fits = step + int(left / per_chat / args.accumulate)
                if fits < plan["steps"]:
                    plan["steps"] = max(warmup + 1, fits)
                note(event="schedule fitted", seconds_per_chat=round(per_chat, 1), steps=plan["steps"])
            if step % 10 == 0 or step == plan["steps"]:
                note(event="step", step=step, loss=round(sum(running) / len(running), 4), lr=schedule.get_last_lr()[0])
                running = []
            if args.resumable and time.time() - last_save > args.save_minutes * 60:
                save_point(boundary, step, skipped)
                last_save = time.time()
            elif not args.resumable and step % 50 == 0:
                model.save_pretrained(args.out)
            if step >= plan["steps"]:
                stop = True
                break
        else:
            epoch, index = epoch + 1, 0
    if args.resumable:
        # Chats seen since the last optimiser step are seen again next session.
        save_point(boundary, step, skipped)
    model.save_pretrained(args.out)
    processor.save_pretrained(args.out)
    note(event="end", step=step, of=plan["steps"], skipped_too_long=skipped,
         check_loss=round(check_loss(), 4) if check else None)


if __name__ == "__main__":
    main()
