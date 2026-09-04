# Case v4y9denCn3Xfb9uDQmPWNVgJ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0226  |  27617 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.9)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, mixed_electronic 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: COROLLA
- Model read off the item: EL-6000-SD
- Rating read: AC 220V 50Hz 3000W, DC 12V 8.3A
- Label, plate or settings screen legible: yes
- Damage noted: some surface dirt and grime, minor scratches on casing, wheels appear worn but intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: COROLLA | EL-6000-SD | ELECTRIC STARTER | AC 220V 50Hz 3000W | DC 12V 8.3A | ENGINE: GX200 | FUEL TANK CAPACITY: 3.5L | OIL CAPACITY: 0.6L

## Chain
- **read_evidence** -> ok. category=generator brand=COROLLA model=EL-6000-SD label=True lines=10
- **retrieval** -> ok. query='COROLLA EL-6000-SD AC 220V 50Hz 3000W, DC 12V 8.3A COROLLA EL-6000-SD ELECTRIC STARTER AC ' hits=['Tiger TG950 0.95kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA']
- **identify** -> ok. chosen=Corolla CL7800E2R margin=0.55
- **abstain** -> pass. top=0.75 margin=0.55

## Identification
Shortlist from the catalogue:
  - Tiger TG950 0.95kVA (0.1833)
  - Lutian LT3900 3.5kVA (0.15)
  - Senwei SW3500 3.5kVA (0.15)

**Answer: Corolla CL7800E2R** (margin 0.55)

## Claims
- [unverifiable_remote] Corolla remote control petrol generator
- [unverifiable_remote] Model cl7800E2r
- [unverifiable_remote] Remote control operation
    priced as: assumed does not start. Agent starts the generator and runs it under load
- [unverifiable_remote] Petrol generator (fuel type: petrol)
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] Comes with warranty of one year
- [unverifiable_remote] Includes key
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
**3,412 to 21,350 NGN** (priced as material, width 1.4488, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 11,375 NGN

Conditions attached to this price:
- Corolla remote control petrol generator -> not proven remotely. Agent will confirm at pickup.
- Model cl7800E2r -> not proven remotely. Agent will confirm at pickup.
- Remote control operation -> not proven remotely. Agent starts the generator and runs it under load.
- Petrol generator (fuel type: petrol) -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Comes with warranty of one year -> not proven remotely. Agent will confirm at pickup.
- Includes key -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'COROLLA Cl7800e2r 4.5kva Petrol Gen Remote Control', 'category': 'generator', 'price_ngn': 350000, 'is_used': False, 'url': '/ojo/power-equipments/corolla-cl7800e2r-4-5kva-petrol-gen-remote-control-v4y9denCn3Xfb9uDQmPWNVgJ.html?page=1&pos=5&cur_pos=5&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
