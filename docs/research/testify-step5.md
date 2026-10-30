# Testify, step 5: the new tests on the baselines

Status on 29 October 2026: part done. Every number here is on the 231 dev
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
| Claude | 44% | **78%** | 96% | 81% |
| nano | 39% | **70%** | 91% | 81% |

No model took the false name into its answer. When one step reports only
what the photos show, the judge can check a claim against it, and true claims
stop being ignored. nano and Claude catch fewer false claims that way.
Judged apart, Claude prices more (32% against 19%) and a lie moves its price
about half as often (16% against 30%), the same pattern as Nemotron.

Nemotron is the first model through all three conditions:

| Nemotron | Read then pick | Judged apart | One call, fixed list |
|---|---|---|---|
| True claim used | 89% | 85% | **93%** |
| False claim caught | 100% | 93% | 100% |
| Called the lie supported | 4% | **0%** | 5% |
| A lie raised the price | 12% | **5%** | 14% |
| Gave a price | 40% | 50% | **71%** |
| Asking price inside the range | 43% | 48% | 49% |
| Offered above the asking price | 26% | 27% | **20%** |
| Priced answers the rules mark wrong, unread | 0 | 14 | 12 |

Judged apart is the honest one: the planted lie never wins and moves the
price less than half as often. One call prices most and closest, but a lie
moves its price most, and on the items with the label taken away it named
the hidden code 30% of the time, copied from the list. The rules' wrong
marks on both wait for a person: the witness names the item from the photos
alone, and the one call from its list.

Claude is the second model through all three (30 Oct):

| Claude | Read then pick | Judged apart | One call, fixed list |
|---|---|---|---|
| True claim used | 44% | **78%** | 41% |
| False claim caught | **96%** | 81% | **96%** |
| Called the lie supported | 1% | 1% | 2% |
| A lie raised the price | 30% | **16%** | 22% |
| Gave a price | 19% | 32% | **55%** |
| Asking price inside the range | **40%** | 33% | **40%** |
| Offered above the asking price | 22% | 27% | **21%** |
| Priced answers the rules mark wrong, unread | 1 | 9 | 9 |

The same pattern as Nemotron's. Judged apart, a lie moves Claude's price
about half as often and a true claim is used, at the cost of catching fewer
false ones. One call with a fixed list prices nearly three times as often
as read then pick, no less closely, and a lie moves it less than there,
though more than judged apart.

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
and it believes the planted lie almost half the time.

## The first training run: the 4B on 500 adverts (29 Oct)

One pass over `sft_500` (1,296 examples, 48 of them the price step) on a
team member's Kaggle T4 pair: 130 steps in 2.8 hours, held-out loss 1.77 to
0.63. Then the same 231 items, read then pick.

| | Untuned 4B | Trained 4B | Nemotron | Claude | Gemini |
|---|---|---|---|---|---|
| Gave a price | 0.9% | **68%** | 40% | 19% | 19% |
| Asking price inside the range | | **10%** | 43% | 40% | 34% |
| Asking price far outside the range | | 32% | 11% | 18% | 7% |
| Offered above the asking price | | **48%** | 26% | 22% | 27% |
| A lie raised the price | | 9% | 12% | 30% | 13% |
| Called the lie supported | 2% | **0%** | 4% | 1% | 3% |
| Right about the item, when it said | 81% | 68% | 85% | 89% | 82% |
| Said it cannot tell | 23 | 0 | | | |
| Expected loss per item, naira | 1,100 | **226,331** | 31,782 | 24,199 | 3,195 |

It failed, and the failure is in the recipe, not the model:

- **The price target aimed at the asking price.** The target was the
  adverts either side of the advert's own asking price. The model never sees
  that price, so it learned to aim at it, and half its offers land above
  it. A buyer's target is the worst case: the cheapest matching advert as the
  offer, and a high end that reaches the asking price. That is what Nemotron
  does (its offer sits at 0.8 of the asking price, the trained 4B's at 1.0).
- **It never learned to refuse a list.** "None of these is the same item"
  was left out of the targets for fear of teaching false refusals. Nemotron
  refuses 50 lists; the trained 4B none, so a wrong name prices from wrong
  adverts.
- **It never learned to decline.** The read targets are 98% "price" and 19
  of 2,288 "cannot identify", so it now prices everything and never says it
  cannot tell. It also drops model numbers ("Sony console"), learnt from
  targets where an unconfirmed code was cut.
- **48 price examples are too few** to teach a pick against 1,248 reads.

What holds: it never believed a lie. The word rules mark 30 of its priced
answers wrong; they wait for a person, but the price numbers above stand
whatever they show.

The next run changes the recipe before the size: the worst case as the
price target, refusals of lists that do not match, a balance of decisions in
the reads, and more second-hand adverts for the price step.

## The second training run: the fixed recipe (29 Oct)

The same 4B, one pass over the rebuilt `sft_500` (1,655 examples from the
same 500 adverts, 553 of them the price step: the worst case as the target,
one list in six for another kind to refuse, new stock capped at one advert
per second-hand one), on the same T4 pair: 146 steps in 3.0 hours,
held-out loss 2.22 to 0.47.

| | Run 1 | Run 2 | Nemotron | Claude | Gemini |
|---|---|---|---|---|---|
| Gave a price | 68% | 64% | 40% | 19% | 19% |
| Typical offer, against the asking price | 1.00 | **0.75** | 0.80 | 0.78 | 0.86 |
| Offered above the asking price | 48% | **26%** | 26% | 22% | 27% |
| Asking price inside the range | 10% | 17% | 43% | 40% | 34% |
| Asking price far outside the range | 32% | 37% | 11% | 18% | 7% |
| Lists refused as another item | 0 of 310 | **30 of 330** | | | |
| A lie raised the price | 9% | 17% | 12% | 30% | 13% |
| Called the lie supported | 0% | 1% | 4% | 1% | 3% |
| Right about the item, when it said | 68% | 70% | 85% | 89% | 82% |
| Expected loss per item, naira | 226,331 | **70,661** | 31,782 | 24,199 | 3,195 |

The fix half worked. The offer moved to the worst case: the typical offer
fell from the asking price to three quarters of it, offers above the asking
price halved to Nemotron's rate, and the model now refuses a list that is
another item. The money lost per item fell by more than two thirds. It is
still twice Nemotron's loss and twenty times Gemini's, for three reasons:

- **It still prices too much.** Its reads say "price" for 227 of 231 items,
  as in run 1, because the read targets are 99% "price". It prices 117 of
  its 300 answers on the kind alone ("motorcycle"), from adverts for any
  motorcycle: a bike asking 280,000 offered 1,500,000.
- **Its range is one advert.** 219 of its 300 picks name the same advert
  for both ends, against a third of the targets, so the asking price is
  rarely inside the range.
- **The target leans on a price the model never sees.** The low end skips
  matches under half the asking price, and the high end is the first match
  at or above it. The model cannot see the asking price, so it learns the
  habit, not the rule, and now and then skips far past the cheapest advert
  (a Nikon D3300 asking 380,000 was offered 1,600,000, the dearest advert on
  a list that started at 100,000).

Most of the money is lost on items it named right (254 of its 300 priced
answers), so the pick, not the name, is what to fix next. The word rules
mark 26 of its priced answers wrong; they wait for a person.

## Which price target to teach: a free check (29 Oct)

Before the third run, each candidate target was tried on the lists the
models were actually shown, for the items they named right, and scored
against the asking price. The rules see only the list, as the student does;
"same item" is the scorer's title rule.

| On run 2's lists, 138 items | Offered above asking | Far outside | Asking inside | Overpaid per item, naira |
|---|---|---|---|---|
| Run 2's own picks | 25% | 40% | 16% | 80,609 |
| Cheapest match, middle match on top | **20%** | **23%** | **38%** | **69,986** |
| The same, skipping matches under half the middle | 40% | 36% | 18% | 356,471 |
| The second run's rule, which reads the asking price | 28% | 10% | 56% | 76,399 |

| On each model's own lists | Its own picks: far outside | overpaid per item | Cheapest match: far outside | overpaid per item |
|---|---|---|---|---|
| Nemotron, 136 items | **11%** | **51,625** | 23% | 65,816 |
| Gemini, 81 items | **7%** | **5,852** | 15% | 29,323 |
| Claude, 75 items | **18%** | 70,200 | 26% | **48,800** |

The best rule beats run 2, but Nemotron's and Gemini's own picks beat
every rule (Claude's land far off less often, and overpay more): a rule
cannot tell which adverts on a list are the same item, and a good model
can. Even the rule that reads the asking price, which no student can,
offers above it 28% of the time. So the third run learns a teacher's own
pick from the list (`taught_pick`): the pick step sends text only, so any
strong model can teach it, and Nemotron does so for free. The asking price
only chooses which of the teacher's picks to learn from (none that offers
above it, none whose high end is under half of it), never what they are.

The same check settled the read. Gemini, the model that loses least, prices
47 of the 54 branded items it names to the model, 6 of the 26 it names by
brand alone and 2 of the 13 it names by kind; the build had been turning
every one of its teacher's reads into a price. In the third run's set, a
branded advert named without its model asks for the label instead.

## Still running

Gemini's, Claude's and nano's remaining conditions, and pushback and
pressure for the Kaggle models, wait on Kaggle's model quota: both accounts
ran out on 29 Oct.
