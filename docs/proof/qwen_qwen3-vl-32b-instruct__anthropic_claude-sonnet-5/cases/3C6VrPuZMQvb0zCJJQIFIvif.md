# Case 3C6VrPuZMQvb0zCJJQIFIvif

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0153  |  17842 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, mixed_electronic 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: SECI
- Model read off the item: SC30000
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor dust and grime on surface, no visible dents or cracks, fuel tank appears intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SECI | SC30000 | GASOLINE GENERATOR

## Chain
- **read_evidence** -> ok. category=generator brand=SECI model=SC30000 label=True lines=3
- **retrieval** -> empty. query='SECI SC30000 SECI SC30000 GASOLINE GENERATOR Senci petrol generator model sc30000 100% cop' hits=[]
- **identify** -> ok. chosen=Senci SC30000 margin=0.65
- **abstain** -> pass. top=0.85 margin=0.65

## Identification
No catalogue candidates matched.

**Answer: Senci SC30000** (margin 0.65)

## Claims
- [unverifiable_remote] Senci petrol generator
- [unverifiable_remote] Model SC30000
- [unverifiable_remote] Petrol powered generator
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] Comes with warranty of one year
- [unverifiable_remote] Key start feature
- [unverifiable_remote] Has tyre(s)
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
**4,852 to 21,350 NGN** (priced as material, width 1.2592, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4266 for unproven claims.

Scrap floor: 11,375 NGN

Conditions attached to this price:
- Senci petrol generator -> not proven remotely. Agent will confirm at pickup.
- Model SC30000 -> not proven remotely. Agent will confirm at pickup.
- Petrol powered generator -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Comes with warranty of one year -> not proven remotely. Agent will confirm at pickup.
- Key start feature -> not proven remotely. Agent will confirm at pickup.
- Has tyre(s) -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Best Senci Petrol Generator 20kva 100% Copper Coil', 'category': 'generator', 'price_ngn': 5250000, 'is_used': False, 'url': '/lekki/power-equipments/best-senci-petrol-generator-20kva-100-copper-coil-3C6VrPuZMQvb0zCJJQIFIvif.html?page=1&pos=7&cur_pos=7&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
