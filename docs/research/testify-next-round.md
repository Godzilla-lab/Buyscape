# Testify, next round: seven fixes from the review

A review of Testify and the fine-tuning plan on 25 Oct 2026 found seven
holes. Each one is real, and each one is something a lab reviewer would find
in the first page. This is the plan to close them, in the order they will be
done, with what each costs and who has to do it.

The short version: the headline number (a lie never raises the price) can be
won by a model that ignores sellers altogether, the prices are asking prices
and not settled ones, one number mixes the model with our crawler, the
rankings are within noise, there is no money metric, the training jumped
straight to a big run, and the word rules that judge identity keep making
mistakes. Nothing below changes the eight rules; it changes how we prove we
kept them.

## 1. Truth lift, paired with lie lift

**The hole.** Zero lie lift is the headline, and a model that never reads the
seller's words scores a perfect zero. The untuned Qwen3-VL 8B already shows
the shape of it: it never prices, so it is never wrong. Worse, the training
set as built only plants claims no photo can prove, so it could teach the
student exactly that: ignore what sellers say.

**The fix.** A third variant of every advert, with a planted claim that is
true and that a photo shows ("the plate reads 7kg", "it is a Hisense", "the
case is a PS4 Pro"). A model must use a claim it can check and stay still on
one it cannot. The two are reported as one pair:

| | Should be |
|---|---|
| Lie lift: price raised, or refusal turned into a price, by a claim no photo proves | 0 on every item |
| Truth uptake: a true, photo-shown claim marked supported and used (the name it gives, the comparables it picks) | as high as possible |
| Contradiction caught: a claim a photo disproves marked contradicted | as high as possible |

**How.**
- True claims come only from facts a photo carries: what the photo check
  (and the OCR, for codes) says is readable, matched to the title. A person
  checks a sample before any is used, and each claim records the photo that
  proves it.
- A contradicted variant comes from the same facts, changed ("the plate reads
  5kg" where it reads 7kg).
- The training set gets the same three twins: a lie listed as unverified, a
  true claim marked supported and used, a contradiction marked contradicted.
  This is the fix to the training set as much as to the benchmark.

**Cost.** Code and a sample check: free. The truth and contradiction variants
for each baseline: 462 more reads per model, about 10 to 15 USD of Kaggle's
free quota for each frontier model, free for Nemotron, about an hour of GPU
for the open model.

## 2. Real price truth for a small set

**The hole.** Every price in Testify is an asking price, which is a seller's
hope. The benchmark cannot say whether a range is calibrated until some items
have a price someone actually paid.

**The fix, two routes, both:**
- **BuyScrap's past deals.** The email is drafted in
  `docs/research/partnership-emails.md`. Fifty settled items with their photos
  are worth more than all 679 test items, because they are the only prices that
  are not hopes. **This needs you to fill in the bracketed parts and send it.**
- **A staged gold set** of 50 to 100 real items: bought or borrowed,
  photographed the way a seller would, then opened and tested. It is the only
  data where the hidden faults are certain, and the only place "price an
  unproven claim at its worst case" can be checked against what was inside.
  It costs a weekend and some naira. I will write the shot list, the test
  sheet and the record format so the weekend goes straight to photographing.

**What it unlocks.** Interval coverage against settled prices, the
calibration (rule 5) the plan has promised since day one, and a money metric
(point 5) on real money.

## 3. The model apart from the retrieval pool

**The hole.** Nemotron returned no price on 120 of 231 items, and most of that
is the comparables pool (729 adverts), not the model. Priced share mixes model
behaviour with our crawler's coverage.

**The fix.**
- **Freeze one comparables list per item**, retrieved for the item's true
  identity from the label, and give every model the same list at the pick
  step. The pick then compares models on picking alone.
- **Two tables, not one number.** The read stage: identity, claim verdicts,
  abstention, names beyond the photos, lie and truth on the read. The pick
  stage on the frozen lists: range coverage, quote against the asking price,
  lie lift on the price.
- The end-to-end run stays as a third, labelled line, because that is what a
  buyer would get.

**Cost.** Code: free. Picks are text only and cheap: a few USD of quota per
frontier model.

## 4. Statistically honest numbers

**The hole.** One, two and three silent wrong answers out of 231 are within
noise, and the scorecard ranks them.

**The fix.**
- **Paired bootstrap intervals** on every rate and on every difference
  between two models, resampling items, since every model saw the same items.
  Free, code only. A difference whose interval crosses zero is reported as a
  tie.
- **Three honest repeats, not one**, so stability is a distribution and not a
  coin flip. Two more passes per model: about 10 to 20 USD of quota per
  frontier model.
- **Human labels for all 231 dev items, two people, agreement published.**
  Today the labels come from Gemini 3.5 Flash Lite, and Gemini models are on
  the leaderboard: a conflict a reviewer will name in the first paragraph. The
  office app already has a sitting page; a labelling page on the same pattern
  shows one item at a time with the same checklist. About two to three hours
  for each person. **This needs you and one more person.** BuyScrap staff
  would be ideal.

## 5. A money metric

**The hole.** "Priced 40% with 3 wrong" and "priced 19% with 2 wrong" cannot be
compared without a cost model.

**The fix.** Expected loss in naira per item:
- **Overpayment** when the offer is above the true price. Until settled prices
  exist, the asking price stands in, and the table says so.
- **A lost deal** when the model refuses an item that was fine: a fixed cost
  per refusal, set by the tenant in `tenants/` (rule: tenant numbers never
  live in code).
- **Which number is the offer** is also the tenant's choice; the default is
  the low end of the range, since that is what a careful buyer offers first.

One number then folds coverage against caution, and it is the one a business
cares about. The fine-tuned model's target becomes plain: **lowest expected
loss, with lie lift at zero as a constraint.** **This needs you to set the
lost-deal cost**, or BuyScrap's number for what a missed pickup costs them.

## 6. The size curve first, on the 4B

**The hole.** The plan jumped to an 8B run that eats a Kaggle week. On 24 Oct
that run also showed how expensive the 8B is on a T4.

**The fix.**
- **Qwen3-VL 4B Instruct** (on Kaggle as
  `qwen-lm/qwen-3-vl/transformers/4b-instruct`) at three sizes: 500, 1,500 and
  all of the training set, in short runs. The 4B fits one T4, so two sizes can
  train at once, one on each card. Nobody has published this curve for a task
  like this; it also tells us whether more labels are worth buying.
- **The untuned 4B sits Testify first**, so each size is measured against its
  own starting point.
- **Split by photo hash and by seller.** Jiji sellers repost the same unit,
  sometimes across cities. Training already drops reposts of a benchmark
  photo; it will also drop any training advert from a seller who appears in
  the benchmark, and the held-out check will keep each seller on one side.
- **Relabel, do not drop.** Every teacher target the photos cannot support
  becomes an abstain target (Gekhman et al.: unknown items labelled "I don't
  know"), not a silent drop and not a guess. Today the set is 98% "price";
  this is also the fix for that.

**Cost.** GPU only. Rough sizes: the untuned 4B baseline about an hour, the
three runs about 1, 3 and 8 hours, each test sitting about an hour. About 15
hours, half a Kaggle week. The 8B run waits for the curve.

## 7. Adjudicated identity

**The hole.** In round three, ten of the fifteen "silent wrong" answers were
the word rules' mistakes, found only by reading. Word rules will keep doing
that.

**The fix.**
- The rules stay as a first pass. **Every answer a rule marks wrong goes to an
  adjudication file** (`eval/testify/adjudication.yaml`): the item, the
  answer, the verdict, who decided and why. The ten fixes already made are its
  first entries.
- **Wrong is split by kind:** wrong kind (a sofa called a bed), wrong version
  (a PS4 Pro called a PS4), wrong brand. They are different failures and are
  scored apart.
- **The file ships with the release**, so anyone can see each call and argue
  with it. I fill in a first reading; a person signs each one off.

## Order and who does what

| Order | Work | Who | Cost |
|---|---|---|---|
| 1 | Bootstrap intervals, adjudication file with the kind and version split, the two tables, the money metric | me | free |
| 2 | Truth and contradiction claims, built and sample-checked; training set rebuilt with three twins, abstain relabels and the seller split | me, then you for the sample | free |
| 3 | Truth and contradiction variants, two more repeats and frozen-list picks for the five baselines | me | about 40 to 60 USD of Kaggle's free quota, over the month |
| 4 | Untuned 4B baseline, then the 4B size curve | me | about 15 GPU hours |
| 5 | Human labels for the 231 dev items, two people | you and one more person | 2 to 3 hours each |
| 6 | BuyScrap email sent; staged gold set photographed and tested | you, with BuyScrap | a weekend and some naira |
| 7 | The 8B run, only if the curve says size helps | me | a Kaggle week |

Steps 1 and 2 start now and need nothing from anyone. Step 5 and step 6 can
start any time and are what turn Testify from an advert-reading benchmark
into a valuation benchmark.
