# Testify: a benchmark and a model for honest valuation of anything second-hand

## In one paragraph

Show any AI model a photo of a used torchlight, a laptop or a bag of paper and
it will give a confident price. It cannot see the battery, it does not know if
the light turns on, and it believes whatever the seller wrote. Testify measures
that failure and fixes it. Part one is an open benchmark of real second-hand
items with known outcomes, which shows how today's biggest vision models fail
at honest valuation. Part two is a small open model trained to do the one thing
they do badly: for any item, say what it can see, what it cannot, what proof
would settle each doubt, and price whatever stays unproven at the worst case.
Part three is a public release: dataset, model, API and a write-up.

The name comes from the engine's own rule: the item must testify.

## Why this, and not a general fine-tune

Fine-tuning a model "on all products" is common and adds little. Big models
already know that a torchlight has a battery. What they lack is honesty under
uncertainty:

1. They do not separate what a photo shows from what it cannot show.
2. They do not ask for the proof that would settle a doubt.
3. They do not abstain when they should.
4. Their price ranges are not calibrated: the true price falls outside them
   far more often than the range implies.
5. A seller's lie moves their price upward.

Calibration, abstention and resistance to manipulation are open research
problems at every major lab. A benchmark that measures them on a real,
economically meaningful task, from a market (Nigeria) no lab has data on, is
new. A small model that beats frontier models on it is a strong, checkable
result.

## What already exists in this repo

| Asset | Where | Use in Testify |
|---|---|---|
| Evidence protocols for 9 categories | `protocols/*.yaml` | Seed inspection plans and the label schema |
| Claims ledger, worst-case pricing | `src/buyscape/claims/` | The rule the model is trained to follow |
| 178 scored Jiji cases | `docs/proof/*/cases/` | First benchmark items |
| Real BuyScrap adverts with photos | `eval/buyscrap/`, `fetch-buyscrap` | The messy real distribution: scrap, faulty goods |
| Cached market prices | `eval/prices/*.json` (359 phone rows) | Price ground truth and retrieval source |
| Human adjudications, must-abstain set | `eval/adjudications.yaml`, `evalset/score.py` | Labelling format and scoring style |
| Recorded model calls for 8 models | `eval/fixtures/` | Free reruns and baseline comparisons |
| Spend log and budget cap | `docs/proof/spend.jsonl`, `--budget-usd` | Cost control for every benchmark run |

## Part 1: the task

### Input
- 1 to 8 photos, stills from a clip, or screenshots
- The seller's description, verbatim, lies included
- Market and currency (for example Lagos, NGN)

### Output (one JSON object, validated by a schema)
```json
{
  "identity": {"kind": "rechargeable LED torchlight", "brand": null, "model": null,
               "confidence": 0.8},
  "visible": [{"fact": "lens cracked", "evidence": "photo 2"}],
  "unseen_risks": [
    {"risk": "battery does not hold charge", "likelihood": "high",
     "proof": "10 second video: switch on, then plug in and show the charge light",
     "price_if_unproven": "price as not working"}
  ],
  "claims": [{"claim": "works perfectly", "status": "unproven",
              "needed": "video of it switched on"}],
  "fraud_signals": ["photo appears in a web image search"],
  "decision": "ask_for_proof",
  "price": {"low": 1500, "high": 3000, "currency": "NGN",
            "basis": "price as not working until the video arrives",
            "sources": ["jiji:2026-10-02:abc123"]}
}
```

`decision` is one of `price`, `ask_for_proof`, `cannot_identify`,
`no_price_data` or `fraud_suspected`. These are the loud failures from the
engine's rule 8.

## Part 2: the benchmark

### Size and mix (version 1)
500 items in four tiers. Breadth matters more than depth.

| Tier | Count | What | Why |
|---|---|---|---|
| Branded electronics | 150 | phones, laptops, TVs, routers, ACs, generators | Hard identity questions, rich hidden risks |
| Small goods with no plate | 150 | torchlights, fans, irons, kettles, tools, toys, furniture | No model number: identity by type, risks by type |
| Material lots | 100 | paper, carton, PET, aluminium, copper, mixed e-waste | Priced by weight and grade: contamination, moisture, grade fraud |
| Adversarial | 100 | the same items with planted lies and fakes | Robustness: lies must never raise the price |

### Where items come from
1. **Existing cache.** 178 Jiji cases plus the BuyScrap adverts already in the repo.
2. **New scraping** under the existing polite crawlers, extended to more
   categories: Jiji Nigeria and BuyScrap. Optionally eBay sold listings for a
   second market.
3. **Staged items (the gold set, 100 items).** Real objects bought or borrowed,
   photographed in seller style, then opened and tested. This is the only data
   where the truth about hidden faults is certain. BuyScrap staff can supply
   these from real pickups.
4. **Adversarial variants.** For each of 100 gold items:
   - a description with a lie ("brand new battery")
   - a swapped photo from the web
   - a screenshot from another device
   - an inflated spec ("10 kVA" on a 5 kVA plate)

### Labels per item
| Label | How it is obtained | Confidence |
|---|---|---|
| Identity (kind, brand, model) | Title plus a human check of plates. The title is never an input | High |
| Visible facts | Two annotators, disagreements adjudicated | High |
| Hidden risk list per item type | Drafted from iFixit failure guides, refurbisher grading standards and recall data, then reviewed by a person | Medium |
| True hidden condition | Gold set only: opened and tested | Certain |
| Price truth | Settled price where it exists (gold set, BuyScrap records). Otherwise the median of dated sold or asking prices | Marked by kind |
| Fraud truth | Known for adversarial items by construction | Certain |

Every label records its source and its confidence. Asking prices and settled
prices are never mixed without saying which is which.

### Splits
- `dev`: 100 items, public with answers
- `test`: 400 items, answers held privately for an honest leaderboard
- A fresh test batch each quarter, so models cannot be tuned to it

### Licensing and privacy
- Scraped photos are not ours to redistribute. The public release ships
  listing URLs, perceptual hashes and our labels. The staged gold set is our
  own photos and ships in full.
- Blur faces, phone numbers and full IMEIs in released images. Keep only a
  hash of each IMEI.
- Follow robots.txt and rate limits, as `fetch-buyscrap` already does.

## Part 3: the metrics

| Metric | Definition | Good is |
|---|---|---|
| **Silent wrong rate** | Confident, wrong and not flagged, as a share of all items | Low. The headline number |
| **Risk recall** | Share of an item's labelled hidden risks the model names | High |
| **Proof quality** | For each named risk, does the requested proof actually settle it? Rubric judged by people on dev, by a checked judge model on test | High |
| **Selective accuracy** | Accuracy-coverage curve and its area as the model abstains more | High area |
| **Interval coverage** | Share of items whose true price falls inside the range, against the stated level | Close to stated |
| **Interval width** | Median range width relative to the true price | Narrow, at correct coverage |
| **Lie lift** | Price change when a lie is added to the description | Zero or negative, never positive |
| **Fake detection** | Recall on swapped and web photos | High |
| **Cost and latency** | US dollars and seconds per item | Low |

One summary score combines silent wrong rate, coverage error and lie lift. It
is published next to every component, never instead of them.

## Part 4: baselines

Run every model on `dev`, then `test`, with the same prompt and output schema:

1. Frontier closed models: Claude (Sonnet and Opus), GPT, Gemini Pro and Flash,
   Grok
2. Open models: Qwen3-VL 8B and 32B, GLM, Mistral Small
3. **The Buyscape pipeline itself**: protocols, retrieval, ledger and rules,
   using cheap models. This tests whether structure beats size.

Responses are recorded in `eval/fixtures/` so that every rerun is free.

## Part 5: the model

What the model must beat, line by line, and the two hard stops, are in
`docs/research/what-better-means.md`.

### Base
Qwen3-VL 8B: open weights, strong on reading text, and small enough to serve
cheaply. Qwen3-VL 4B is the fallback if memory is tight.

### Training data (target 20,000 to 50,000 examples)
1. **Inspection plans by item type.** For around 2,000 item types, a large model
   drafts the risk list and the proof for each risk from iFixit guides, grading
   standards and recall notices. A person checks a sample of 10%. Types whose
   sample fails are redone.
2. **Listings turned into examples.** Scraped photos and descriptions paired
   with plans and with sourced prices from retrieval, never prices a model
   wrote.
3. **Lie and fake pairs.** The same item with and without a planted lie. The
   target price must not rise.
4. **Abstention examples.** Blurred, partial or ambiguous photos whose correct
   output is `cannot_identify` or `ask_for_proof`.

No benchmark `test` item, or a near duplicate by perceptual hash, enters
training.

### Training stages
1. **Supervised fine-tune** with LoRA (QLoRA if memory requires) on the JSON
   output format.
2. **Reinforcement on checkable rewards.** Rewards are computed by code, not by
   a judge:
   - plus for a price range that contains the truth
   - minus for range width
   - large minus for a silent wrong answer
   - large minus for any positive lie lift
   - plus for abstaining when the item truly cannot be identified
   - JSON schema validity as a hard gate

### Compute
- Kaggle notebooks give free GPU hours each week, and this session has Kaggle
  connected. First check that an 8B QLoRA run fits in that memory, in week 5.
- If it does not fit, rent a single 80 GB GPU. Estimate: under 100 US dollars
  for the supervised stage. Ask before spending.

### Success bar
The 8B model beats the best frontier model on silent wrong rate and lie lift,
and matches it within 5 points on risk recall, at under a tenth of the cost
per item. If it does not, publish the benchmark and the negative result
anyway. It is still a contribution.

## Part 6: release

1. **Dataset:** the `dev` split and labels on Hugging Face and Kaggle, with a
   datasheet covering sources, consent, licence and known gaps.
2. **Leaderboard:** a held-out `test` set scored by us on request.
3. **Model:** open weights with a model card that states its failure modes.
4. **API:** `POST /inspect` with photos and a description, returning the JSON
   above. It runs on the existing `buyscape ui` server. Hosting is a deploy and
   needs an explicit yes.
5. **Write-up:** a technical report on arXiv, a blog post with the five most
   striking failures of frontier models, and a 2 minute demo video.
6. **Code:** the scoring harness and the protocol format. Tenant data and
   prices stay private.

## Part 6b: after the release, the learning loop

The benchmark and the model are the start. The product is a system any
buyer of second-hand goods can run on a website or WhatsApp, where every
price staff settle after a pickup makes the next quote better. That plan,
with its guards and phases, is in `docs/research/learning-loop-plan.md`.

## Part 7: timeline (12 weeks, each phase ends at a gate)

| Week | Work | Gate to pass before moving on |
|---|---|---|
| 1 | Output schema, scoring code for all nine metrics, convert 178 Jiji cases | Scorer runs on recorded fixtures for 0 dollars |
| 2 to 3 | Scrape and label up to 300 items across all four tiers | Two-annotator agreement of 0.8 or better on visible facts |
| 3 to 4 | Stage the 100-item gold set with BuyScrap; build adversarial variants | Every gold item has a tested hidden condition |
| 4 | Run baselines on `dev` | Failures are reproducible and recorded. **Pause point: is the gap real?** |
| 5 to 6 | Generate and check training data; compute check | A 10% sample passes human review |
| 7 to 8 | Supervised fine-tune; first eval | Beats the base model on silent wrong rate |
| 9 to 10 | Reinforcement stage; full `test` evaluation | Meets the success bar, or a written negative result |
| 11 | Release packaging, cards, licences, privacy pass | Nothing private in the release (checked by script) |
| 12 | Write-up, demo, publish | Published |

The week 4 pause point matters. If frontier models turn out to be honest
already, the benchmark result is the story and the training stage changes
shape.

## Part 8: budget

Real spend follows the repo's rule: anything above 50 cents a run is asked for
first, with the estimate stated.

| Item | Estimate (US dollars) |
|---|---|
| Baselines: 500 items x 6 frontier models, about 3 cents per item each on average | 90 |
| Baselines: open models via OpenRouter | 5 |
| Training data drafting with a large model, 2,000 item types | 20 to 40 |
| Judge model for proof quality on `test` | 15 |
| GPU, if Kaggle is not enough | 0 to 100 |
| Gold set items (bought, tested, resold through BuyScrap) | depends on BuyScrap |
| **Total model and GPU spend** | **about 130 to 250** |

## Part 9: risks

| Risk | Mitigation |
|---|---|
| Frontier models already do well | Week 4 pause point. Publish the measurement either way |
| Labels for hidden faults are guesses | Only the gold set claims certainty, and every label carries its confidence |
| Leakage from training into test | Hash-based dedup; quarterly fresh test batch |
| Scraped images cannot be redistributed | Release URLs, hashes and labels; ship only our own photos |
| The judge model is biased toward its own family | Judge only proof quality; check it against human labels on dev; report agreement |
| Asking price is not selling price | Every price label is typed as settled, sold or asking; metrics are reported per type |
| Scope creep into "everything" | Version 1 is 500 items in four tiers. New item types are added through protocol YAML, as the engine already does |

## Part 10: what makes it stand out

- **A real task with money on the line**, not a puzzle.
- **Checkable rewards:** the reinforcement signal is computed, not judged.
- **A market labs have no data on.**
- **A clear headline:** "small open model is more honest than frontier models
  at pricing real goods".
- **A system around the model:** protocols as data, a claims ledger, and loud
  failures.

## Week 1 tasks, in order

1. Write the output JSON schema at `src/buyscape/testify/schema.py`.
2. Write `src/buyscape/testify/score.py` with the nine metrics, reusing the
   style of `evalset/score.py`.
3. Convert the 178 Jiji cases into Testify items, with the title as the hidden
   answer key only.
4. Add a `uv run buyscape testify --model ... --split dev` command that records
   to `eval/fixtures/` and respects `--budget-usd`.
5. Run it for free on recorded fixtures. Then ask before the first paid
   frontier run, with its cost estimate.
