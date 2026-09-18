# Case scrap-car-metal-parts

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  63454 ms

## What the engine saw
- Presentation: mixed_lot
- Category: automotive parts (confidence 0.9)
- Made of: steel 60%, rubber 20%, copper_bare 10%, plastic 10%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: rust on metal surfaces, dirt and grime accumulation, some components appear worn or damaged
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type agreed by both readers
- **read_evidence** -> ok. category=automotive parts brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped
- **condition** -> not working. by the seller's own account

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 18486 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 39460 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 5508 ms (replayed)
- total across calls: 63454 ms; wall clock: 1379 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- This is a mixed lot, so it is priced by material and weight rather than identified.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] Two Drive Shafts (Axle Shafts) are available for sale.
- [unverifiable_remote] A Steering Rack (or Steering Gear) is available for sale.
- [unverifiable_remote] A Radiator (or Condenser) is available for sale.
- [unverifiable_remote] A Starter Motor is available for sale.
- [unverifiable_remote] The car parts are being sold as is, for parts, repair or recycling.
- [unverifiable_remote] Buyer is responsible for pickup.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**11,854 to 25,470 NGN** (priced as material, width 0.7296, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of steel 60%, rubber 20%, copper_bare 10%, plastic 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 19,800 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Two Drive Shafts (Axle Shafts) are available for sale. -> not proven remotely. Agent will confirm at pickup.
- A Steering Rack (or Steering Gear) is available for sale. -> not proven remotely. Agent will confirm at pickup.
- A Radiator (or Condenser) is available for sale. -> not proven remotely. Agent will confirm at pickup.
- A Starter Motor is available for sale. -> not proven remotely. Agent will confirm at pickup.
- The car parts are being sold as is, for parts, repair or recycling. -> not proven remotely. Agent will confirm at pickup.
- Buyer is responsible for pickup. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Scrap car metal parts', 'category': None, 'site_category': 'Iron', 'price_ngn': 80000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/scrap-car-metal-parts/'}`
