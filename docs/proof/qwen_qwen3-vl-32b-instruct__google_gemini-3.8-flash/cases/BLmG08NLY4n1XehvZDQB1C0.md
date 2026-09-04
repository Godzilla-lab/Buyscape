# Case BLmG08NLY4n1XehvZDQB1C0

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: google/gemini-3.8-flash  |  cost: $0.0004  |  9510 ms

## What the engine saw
- Presentation: mixed_lot
- Category: electronic devices (confidence 0.7)
- Made of: plastic 60%, circuit_board 20%, steel 10%, glass 10%
- Estimated weight: 2.5 kg (confidence 0.6)
- Brand read off the item: Apple
- Model read off the item: iPhone 6s
- Rating read: 128GB
- Label, plate or settings screen legible: yes
- Damage noted: Screen shows signs of use, minor smudges, Case appears worn, Items stacked together, no clear indication of individual condition
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Settings | Battery | Battery Health | Battery is currently at 84% health | This battery has degraded and may not hold a charge as well as when new. | Learn more about battery health | iPhone | Apple

## Chain
- **read_evidence** -> ok. category=electronic devices brand=Apple model=iPhone 6s label=True lines=21
- **gate** -> lot. priced by material, identification skipped

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

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
**838 to 2,432 NGN** (priced as material, width 0.9742, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 2.5 kg of plastic 60%, circuit_board 20%, steel 10%, glass 10% (rates for circuit_board, glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 1,030 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 5s 16 GB Silver', 'category': 'phone', 'price_ngn': 35000, 'is_used': True, 'url': '/lekki/mobile-phones/apple-iphone-5s-16-gb-silver-BLmG08NLY4n1XehvZDQB1C0.html?page=1&pos=19&cur_pos=19&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
