# Case massive-scrap-lot-for-sale-in-rivers-state

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  33214 ms

## What the engine saw
- Presentation: single_unit
- Category: vacuum truck (confidence 0.9)
- Made of: steel 60%, rubber 20%, plastic 10%, glass 5%, copper 5%
- Estimated weight: 12000.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: extensive paint damage and rust on cab, cracked windshield, dirt and grime covering entire vehicle, missing front bumper section, tires appear worn and dirty
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: CALL

## OCR read off the photos
- 非

## Chain
- **ocr** -> ok. 1 lines: 非
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=vacuum truck brand=None model=None label=False lines=1
- **retrieval** -> ok. query='CALL Massive scrap lot for sale—225 tons total in Port Harcourt, Rivers State, going for ₦' hits=['Acer Aspire 5', 'Tecno Camon 40', 'Tecno Camon 50', 'Tecno Spark 10', 'Tecno Spark 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused
- **weight** -> stated. 225000 kg from the seller's words

## Identification
Shortlist from the catalogue:
  - Acer Aspire 5 (0.2)
  - Tecno Camon 40 (0.2)
  - Tecno Camon 50 (0.2)
  - Tecno Spark 10 (0.2)
  - Tecno Spark 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** Photo shows a sewage/vacuum tank truck with no legible brand or model; none of the shortlist items (laptops, phones) remotely match.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 24%
- Photo shows a sewage/vacuum tank truck with no legible brand or model; none of the shortlist items (laptops, phones) remotely match.
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
**142,940,205 to 236,362,500 NGN** (priced as material, width 0.4926, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 225000 kg of steel 60%, rubber 20%, plastic 10%, glass 5%, copper 5% (rates for glass, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 184,725,000 NGN

Conditions attached to this price:
- Not identified: Photo shows a sewage/vacuum tank truck with no legible brand or model; none of the shortlist items (laptops, phones) remotely match.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it against the windscreen..
- Required evidence 'four_corners' was not supplied -> not proven remotely. Four photos, one from each corner, showing the whole vehicle..
- Required evidence 'vin_plate' was not supplied -> not proven remotely. Close-up of the VIN plate, usually on the dashboard by the windscreen or inside the driver's door..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Open the bonnet and photograph the engine..
- Required evidence 'boot_and_cabin' was not supplied -> not proven remotely. Open the boot and photograph inside, then the cabin with the seats folded..

## Answer key (not shown to the engine)
`{'title': 'Massive Scrap Lot for Sale in Rivers State', 'category': None, 'site_category': 'Scrap Vehicles', 'price_ngn': 500000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/massive-scrap-lot-for-sale-in-rivers-state/'}`
