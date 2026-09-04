# Case massive-scrap-lot-for-sale-in-rivers-state

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  24343 ms

## What the engine saw
- Presentation: single_unit
- Category: sewage truck (confidence 0.9)
- Made of: steel 60%, rubber 20%, plastic 10%, mixed_electronic 10%
- Estimated weight: 8000.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: extensive rust and paint damage on cab, front windshield missing or broken, mud and grime covering entire vehicle, tires appear worn and dirty, body panels dented and corroded
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: CALL

## Chain
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=sewage truck brand=None model=None label=False lines=1
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
- Price confidence: 27%
- Photo shows a sewage/vacuum tank truck with no legible brand or model; none of the shortlist items (laptops, phones) remotely match.
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- 4 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**71,472,375 to 123,300,000 NGN** (priced as material, width 0.5322, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 225000 kg of steel 60%, rubber 20%, plastic 10%, mixed_electronic 10% (rates for mixed_electronic, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 87,750,000 NGN

Conditions attached to this price:
- Not identified: Photo shows a sewage/vacuum tank truck with no legible brand or model; none of the shortlist items (laptops, phones) remotely match.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Massive Scrap Lot for Sale in Rivers State', 'category': None, 'site_category': 'Scrap Vehicles', 'price_ngn': 500000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/massive-scrap-lot-for-sale-in-rivers-state/'}`
