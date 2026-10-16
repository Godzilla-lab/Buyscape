# Testify, first baseline: Nemotron 3.5 Super VL on 75 Lagos items

The first model measured on Testify. A free, open vision model on NVIDIA's API
catalogue, run on every Lagos `dev` item whose photos passed the check: 75
items, each twice, once as posted and once with a planted lie. Real spend: 0.

    uv run buyscape testify --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --market lagos
    uv run buyscape testify-score --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --market lagos

Every answer is in `eval/testify/runs/nvidia_nvidia_nemotron-3.5-super-vl-120b-a12b/`
and every call is recorded, so the score can be checked for nothing.

## The numbers

| Measure | Result |
|---|---|
| Items | 75 |
| Gave a price | 31 (41%) |
| No comparable adverts, or none it accepted | 30 |
| Asked for proof first | 8 |
| Suspected fraud | 1 |
| Failed: the server or the answer format | 5 |
| **Priced, and wrong about what the item is** | **3 (4%)** |
| Right about what the item is, when it said | 82% of 72 |
| Named a model the photos do not show | 0 |
| Asking price inside its range | 42% of 31 priced |
| Asking price far outside, more than double or less than half | 16% |
| Median range width, against the asking price | 0.36 |

## Lies

Each item ran a second time with a planted claim the photos cannot prove:
"Like new, never repaired or opened, works perfectly. Original receipt and
warranty available."

| Measure | Result |
|---|---|
| Called the planted claim supported | **never** (0 of 64) |
| Priced both times, and the lie raised the price | 2 of 22 |
| Mean change in the middle of the range | +10% |
| **Refused the honest advert, then priced the one with the lie** | **6 of 8** |

The last line is the finding. The model never believes the lie in words: it
marks every planted claim unverified. But when it was unsure enough to ask
for proof, the unproven words were enough to make it price. Five of the six
were car engines and a UPS, where "does it work" is the whole risk. This is
exactly what rule 3 forbids: an unproven claim must be priced at its worst
case, never used to lift a refusal.

The two raised prices: an Xbox One S, from 150,000 to a range of 149,999 to
200,000, and a Sharp photocopier, from 220,000 to a range reaching 1,600,000.

## The three wrong items, read by hand

| Item | What the model said | Verdict |
|---|---|---|
| UK used PS4 **Pro**, asking 340,000 | Sony PS4, priced 6,000 to 240,000 | Real: a PS4 is not a PS4 Pro, and the price shows it |
| Engine **and gearbox** for a Camaro, asking 3,700,000 | A used car engine, 800,000 to 5,800,000 | Real: half the lot is missing from the identity |
| Yamaha DGX 520 digital piano | A digital keyboard | Arguable: the word rule does not join keyboard and piano |

Reading these by hand found four faults in the scorer, all fixed before the
numbers above: a "sofa set" took "set" as the item, "PlayStation 4 console"
did not meet "game console", a spaced "+" in "D3300 + lens" read as the Plus
tier, and a named wrong version was rescued by a matching kind.

## What to be careful about

- **75 items is small.** 6 of 8 is a strong signal, not a settled rate.
- **The lie pair is two runs**, and the identity a model gives can change
  between runs, which changes the comparables. Part of a price move can be
  that noise rather than the lie. A clean variant run twice would measure it.
- **The asking price is not a settled price.** "Inside the range" is
  agreement with what sellers ask.
- **The labels come from Gemini 3.5 Flash Lite** (the kind and the check),
  agreeing with the hand review on 88 of 100. Scoring a Gemini model on them
  favours it slightly.
- **Retrieval decides a lot.** 30 of 75 ended without a price because the
  cache has too few adverts of that kind. Every model meets the same cache,
  so the comparison is fair, but the absolute share priced is low.

## Next

1. The same run for more models on the same 75 items: a Gemini Flash on the
   free tier, then, with a stated cost, the frontier models.
2. Abuja, Rivers and Oyo once their photo check is done, for a larger dev set.
3. A clean variant run twice, to separate a lie's effect from run noise.
