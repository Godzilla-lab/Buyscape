# Buyscape

**Honest prices for second-hand goods, from photos.** A seller sends photos and
a few words. Buyscape says what the item is, checks every claim against the
photos, and returns a price range drawn from real adverts, with the
conditions attached to it. A person approves the quote; the agent confirms at
pickup; the price actually paid feeds back into the next quote.

It is built for any business that buys used goods remotely, and onboards a new
one by configuration alone. [BuyScrap Nigeria](https://buyscrap.com.ng), which
buys scrap, appliances, electronics and car parts in Lagos, is the first.

| | |
|---|---|
| **Benchmark** | [Testify on Hugging Face](https://huggingface.co/datasets/godzilla1215/testify): 910 real Nigerian adverts, links and labels only |
| **Market data** | [Buyscape Nigeria second-hand market on Kaggle](https://www.kaggle.com/datasets/godzilla1215/buyscape-market-data-public): 15,471 adverts from 31 cities and regions |
| **Research** | [`docs/research/`](docs/research/README.md): every experiment, what it changed and what it cost |

## Why this is hard, and what is different here

Earlier attempts at photo-based valuation failed in four ways. Quotes were cut
by a third at the doorstep, so sellers stopped trusting them. Models guessed
instead of admitting they could not tell. Identification was attempted from the
photo alone, which published work puts at 13 percent on fine-grained identity.
And the risk was pushed onto expensive hardware that never paid back.

Buyscape answers each one:

- **Unproven claims are priced at the worst case up front**, so the pickup
  price can only hold or improve. A lie cannot raise the remote price.
- **Abstention is a rule outside the model.** "Cannot identify", "no price
  data", "evidence incomplete" and "fraud suspected" are first-class answers,
  never a silent guess.
- **Prices are retrieved, never generated.** Every number comes from a dated,
  sourced advert. The model explains; it does not invent figures.
- **The model ranks a retrieved shortlist** rather than answering alone, and
  a small fine-tuned model does that job on one modest GPU.

## How it works

```
 seller's photos and words
          │
          ▼
 1. Read      a vision model names the item: brand and model where it carries one,
              its type in a buyer's words where it does not ("2 seater sofa")
          │
          ▼
 2. Check     every seller claim is tied to the photo that would prove it;
              an unproven claim is priced at its worst case
          │
          ▼
 3. Retrieve  real adverts for the same item, each with a source and a date
          │
          ▼
 4. Price     a range from those adverts, with the conditions that would raise it
          │
          ▼
 5. Approve   the tenant's team approves in the back office; the agent opens,
              weighs and confirms the item at pickup
          │
          ▼
 6. Learn     the price actually paid is saved, and becomes a calibration row
              and a training example for the next model
```

What a category needs (which photos, which claims, how to price it when
unproven) is data: one YAML file per category in [`protocols/`](protocols).
What a business needs (its price list, its questions, its resale fractions) is
data too, in [`tenants/`](tenants). Adding either is never a code change.

## Results

On Testify's 679-item test split, adverts no model trained on. The money
measure is what a buyer would lose per item acting on the answers: an offer
above the asking price costs the difference, a request for proof costs half
of a lost deal, a refusal the whole lost deal. Lower is better.

| Model | Gave a price | Named the item right (judged) | Expected loss per item |
|---|---|---|---|
| Qwen3-VL 2B, fine-tuned (run 4) | 31% | 94% | **₦3,873** |
| Qwen3-VL 2B, fine-tuned (run 5) | 21% | 95% | **₦3,850** |
| Qwen3-VL 2B, fine-tuned (run 7) | 22% | 95% | ₦6,204 |
| Claude Sonnet 5 | 19% | 99% | ₦7,415 |
| Nemotron 3.5 Super VL | 43% | 97% | ₦55,602 |

The small fine-tuned model loses about half what Claude Sonnet 5 loses and
fourteen times less than Nemotron. The big models still name items a little
better. The full tables, every training run and what each one taught, are in
[`docs/research/testify-step5.md`](docs/research/testify-step5.md).

## Quick start

Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Godzilla-lab/Buyscape && cd Buyscape
uv sync

uv run buyscape protocols                               # validate every category protocol
uv run buyscape run --reader fake --reasoner fake --limit 8   # the whole engine, offline, no keys
uv run buyscape ui                                      # seller page at /, back office at /office
uv run --group dev pytest                               # the tests
```

Real model calls need keys, read from the environment or a `.env` file at the
root (never committed): `OPENROUTER_API_KEY` for the default reader and
reasoner, and optionally `GEMINI_API_KEY`, `NVIDIA_API_KEY` or `HF_TOKEN`.
Without them, recorded calls replay and the run says so. Every paid run
appends its cost to `docs/proof/spend.jsonl`, and the default cap is 50 cents
a run.

```bash
uv run buyscape assess path/to/photos/        # value one item from a folder of photos
uv run buyscape run --preset balanced --budget-usd 0.5
uv run buyscape spend                         # what every run cost, per item
```

## Scoring a model on Testify

```bash
uv run buyscape testify --model <provider:model> --split dev     # score a model on the dev split
uv run buyscape testify-judge --split dev                       # other words for the same thing count as right
uv run buyscape testify-compare --split dev                     # every model side by side, with the money measure
uv run buyscape testify-export --model human:ada --split dev    # a person sits the test at /office/testify
```

A model you run on your own GPU answers through batches:
`testify-batch-export` writes the requests, any server that speaks the chat
format answers them, and `testify-batch-import` records the answers to score
for free. The test split's answers stay out of the release; ask to have a
model scored on it.

## Fine-tuning

The fine-tuned models are Qwen3-VL 2B and 4B Instruct with LoRA adapters,
trained on Kaggle's free GPUs and on rented ones. The training set is built
from teachers' reads of training adverts that never appear in the benchmark
(`buyscape testify-train-build`), and [`scripts/kaggle/`](scripts/kaggle/README.md)
writes the notebooks that train, resume, top up and test a model. The recipe
and its sources are in
[`docs/research/fine-tuning-research.md`](docs/research/fine-tuning-research.md).

## Repository layout

```
src/buyscape/        the engine
  identify/            reading the item, the candidate catalogue, the local OCR witness
  claims/              the claims ledger: each statement against the evidence that proves it
  pricing/             comparables, market words, new prices times resale fractions
  evalset/             scoring the engine's own runs
  testify/             the benchmark: building, running, scoring, judging, training sets, the trainer
  providers/           model providers (OpenRouter, NVIDIA, Google, Kaggle, vLLM, replay)
  ui/                  the seller page, the back office and the test bench, on stdlib http
  media/               stills cut from seller clips, plain OpenCV
protocols/           one YAML per category: shots, questions, claims, pickup checks
catalogue/           candidate catalogue, one CSV per category
tenants/             one YAML per business: prices, questions, resale fractions
release/testify-v0.1 the public benchmark release, as published on Hugging Face
scripts/kaggle/      notebooks that train and test the models on Kaggle
docs/research/       every experiment and plan, in order
docs/proof/          the engine's case reports and the cost of every run
eval/                cached adverts, recorded model calls, benchmark runs (photos are never committed)
tests/               the tests
```

## Data and terms

Testify and the public market data are **links and labels only**: no photos,
no sellers' words, no contact details. Jiji adverts are used with the
permission of Jiji Nigeria (jiji.ng), granted on 4 Nov 2026, on those terms.
A private research version with photos exists and is shared only under a data
agreement and the source's terms.

## Licence

The code is under the Apache License 2.0 ([`LICENSE`](LICENSE)). Testify's
labels, lies, schema and scores are released under CC BY 4.0, and the public
market table under CC BY-SA 4.0. The adverts they point to belong to their
sellers and the sites that host them, and are not covered by either licence.

## Contact

Olamilekan, olamibusari607@gmail.com. Questions, a model to score on the test
split, or settled prices to contribute are welcome.
