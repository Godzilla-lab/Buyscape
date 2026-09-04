# Case jPks3Z0tX3eLbv4bCm4KsKuX

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0140  |  21860 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.95)
- Made of: plastic 60%, steel 30%, copper 10%
- Estimated weight: 18.0 kg (confidence 0.8)
- Brand read off the item: Hisense
- Model read off the item: KFR-26GW/100A
- Rating read: 1.0HP, 2600W
- Label, plate or settings screen legible: yes
- Damage noted: Unit is covered in plastic wrap, appears new., Coil and hose are wrapped and undamaged.
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Hisense | SPLIT AIR CONDITIONER | MODEL: KFR-26GW/100A | SERIAL NO: 1234567890 | RATING: 1.0HP, 2600W

## Chain
- **read_evidence** -> ok. category=split air conditioner brand=Hisense model=KFR-26GW/100A label=True lines=5
- **retrieval** -> ok. query='Hisense KFR-26GW/100A 1.0HP, 2600W Hisense SPLIT AIR CONDITIONER MODEL: KFR-26GW/100A SERI' hits=['Hisense AS-09 1HP', 'LG S4-Q09 1HP', 'Hisense AS-12 1.5HP', 'LG S4-Q12 1.5HP', 'LG S4-Q18 2HP']
- **identify** -> ok. chosen=Hisense KFR-26GW/100A margin=0.65
- **abstain** -> pass. top=0.9 margin=0.65

## Identification
Shortlist from the catalogue:
  - Hisense AS-09 1HP (0.6)
  - LG S4-Q09 1HP (0.6)
  - Hisense AS-12 1.5HP (0.51)
  - LG S4-Q12 1.5HP (0.51)
  - LG S4-Q18 2HP (0.4)

**Answer: Hisense KFR-26GW/100A 1.0HP/2600W** (margin 0.65)

## Claims
- [unverifiable_remote] LG air conditioner
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 1HP capacity
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Regular (non-inverter) type
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
**6,534 to 28,584 NGN** (priced as material, width 1.2558, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 21,780 NGN

Conditions attached to this price:
- LG air conditioner -> not proven remotely. Weigh on the scale and photograph the display.
- 1HP capacity -> not proven remotely. Weigh on the scale and photograph the display.
- Regular (non-inverter) type -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'LG Split Air Conditioner 1hp Regular', 'category': 'split_ac', 'price_ngn': 290000, 'is_used': False, 'url': '/amuwo-odofin/home-appliances/lg-split-air-conditioner-1hp-regular-jPks3Z0tX3eLbv4bCm4KsKuX.html?page=1&pos=17&cur_pos=17&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
