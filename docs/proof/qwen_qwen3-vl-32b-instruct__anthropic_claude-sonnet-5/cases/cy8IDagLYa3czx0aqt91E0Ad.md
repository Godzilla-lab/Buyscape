# Case cy8IDagLYa3czx0aqt91E0Ad

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0186  |  26442 ms

## What the engine saw
- Presentation: single_unit
- Category: welding generator (confidence 0.95)
- Made of: plastic 60%, steel 30%, circuit_board 5%, rubber 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: STAR ARC
- Model read off the item: GENERATOR-350
- Rating read: 3 kVA / 2.5 kW
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: STAR ARC WELDING GENERATOR-350 | SPECIFICATION | Data/Model | STAR ARC WELDING GENERATOR 350 | AC Rated Output: 3 kVA / 2.5 kW | Frequency: 50 Hz | Engine Model: 170 F/P | Max. Output: 3 kVA

## Chain
- **read_evidence** -> ok. category=welding generator brand=STAR ARC model=GENERATOR-350 label=True lines=16
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='STAR ARC GENERATOR-350 3 kVA / 2.5 kW STAR ARC WELDING GENERATOR-350 SPECIFICATION Data/Mo' hits=['Tiger TG950 0.95kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA', 'Lutian LT3900 3.5kVA']
- **identify** -> ok. chosen=STAR ARC GENERATOR-350 margin=0.9
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Tiger TG950 0.95kVA (0.1833)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)
  - Lutian LT3900 3.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads 2.5kw but the seller says 1kw. A clear photo of the rating plate on this exact unit would settle it.

Evidence flags: looks like a catalogue or stock image

## Claims
- [unverifiable_remote] AC Rated Output: 3 KVA/1.0 KW
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Max. Output: 7 HP
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Engine Model: 170 F/P
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**2,156 to 12,325 NGN** (priced as material, width 1.4044, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of plastic 60%, steel 30%, circuit_board 5%, rubber 5% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 7,187 NGN

Conditions attached to this price:
- Not identified: The item reads 2.5kw but the seller says 1kw. A clear photo of the rating plate on this exact unit would settle it.
- Evidence flag: looks like a catalogue or stock image
- AC Rated Output: 3 KVA/1.0 KW -> not proven remotely. Weigh on the scale and photograph the display.
- Max. Output: 7 HP -> not proven remotely. Weigh on the scale and photograph the display.
- Engine Model: 170 F/P -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Star Arc Welding Generator 350a', 'category': 'generator', 'price_ngn': 450000, 'is_used': False, 'url': '/lagos-island-west/power-equipments/star-arc-welding-generator-350a-cy8IDagLYa3czx0aqt91E0Ad.html?page=3&pos=3&cur_pos=3&ads_per_page=24&ads_count=15133&lid=w4bgywJfSACOHKND'}`
