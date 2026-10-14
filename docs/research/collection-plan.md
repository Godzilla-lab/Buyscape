# Paid photo collection in Lagos

## The idea

Pay people in Lagos to photograph things they own, using the Buyscape seller
page. Then a BuyScrap agent checks a share of the items in person. This
produces the one kind of data that cannot be scraped: real Nigerian items, in
real seller-style photos, with **consent to publish** and, for the checked
share, **the true hidden condition**.

Scraped photos can only be released as links. Collected photos can be
released in full, which makes the benchmark far more useful to researchers.

## Size and cost

| Phase | Items | Pay per item | Agent checks | Cost |
|---|---|---|---|---|
| Pilot | 200 | ₦500 | 40 items at ₦2,000 | ₦180,000 |
| Main | 2,000 | ₦500 | 300 items at ₦2,000 | ₦1,600,000 |
| **Total** | **2,200** | | **340 checked** | **about ₦1.8 million** |

Convert at the day's rate before budgeting. Add about 10% for transfer fees and
repeats.

Optional bonus: ₦200 extra when the contributor also records the guided
30 second video, because video makes the hidden-risk proof checkable.

## What to collect: a mix across all four tiers

| Tier | Share | Examples |
|---|---|---|
| Branded electronics | 30% | phones, laptops, TVs, ACs, generators, routers |
| Small goods, no model number | 35% | torchlights, fans, irons, kettles, blenders, chairs, tools, power banks |
| Material lots | 25% | paper, carton, PET bottles, aluminium cans, copper wire, scrap metal |
| Items with something wrong | 10% | a known fault the contributor states privately to us |

The last row is important. A contributor who knows their fan's motor is dead
tells us privately, then photographs it like a normal seller. That gives
items whose hidden fault we know for certain, at no extra cost.

## How it works, step by step

1. **Sign-up.** The contributor reads the consent form below and agrees.
   We record their agreement, not their identity, against the session.
2. **Capture.** They open the seller page, pick a category, and follow its
   guided shots. That includes the handwritten code, so we know the photos are
   new and of this item.
3. **Private truth.** A short extra form asks what is wrong with the item, how
   old it is, and roughly what they paid. They know the seller page never sees it.
4. **Pay.** Payment goes out within 48 hours of an accepted session.
5. **Check.** For about 15% of items, chosen at random, a BuyScrap agent visits
   on a normal route. They power the item on, open what opens, weigh lots, and
   record the findings. That is the gold set.
6. **Settle where real.** If the contributor actually wants to sell, BuyScrap
   makes an offer. The settled price is the best label of all.

## Quality rules (a session is paid only if it passes)

- All required shots are present and not blurred. The seller page already
  measures sharpness.
- The handwritten code is legible in the code shot.
- The photos are not near-duplicates of another session. The seller page
  already computes perceptual hashes.
- The item matches the category chosen.
- One item per session. Up to 10 sessions per contributor in the main phase,
  so no single home dominates the data.

## Consent form (plain words, to translate into Pidgin and Yoruba too)

> **Help build fair prices for used goods in Nigeria**
>
> We will pay you ₦500 for photos of one item you own, taken with our
> guided page.
>
> - Your photos and the facts about the item may be **published** in an open
>   research dataset that anyone can use.
> - We will **not** publish your name, phone number, address, or your face.
>   Do not include people, documents or house numbers in the photos. We will
>   blur any that get in.
> - Your private answers (what is wrong with it, what you paid) are used to
>   test the AI and may be published without your name.
> - You can ask us to remove your photos at any time before publication by
>   contacting [email]. After publication we will remove them from future
>   versions.
> - You must own the item. Taking part does not oblige you to sell it.
>
> [ ] I agree.

This follows the Nigeria Data Protection Act 2023: consent, a stated purpose,
data minimised, and a right to withdraw. Have a Nigerian lawyer read it once
before the main phase.

## Privacy work before anything is published

- Blur faces, house numbers, and documents in frame. This can be automatic,
  with a person spot-checking.
- Keep only a hash of each IMEI and serial number.
- Strip location data (EXIF GPS) from every photo.
- Store contributor payment details separately from the photos, and delete
  them after payment.

## Small additions to the seller page

The page already has guided shots, the code shot, sharpness checks,
perceptual hashes, and a settled-price box. It needs:

1. A **consent** checkbox recorded in the session, with the form's version.
2. A **contributor mode** that shows the private truth form after capture
   and hides the offer.
3. An **inspection** form in the back office, where the agent records what
   they found.
4. An **export** to Testify items, with photos marked `public: true` only
   when consent is present.

Hosting the page so contributors can reach it is a deploy and needs an
explicit yes first.

## Timeline

| Week | Work |
|---|---|
| 1 | Build the four additions. Lawyer reads the consent form |
| 2 | Pilot: 200 items from people BuyScrap already knows |
| 3 | Fix what the pilot shows. Check 40 items in person |
| 4 to 8 | Main phase: 2,000 items, 300 checked |
| 9 | Privacy pass, then release with the benchmark |

## How we will know it worked

- At least 90% of pilot sessions pass the quality rules.
- In-person checks agree with the contributor's private answers at least 80%
  of the time. Where they disagree, the agent's finding is the label.
- At least 300 items in the gold set, across all four tiers.
