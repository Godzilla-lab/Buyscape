# Case plastic-pet-bottle-for-sale

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0070  |  8598 ms

## What the engine saw
- Presentation: mixed_lot
- Category: recyclable plastic bottles (confidence 0.9)
- Made of: pet_bottle 90%, plastic 10%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **read_evidence** -> ok. category=recyclable plastic bottles brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

## Claims
- [unverifiable_remote] Plastic PET bottle for sale.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The items are clean.
- [unverifiable_remote] The items are sorted.
- [unverifiable_remote] Located in Ikosi, Ketu, Lagos State, Nigeria.
- [unverifiable_remote] Ready for weighing and pickup.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**1,369 to 4,950 NGN** (priced as material, width 1.1329, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of pet_bottle 90%, plastic 10% (rates for pet_bottle, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,950 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Plastic PET bottle for sale. -> not proven remotely. Weigh on the scale and photograph the display.
- The items are clean. -> not proven remotely. Agent will confirm at pickup.
- The items are sorted. -> not proven remotely. Agent will confirm at pickup.
- Located in Ikosi, Ketu, Lagos State, Nigeria. -> not proven remotely. Agent will confirm at pickup.
- Ready for weighing and pickup. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Plastic PET Bottle for Sale', 'category': None, 'site_category': 'Plastic and Rubbers', 'price_ngn': 0, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/plastic-pet-bottle-for-sale/'}`
