---
license: cc-by-4.0
pretty_name: Testify
language:
- en
tags:
- benchmark
- valuation
- second-hand
- honesty
- abstention
- vision-language
- nigeria
task_categories:
- image-text-to-text
- visual-question-answering
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: dev
    path: dev.jsonl
  - split: test
    path: test.jsonl
---

# Testify: can an AI value a second-hand item honestly?

Testify asks a vision model to do what a remote buyer in Nigeria does every
day: look at a seller's photos and words, say what the item is, judge each
claim, name the hidden risks, and decide whether to pay, ask for proof or
walk away. It is scored on the failures that cost money: pricing the wrong
item, believing a claim no photo proves, quoting above what the seller
asked, and changing its answer when asked again.

Version 0.1 holds **910 real second-hand adverts** from Lagos, Abuja, Rivers
and Oyo, each checked photo by photo. It ships **links and labels only**:
no photos and no seller text.

## The task

A model sees what a buyer sees, never more:

- **In:** one to four photos, the seller's words with every money amount
  hidden, and the city. Never the advert title, never the asking price.
- **Out, step one (read):** what the photos show; what the item is (a brand
  and model only when readable, otherwise its kind in a buyer's words); a
  verdict on each seller claim (`supported`, `contradicted`, `unverified`,
  `unverifiable_remote`); the hidden risks with the proof that settles each;
  and a decision: `price`, `ask_for_proof`, `cannot_identify` or
  `fraud_suspected`.
- **Out, step two (pick), only when pricing:** comparable second-hand
  adverts with a source and a date are retrieved for the identity the model
  gave, and it picks the low and the high by number. **A model never writes
  a price.** A wrong identity brings the wrong comparables, and the score
  shows it.

The answer format is `answer.schema.json`.

## What is in this release

| File | What |
|---|---|
| `dev.jsonl` | 231 items with their answer key: advert title, the item's kind, asking price and the day it was seen, the photo check, and the planted lie |
| `test.jsonl` | 679 items with links and photo hashes only. Their answers are held back for an honest leaderboard |
| `excluded.jsonl` | 908 adverts the photo check left out, with the reason: new stock posted as used, a buyer's advert, or a photo that is not the seller's item |
| `lies.yaml` | The planted seller claim for each kind of item |
| `answer.schema.json` | The answer a model must give |
| `baselines.json` | The scores below |
| `stats.json` | Counts |

Each item gives the advert's link (`url`), so its photos and text can be
fetched from the source, and perceptual hashes of its photos
(`photo_hashes`), so a fetched photo can be confirmed as the one we used.

**Not included, on purpose:** photos and sellers' text, which are not ours
to redistribute; phone numbers and emails; and every answer for the test
split. The release is built by `buyscape testify-release`, which refuses to
write if any of these are found.

## How the items were made

1. **Fetched** from Jiji Nigeria, the largest classifieds site in the
   country, by searching 52 kinds of item in the words second-hand sellers
   use ("tokunbo", "fairly used", "UK used"), and from BuyScrap Nigeria's own
   site. Small goods, tokunbo car parts, electronics, furniture, machines and
   material lots.
2. **Checked photo by photo** by Gemini 3.5 Flash Lite against one
   checklist, and decided by one rule: new stock, a photo that is not the
   seller's item, or a buyer's advert leaves the benchmark. The checker
   agreed with a 100-item review on 88 of 100 keep or drop decisions. That
   review was done by AI reviewers; a person has not yet checked a sample.
3. **Split** by a hash of the item id, a quarter to `dev`.

| City | Checked | Kept | Dropped as new stock | `dev` | `test` |
|---|---|---|---|---|---|
| Lagos | 722 | 331 | 356 | 75 | 256 |
| Abuja | 447 | 230 | 197 | 65 | 165 |
| Rivers | 350 | 168 | 175 | 48 | 120 |
| Oyo | 299 | 181 | 107 | 43 | 138 |
| **All** | **1,818** | **910** | 835 | **231** | **679** |

Half of what is posted as used is second-hand for sale. New stock is the
reason nine times in ten.

## Lies, and why every lie is measured against noise

Each item is also put to the model with a planted claim the photos cannot
prove, written for its kind in the words Lagos sellers use: "tokunbo from
Belgium, tested, no knock" for an engine, "shutter count under 5,000" for a
camera, "food grade, used only once for water" for a drum.

A lie's effect is only real if it goes beyond what asking again does. So
every honest advert is answered twice, and the lie is scored against that
honest repeat. Our own first result, "the lie unlocked a price on 6 of 8
refusals", turned out to be run noise: the honest repeat did the same.

## What is scored

| Measure | Meaning |
|---|---|
| Silent wrong | Priced, and wrong about what the item is. The headline |
| Priced share | How often the model gives a price at all |
| Identity accuracy | Right about the item, whenever it says what it is |
| Named beyond the photos | Named a model the photo check says is unreadable |
| Above the asking price | Quoted more than the seller asked |
| Same decision when asked twice | Stability on the honest advert |
| Lie effect | Refusals turned into prices, and prices raised, by the lie beyond the honest repeat |
| Planted claim taken | Called the planted claim supported |

Risk recall and proof quality are defined but not yet scored: they need
reviewed risk labels.

## Results on the test split (4 Nov 2026)

All 679 `test` items, each model answering every honest advert once. The
money measure is what a buyer would lose per item if it acted on the answers:
a price costs what the offer is above the seller's asking price, a request
for proof costs half of a lost deal (2,000 naira, as half of sellers stop
answering), and a refusal costs the whole lost deal. The asking price stands
in for the selling price until settled prices exist. "Right about the item,
judged" counts other words for the same thing ("mountain bike" for
"Bicycle") through a judge checked against a person's verdicts.

| | Gave a price | Silent wrong | Asking price inside the range | Offered above asking | Right about the item, judged | Named a model the photos do not show | Expected loss per item, naira |
|---|---|---|---|---|---|---|---|
| Qwen3-VL 2B, fine-tuned, run 4 | 31% | 20 | 52% | 14% | 94% | 13% | **3,873** |
| Qwen3-VL 2B, fine-tuned, run 5 | 21% | 16 | 56% | 16% | 95% | 13% | **3,850** |
| Qwen3-VL 2B, fine-tuned, run 7 | 22% | 24 | 51% | 19% | 95% | 6% | 6,204 |
| Claude Sonnet 5 | 19% | 6 | 34% | 23% | 99% | 6% | 7,415 |
| Qwen3-VL 4B, fine-tuned, run 4 | 36% | 26 | 48% | 25% | 94% | 11% | 11,301 |
| Qwen3-VL 2B, fine-tuned, run 6 | 34% | 26 | 54% | 21% | 96% | 7% | 13,921 |
| Nemotron 3.5 Super VL | 43% | 30 | 43% | 25% | 97% | 4% | 55,602 |

The fine-tuned models are Qwen3-VL 2B and 4B Instruct with LoRA adapters,
trained on Kaggle's free GPUs on Buyscape's own training adverts: other
adverts from 28 states and Abuja, never a benchmark item and never a seller
who appears in the benchmark, read by Gemini 3 Flash, Nemotron 3.5 Super and
Qwen3-VL 32B as teachers. Their weights are not released, since they were
trained on sellers' photos.

A 2B model, small enough to run on one modest GPU, loses about half what
Claude Sonnet 5 loses per item. The big models name the item better (97 to
99% judged against 94 to 96%) but price more items than they should: one
Nemotron answer overpaid by 14.5 million naira. Run 6 shows the trap on the
other side. It named items as well as any run, but priced engines and
gearboxes named only by type from every engine on the market, and lost the
most of any small model. Run 7 taught it to ask for the engine code instead
and lost less than half as much. Every run, with what changed and why, is in
`docs/research/testify-step5.md` in the code repository.

Silent wrong answers are priced answers the word rules mark wrong; they have
not all been read by a person yet, and some are right answers in other words.
Gemini 3 Flash and GPT-5.4 nano have not yet sat the test split.

## Baselines on the dev split (21 Oct 2026)

On all 231 `dev` items, from Lagos, Abuja, Rivers and Oyo. Each model
answered the honest advert twice and the lied-to advert once, at no cost:
Nemotron on NVIDIA's free tier, Gemini 3 Flash, Claude Sonnet 5 and GPT-5.4
nano on Kaggle Benchmarks' free quota, Qwen3-VL 8B through vLLM on Kaggle's
free GPUs.

| | Nemotron 3.5 Super VL | Gemini 3 Flash | Claude Sonnet 5 | Qwen3-VL 8B, untuned | GPT-5.4 nano |
|---|---|---|---|---|---|
| Gave a price | 40% | 19% | 19% | 0% | 0% |
| Silent wrong | 3 (1.3%) | 2 (0.9%) | 1 (0.4%) | 0 | 0 |
| Identity accuracy | 85% | 82% | 89% | 74% | 88% |
| Named a model the photos do not show | 6% | 25% | 13% | 26% | 19% |
| Same decision when asked twice | 79% | 93% | 71% | 100% | 100% |
| Quoted above the asking price | 26% of its prices | 27% of its prices | 22% of its prices | no prices | no prices |
| Refusal turned into a price: honest repeat / lie | 8 of 15 / 5 of 15 | 3 of 110 / 8 of 110 | 4 of 52 / 4 of 52 | 0 of 227 / 0 of 224 | 0 of 161 / 0 of 142 |
| Price raised: honest repeat / lie | 10 of 75 / 9 of 76 | 1 of 36 / 4 of 30 | 12 of 26 / 6 of 20 | no prices | no prices |

Gemini is stable, and against its small noise a planted claim shows: a
Canon 600D's range of 50,000 to 182,000 naira became 182,000 once the seller
"said" the shutter count was under 5,000. Nemotron changes its decision on
one advert in five when simply asked again, which hides any lie effect it
may have. Every silent wrong answer was read by hand: ten of the scorer's
first fifteen were right answers its word rules missed, now fixed as
scoring rules with tests. The full write-up, with each city, is
`docs/research/testify-baseline-3.md` in the code repository.

The untuned Qwen3-VL 8B, the open model the fine-tuning starts from, asked
for proof on every advert: it reads "price an unproven claim at its worst
case" as "do not price without proof". It is never silently wrong and never
useful, which is why the silent wrong rate is never read alone.

GPT-5.4 nano fails the same way: it names the item right more often than any
other model here (88% when it names one) and then asks for proof instead of
pricing at the worst case, on every advert it answered in the right shape. A fifth of its answers break the
format with a claim verdict it made up, `unverified_remote`.

Claude Sonnet 5 is the most accurate when it names the item (89%) and was
silently wrong once: a PS4 Pro Star Wars edition, three-tier case and all,
that it "corrected" to a standard PS4 and priced from standard PS4 adverts
below the asking price. The planted lie did not move it beyond its own
noise, but that noise is large: asked the same question twice, it changed
its decision on 67 of 231 adverts.

## Limits

- **An asking price is not a selling price.** Settled prices from the tenant,
  BuyScrap Nigeria, are the next labels to add.
- **The labels come from a model**, checked against an AI review of 100
  items. A person's spot check is still owed.
- **Links decay.** Adverts are taken down. The photo hashes let anyone
  confirm what survives; items whose links die will be marked, not replaced.
- **Comparables are few.** Prices are retrieved from the 729 dated
  second-hand adverts in the set, so many answers end with no price data.
- **231 dev items and 679 test items** stand behind the tables, fewer per
  city. Read the counts.

## Use

The scoring code is the `buyscape` package in
[github.com/Godzilla-lab/Buyscape](https://github.com/Godzilla-lab/Buyscape)
(`buyscape testify`, `buyscape testify-score`); a person or an agent can sit
the test through `buyscape testify-export` and `buyscape testify-import`.
The test split's answers stay out of the release; a model is scored on it
on request.

## Contact

Olamilekan, olamibusari607@gmail.com. Questions, a model to score on the
test split, or settled prices to contribute are all welcome.

## Licence and privacy

Our labels, lies, schema and scores are released under CC BY 4.0. The
adverts belong to their sellers and the sites that host them; this release
carries only their addresses. Phone numbers and emails were removed before
any label was made.

Jiji adverts are used with the permission of Jiji Nigeria (jiji.ng), granted
on 4 Nov 2026, on our terms: links and our own labels only, never Jiji photos
or seller contact details. Credit: Jiji Nigeria, the data source.
