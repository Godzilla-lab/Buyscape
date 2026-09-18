# Case massive-scrap-lot-for-sale-in-rivers-state

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  95587 ms

## What the engine saw
- Presentation: single_unit
- Category: vacuum truck (confidence 0.9)
- Made of: steel 70%, rubber 20%, plastic 10%
- Estimated weight: 8000.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: extensive rust on cab and chassis, peeling paint on cab, damaged front bumper, cracked windshield, dirt and grime covering entire vehicle, tires appear worn and dirty
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: CALL

## Two readers
- item_type agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type agreed by both readers
- **read_evidence** -> ok. category=vacuum truck brand=None model=None label=False lines=1
- **retrieval** -> ok. query='CALL Massive scrap lot for sale—225 tons total in Port Harcourt, Rivers State, going for ₦' hits=['Acer Aspire 5', 'Tecno Camon 40', 'Tecno Camon 50', 'Tecno Spark 10', 'Tecno Spark 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused
- **weight** -> stated. 225000 kg from the seller's words

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 44734 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 39441 ms (replayed)
- identify on z-ai/glm-5.3-flash: 11412 ms (replayed)
- total across calls: 95587 ms; wall clock: 1810 ms

## Identification
Shortlist from the catalogue:
  - Acer Aspire 5 (0.2)
  - Tecno Camon 40 (0.2)
  - Tecno Camon 50 (0.2)
  - Tecno Spark 10 (0.2)
  - Tecno Spark 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** Item is a sewage vacuum truck; shortlist contains only phones/laptops with no match and no legible brand plate.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 24%
- Item is a sewage vacuum truck; shortlist contains only phones/laptops with no match and no legible brand plate.
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- 5 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of the VIN plate, usually on the dashboard by the windscreen or inside the driver's door.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Does it start and drive?
- Is the engine, gearbox and all four wheels still on it?
- Do you have the papers proving you own it?

## Claims
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it against the windscreen.
- [unverified] Required evidence 'four_corners' was not supplied
    priced as: priced as if the worst case is true. Four photos, one from each corner, showing the whole vehicle.
- [unverified] Required evidence 'vin_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of the VIN plate, usually on the dashboard by the windscreen or inside the driver's door.
- [unverified] Required evidence 'engine_bay' was not supplied
    priced as: priced as if the worst case is true. Open the bonnet and photograph the engine.
- [unverified] Required evidence 'boot_and_cabin' was not supplied
    priced as: priced as if the worst case is true. Open the boot and photograph inside, then the cabin with the seats folded.

## Price
**64,418,850 to 103,050,000 NGN** (priced as material, width 0.4614, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 225000 kg of steel 70%, rubber 20%, plastic 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 83,250,000 NGN

Conditions attached to this price:
- Not identified: Item is a sewage vacuum truck; shortlist contains only phones/laptops with no match and no legible brand plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it against the windscreen..
- Required evidence 'four_corners' was not supplied -> not proven remotely. Four photos, one from each corner, showing the whole vehicle..
- Required evidence 'vin_plate' was not supplied -> not proven remotely. Close-up of the VIN plate, usually on the dashboard by the windscreen or inside the driver's door..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Open the bonnet and photograph the engine..
- Required evidence 'boot_and_cabin' was not supplied -> not proven remotely. Open the boot and photograph inside, then the cabin with the seats folded..

## Answer key (not shown to the engine)
`{'title': 'Massive Scrap Lot for Sale in Rivers State', 'category': None, 'site_category': 'Scrap Vehicles', 'price_ngn': 500000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/massive-scrap-lot-for-sale-in-rivers-state/'}`
