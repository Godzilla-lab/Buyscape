# Case scrap-1hp-window-ac

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0151  |  20964 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.9)
- Made of: steel 40%, copper 20%, plastic 20%, circuit_board 10%, rubber 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: exposed internal components, dusty and dirty condenser coils, missing front panel, wiring exposed, rust on metal casing
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **read_evidence** -> ok. category=split air conditioner brand=None model=None label=False lines=0
- **retrieval** -> ok. query='A scrap 1 horsepower (1HP) window AC is available for sale. Location: Agege, Lagos State P' hits=['Samsung AR09 1HP', 'Hisense AS-09 1HP', 'LG S4-Q09 1HP', 'Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP']
- **identify** -> refused. chosen=None None margin=0.05
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Samsung AR09 1HP (0.2333)
  - Hisense AS-09 1HP (0.2)
  - LG S4-Q09 1HP (0.2)
  - Samsung AR12 1.5HP (0.15)
  - Scanfrost SFAC12 1.5HP (0.15)

**Not identified: CANNOT_IDENTIFY.** No legible brand, model, or rating plate visible on the unit; it's a stripped/scrap window AC with only internal coils and wiring visible from the back. The seller's '1HP' claim cannot be verified against any specific catalogue model since none of the shortlisted brands' names or badges are visible in the photo.

## Claims
- [unverifiable_remote] The item is a window AC unit.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 1 horsepower (1HP) rating.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Described as 'scrap', implying non-working or for-parts condition.
- [unverifiable_remote] Item is located in Agege, Lagos State.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**21,386 to 82,150 NGN** (priced as material, width 1.1737, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, copper 20%, plastic 20%, circuit_board 10%, rubber 10% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 59,375 NGN

Conditions attached to this price:
- Not identified: No legible brand, model, or rating plate visible on the unit; it's a stripped/scrap window AC with only internal coils and wiring visible from the back. The seller's '1HP' claim cannot be verified against any specific catalogue model since none of the shortlisted brands' names or badges are visible in the photo.
- The item is a window AC unit. -> not proven remotely. Weigh on the scale and photograph the display.
- 1 horsepower (1HP) rating. -> not proven remotely. Weigh on the scale and photograph the display.
- Described as 'scrap', implying non-working or for-parts condition. -> not proven remotely. Agent will confirm at pickup.
- Item is located in Agege, Lagos State. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Scrap 1HP window AC', 'category': None, 'site_category': 'E-waste', 'price_ngn': 35000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/scrap-1hp-window-ac/'}`
