# Case ggcpk3xakCnKxFmGcN50Iuee

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0113  |  20278 ms

## What the engine saw
- Presentation: single_unit
- Category: inverter system (confidence 0.9)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: Sage Tech Electrical
- Model read off the item: SAGE-INV-2000
- Rating read: 12V 2000W, 1200VA
- Label, plate or settings screen legible: yes
- Damage noted: Minor dust on surface, No visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SAGE TECH ELECTRICAL | INVERTER | 12V 2000W | INPUT: 12V DC | OUTPUT: 230V AC | MODEL: SAGE-INV-2000 | SERIAL: SAGE123456789 | 1200VA

## Chain
- **read_evidence** -> ok. category=inverter system brand=Sage Tech Electrical model=SAGE-INV-2000 label=True lines=8
- **retrieval** -> ok. query='Sage Tech Electrical SAGE-INV-2000 12V 2000W, 1200VA SAGE TECH ELECTRICAL INVERTER 12V 200' hits=['Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Sage Tech Electrical SAGE-INV-2000 margin=0.68
- **abstain** -> pass. top=0.7 margin=0.68

## Identification
Shortlist from the catalogue:
  - Kemage KM6500 5.5kVA (0.15)

**Answer: Sage Tech Electrical SAGE-INV-2000** (margin 0.68)

## Claims
- [unverifiable_remote] This is a solar generator and inverter
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Best quality in solar generator and inverter
- [unverifiable_remote] Will serve you 5 to 8 years
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
**4,550 to 20,350 NGN** (priced as material, width 1.269, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3792 for unproven claims.

Scrap floor: 12,000 NGN

Conditions attached to this price:
- This is a solar generator and inverter -> not proven remotely. Weigh on the scale and photograph the display.
- Best quality in solar generator and inverter -> not proven remotely. Agent will confirm at pickup.
- Will serve you 5 to 8 years -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Solar Generator And Inverter', 'category': 'generator', 'price_ngn': 450000, 'is_used': False, 'url': '/agege/power-equipments/solar-generator-and-inverter-ggcpk3xakCnKxFmGcN50Iuee.html?page=2&pos=9&cur_pos=9&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
