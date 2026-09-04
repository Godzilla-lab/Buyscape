# Case jRMbUhqAqIZE2pkBwQcCLDO2

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0144  |  99757 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 45%, iron 25%, copper 10%, plastic 15%, rubber 5%
- Estimated weight: 70.0 kg (confidence 0.45)
- Brand read off the item: MAXMECH
- Model read off the item: MFS-15000E
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MAXMECH | GASOLINE GENERATOR | ENGINE | Voltmeter | 3x120V AC | Circuit Breaker | AC 240V | MAXMECH

## Chain
- **read_evidence** -> ok. category=generator brand=MAXMECH model=MFS-15000E label=True lines=10
- **retrieval** -> ok. query='MAXMECH MFS-15000E MAXMECH GASOLINE GENERATOR ENGINE Voltmeter 3x120V AC Circuit Breaker A' hits=['Maxmech MX3500 3.5kVA', 'Maxmech MX10000 10kVA']
- **identify** -> ok. chosen=MAXMECH MFS-15000E margin=0.93
- **abstain** -> pass. top=0.98 margin=0.93

## Identification
Shortlist from the catalogue:
  - Maxmech MX3500 3.5kVA (0.5)
  - Maxmech MX10000 10kVA (0.4333)

**Answer: MAXMECH MFS-15000E** (margin 0.93)

## Claims
- [unverified] Maxmech 12kva petrol generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% pure copper coil
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
**39,464 to 650,000 NGN** (priced as material, width 1.771, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4933 for unproven claims.

Scrap floor: 95,725 NGN

Conditions attached to this price:
- Maxmech 12kva petrol generator -> not proven remotely. Agent reads the rating plate.
- 100% pure copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Maxmech Peteol Generator 12kva.', 'category': 'generator', 'price_ngn': 848000, 'is_used': False, 'url': '/alimosho/power-equipments/maxmech-peteol-generator-12kva-jRMbUhqAqIZE2pkBwQcCLDO2.html?page=1&pos=23&cur_pos=23&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
