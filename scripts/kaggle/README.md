# Training and testing on Kaggle's free GPUs

The fine-tuned Qwen3-VL models were trained and scored entirely on Kaggle
notebooks (two T4 cards, 30 GPU hours a week per account). These scripts
write those notebooks. Each one carries the code it needs (the trainer and
the batch runner are embedded from `src/buyscape/testify/`), runs without
internet, and always exits within its time limit.

Nothing here pushes anything. A script writes a notebook folder under
`scripts/kaggle/out/` (not committed); you push it yourself with
`kaggle kernels push -p <folder>`.

## The files

| File | What it writes |
|---|---|
| `template.py` | The notebook every maker starts from: unpack the photos, check a dozen chats, train with LoRA, fold the adapter into the base, answer the dev reads with vLLM |
| `environment.json` | The Kaggle docker image the notebooks are pinned to |
| `make_training.py` | A training notebook for one model size and one training set |
| `make_resume.py` | A notebook that goes on from a save point, so one run can span several sessions or machines |
| `make_topup.py` | A short top-up: a small set taught on from a finished run's adapter (`sft_lora --init-adapter`) |
| `topup_set.py` | The top-up set itself: what a rebuilt training set changed, plus unchanged examples |
| `make_test.py` | A notebook that answers the test split's reads with a trained adapter |
| `make_picks.py` | A notebook that answers the price picks those reads lead to |
| `first_look/` | The public notebook *Buyscape Nigeria market: a first look* |

## One run, end to end

```bash
# 1. The training set, from the teachers' recorded reads (never committed).
uv run buyscape testify-train-build --out eval/testify/train/sft_r7.jsonl

# 2. Upload it with its photos as a private Kaggle dataset, then write and push the notebook.
python scripts/kaggle/make_training.py 2b sft_r7 --owner yourname --hours 11.5
kaggle kernels push -p scripts/kaggle/out/2b_sft_r7

# 3. Bring its dev answers home and score them (free, replayed).
uv run buyscape testify-batch-import --model local:qwen/qwen3-vl-2b-r7 --split dev \
    --results <output>/dev.results.jsonl --batch eval/testify/batches/local_qwen_qwen3-vl-8b-instruct/dev.jsonl
uv run buyscape testify --model local:qwen/qwen3-vl-2b-r7 --split dev --mode replay

# 4. The price picks those reads lead to, then the test split the same way.
uv run buyscape testify-batch-export --model local:qwen/qwen3-vl-2b-r7 --split dev
python scripts/kaggle/make_picks.py 2b <training notebook slug> eval/testify/batches/local_qwen_qwen3-vl-2b-r7 --owner yourname
python scripts/kaggle/make_test.py 2b <training notebook slug> --owner yourname

# 5. Compare every model on money and naming.
uv run buyscape testify-judge --split dev --split test
uv run buyscape testify-compare --split test --out eval/testify/runs/compare_test.json
```

`docs/research/testify-step5.md` records all seven runs: what each changed,
how long it took, and what it scored.

## Lessons the scripts already carry

- **Kaggle unpacks `.tar` uploads** into thousands of loose files. Photos go
  up as `<cache>.photos` tar files, which it leaves packed, and the notebooks
  unpack them.
- **Never glob the whole input tree**: one recursive glob over unpacked photos
  took 48 minutes. The notebooks walk the inputs once and skip photo folders.
- **A save point resumes only with the recipe it was made with**, so a run
  can move between Kaggle and a rented GPU and pick up where it stopped.
- **Check before you train**: a dozen chats with the run's own settings come
  first, so a setup fault costs minutes, not a session.

The dataset names in the scripts' defaults are this project's own private
Kaggle datasets; pass your own with `--sources`.
