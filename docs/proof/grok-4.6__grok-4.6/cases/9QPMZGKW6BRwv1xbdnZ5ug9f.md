# Case 9QPMZGKW6BRwv1xbdnZ5ug9f

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0137  |  93348 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, iron 20%, plastic 15%, aluminium 10%, copper 10%, rubber 5%
- Estimated weight: 42.0 kg (confidence 0.55)
- Brand read off the item: SUMEC FIRMAN
- Model read off the item: SPC4000
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SUMEC | FIRMAN | SPC4000 | Petrol Generator | ENG. ON

## Chain
- **read_evidence** -> ok. category=generator brand=SUMEC FIRMAN model=SPC4000 label=True lines=5
- **retrieval** -> ok. query='SUMEC FIRMAN SPC4000 SUMEC FIRMAN SPC4000 Petrol Generator ENG. ON Firman 4kva generator. ' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Sumec Firman ECO8990ES 6.5kVA', 'Sumec Firman SPG8800 8.1kVA']
- **identify** -> ok. chosen=Sumec Firman SPC4000 margin=None
- **abstain** -> pass. top=0.98 margin=None

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.5)
  - Sumec Firman SPG3000 3.1kVA (0.4)
  - Sumec Firman ECO8990ES 6.5kVA (0.3)
  - Sumec Firman SPG8800 8.1kVA (0.3)

**Answer: Sumec Firman SPC4000** (margin None)

## Claims
- [unverified] Firman 4kva generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] Firman 4kva generator
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
**12,579 to 80,000 NGN** (priced as material, width 1.4565, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4193 for unproven claims.

Scrap floor: 63,735 NGN

Conditions attached to this price:
- Firman 4kva generator -> not proven remotely. Agent reads the rating plate.
- Firman 4kva generator -> not proven remotely. Agent reads the rating plate.
- Pure copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Firman 4kva Generator', 'category': 'generator', 'price_ngn': 368000, 'is_used': False, 'url': '/ajah/power-equipments/firman-4kva-generator-9QPMZGKW6BRwv1xbdnZ5ug9f.html?page=1&pos=19&cur_pos=19&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
