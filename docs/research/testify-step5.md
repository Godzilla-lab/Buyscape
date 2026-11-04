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
| nano | 44% | **70%** | 92% | 81% |

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

GPT 5.4 nano is the third (1 Nov), and the conditions barely matter for it,
because it almost never prices:

| nano | Read then pick | Judged apart | One call, fixed list |
|---|---|---|---|
| True claim used | 44% | **70%** | 44% |
| False claim caught | **92%** | 81% | 84% |
| Called the lie supported | 0% | 1% | 0% |
| Gave a price, clean items | 0% | 0% | 0.4% (one item) |
| Asked for proof | 80% | 54% | 71% |
| Broke the answer format | 20% | 12% | 18% |

It asks for proof on most items whatever it is shown, and one answer in
five breaks the format. That is safe, never wrong about money, and useless
to a buyer: a model that never prices cannot lose and cannot buy.

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
- **Pushback, Claude, 198 items (31 Oct):** the same. No answer flipped to
  believing the lie and none unlocked a price; the price rose on 14% of
  items, against 46% between two honest runs (Claude prices few items
  twice, 26, so its noise is wide).
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
strong model can teach it. Gemini taught it, the model whose own picks lose
least; Nemotron, free but rate-limited after a day's reads, answered too
few in time. The asking price
only chooses which of the teacher's picks to learn from (none that offers
above it, none whose high end is under half of it), never what they are.

The same check settled the read. Gemini, the model that loses least, prices
47 of the 54 branded items it names to the model, 6 of the 26 it names by
brand alone and 2 of the 13 it names by kind; the build had been turning
every one of its teacher's reads into a price. In the third run's set, a
branded advert named without its model asks for the label instead.

## The third training run: a teacher's picks (30 Oct)

The same 4B on `sft_r3`: 526 adverts and 1,849 chats, every advert that
teaches the price step first. 303 Gemini picks with their lied-to twins
(Gemini answered all 549 training lists, found no matching advert on 178,
and 68 of its picks were left out for offering above the asking price or
falling far under it), 68 lists for another kind to refuse, and reads that
ask for the label on 24% of adverts. Dealers' new stock teaches the pick
too. One full pass on the same T4 pair: 220 steps in 4.7 hours, held-out
loss 2.32 to 0.42.

| | Run 2 | Run 3 | Nemotron | Claude | Gemini |
|---|---|---|---|---|---|
| Gave a price | 64% | 65% | 40% | 19% | 19% |
| Typical offer, against the asking price | 0.75 | 0.74 | 0.80 | 0.78 | 0.86 |
| Offered above the asking price | 26% | 23% | 26% | 22% | 27% |
| Asking price inside the range | 17% | **49%** | 43% | 40% | 34% |
| Asking price far outside the range | 37% | 15% | 11% | 18% | 7% |
| A lie raised the price | 17% | **12%** | 12% | 30% | 13% |
| Called the lie supported | 1% | **0.4%** | 4% | 1% | 3% |
| Lists refused as another item, both twins | 30 | 18 | 92 | 71 | 72 |
| Right about the item, when it said | 70% | 78% | 85% | 89% | 82% |
| Priced answers the rules mark wrong, unread | 26 | 13 | | | |
| Expected loss per item, naira | 70,661 | **55,208** | 31,782 | 24,199 | 3,195 |

It worked on the pick and not yet on the money. Its range now holds the
asking price more often than any model's, it lands far off less than half
as often as run 2, a lie moves its price no more than Nemotron's, and on its
own lists its picks now beat every rule (58,073 naira overpaid per item
against 78,014 for the best rule; run 2's lost to the rules). The money
lost per item fell by a fifth, but it is still about twice Nemotron's and
Claude's, and seventeen times Gemini's.

The money is in a few items. Three carry 64% of what it overpays: the
Caterpillar engine Claude also overpays on (offered 7,900,000 against an
asking price of 3,950,000), a Lumix camera offered 4,000,000 against
600,000, and a motorcycle offered from dearer bikes. What Gemini does that
the student does not is decline: it prices 19% of items, the student 65%.
Its reads still say "price" for 222 of 231 clean items, asking mostly when
a seller makes a claim (22 of the lied-to items). And the 178 lists Gemini
refused taught nothing: only lists of another kind are taught as
refusals, so a list of dearer bikes for a cheap one is never refused.

## The fourth training run: the teacher's refusals (31 Oct)

Run 3 learnt Gemini's picks but never its refusals, so the 178 training
lists Gemini turned down were taught as nothing. In `sft_r4` they are taught
as refused, for the advert and its lied-to twin: 957 adverts and 3,299
chats, every advert that teaches the price step first (303 picks, 178
refusals, 119 lists of another kind), reads that ask for the label on 31%
of adverts. The same set trains both sizes, each on its own team account's
T4 pair, so the size curve and the recipe are read on the same data.

The 2B came first: one full pass, 389 steps in 3.8 hours (4.3 seconds a
chat, half the 4B's), held-out loss 2.40 to 0.46.

| | Untuned 2B | Run 3, 4B | **Run 4, 2B** | Nemotron | Claude | Gemini |
|---|---|---|---|---|---|---|
| Gave a price | 0% | 65% | **30%** | 40% | 19% | 19% |
| Typical offer, against the asking price | | 0.74 | 0.75 | 0.80 | 0.78 | 0.86 |
| Offered above the asking price | | 23% | **16%** | 26% | 22% | 27% |
| Asking price inside the range | | 49% | **56%** | 43% | 40% | 34% |
| Asking price far outside the range | | 15% | 10% | 11% | 18% | **7%** |
| A lie raised the price | | 12% | **6%** | 12% | 30% | 13% |
| Called the lie supported | 47% | 0.4% | 0.4% | 4% | 1% | 3% |
| Lists refused as another item, both twins | | 18 | 111 | 92 | 71 | 72 |
| Asked for the label, clean items | | 6 | 43 | | | |
| Right about the item, when it said | 77% | 78% | 74% | 85% | 89% | 82% |
| Priced answers the rules mark wrong, unread | | 13 | 8 | | | |
| Largest overpayment, naira | | 3,950,000 | **250,000** | 4,500,000 | 3,950,000 | 163,000 |
| Expected loss per item, naira | 1,012 | 55,208 | **3,600** | 31,782 | 24,199 | 3,195 |

It worked. The 2B, the smallest model in the size curve, now loses about
as little money as Gemini, a seventh of what Claude loses and a ninth of
Nemotron, while pricing half again as many items as Gemini. Its range holds
the asking price more often than any model's, it offers above the asking
price least, and a lie moves its price least. The untuned 2B believed the
planted lie 47% of the time; the trained one almost never does.

Declining is what changed. It refused 111 lists where run 3 refused 18, and
asked for the label on 43 clean items where run 3 asked on 6. The items
that cost the others most it declined: the Caterpillar engine list (offered
at twice its asking price by Claude and run 3) it refused, and the Lumix
camera it asked a label for. On its own lists its picks overpay 4,429 naira
per item against 16,750 for the best rule. Its largest overpayment is a
gearbox at 900,000 against 650,000.

What it does worse: it is right about the item 74% of the time, under every
frontier model, and the word rules mark 8 of its priced answers wrong; they
wait for a person. Gemini still lands far off less often. These are dev
numbers on 231 items; the test split is untouched.

The 4B on the same set: one full pass, 389 steps in 8.0 hours, held-out
loss 2.36 to 0.41.

| | Run 3, 4B | Run 4, 4B | Run 4, 2B | Gemini |
|---|---|---|---|---|
| Gave a price | 65% | 41% | 30% | 19% |
| Offered above the asking price | 23% | 22% | **16%** | 27% |
| Asking price inside the range | 49% | 54% | **56%** | 34% |
| Asking price far outside the range | 15% | 12% | 10% | **7%** |
| A lie raised the price | 12% | 7% | **6%** | 13% |
| Called the lie supported | 0.4% | **0%** | 0.4% | 3% |
| Lists refused as another item, both twins | 18 | 102 | 111 | 72 |
| Asked for the label, clean items | 6 | 21 | 43 | |
| Right about the item, when it said | 78% | **78%** | 74% | 82% |
| Priced answers the rules mark wrong, unread | 13 | 8 | 8 | |
| Largest overpayment, naira | 3,950,000 | 1,050,000 | 250,000 | 163,000 |
| Expected loss per item, naira | 55,208 | 14,961 | **3,600** | 3,195 |

The refusals worked at both sizes: the 4B's loss fell to a quarter of run
3's, under Claude's and Nemotron's. But the bigger model is not the better
buyer here. It prices more items (41% to the 2B's 30%) and names them
better (78% to 74%), and loses four times as much, because it still prices
a few dear items the 2B refuses: the Caterpillar engine (5,000,000 offered
against 3,950,000 asked) and two motorcycles priced from dearer bikes carry
71% of its overpayment. On its own lists its picks overpay 23,388 naira per
item against 67,194 for the best rule.

The gap between the two sizes rests on those three items, out of 231, so
it is a direction, not a settled ranking. Both runs answer the dev split
only; the test split is untouched and is the place to settle it.

## The test split (31 Oct)

The four training runs were all read on the same 231 dev items, so the
better of the two run 4 models could simply fit them. The test split had
never been answered by any model: 679 items from Lagos, Abuja, Oyo and
Rivers, each clean and with a planted lie, the same recipe of reads then
picks.

| On 679 unseen items | Run 4, 2B | Run 4, 4B |
|---|---|---|
| Gave a price | 31% | 36% |
| Offered above the asking price | **14%** | 25% |
| Asking price inside the range | **52%** | 48% |
| Asking price far outside the range | 13% | **8%** |
| A lie raised the price | 6% | 6% |
| Called the lie supported | 0.8% | 0.8% |
| Right about the item, when it said | 74% | **77%** |
| Priced answers the rules mark wrong, unread | 20 | 26 |
| Largest overpayment, naira | **300,000** | 1,440,000 |
| Expected loss per item, naira | **3,873** | 11,301 |

The 2B holds up: on items it never saw it prices, picks and loses as it did
on dev (3,600 naira per item there). And it beats the 4B on money here too,
by about three times, with the gap spread wide, not carried by a few items:
the 4B offers above the asking price on 60 clean items to the 2B's 29, and
leaving out each one's three dearest the 4B still loses about four times as
much. The 4B names the item better and lands far off less often; the 2B is
the more careful buyer. Nemotron, Gemini and Claude answer the same test
items next, for the comparison that matters.

Nemotron, a 120B model, has now answered all 679 (1 Nov). Six of its
answers broke the answer format and count against it, as on dev; Gemini's
and Claude's wait for Kaggle's quota (Claude's is half done and left out
until it finishes).

| On 679 unseen items | Run 4, 2B | Nemotron 3.5 Super (120B) |
|---|---|---|
| Gave a price | 31% | **43%** |
| Asking price inside the range | **52%** | 43% |
| Offered above the asking price | **14%** | 25% |
| Priced answers the rules mark wrong, unread | **20** | 30 |
| Right about the item, judged | 94% | **97%** |
| Items overpaid | **29** | 73 |
| Largest overpayment, naira | **300,000** | 14,550,000 |
| Overpaid per item, naira | **2,560** | 54,059 |
| The same, leaving out each one's five dearest | **1,205** | 14,207 |
| Expected loss per item, naira | **3,873** | 55,602 |

On items no one tuned on, the 2B loses about a fourteenth of what Nemotron
loses per item, and about a twelfth with each one's five worst items left
out, so the gap is not one disaster: Nemotron offered above the asking price
on 73 items to the 2B's 29. Nemotron prices more items and names them a
little better; the 2B prices fewer but closer, and is the better buyer.
Nemotron's worst was ₦15 million offered for a 15kVA Stamford alternator
listed at ₦450,000.

Claude Sonnet 5 has now answered all 679 too (3 Nov; its last 35 waited a
night for Kaggle's quota), with no call unanswered. All three on the same
679 items:

| On 679 unseen items | Run 4, 2B | Nemotron (120B) | Claude Sonnet 5 |
|---|---|---|---|
| Gave a price | 30% | **43%** | 19% |
| Asking price inside the range | **52%** | 43% | 34% |
| Offered above the asking price | **14%** | 25% | 23% |
| Priced answers the rules mark wrong, unread | 20 | 30 | **6** |
| Right about the item, judged | 94% | 97% | **99%** |
| Items overpaid | **29** | 73 | **29** |
| Largest overpayment, naira | **300,000** | 14,550,000 | 1,500,000 |
| Overpaid per item, naira | **2,560** | 54,059 | 6,007 |
| The same, leaving out each one's five dearest | **1,205** | 14,207 | 1,284 |
| Expected loss per item, naira | **3,873** | 55,602 | 7,415 |

Claude names the item best and prices least: it gives a price on one item
in five, and when it does the asking price falls inside its range only a
third of the time. The 2B prices half again as many items, lands inside the
range half the time, and loses about half of what Claude loses per item.
With each one's five worst overpayments left out the two overpay about the
same, so the gap is Claude's few large misses (₦1.5 million and ₦752,000
over the asking price) and the items it would not price at all. Claude
breaks the rules least: six priced answers the rules mark wrong to the
2B's twenty.

## The fifth training run: every advert (1 Nov)

The 2B again, on `sft_r5`: every training advert, 1,443 (957 in run 4),
including 72 that a second teacher rescued (Nemotron re-read the 207
adverts Gemini named wrong and had not seen). One full pass, 528 steps in
4.75 hours, held-out loss 2.40 to 0.44.

| | Run 4 2B, dev | Run 5 2B, dev | Run 4 2B, test | Run 5 2B, test |
|---|---|---|---|---|
| Gave a price | 30% | 23% | 31% | 21% |
| Asked for the label, clean items | 19% | 54% | | |
| Offered above the asking price | 16% | 21% | 14% | 16% |
| Asking price inside the range | 56% | 58% | 52% | 56% |
| Asking price far outside the range | 10% | 4% | 13% | 14% |
| A lie raised the price | 6% | 16% | 6% | 6% |
| Right about the item, when it said | 74% | 74% | 74% | 75% |
| Priced answers the rules mark wrong, unread | 8 | 3 | 20 | 16 |
| Largest overpayment, naira | 250,000 | 250,000 | 300,000 | 550,000 |
| Expected loss per item, naira | 3,600 | **3,241** | 3,873 | 3,850 |

More data did not help on its own. On dev run 5 came within 46 naira of
Gemini, but on the 679 test items it loses what run 4 lost while pricing a
third fewer items: the same money for fewer deals. The extra adverts were
mostly reads, not price steps: the set grew by half, its price picks only
from 303 to 318, and most of the new adverts were branded ones named
without a model, which ask for the label. Asked on 37% of reads in the set,
the trained model asks on 54% of clean dev items. Reading did not move
either (74% to 75%). The dev gain was the dev items, which is why the test
split exists. (The lie figure on dev rests on 32 items priced both ways;
on test it is 6% for both.)

Run 4's 2B stays the one to build on: it prices half again as many items
for the same loss. What would move the price step is more priced
second-hand adverts with matching adverts to pick from, which more cities
bring, not more reads.

## Naming, judged: the same thing in other words (1 Nov)

The naming figure so far was a word rule: an answer had to carry the title's
own words. Sellers name things loosely and titles can be wrong, so "mountain
bike" for a "Bicycle", "car headlight" for a "Headlamp" and "multifunction
copier" for an old "Photocopier" all counted as wrong. The user's rule: the
answer does not have to use the seller's name for it, it has to name the
same thing.

A judge now reads every answer the word rule marks wrong, with the title,
the benchmark's kind and what the photo check saw, and decides right, or
wrong kind, brand or version (`buyscape testify-judge`, `testify/judge.py`).
It is MiniMax M3.1 on NVIDIA's free tier, a family that sits no Testify
table, fifteen answers to a call. A person's verdict always comes first.
Before it was used it was checked three ways:

| Check | Result |
|---|---|
| A person's verdicts from round 2 | agrees on 15 of 15 |
| Right answers moved to another kind's advert | calls 40 of 40 wrong |
| Answers moved to another advert of the same kind, with its own model | calls 38 of 40 wrong |

The first prompt called a "PS4" for a PS4 Pro wrong; the person had called it
right, as the less exact name for the same thing, and the engine of an
"engine, gearbox and wiring" bundle right too. The prompt now says less exact
is right unless it contradicts the advert (a PS4 Slim for a PS4 Pro stays
wrong). Mistral Large 4 and DeepSeek on the same free tier were too slow to
use. 1,143 answers judged: 881 right, 134 wrong kind, 65 wrong version, 63
wrong brand.

| Right about the item, when it said | Word rule, dev | Judged, dev | Word rule, test | Judged, test |
|---|---|---|---|---|
| Claude Sonnet 5 | 89% | **99%** | 85% | **99%** |
| Gemini 3 Flash | 83% | 98% | | |
| Nemotron 3.5 Super | 87% | 98% | 80% | 97% |
| GPT 5.4 nano | 88% | 98% | | |
| Qwen3-VL 8B, untuned | 75% | 94% | | |
| Qwen3-VL 2B, untuned | 77% | 93% | | |
| Qwen3-VL 4B, untuned | 81% | 98% | | |
| Run 4, 4B | 78% | 97% | 77% | 94% |
| Run 4, 2B | 74% | 95% | 74% | 94% |
| Run 5, 2B | 74% | 94% | 75% | 95% |

The gap was mostly the rule's. Judged, the run 4 2B trails the big models by
three to five points, not eight to fifteen. What it still gets wrong, on
both splits (50 answers):

- model numbers misread: a PSR-550 read as a PSR-350, a PSR-S910 as a PSR-S310,
  a PSR-175 as a PGR-173, the small digits of a plate at about 570 pixels;
- brands made up: Panasonic on an unbranded iron, Bosch on a BMX, Porsche on an
  Audi gearbox;
- the accessory for the item: a gamepad for a PS4 bundle;
- rare kinds it has not seen: a PET blowing machine called an injection
  moulder, a gearbox called a gear pump.

Most of these it did not price (no price data, or it asked for the label), so
they cost little money. Sharper photos, brands only when they show, and the
rare kinds from more cities are what run 6 would add.

## The sixth training run: the whole pool (4 Nov)

The 2B again, on `sft_r6`: 21,655 examples from 8,391 adverts, every advert
we hold. Qwen3-VL 32B read 7,775 crawled and searched adverts on a rented
A100 as the teacher (about $5), and the set carries 688 teacher price picks,
378 refusals and 4,593 price steps with no teacher pick. One pass, 2,573
steps: the first 1,760 on a rented A100 ($1.68), the rest on Kaggle from
its save point. Held-out loss 0.44, as run 5.

| | Run 5, dev | Run 6, dev | Run 5, test | Run 6, test |
|---|---|---|---|---|
| Gave a price | 23% | **36%** | 21% | **34%** |
| Asked for proof, items | 125 | **13** | 333 | **50** |
| Offered above the asking price | 21% | 19% | 16% | 21% |
| Asking price inside the range | 58% | **70%** | 56% | 54% |
| Asking price far outside the range | 4% | 11% | 14% | 15% |
| A lie raised the price | 16% | **4%** | 6% | 7% |
| Right about the item, word rule | 74% | 77% | 75% | 77% |
| Right about the item, judged | 94% | **97%** | 95% | **96%** |
| Named a model the photos do not show | | | 13% | **7%** |
| Priced answers the rules mark wrong, unread | 3 | 4 | 16 | 26 |
| Largest overpayment, naira | 250,000 | 570,000 | 550,000 | 2,850,000 |
| Expected loss per item, naira | **3,241** | 7,991 | **3,850** | 13,921 |

The read got better: judged naming is within three points of Claude Sonnet 5
(99%) and Nemotron (97%) on test, and it names a model the photos do not show
half as often (7%, Claude 6%, Nemotron 4%). It stopped asking for proof it
does not need, and on dev a planted lie raised its price on 4% of pairs.

The money got worse, almost all of it from one mistake. Half of the test loss
is three answers, and nearly every large one is a car engine or gearbox named
by type ("car engine", "automotive transmission or gearbox") and priced from
every engine or gearbox in the market: a Mark gearbox asked at 850,000 was
offered 3.7 million, Honda and Audi engines and gearboxes two to three times
their asking. Run 5 asked for the label on the same adverts. The training set
taught it: of its engine and gearbox reads, 630 name the kind only and 600 of
those go on to a price, while 16 name a make and model. A type-only name is
for items that carry no model (the answer schema says so); an engine carries
one, so without a readable code the right answer is to ask for it.

Had run 6 asked for the label on its 54 type-only engines and gearboxes, it
would lose about 4,720 naira per item: better than Claude (7,415), still worse
than run 5 (3,850). The rest is eagerness: it offers above the asking price
on 21% of its prices (run 5: 16%), most visibly on faulty or vintage items it
priced as working, and 4,593 of its price steps came with no teacher's pick.

Run 4's and run 5's 2B stay the ones to beat on money. Run 7, from what run 6
shows:

- engines, gearboxes and the other parts that carry a make and model are
  never priced on a type-only name in the training set: those reads teach
  asking for the label instead (protocol data, not code);
- a teacher's pick for the 4,593 price steps that have none (Claude Haiku
  5.5 through the Batch API, about $2, on the owner's yes);
- faulty and for-parts adverts priced at their worst case, as rule 3 asks.

## The seventh training run: a type-only name never prices a part with a model (4 Nov)

The fix is data. A new protocol, `protocols/vehicle_part.yaml`, says an engine
or gearbox sets its price by its code and is never priced by type, and the
training build now asks, on every advert, whether the kind a reader named
reaches a protocol that prices by model: if it does and no model is named, the
answer asks for that protocol's model shot instead of a price. Before, only
branded electronics that a photo check had seen got this, and the crawled
adverts had no photo check. Rebuilt, the set (`sft_r7`) changed 1,830
examples, mostly to asking for the label: laptops (804), engines and gearboxes
(about 400), air conditioners and washing machines.

Run 7 is run 6 taught on from its adapter (`sft_lora --init-adapter`) at half
the learning rate, on those 1,830 and 915 unchanged examples drawn at random.
The examples carry more photos than run 6's, so it ran at 6.4 seconds a chat
and stopped on Kaggle's time limit at step 286 of 325, the learning rate
already near zero; held-out loss 0.437.

| Test, 679 items | Run 5 | Run 6 | **Run 7** | Claude Sonnet 5 | Nemotron 3.5 Super |
|---|---|---|---|---|---|
| Gave a price | 21% | 34% | 22% | 19% | 43% |
| Asked for the label | 333 | 50 | 267 | | |
| Right about the item, judged | 95% | 96% | 95% | 99% | 97% |
| Named a model the photos do not show | 13% | 7% | **6%** | 6% | 4% |
| Asking price inside the range | 56% | 54% | 51% | 34% | 43% |
| Offered above the asking price | 16% | 21% | 19% | 23% | 25% |
| Priced answers the rules mark wrong, unread | 16 | 26 | 24 | 6 | 30 |
| Largest overpayment, naira | 550,000 | 2,850,000 | 1,250,000 | 1,500,000 | 14,550,000 |
| Expected loss per item, naira | **3,850** | 13,921 | 6,204 | 7,415 | 55,602 |

The engines are fixed: of the dev items whose kind reaches the new protocol,
run 6 priced 19 and asked on 1, run 7 prices 2 and asks for the code on 27,
and the gearbox and engine overpayments that made run 6's loss are gone from
the test list. Run 7 loses less than Claude Sonnet 5 and less than half what
run 6 lost, while naming as well as run 6. On dev it loses 5,203 naira per item (run 5
3,241, run 6 7,991).

It did not reach run 5, for two reasons the answers show:

- the lesson spread: on dev it also asks for the label on 65 items of kinds
  with no protocol of their own, where run 6 asked on 10, and each request
  costs a buyer half a deal;
- the price step still takes the top of a range: its largest loss is a Nikon
  DSLR asked at 350,000, named "Nikon" without a model, priced from the one
  matching advert at 1.6 million. Cameras have no protocol, so nothing made it
  ask for the model, and its pick ran from the dearest advert, not the
  cheapest.

Next, in the same spirit: protocols for the branded kinds that still have
none (cameras, game consoles, televisions, freezers), so they ask for the
model too, and teacher picks for the 4,593 price steps that have none, so the
pick learns to start at the worst case (Claude Haiku 5.5 through the Batch
API, about $2, on the owner's yes). Both go into one full retrain once
Kaggle's GPU hours reset on 7 Nov.

## Still running

Gemini's, Claude's and nano's remaining conditions, and pushback and
pressure for the Kaggle models, wait on Kaggle's model quota: both accounts
ran out again on 30 Oct.
