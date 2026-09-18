# Case scrap-electric-standing-fan

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0013  |  65912 ms

## What the engine saw
- Presentation: single_unit
- Category: fan (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 5.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: dusty, grime on central hub, some rust on metal parts
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type agreed by both readers
- **read_evidence** -> ok. category=fan brand=None model=None label=False lines=0
- **retrieval** -> ok. query='Description: This is a scrap electric standing fan that is currently not functioning prope' hits=['Google Pixel 7']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused
- **condition** -> not working. by the seller's own account

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 11521 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 16765 ms (replayed)
- identify on z-ai/glm-5.3-flash: 31061 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 6565 ms (replayed)
- total across calls: 65912 ms; wall clock: 3209 ms

## Identification
Shortlist from the catalogue:
  - Google Pixel 7 (0.2)

**Not identified: CANNOT_IDENTIFY.** Item is a generic standing fan with no legible brand or model markings; the only shortlist entry (Google Pixel 7) is clearly not this item.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 16%
- Item is a generic standing fan with no legible brand or model markings; the only shortlist entry (Google Pixel 7) is clearly not this item.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] This is a scrap electric standing fan
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] It is currently not functioning properly
    priced as: assumed not working. Agent powers the item on before payment
- [unverifiable_remote] It is being sold as is for parts or recycling
- [unverifiable_remote] Buyer is responsible for pickup
- [unverifiable_remote] Location: Oshodi, Lagos State
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**1,995 to 8,570 NGN** (priced as material, width 1.2447, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 5 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 6,650 NGN

Conditions attached to this price:
- Not identified: Item is a generic standing fan with no legible brand or model markings; the only shortlist entry (Google Pixel 7) is clearly not this item.
- This is a scrap electric standing fan -> not proven remotely. Weigh on the scale and photograph the display.
- It is currently not functioning properly -> not proven remotely. Agent powers the item on before payment.
- It is being sold as is for parts or recycling -> not proven remotely. Agent will confirm at pickup.
- Buyer is responsible for pickup -> not proven remotely. Agent will confirm at pickup.
- Location: Oshodi, Lagos State -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Scrap Electric Standing Fan', 'category': None, 'site_category': 'E-waste', 'price_ngn': 0, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/scrap-electric-standing-fan/'}`
