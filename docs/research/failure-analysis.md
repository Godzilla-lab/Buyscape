# Reading 100 cases by hand: what goes wrong

Before scoring any model, we read 100 benchmark items photo by photo. This is
what a careful benchmark builder does first: it shows whether the data
measures what it claims to, and it names the ways a valuation goes wrong.

## How it was done

- **Which items:** 100 from the `dev` split only, so the `test` split stays
  unseen. All 18 BuyScrap adverts with photos, all 34 scrap and material lots,
  and 48 small goods spread across the kinds. The 178 phone, laptop and
  appliance cases were not included: their photos are not on this machine.
- **Who read them:** five Claude reviewers, 20 items each, with one fixed
  checklist. **These are AI reviews, not human labels.** A person should
  spot-check them and the agreement should be measured before they are cited
  as ground truth.
- **Output:** `eval/testify/review_dev.yaml`, one entry per item.
  `testify-convert` attaches each review to its item, and a dropped item gets
  an `exclude` reason so scoring skips it.

## The headline numbers

| Finding | Count of 100 |
|---|---|
| Dropped from the benchmark | **49** |
| Labels needing a fix (tier, kind or answer key) | **71** |
| Looks like new dealer stock, not second-hand | **47** (only 39 clearly used) |
| Title fully matches the photos | 59 (38 partly, 2 no) |
| Brand and model readable from photos alone | 25 (74 only by type, 1 unknown) |
| Photos carrying a shop watermark | 76 |

By source:

| Source | Reviewed | Kept |
|---|---|---|
| BuyScrap, the tenant's own adverts | 18 | **18** |
| Jiji, fetched by search | 82 | **33** |
| Jiji items labelled `material_lot` | 35 | **6** |

**The tenant's own data is clean. The scraped Jiji data is not.** Fewer than
half of the Jiji items survive, and the material tier from Jiji is almost all
wrong: of 35 "scrap lots", the review found machines, new packaging, new
books, a sculpture and waste bins.

## What would make an AI value an item wrongly

Each reviewer named the most likely failure for each item. Grouped by
keyword (an item can fall in more than one group):

| Failure | Items |
|---|---|
| New dealer stock passed off as used, so a new retail price looks like a used one | 35 |
| A wrong kind or tier label sends pricing to the wrong market (a baling press priced as scrap metal, waste bins as scrap tyres, a shredder as waste paper) | 31 |
| A claim in the title or text the photos cannot show (engine code, tank capacity, panel wattage, a games bundle) | 22 |
| Unit of sale: one piece against a set, a pack, a pair or a van load | 22 |
| The photo is not the seller's item: a catalogue image, a stock cover, a generated graphic, a web thumbnail of a different laptop | 16 |
| Faulty or e-waste priced as working | 12 |
| A local reprint, clone or third-party part priced as the original | 7 |
| A buyer's "we buy" advert read as a sale | 4 |

Two seller texts were contradicted by their own packaging: a torch sold as 10W
whose pack says 6W, and a shredder sold as 10 sheets whose box says 5. These
are natural "lie" items for the trick tier.

## What this changes

### In the data, fixed now
- **Photos were thumbnails.** Every Jiji photo was about 300 pixels wide, too
  small to read a plate. The fetcher now takes the largest size an advert
  lists, and a refetch upgrades photos already cached.
- **49 dev items no longer count** in scoring, each with its reason kept.
- **47 adverts tagged "used" are marked not used**, whatever the seller's tag said.

### In the data, still to do
- **The remaining Jiji items have the same problems.** Expect only about 40%
  of them to survive. Every item needs this kind of check before scoring,
  including the test split. Checking labels is allowed on the test split;
  tuning models on it is not.
- **Labels must come from the photo, not the search word.** The tier and kind
  came from the phrase that found the advert, which is why "copper" in a grill
  brand became copper wire. A labelling pass should replace them.
- **Material lots should come from recyclers and BuyScrap, not Jiji.** Jiji
  scrap search returns buyers, machines and new packaging.

### In the engine and its protocols
- **Ask the unit of sale.** "Is the price for one, a pair, or the lot? How many?"
  belongs in every protocol's questions.
- **An item filed as e-waste is not working** until a clip shows it working.
- **A watermark, several identical units or a studio background** is a
  signal of dealer stock, and should lower trust that an item is second-hand.

### In the benchmark design
- The tenant's adverts are the cleanest source. More of them, through the
  BuyScrap past-deals request, beats more scraping.
- The failure groups above become the benchmark's **error categories**: every
  model's mistakes will be counted under them, not just as "wrong".

## Can a model do this check? Agreement on the same 100

Gemini 3.5 Flash Lite answered the same checklist for the same 100 items
(`buyscape testify-label`), at about 5 seconds and 0.4 cents an item at list
price. Agreement with the review, item by item:

| Check | Agreement |
|---|---|
| Is the photo a stock or catalogue image | 95 of 100 |
| Is it really second-hand | 86 of 100 |
| Brand and model readable, or only the type | 76 of 100 |
| Does the title match the photos | 69 of 100 |
| Keep or drop, by each reviewer's own vote | 66 of 100 |
| **Keep or drop, by the same rule applied to both** | **88 of 100** |

The votes disagreed because both reviewers broke their own rule. Gemini
judged an advert to be dealer stock and kept it anyway 33 times; the hand
review did the same 12 times. So the decision no longer comes from a vote.
It comes from the facts by one rule (`src/buyscape/testify/rules.py`): new
stock, a photo that is not the seller's item, or a buyer's advert means drop.

Of the 12 remaining disagreements, 11 are items the review drops and Gemini
keeps, mostly bookshop stock it takes for used. So the model check is a
little lenient: it should be spot-checked by a person before it is trusted
on the test split.

## Lagos, checked in full

Every Lagos item with photos here was checked the same way on 16 Oct 2026,
on the sharp photos (`buyscape testify-label --market lagos`). The same rule
decides. Free on the Google AI Studio free tier; it would cost about 3 dollars
at list price.

| Lagos | Items |
|---|---|
| Checked | 722 |
| **Kept** | **331** (46%) |
| Dropped as new stock | 356 |
| Dropped as a buyer's advert or a service | 16 |
| Dropped because the photo is not the seller's item | 14 |
| Dropped for other reasons in the hand review | 5 |
| Not checked: no photos on this machine | 186 |

Of the 331 kept, 40 are BuyScrap's own adverts and 291 are Jiji. Only 5 Jiji
material lots survive, which confirms that material lots must come from
recyclers and BuyScrap. The 186 unchecked are the 178 original phone, laptop
and appliance cases, whose photos are only on the machine that fetched them,
and 8 BuyScrap adverts with no photos at all.

The keep or drop agreement with the hand review is still 88 of 100 after the
photos were sharpened.

## Next step

Check every remaining item the same way, measure how often an AI reviewer
agrees with a human on a sample of 30, and only then score models.
