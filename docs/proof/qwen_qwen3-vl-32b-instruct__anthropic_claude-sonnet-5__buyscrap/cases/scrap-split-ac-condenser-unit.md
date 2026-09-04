# Case scrap-split-ac-condenser-unit

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0154  |  16006 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner outdoor unit (confidence 0.9)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: dusty surface, grime on casing and grille, possible minor corrosion on metal parts
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **read_evidence** -> ok. category=split air conditioner outdoor unit brand=None model=None label=False lines=0
- **retrieval** -> ok. query='A scrap split AC condenser unit is available for sale. Location: Agege, Lagos State Price:' hits=['Infinix Note 50', 'Tecno Camon 50', 'Infinix Hot 50', 'Infinix Note 30', 'Infinix Note 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Infinix Note 50 (0.4)
  - Tecno Camon 50 (0.2)
  - Infinix Hot 50 (0.2)
  - Infinix Note 30 (0.2)
  - Infinix Note 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** The image and seller description clearly show a scrap split air conditioner condenser unit, not a smartphone. None of the shortlist entries (Infinix/Tecno phone models) match this item at all, and no brand/model plate is legible on the unit itself. This appears to be a catalogue mismatch - the shortlist is for phones while the item is an AC condenser.

## Claims
- [unverifiable_remote] This is a split AC condenser unit.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The unit is scrap, sold for parts, repair or recycling.
- [unverifiable_remote] The unit is sold as is.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**17,110 to 42,850 NGN** (priced as material, width 0.8586, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: The image and seller description clearly show a scrap split air conditioner condenser unit, not a smartphone. None of the shortlist entries (Infinix/Tecno phone models) match this item at all, and no brand/model plate is legible on the unit itself. This appears to be a catalogue mismatch - the shortlist is for phones while the item is an AC condenser.
- This is a split AC condenser unit. -> not proven remotely. Weigh on the scale and photograph the display.
- The unit is scrap, sold for parts, repair or recycling. -> not proven remotely. Agent will confirm at pickup.
- The unit is sold as is. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Scrap split AC condenser unit', 'category': None, 'site_category': 'E-waste', 'price_ngn': 50000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/scrap-split-ac-condenser-unit/'}`
