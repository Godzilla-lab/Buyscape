# Case ideal-topstar-manual-sewing-machine

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  22925 ms

## What the engine saw
- Presentation: single_unit
- Category: sewing machine (confidence 0.95)
- Made of: steel 60%, plastic 30%, rubber 10%
- Estimated weight: 8.5 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dusty surface, stains on body, worn plastic cover, foot pedal appears intact but aged
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: IDEAL TOPSTAR | Super Automatic

## Two readers
- brand_text agreed by both readers
- 2 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; 2 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=sewing machine brand=IDEAL TOPSTAR model=None label=True lines=2
- **grounding** -> dropped. brand
- **forensics** -> flag. the reader stated brand it could not point to in the photos
- **retrieval** -> ok. query='IDEAL TOPSTAR Super Automatic Ideal Topstar manual sewing machine available for sale. Loca' hits=['Tecno Spark 10']
- **identify** -> ok. chosen=IDEAL TOPSTAR Super Automatic margin=None
- **abstain** -> pass. confidence=0.45 margin=None

## Identification
Shortlist from the catalogue:
  - Tecno Spark 10 (0.2)

**Answer: IDEAL TOPSTAR Super Automatic** (margin None)

Evidence flags: the reader stated brand it could not point to in the photos

## How sure the engine is (back office)
**Not sure enough to price: 45% on the best answer. It is probably a IDEAL TOPSTAR Super Automatic, and the photos cannot separate them.**

- Identification confidence: 45% (unsure)
- Price confidence: 0%
- It is weighing: IDEAL TOPSTAR Super Automatic (0.9)
- read off the item's own label
- 2 lines seen by both readers
- the reader stated brand it could not point to in the photos
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] Ideal Topstar manual sewing machine
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] manual sewing machine
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] available for sale
- [unverifiable_remote] Location: Ikorodu, Lagos State
- [unverifiable_remote] Price: 10,000 naira
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**974 to 3,604 NGN** (priced as material, width 1.1487, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3422 for unproven claims.

Scrap floor: 2,847 NGN

Conditions attached to this price:
- Evidence flag: the reader stated brand it could not point to in the photos
- Ideal Topstar manual sewing machine -> not proven remotely. Weigh on the scale and photograph the display.
- manual sewing machine -> not proven remotely. Weigh on the scale and photograph the display.
- available for sale -> not proven remotely. Agent will confirm at pickup.
- Location: Ikorodu, Lagos State -> not proven remotely. Agent will confirm at pickup.
- Price: 10,000 naira -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Ideal topstar manual sewing machine', 'category': None, 'site_category': 'Industrial Machines', 'price_ngn': 10000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/ideal-topstar-manual-sewing-machine/'}`
