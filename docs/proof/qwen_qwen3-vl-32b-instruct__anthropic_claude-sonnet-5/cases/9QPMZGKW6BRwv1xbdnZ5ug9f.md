# Case 9QPMZGKW6BRwv1xbdnZ5ug9f

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0116  |  19541 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, unknown 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: SUMEC FIRMAN
- Model read off the item: SPG4000
- Rating read: 3.5kW
- Label, plate or settings screen legible: yes
- Damage noted: Item wrapped in plastic film, No visible damage or wear on generator body, Control panel and labels appear clean and intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SUMEC FIRMAN SPG4000 Petrol Generator | ENG. NO. FZ-4000 | OUTPUT AC 230V 50Hz | MAX POWER 3.5kW | RATED POWER 3.0kW | FUEL TANK CAPACITY 15L | RUNNING TIME 8H | ENGINE SPEED 3000rpm

## Chain
- **read_evidence** -> ok. category=generator brand=SUMEC FIRMAN model=SPG4000 label=True lines=14
- **retrieval** -> ok. query='SUMEC FIRMAN SPG4000 3.5kW SUMEC FIRMAN SPG4000 Petrol Generator ENG. NO. FZ-4000 OUTPUT A' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Sumec Firman ECO8990ES 6.5kVA', 'Sumec Firman SPG8800 8.1kVA', 'Lutian LT3900 3.5kVA']
- **identify** -> ok. chosen=Sumec Firman SPG4000 margin=0.85
- **abstain** -> pass. top=0.95 margin=0.85

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.5)
  - Sumec Firman SPG3000 3.1kVA (0.45)
  - Sumec Firman ECO8990ES 6.5kVA (0.3)
  - Sumec Firman SPG8800 8.1kVA (0.3)
  - Lutian LT3900 3.5kVA (0.15)

**Answer: Sumec Firman SPG4000** (margin 0.85)

## Claims
- [unverifiable_remote] Firman 4kva generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Pure copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
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
**14,799 to 80,000 NGN** (priced as material, width 1.3756, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4933 for unproven claims.

Scrap floor: 30,000 NGN

Conditions attached to this price:
- Firman 4kva generator -> not proven remotely. Agent reads the rating plate.
- Pure copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Firman 4kva Generator', 'category': 'generator', 'price_ngn': 368000, 'is_used': False, 'url': '/ajah/power-equipments/firman-4kva-generator-9QPMZGKW6BRwv1xbdnZ5ug9f.html?page=1&pos=19&cur_pos=19&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
