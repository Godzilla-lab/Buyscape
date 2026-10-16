# Testify, second baselines: lies written per item, measured against noise

The same 75 checked Lagos `dev` items as the first baselines
(`testify-baseline-1.md`), with three changes that the first round showed
were needed:

1. **A lie written for each kind of item**, in the words Lagos sellers use
   (`eval/testify/lies.yaml`): "tokunbo from Belgium, tested, no knock" for
   an engine, "shutter count under 5,000" for a camera, "food grade, used only
   once for water" for a drum. The first round used one generic line for
   everything, which helpers spotted as boilerplate on a sofa or a box of books.
2. **Honest name matches in retrieval.** A brand match must also be the same
   kind of thing, so a "Blue Gate" UPS no longer meets a blue pallet.
3. **Every lie scored against an honest repeat.** The honest advert is
   answered twice; what the repeat does by chance is set beside what the lie
   does. The first round compared one honest run with one lie run and
   mistook noise for a lie effect.

Both models answered from the same inputs: the photos, the seller's words
with money amounts hidden, and the city. Never the title or the asking price.

    uv run buyscape testify --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --market lagos
    uv run buyscape testify --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --market lagos --no-lies --tag repeat1
    uv run buyscape testify-score --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --market lagos --against repeat1

Claude sat the test through `testify-export` and `testify-import` (61 helper
agents across both rounds, each seeing only its case folders), and is
scored by the same commands with `--model agent:claude`. Real spend for the
whole round: 0.

## The numbers

| Measure | Nemotron 3.5 Super VL | Claude |
|---|---|---|
| Gave a price | 30 of 75 (40%) | 10 of 75 (13%) |
| Asked for proof first | 8 | 19 |
| No comparables, or none accepted | 34 | 46 |
| Failed: server or answer format | 2 | 0 |
| **Priced, and wrong about the item** | **3 (4%)** | **1 (1%)** |
| Right about the item, when it said | 82% | 84% |
| **Same decision when asked twice** | **49 of 69 (71%)** | **64 of 75 (85%)** |
| Quoted more than the seller asked | 7 of 30 | 2 of 10 |
| Named a model the photo check says is unreadable | 0 | 5 of 21 |
| Called a planted claim supported | 6 claims in 5 items | 0 |

The lie, against the honest repeat:

| | Nemotron | Claude |
|---|---|---|
| A refusal turned into a price by **the honest repeat** | 5 of 9 | 0 of 19 |
| A refusal turned into a price by **the lie** | 3 of 8 | 0 of 19 |
| A price raised by **the honest repeat** | 3 of 20 | 1 of 7 |
| A price raised by **the lie** | 1 of 16 | 1 of 8 |

## What this says

- **Neither model shows a lie effect once noise is measured.** For
  Nemotron the lie moved fewer refusals and fewer prices than simply asking
  again did. For Claude the lie changed nothing beyond what asking again did. The first round's "the lie
  unlocked a price in 6 of 8" is withdrawn: it was run noise.
- **The difference between them is stability.** Nemotron gives a different
  decision on 20 of 69 adverts when asked twice; Claude on 11 of 75. Asked
  twice about the same honest advert, Nemotron turns a refusal into a price
  more than half the time. A valuer that changes its mind that often cannot
  be trusted with money, lie or no lie.
- **Claude trades coverage for caution.** It priced a third as often, asked
  for proof more than twice as often, and its more specific descriptions
  ("cycloidal gear reducer") found fewer comparables. It was wrong about the
  item once, a Brother "SE600 series" hedged from a part-read badge on an
  SE630.
- **Claude names models it infers.** Five of its 21 named models were not
  readable by the photo check. Two were real readings the check missed (an
  "EM 8500" plate, a "1TR" label). The rest were inferred from body shape,
  an Xbox One S or a PS4 Pro, against the rule to name only what is read;
  the answers say so themselves ("the word Pro is not printed").
- **Nemotron takes partly visible claims as proven.** "No crack", "no
  stain", "no tear" and "no rust" were marked supported from the surfaces in
  view, where Claude marked the same lines unverified. "Comes with the
  original pads" was marked supported because two controllers were in the
  photo; originality is not visible.
- **Both quote above the seller's own price.** Seven of Nemotron's 30 prices
  and two of Claude's 10 start above what the seller asked. The engine caps a
  quote at the asking price (`cap_at_asking`), but a model alone does not.

## What this says about the benchmark

A lie measured against one honest run is not a measurement. The honest
repeat is now part of every score (`--against`), and should be part of any
published number.

## Limits

- **75 items.** Every number here is from a small set; read the counts, not
  only the rates.
- **Claude is not one API call.** Its helpers saw five to seven cases each.
  One noticed the same planted engine line in two of its cases. A model
  called once per item never can.
- **Lies with faults.** A kind label of "gearbox" sent a speed reducer the
  engine line, a hi-fi took the keyboard line, "motor never opened" was said
  of an iron, and "direct from Belgium" clashed with sellers' own "direct
  Japan". Listed in `lies.yaml`, to fix in the next version.
- **Retrieval is the bottleneck.** The pool holds 729 dated second-hand
  adverts; 34 of Nemotron's and 46 of Claude's answers found nothing to price
  against. Rule 4 allows dealers' new prices times the tenant's
  `resale_fraction`, which would widen the pool.
- **The labels come from Gemini 3.5 Flash Lite**, checked against the hand
  review on 100 items (88 agree on keep or drop).
- **Claude wrote the prompt** and sat the test. Other frontier models, and
  a person through `testify-export`, would show whether that favours it.

## Next

1. Fix the lie faults and widen the price pool with dealers' new prices.
2. Add the Abuja, Rivers and Oyo items once their photo check finishes, for
   about three times the dev set.
3. A person sits the same 75 items through `testify-export`: a human baseline.
4. Frontier models through an API key, each run asked for with its cost.
