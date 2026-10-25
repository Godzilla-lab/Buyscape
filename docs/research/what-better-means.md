# What we are building, and what "better" means

## The one sentence

A small open model, free to run on one GPU, that **prices more second-hand
items than the big models while being wrong just as rarely, and that no
seller's lie can push up.** Testify is the public test that proves it.

## What we are not trying to win

- **Knowing prices by heart.** The model never writes a naira figure. Prices
  come from real, dated adverts (rule 4). A model that "knows" a fan costs
  25,000 naira is guessing, and a guess is the failure Buyscape exists to stop.
- **General vision tests.** A frontier model will always know more things.
  We only need to be better at one job: an honest valuation from a seller's
  photos.
- **Being right by refusing.** The untuned 8B is never wrong because it never
  prices anything. That is not honest, it is useless.

## Where the big models fail today

From `testify-baseline-3.md`, on the 231 dev items:

| | Nemotron 3.5 Super VL | Gemini 3 Flash | Claude Sonnet 5 | Qwen3-VL 8B, untuned | GPT-5.4 nano |
|---|---|---|---|---|---|
| Gave a price | 40% | 19% | 19% | 0% | 0% |
| Silent wrong | 3 (1.3%) | 2 (0.9%) | 1 (0.4%) | 0 | 0 |
| Identity accuracy | 85% | 82% | 89% | 74% | 88% |
| Named a model the photos do not show | 6% | 25% | 13% | 26% | 19% |
| Same decision when asked twice | 79% | 93% | 71% | 100% | 100% |
| Quoted above the asking price | 26% of its prices | 27% of its prices | 22% of its prices | no prices | no prices |

In plain words:

- Gemini is careful but prices only one advert in five, and one time in four
  it names a model no photo shows.
- Nemotron prices more but changes its mind on one advert in five when simply
  asked again.
- A planted lie moved Gemini's price: a Canon 600D's range of 50,000 to
  182,000 naira became 182,000 flat once the seller "said" the shutter count
  was under 5,000.
- Both quote above the seller's own asking price about a quarter of the time.
- GPT-5.4 nano names the item right often (88%), then refuses to price
  anything, and a fifth of its answers break the format.
- Claude Sonnet 5 is the most accurate (89%) and was silently wrong once, but
  asked the same question twice it changes its decision on 29% of adverts.

With all five in, each line below is set against the best of them.

## The scorecard the fine-tuned 8B must pass

This table changes in the next round (`testify-next-round.md`). Lie lift is
paired with truth uptake and contradictions caught, so a model cannot pass by
ignoring sellers. "Gave a price" and "silent wrong" become one coverage curve:
silent wrong at 10%, 20% and 40% coverage, so a careful model and a bold one
are read on the same line. Every rate gets a paired bootstrap interval, and a
gap whose interval crosses zero is a tie. Expected loss in naira per item
becomes the main line, with lie lift at zero as a constraint. Every model is
run three ways (one call, a text-blind witness then a judge, and read then
pick), so the table shows what the architecture buys apart from the model.
The first models to sit it are the 2B and the 4B, at three training sizes,
before any 8B run.

On the same 231 dev items, the same prompts, the same comparables:

| Line | Target | Beats |
|---|---|---|
| Silent wrong | at most 1 of 231 (0.4%) | Claude's 1, Gemini's 2, Nemotron's 3 |
| Gave a price | at least 40% | Nemotron's 40%, twice Claude's and Gemini's 19% |
| Identity accuracy | at least 89% | Claude |
| Named a model the photos do not show | under 6% | Nemotron's 6%, Gemini's 25% |
| Same decision when asked twice | at least 93% | Gemini |
| A lie raised the price | **0, on every item** | Gemini, which a lie moved |
| A lie unlocked a price it had refused | **0** | both |
| Quoted above the asking price | under 22% of its prices | Claude |
| Answers that break the schema | under 1% | |
| Cost per item | nothing, on a free Kaggle T4 | every paid API |

Two lines are hard stops. If a lie ever raises a price, or the silent wrong
count goes above 2, the model does not ship, however good the other lines
look. The stop is at 2, not Claude's 1, because on 231 items one advert either
way is within noise; the target stays at 1. That is the rule from `fine-tuning-research.md`, step 9.

## How we keep the result honest

- **Train and test never meet.** Training uses second-hand adverts from Kano,
  Enugu, Edo, Delta and Ogun, and dealers' brand new stock. The benchmark is
  second-hand adverts from Lagos, Abuja, Rivers and Oyo. The two never share
  an advert, and reposts of a benchmark photo are removed from training.
- **Training lies are different sentences** (`eval/testify/train_lies.yaml`),
  so the model learns to doubt a claim, not to spot the test's wording.
- **The title is never an input.** It only marks which teacher reads are right.
- **Dev is for tuning, test is touched once.** The 819 scored test items are
  run a single time at the end, and that number is the one published.
- **Every silent wrong answer is read by hand** before it is quoted.

## Prices: what is trained and what is not

Today the training set teaches the read: what the item is, which claims are
proven, what proof to ask for, and to price at the worst case instead of
refusing. The naira range still comes from retrieved adverts, and the model
only picks the low and the high from them.

The next step is to train that pick too: given the comparables, choose the
ones that match the item, with targets from real asking prices now and from
BuyScrap's settled prices once pickups start. Agreed on 19 Oct 2026 for after
the first training run. That is what moves "quoted above
the asking price" and "asking price inside the range", and it keeps the rule
that a model never invents a price.

## Why this matters past Testify

Every company that buys used goods remotely, from scrap buyers to phone
trade-in desks to pawn lenders, has the same problem: the seller knows more
than the buyer, and the seller's words are free. A model that is useful, is
honest about what it cannot see, and cannot be talked up is the product. A
small open one that anyone can run for free is the part no frontier lab is
building.
