# Testify, step 5: the new tests on the baselines

Status on 28 October 2026: part done. Every number here is on the 231 dev
items unless it says otherwise, and every silent wrong answer counts only once
a person has read it (`eval/testify/adjudication.yaml`).

## What step 5 adds

The third baselines asked one question of each advert: name it and price it,
with or without a planted lie. Step 5 asks the same models six more:

- **A true claim and its false twin.** A claim a photo proves ("The model is
  D3300.") must be used, and the same claim made false ("D3400") caught.
- **The label taken away.** The photo that names a branded item is removed or
  its code painted out. The right answer is to ask for that shot.
- **Three ways to put the item** (`--condition`): read then pick, a witness
  who sees only the photos and a judge who weighs the words against it, and
  one call with a fixed list of adverts for the item's kind.
- **Pushback.** After a lie is left unproven, the seller replies "I tested it
  myself yesterday". No new photo comes with it.
- **Pressure.** The business adds "we need 50 pickups this week".
- **The shared list.** Every model picks its price from the same list of
  adverts for the item's kind, so the pick is measured apart from the search.

## A person read the disputed answers

The word rules marked 20 priced answers wrong. A person read all 20: 16 were
right, 1 was the wrong kind of item, and 3 could not be settled. With those
verdicts in, Gemini, Nemotron and nano have no silent wrong answer left and
Claude has one, the PS4 Pro advert marked unsure. So the silent wrong count no
longer separates the models. What does is below.

## True and false claims

| Model | True claim used, read then pick | Judged apart | False claim caught, read then pick | Judged apart |
|---|---|---|---|---|
| Nemotron | 89% | 85% | 100% | 93% |
| Gemini | 74% | **93%** | 96% | **100%** |
| Claude | 44% | running | 96% | running |
| nano | 39% | **70%** | 91% | 81% |

No model took the false name into its answer. When one step reports only
what the photos show, the judge can check a claim against it, and true claims
stop being ignored. nano catches fewer false claims that way.

Judged apart, Nemotron never called the planted lie supported (0% against
4.4%), and a lie raised its price on 4.9% of items against 11.8%. It prices
more (48% against 40%), but the word rules mark 14 of those answers wrong:
the witness names the item from the photos alone. They wait for a person.

## The label taken away

Ten branded items, read then pick:

| Model | Said it cannot tell | Asked for the label first |
|---|---|---|
| Nemotron | 30% | 70% |
| Gemini | 60% | 50% |
| Claude | 60% | 60% |
| nano | 100% | 100% |

nano never prices anything, so its 100% is not a skill. Nemotron under the
three conditions:

| Condition | Said it cannot tell | Asked for the label first | Named the hidden code anyway |
|---|---|---|---|
| Read then pick | 30% | 70% | 0% |
| Judged apart | 20% | 20% | 0% |
| One call, fixed list | 10% | 60% | **30%** |

The fixed list names the models of the item's kind, so a model can copy the
code it can no longer see. That is a flaw of the one-call condition, not good
reading. Ten items move a share by ten points: these are directions.

## Pushback and pressure

- **Pushback, Nemotron, 228 items:** no answer flipped to believing the lie,
  none unlocked a price, and the price rose on 5.3% of items against 13%
  between two honest runs.
- **Pressure, Nemotron:** 44.6% priced under the quota note against 40.7%
  without it. Two honest repeats priced 39.0% and 43.3%, and the item by item
  churn is the same size (28 newly priced and 19 dropped under pressure,
  against 25 and 18 between two honest runs). No effect beyond noise.

## The shared list

Nemotron picking from the list for the item's kind instead of its own search:

| | Its own search | The shared list |
|---|---|---|
| Gave a price | 40% | 56% |
| Asking price inside the range | 43% | 50% |
| Offered above the asking price | 26% | 21% |

The word rules mark 9 of the shared list's priced answers wrong; they wait
for a person.

## The small models, untuned

The models the size curve starts from, on Kaggle's free T4 pair:

| Model | Right about the item | Named a model the photos do not show | Called the lie supported | Broke the format | Gave a price |
|---|---|---|---|---|---|
| Qwen3-VL 8B | 74% | 26% | 3% | 4 of 231 | 0% |
| Qwen3-VL 4B | **81%** | **24%** | **2%** | **1 of 231** | 0.9% |
| Qwen3-VL 2B | 77% | 54% | 47% | 60 of 231 | 0% |

The 4B reads better than the 8B, and like it almost never prices. The 2B is
not a usable starting point as it stands: 163 of its 462 answers repeat
until the 8,000 token cap, a quarter of its honest answers break the format,
and it believes the planted lie almost half the time. The training set now also teaches the price step, the
pick from real adverts that bracket an advert's own asking price, on the 222
second-hand training adverts where one exists.

## Still running

Nemotron's judged apart and one call runs, Claude's judged apart run (23
answers short), Gemini's and nano's remaining conditions, pushback and
pressure for the Kaggle models, the rest of the untuned 2B, and the size
curve, which starts with the 4B on the 500 advert set once it is agreed.
