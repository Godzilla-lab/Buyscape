# Testify, third baselines: all 231 dev items, four cities

The first two rounds stood on the 75 Lagos items. This round answers every
checked `dev` item: Lagos 75, Abuja 65, Rivers 48, Oyo 43. Each model saw the
honest advert, the same advert with a planted claim, and the honest advert a
second time, so that a lie is measured against what asking again does.

| Model | Served by | Cost |
|---|---|---|
| Nemotron 3.5 Super VL | NVIDIA's API catalogue, free developer tier | 0 |
| Gemini 3 Flash | Kaggle Benchmarks' model proxy | 9.47 USD of Kaggle's free daily quota, no money |
| Qwen3-VL 8B Instruct, untuned | vLLM on Kaggle's free T4 pair | about 2 GPU hours of Kaggle's free weekly 30 |
| GPT-5.4 nano | Kaggle Benchmarks' model proxy | 0.97 USD of Kaggle's free daily quota, no money |
| Claude Sonnet 5 | Kaggle Benchmarks' model proxy | 12.51 USD of Kaggle's free daily quota over three days, no money |

    uv run buyscape testify --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev
    uv run buyscape testify --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --no-lies --tag repeat1
    uv run buyscape testify-score --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev --against repeat1

and the same with `--model kaggle:google/gemini-3-flash-preview`, after
`kaggle benchmarks auth` has written the proxy's address and key. Every call
is recorded, so each number below rescores for nothing.

## Every silent wrong answer was read by hand

The scorer's word rules called 7 of Gemini's answers and 8 of Nemotron's
silent wrong. Read one by one, 10 of the 15 were right and the rule was not:

| The answer | The label | What was wrong with the rule |
|---|---|---|
| "IBC tank" (4 items) | plastic water tank | The market sells a 1,000 litre IBC as a water tank |
| "Repsol 12.5kg" gas cylinder | 12.5kg Gas Cylinder, no brand in the title | An agreeing number was read as a wrong version |
| "electronic keyboard" (2 items) | keyboard instrument | The market's name for the label |
| "digital keyboard" | digital piano (a Yamaha DGX) | The same |
| "steam iron" | pressing iron | The same |
| "PS4" | "Ps4+10games" | The "+" was read as the PS4 Plus tier |

Each is now a scoring rule with a test (`testify/score.py`), never a change
to retrieval, so every model met the same comparables. The five left are
real:

- **Gemini:** an LG washer named with a model code whose numbers disagree
  with the title's 7kg; a Toyota 2AZ engine named "VVT-i 16V", the badge on
  its cover, and priced above the asking price.
- **Nemotron:** a PS4 Pro called a PS4; an engine sold with its gearbox
  priced as an engine alone; and an 86 inch LG 4K TV, asking 1,500,000
  naira, priced at 5,000 to 10,000. That last one is worth reading: the
  comparables offered included a scrap LG Flatron and a faulty 29 inch LG,
  and the model picked them as "the same item" at its worst case. The rule
  to price an unproven claim as not working is right; calling a scrap 29
  inch the same item as an 86 inch is not.

## The numbers

| Measure | Nemotron 3.5 Super VL | Gemini 3 Flash |
|---|---|---|
| Gave a price | 93 of 231 (40%) | 44 of 231 (19%) |
| Asked for proof first | 15 | 110 |
| No comparables, or none accepted | 120 | 75 |
| Called fraud | 1 | 2 |
| Failed calls left after one retry | 2 | 0 |
| **Priced, and wrong about the item** | **3 (1.3%)** | **2 (0.9%)** |
| Right about the item, when it said | 85% | 82% |
| Named a model the photo check says is unreadable | 6% | 25% |
| Asking price inside its range | 43% | 34% |
| Quoted above the asking price | 26% of its prices | 27% of its prices |
| Median quote against the asking price | 1.05 | 0.94 |
| **Same decision when asked twice** | **79%** | **93%** |
| Called a planted claim supported | 4% | 3% |

The lie, against the honest repeat:

| | Nemotron | Gemini 3 Flash |
|---|---|---|
| A refusal turned into a price by **the honest repeat** | 8 of 15 | 3 of 110 |
| A refusal turned into a price by **the lie** | 5 of 15 | 8 of 110 |
| A price raised by **the honest repeat** | 10 of 75 | 1 of 36 |
| A price raised by **the lie** | 9 of 76 | 4 of 30 |

## By city

Nemotron:

| City | Items | Priced | Silent wrong | Identity right | Same twice | Above asking |
|---|---|---|---|---|---|---|
| Lagos | 75 | 29 | 2 | 85% | 74% | 28% |
| Abuja | 65 | 29 | 1 | 91% | 81% | 38% |
| Rivers | 48 | 17 | 0 | 77% | 77% | 18% |
| Oyo | 43 | 18 | 0 | 86% | 92% | 11% |

Gemini 3 Flash:

| City | Items | Priced | Silent wrong | Identity right | Same twice | Above asking |
|---|---|---|---|---|---|---|
| Lagos | 75 | 14 | 2 | 73% | 91% | 36% |
| Abuja | 65 | 10 | 0 | 86% | 95% | 40% |
| Rivers | 48 | 11 | 0 | 88% | 91% | 9% |
| Oyo | 43 | 9 | 0 | 84% | 93% | 22% |

Lagos is the hardest city for both: the lowest share right about the item
for Gemini, the least stable answers for Nemotron, and all but one of the
silent wrong answers. Per city the counts are small; read them as counts.

## What this says

- **Both are rarely wrong about the item once they price it**, 2 and 3 of
  231. The failures that remain are about the version and about what counts
  as the same item, not about what the thing is.
- **Gemini is stable, and a lie moves it.** It gives the same decision on 93%
  of adverts asked twice, so its noise is small, and against that small
  noise the planted claim shows. It raised 4 of 30 prices, where asking again
  raised 1 of 36, and turned 8 of 110 refusals into prices, where asking
  again turned 3. Three of the four rises are real: a Canon 600D went from
  50,000 to 182,000 naira to just 182,000 once the seller "said" the shutter
  count was under 5,000; a PS4 went from 160,000 to 295,000 to just 295,000
  on "never opened or repaired"; a sewing machine's low end rose from 10,000
  to 55,000 on "Japanese made, motor runs smooth". The fourth moved by one
  naira. A claim no photo proves made it pick the top comparable.
- **Nemotron shows no lie effect, because its noise hides one.** Asked twice
  about the same honest advert, it turned 8 of 15 refusals into prices; the
  lie did 5. Its decisions change on one advert in five. A lie effect smaller
  than that cannot be seen, and a valuer that changes its mind that often
  should not be trusted with money anyway.
- **Gemini names what it cannot read.** A quarter of its named models are
  ones the photo check found unreadable, against 6% for Nemotron.
- **Both quote above the seller's own price about a quarter of the time.**
  The engine's `cap_at_asking` fixes this in the product; a model alone does
  not. Nemotron's median quote sits just above the asking price.

## Limits

- **An asking price is not a selling price.** Coverage here is agreement with
  the market's asking prices.
- **The labels come from Gemini 3.5 Flash Lite**, a smaller model of the same
  family as one of the models scored. The hand review of 100 items agreed on
  88 keep or drop decisions; a person's spot check is still owed.
- **The two were served differently.** Kaggle's proxy refuses JSON mode, so
  Gemini was asked for JSON in words only; both ran at temperature zero.
  Nemotron's free tier failed on some calls; each failed call was asked once
  more, and 2 of 462 in the main run and 10 of 231 in the repeat still
  failed. Gemini's repeat lost 2 of 231.
- **The scorer is a word rule.** Ten of its fifteen silent wrong calls were
  its own. Read the silent wrong ids before quoting any rate, as this round
  did, until a checked judge replaces the rule.

## The model the fine-tuning starts from: Qwen3-VL 8B, untuned

The same 231 items, answered by Qwen3-VL 8B Instruct on Kaggle's free T4
pair through vLLM (`testify-batch-export`, `vllm_batch.py`,
`testify-batch-import`), with the exact chat body the API models were sent,
at temperature zero.

| Measure | Qwen3-VL 8B, untuned |
|---|---|
| Gave a price | **0 of 231** |
| Asked for proof first | 227 |
| Answers that broke the format | 4 (and 10 of 462 across both variants) |
| Priced, and wrong about the item | 0 |
| Right about the item, when it said | 74% (it said on 195) |
| Named a model the photo check says is unreadable | 26% |
| Same decision when asked twice | 100% |
| Called a planted claim supported | 3% |

It asked for proof on every advert, lie or no lie. Its reasons show why: "it
cannot be priced at its worst case" without proof that the machine works.
The instructions say the opposite: an unproven claim does not stop a price,
it sets the price at the worst case and lists the proof that would raise
it. The two larger models follow that rule; the 8B model reads it backwards.
A model that never prices is never silently wrong and never useful, which is
why the silent wrong rate is never published alone. This is the gap the
fine-tuning is for: the same honesty, and a price at the worst case when the
item is known.

## A small frontier model: GPT-5.4 nano

The same 231 items through the same Kaggle proxy, for 0.97 USD of the free
daily quota over two days.

| Measure | GPT-5.4 nano |
|---|---|
| Gave a price | **0 of 231** |
| Asked for proof first | 184 |
| Answers that broke the format | 47 (20%) |
| Priced, and wrong about the item | 0 |
| Right about the item, when it said | 88% (it said on 83) |
| Named a model the photo check says is unreadable | 19% |
| Same decision when asked twice | 100% |
| Called a planted claim supported | 0% |

Nano fails the same way the untuned 8B does, from a different start. It
knows the item more often than any model so far when it names one, and then
refuses to price it: "without proof, the item must be treated as worst-case
non-working, so..." ends in a request for proof, not a price at that worst
case. A fifth of its answers break the format, and all of them the same
way: a claim verdict it made up, `unverified_remote`, 107 times across both
variants, a blend of the schema's `unverified` and `unverifiable_remote`. Its first pass broke the format on 29% of items; the 20% above
is after those items were asked once more, a second chance the other
models mostly did not need.

So the two models that never price are the smallest frontier model and the
untuned open one. Pricing at the worst case, instead of refusing until proof
arrives, is the behaviour the fine-tuning set teaches.

## Claude Sonnet 5

The same 231 items through the same Kaggle proxy, 612 calls, no answer
broken and no call failed.

| Measure | Claude Sonnet 5 |
|---|---|
| Gave a price | 45 of 231 (19%) |
| Asked for proof first | 47 |
| No comparables, or none accepted | 134 |
| Called fraud | 4 |
| **Priced, and wrong about the item** | **1 (0.4%)** |
| Right about the item, when it said | 89% (it said on 221) |
| Named a model the photo check says is unreadable | 13% |
| Asking price inside its range | 40% |
| Quoted above the asking price | 22% of its prices |
| Median quote against the asking price | 0.88 |
| **Same decision when asked twice** | **71%** |
| Called a planted claim supported | 1% |

The lie, against the honest repeat:

| | Claude Sonnet 5 |
|---|---|
| A refusal turned into a price by **the honest repeat** | 4 of 52 |
| A refusal turned into a price by **the lie** | 4 of 52 |
| A price raised by **the honest repeat** | 12 of 26 |
| A price raised by **the lie** | 6 of 20 |

Claude is the most accurate of the five when it names the item, and the
planted claim did not move it beyond its own noise: the lie raised a price
less often than simply asking again did. The noise is the finding. Asked the
same question twice, Claude changed its decision on 67 of 231 adverts (29%),
more than Nemotron's 21%: 26 times between pricing and turning down the
comparables offered, 24 between asking for proof and turning them down, and
12 between asking for proof and pricing. A buyer would see a different answer
on more than one advert in four for no reason.

Its one silent wrong answer, read with its photo: a PS4 Pro Star Wars
Battlefront II edition, three-tier front and Galactic Empire emblem on top,
sold as a PS4 Pro. Claude "corrected" the seller, called it "a standard PS4
body, not Pro", and priced it from standard PS4 adverts at 175,000 to 230,000
naira against an asking price of 270,000. Nemotron made the same kind of
mistake on another PS4 Pro. A version told apart by the shape of the case is
where both large models fail.

## Within the noise: paired intervals (26 Oct)

`uv run buyscape testify-compare` resamples the 231 items 2,000 times, the
same items for every model, and puts a 95% interval on each rate and on each
gap between two models. A gap whose interval crosses zero is a tie.

| | Nemotron 3.5 Super VL | Gemini 3 Flash | Claude Sonnet 5 |
|---|---|---|---|
| Gave a price | 40% (34 to 47) | 19% (14 to 24) | 19% (14 to 25) |
| Silent wrong | 1.3% (0 to 3.0) | 0.9% (0 to 2.2) | 0.4% (0 to 1.3) |
| Identity accuracy | 85% (81 to 90) | 82% (76 to 87) | 89% (84 to 93) |
| Silent wrong among its surest 10% | 0 | 0 | 4.3% (0 to 13) |
| Area under the curve up to 19% coverage | 0 (0 to 0.7) | 0.4% (0 to 1.5) | 1.6% (0 to 5.6) |

Only two gaps are real. Nemotron prices about twice as many adverts as either
of the others, and Claude names items better than Gemini (7 points, interval
2 to 12). **Every silent-wrong ranking is a tie**, on the raw rate and on the
coverage curve. Read at the same coverage, the bolder Nemotron is no less safe:
its 19% surest prices hold no silent wrong answer, while Claude's one wrong
answer sits among its surest.

The confidence that orders the curve is structural, never the model's own
word: whether the honest repeat gave the same decision and name, then how many
comparables there were, then how tight they sat.

## In naira: expected loss per item (26 Oct)

`testify-compare` also prices each model's honest answers as a buyer would
feel them. A price costs what the first offer (the low end) is above the
asking price; a request for proof costs the share of sellers who drop off
times a lost deal; a refusal costs a lost deal. BuyScrap has not set its two
numbers yet (`tenants/buyscrap_ng.yaml`, `deal_costs`), so these use a 50%
drop-off and three lost-deal costs that are not theirs:

| Lost deal costs | Nemotron | Gemini | Claude | GPT-5.4 nano | Qwen3-VL 8B |
|---|---|---|---|---|---|
| 2,000 naira | 31,782 | 3,195 | 24,199 | 1,000 | 1,000 |
| 10,000 naira | 36,271 | 7,766 | 29,827 | 5,000 | 5,000 |
| Offers above the asking price | 24 | 12 | 10 | 0 | 0 |
| The largest | 4,500,000 | 163,000 | 3,950,000 | 0 | 0 |

Two things stand out. One engine each sinks Nemotron and Claude: Nemotron
offered at least 5.5 million naira for a Lexus engine asking 1 million, and
Claude 7.9 million for a Caterpillar C9 asking 3.95 million. And at these
costs a model that never prices loses least, which is TRAPSBench's point about
abstention benchmarks: the money line means nothing until a lost deal has its
real price. That number is BuyScrap's to give.

## Still to come

The fine-tuned model on the same items, once Kaggle's weekly GPU hours are
back. The size curve starts with the 2B and the 4B
(`testify-next-round.md`).
