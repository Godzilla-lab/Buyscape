# Case gsbW9Vdx7tp7RvFb4wDvrF4r

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0160  |  24360 ms

## What the engine saw
- Presentation: single_unit
- Category: portable generator (confidence 0.95)
- Made of: plastic 70%, steel 20%, circuit_board 10%
- Estimated weight: 8.5 kg (confidence 0.8)
- Brand read off the item: KENMORE
- Model read off the item: KM5000i
- Rating read: 5000W MAX / 4000W CONTINUOUS
- Label, plate or settings screen legible: yes
- Damage noted: item appears clean and undamaged, plastic casing shows no visible cracks or dents, no visible rust or stains, handle and control panel intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: KENMORE | KM5000i | INVERTER GENERATOR | 4 STROKE ENGINE | 230V / 120V | OUTPUT: 5000W MAX / 4000W CONTINUOUS | FUEL TANK CAPACITY: 6L | RUN TIME @ 50% LOAD: 10 HOURS

## Chain
- **read_evidence** -> ok. category=portable generator brand=KENMORE model=KM5000i label=True lines=18
- **retrieval** -> ok. query='KENMORE KM5000i 5000W MAX / 4000W CONTINUOUS KENMORE KM5000i INVERTER GENERATOR 4 STROKE E' hits=['Kemage KM10000 10kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Kemage KM5000i margin=0.8
- **abstain** -> pass. top=0.9 margin=0.8

## Identification
Shortlist from the catalogue:
  - Kemage KM10000 10kVA (0.4333)
  - Kemage KM6500 5.5kVA (0.4)

**Answer: Kemage KM5000i** (margin 0.8)

## Claims
- [unverifiable_remote] Equipped with overload protection
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Equipped with low-oil shutdown
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The model is referred to as the Kemage 5000
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
**816 to 5,491 NGN** (priced as material, width 1.4825, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 2,720 NGN

Conditions attached to this price:
- Equipped with overload protection -> not proven remotely. Weigh on the scale and photograph the display.
- Equipped with low-oil shutdown -> not proven remotely. Weigh on the scale and photograph the display.
- The model is referred to as the Kemage 5000 -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Kemage 5000i 4.5kva Low-Noise Inverter Generator', 'category': 'generator', 'price_ngn': 480000, 'is_used': False, 'url': '/ajah/power-equipments/kemage-5000i-4-5kva-low-noise-inverter-generator-gsbW9Vdx7tp7RvFb4wDvrF4r.html?page=2&pos=6&cur_pos=6&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
