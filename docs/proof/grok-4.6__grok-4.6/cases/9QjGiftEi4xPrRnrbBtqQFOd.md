# Case 9QjGiftEi4xPrRnrbBtqQFOd

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0149  |  111480 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 55%, plastic 20%, copper 10%, rubber 10%, mixed_electronic 5%
- Estimated weight: 55.0 kg (confidence 0.5)
- Brand read off the item: FIRMAN
- Model read off the item: AC8000E2
- Rating read: 5000 STARTING WATTS, 4200 RUNNING WATTS
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: AC MASTER | FIRMAN | 5000 STARTING WATTS | 4200 RUNNING WATTS | AC8000E2 | PETROL GENERATOR

## Chain
- **read_evidence** -> ok. category=generator brand=FIRMAN model=AC8000E2 label=True lines=6
- **retrieval** -> ok. query='FIRMAN AC8000E2 5000 STARTING WATTS, 4200 RUNNING WATTS AC MASTER FIRMAN 5000 STARTING WAT' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Sumec Firman ECO8990ES 6.5kVA', 'Sumec Firman SPG8800 8.1kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=FIRMAN AC8000E2 margin=None
- **abstain** -> pass. top=0.95 margin=None

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.35)
  - Sumec Firman SPG3000 3.1kVA (0.25)
  - Sumec Firman ECO8990ES 6.5kVA (0.15)
  - Sumec Firman SPG8800 8.1kVA (0.15)
  - Kemage KM6500 5.5kVA (0.15)

**Answer: FIRMAN AC8000E2** (margin None)

## Claims
- [unverifiable_remote] Original
- [unverifiable_remote] fireman generator
- [unverified] 5 kVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% copper
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] coin
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the generator.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole generator from the front.
- [unverified] Required evidence 'plate_kva' was not supplied
    priced as: priced as if the worst case is true. Close-up of the rating plate showing the kVA and model number.
- [unverified] Required evidence 'side_cover_off' was not supplied
    priced as: priced as if the worst case is true. Open the side cover and photograph the alternator windings.
- [unverified] Required evidence 'engine_bay' was not supplied
    priced as: priced as if the worst case is true. Photo of the engine, showing the recoil starter and carburettor.

## Price
**12,687 to 80,000 NGN** (priced as material, width 1.4525, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4229 for unproven claims.

Scrap floor: 73,425 NGN

Conditions attached to this price:
- Original -> not proven remotely. Agent will confirm at pickup.
- fireman generator -> not proven remotely. Agent will confirm at pickup.
- 5 kVA -> not proven remotely. Agent reads the rating plate.
- 100% copper -> not proven remotely. Agent opens the side cover and inspects the windings.
- coin -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Original Fireman Generator 5 Kva 100% Copper Coin', 'category': 'generator', 'price_ngn': 735000, 'is_used': False, 'url': '/ajah/power-equipments/original-fireman-generator-5-kva-100-copper-coin-9QjGiftEi4xPrRnrbBtqQFOd.html?page=2&pos=10&cur_pos=10&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
