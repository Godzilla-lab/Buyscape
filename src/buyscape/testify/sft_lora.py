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

    python sft_lora.py --model <base> --merge adapter/ --out merged/

folds the adapter into the 16 bit base, a plain model folder vLLM serves
with `vllm_batch.py` as it served the untuned one.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
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


def merge(base: str, adapter: Path, out: Path) -> None:
    """The base with the adapter folded in, saved in 16 bits with its processor."""
    import torch
    from peft import PeftModel
    from transformers import AutoModelForImageTextToText, AutoProcessor

    half = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16
    model = AutoModelForImageTextToText.from_pretrained(base, dtype=half, device_map="cpu")
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
    check = [e for e in examples if held_out(e, args.held_out)]
    print(f"{len(train)} chats to train on, {len(check)} held out", flush=True)

    # A T4 has no bfloat16, so the work is done in float16 with a loss scaler.
    half = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
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
    trainable = [p for p in model.parameters() if p.requires_grad]
    for param in trainable:
        # The scaler can only unscale float32 gradients.
        param.data = param.data.float()
    model.print_trainable_parameters()
    optimiser = torch.optim.AdamW(trainable, lr=args.lr, weight_decay=0.0)
    # Planned from the epochs, then cut to what the time limit allows once
    # the first steps show the speed, so the learning rate still ends low.
    plan = {"steps": max(1, int(len(train) * args.epochs / args.accumulate))}
    warmup = max(1, plan["steps"] // 20)

    def rate(step: int) -> float:
        if step < warmup:
            return (step + 1) / warmup
        return 0.5 * (1 + math.cos(math.pi * (step - warmup) / max(1, plan["steps"] - warmup)))

    schedule = torch.optim.lr_scheduler.LambdaLR(optimiser, rate)
    scaler = torch.amp.GradScaler("cuda", enabled=half == torch.float16)

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

    note(event="start", check_loss=round(check_loss(), 4) if check else None, steps=plan["steps"])
    model.train()
    trained_from = time.time()
    rng = random.Random(0)
    step, seen, skipped, running = 0, 0, 0, []
    stop = False
    while step < plan["steps"] and not stop:
        order = train[:]
        rng.shuffle(order)
        for example in order:
            if time.time() - started > args.hours * 3600:
                note(event="time limit", step=step)
                stop = True
                break
            loss = loss_of(example)
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
            if step == 3:
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
            if step % 50 == 0:
                model.save_pretrained(args.out)
            if step >= plan["steps"]:
                break
    model.save_pretrained(args.out)
    processor.save_pretrained(args.out)
    note(event="end", step=step, skipped_too_long=skipped, check_loss=round(check_loss(), 4) if check else None)


if __name__ == "__main__":
    main()
