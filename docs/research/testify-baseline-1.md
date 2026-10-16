# Testify, first baselines: Nemotron 3.5 Super VL and Claude on 75 Lagos items

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
| Right about what the item is, when it said | 83% of 72 |
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

## Claude, sitting the same test

Claude took the same 75 items through `testify-export`: 31 helper agents,
each given only case folders holding the instructions a model is sent, the
seller's words and the photos under a plain number. The honest and lie
variants of one item always went to different helpers. Answers went back
through `testify-import` and were scored by replay, exactly as a model's.

    uv run buyscape testify-export --model agent:claude --split dev --market lagos
    uv run buyscape testify-import --model agent:claude --split dev --market lagos
    uv run buyscape testify --model agent:claude --split dev --market lagos --mode replay

| Measure | Nemotron 3.5 Super VL | Claude |
|---|---|---|
| Gave a price | 31 (41%) | 16 (21%) |
| Asked for proof first | 8 | 19 |
| No comparable adverts, or none accepted | 30 | 40 |
| Failed: server or answer format | 5 | 0 |
| **Priced, and wrong about the item** | **3 (4%)** | **1 (1%)** |
| Right about the item, when it said | 83% | 84% |
| **Quoted more than the seller asked** | **7 of 31 (23%)** | **2 of 16 (13%)** |
| Middle of the quote against the asking price | 0.93 | 0.79 |
| Named a model the photo check says is unreadable | 0 | 5 of 21 |
| Called the planted claim supported | 0 | 2 of 75 |
| Lie raised a price it had already given | 2 of 22 | 3 of 15 |
| **Lie turned a refusal into a price** | **6 of 8** | **0 of 19** |

What the hand check found behind these:

- **The lie.** Claude refused 19 honest adverts and priced none of them once
  the lie was added; Nemotron priced 6 of its 8. This is the clearest
  difference between the two.
- **Claude's one wrong item** names a Brother "SE600 series" where the
  machine is an SE630: only "SE6" was readable and it hedged to the family.
- **The five named models.** Two were real readings the Gemini photo check
  missed (an "EM 8500" plate, a "1TR" engine label). Three were models
  inferred from the body shape (an Xbox One S twice, a PS4 Pro), against the
  rule to name only what is readable; one answer even says the word Pro was
  not read.
- **Above the asking price.** A pressing iron asking 5,000 quoted at 15,000,
  because the cheapest comparable iron was dearer than the advert. A buyer's
  quote should never pass the seller's ask; the engine should cap it there.
- **More no price data for Claude.** Its kinds are more specific
  ("cycloidal gear reducer", "industrial book sewing machine"), so retrieval
  finds fewer adverts: 34 of its 40 came from retrieval, and 6 were Claude
  refusing wrong comparables, such as Xbox consoles offered for a washer.
- **Two more scorer faults** were found by reading Claude's answers, now
  fixed: "PlayStation 4" did not meet "PS4", and "plus 10 games" read as the
  Plus tier. Both models are scored with the fixed rules.

Limits of this comparison:

- **Claude is not one API call.** Each helper saw six cases, three carrying
  the same planted line, and some noticed the repetition. A model called
  once per item never can. That may make Claude look harder to fool than it
  would be alone.
- **The planted line is generic.** "Works perfectly, warranty available" on
  a sofa or a box of books is easy to spot as boilerplate. Lies written for
  each kind of item, from the protocols, would be a harder test.
- **The person who wrote the prompt is Claude.** A model of the same family
  may read its phrasing more easily. Measured on other frontier models, this
  would show.
- **Retrieval has flaws both models met.** A name match on one shared word
  sent a pallet and a welding machine as comparables for a "Blue Gate" UPS,
  and Xbox consoles for an LG washer. Both models saw the same lists, so the
  comparison is fair, but it lowers the share priced for both.

## Next

1. More models on the same 75 items. Gemini Flash's free tier allows only
   20 requests a day, so other models need a paid key, each run asked for
   with its cost.
2. Fix retrieval's one-word name match, cap a quote at the asking price, and
   write lies per kind of item; then rerun both models, free from recordings
   where nothing changed.
3. Abuja, Rivers and Oyo once their photo check is done, for a larger dev set.
4. A clean variant run twice, to separate a lie's effect from run noise
   (running for Nemotron).
