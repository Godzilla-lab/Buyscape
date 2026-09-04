# Case faulty-inverter-ac

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0126  |  16748 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.95)
- Made of: plastic 40%, steel 30%, copper 20%, mixed_electronic 10%
- Estimated weight: 35.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dusty exterior, some discoloration on casing, red handwritten number '14,700' on side panel
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Inverter | 14,700

## Chain
- **read_evidence** -> ok. category=split air conditioner brand=None model=None label=True lines=2
- **retrieval** -> empty. query='Inverter 14,700 Faulty inverter AC available for sale. Location: Oshodi, Lagos State Price' hits=[]
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** The image shows a split-type inverter air conditioner (indoor wall unit and outdoor condenser unit) with a label plate visible but no legible brand or model text captured in the OCR read. A partial red logo is visible on the outdoor unit but is not clearly legible enough to confirm a brand name. Only generic text 'Inverter' and a number '14,700' (likely BTU rating) were read. Without a legible brand/model on the label plate, no catalogue match can be confidently made.

## Claims
- [unverifiable_remote] Inverter AC
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Faulty
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
**40,704 to 105,070 NGN** (priced as material, width 0.8831, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 35 kg of plastic 40%, steel 30%, copper 20%, mixed_electronic 10% (rates for mixed_electronic, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 79,100 NGN

Conditions attached to this price:
- Not identified: The image shows a split-type inverter air conditioner (indoor wall unit and outdoor condenser unit) with a label plate visible but no legible brand or model text captured in the OCR read. A partial red logo is visible on the outdoor unit but is not clearly legible enough to confirm a brand name. Only generic text 'Inverter' and a number '14,700' (likely BTU rating) were read. Without a legible brand/model on the label plate, no catalogue match can be confidently made.
- Inverter AC -> not proven remotely. Weigh on the scale and photograph the display.
- Faulty -> not proven remotely. Agent will confirm at pickup.
- Location: Oshodi, Lagos State -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Faulty Inverter AC', 'category': None, 'site_category': 'E-waste', 'price_ngn': 60000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/faulty-inverter-ac/'}`
