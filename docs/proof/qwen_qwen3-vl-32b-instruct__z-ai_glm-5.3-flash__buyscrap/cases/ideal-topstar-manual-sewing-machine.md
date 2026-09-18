# Case ideal-topstar-manual-sewing-machine

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  25912 ms

## What the engine saw
- Presentation: single_unit
- Category: sewing machine (confidence 0.95)
- Made of: steel 60%, plastic 30%, rubber 10%
- Estimated weight: 8.5 kg (confidence 0.7)
- Brand read off the item: IDEAL TOPSTAR
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

## OCR read off the photos
- IDEAL TOPSTAR
- DEN

## Chain
- **ocr** -> ok. 2 lines: IDEAL TOPSTAR | DEN
- **corroborate** -> dispute. brand_text agreed by both readers; 2 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=sewing machine brand=IDEAL TOPSTAR model=None label=True lines=2
- **retrieval** -> ok. query='IDEAL TOPSTAR IDEAL TOPSTAR Super Automatic Ideal Topstar manual sewing machine available ' hits=['Tecno Spark 10']
- **identify** -> ok. chosen=Ideal Topstar Super Automatic margin=None
- **abstain** -> pass. confidence=0.9 margin=None

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5233 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 10292 ms (replayed)
- identify on z-ai/glm-5.3-flash: 6845 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3542 ms (replayed)
- total across calls: 25912 ms; wall clock: 438 ms

## Identification
Shortlist from the catalogue:
  - Tecno Spark 10 (0.2)

**Answer: Ideal Topstar Super Automatic** (margin None)

## How sure the engine is (back office)
**90% sure this is a Ideal Topstar Super Automatic.**

- Identification confidence: 90% (certain)
- Price confidence: 0%
- It is weighing: Ideal Topstar Super Automatic (0.9)
- read off the item's own label
- 2 lines seen by both readers
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on a piece of paper and take one photo with the paper next to the item.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] One photo showing the whole item.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: this is needed before the price can be confirmed_

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
**NO_PRICE_DATA.** Only 0 comparable asking prices were found and there is no published band for this category, so no honest range can be produced. Nothing below the 2,847 NGN floor.

Conditions attached to this price:
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
