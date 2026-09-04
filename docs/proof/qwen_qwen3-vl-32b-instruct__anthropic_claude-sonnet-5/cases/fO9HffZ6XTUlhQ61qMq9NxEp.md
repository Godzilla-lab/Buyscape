# Case fO9HffZ6XTUlhQ61qMq9NxEp

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0198  |  27739 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, mixed_electronic 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAO
- Model read off the item: YADENG
- Rating read: MAX POWER 2.5kW, RATED POWER 2.0kW, OUTPUT AC 220V 50Hz
- Label, plate or settings screen legible: yes
- Damage noted: Item wrapped in plastic film, No visible damage or wear
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAO | YADENG | SINUSOIDAL WAVE GENERATOR | CONSTANT | CE | OUTPUT AC 220V 50Hz | MAX POWER 2.5kW | RATED POWER 2.0kW

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAO model=YADENG label=True lines=17
- **retrieval** -> ok. query='ELEPAO YADENG MAX POWER 2.5kW, RATED POWER 2.0kW, OUTPUT AC 220V 50Hz ELEPAO YADENG SINUSO' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Elepaq SV2200 margin=0.45
- **abstain** -> abstain. top score 0.55

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.6)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.2333)
  - Haier Thermocool HTG2700 2.5kVA (0.2333)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.55, which is not sure enough to price.

## Claims
- [unverifiable_remote] 4.5kVA generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Elepaq brand generator
- [unverifiable_remote] Petrol-powered generator
- [unverifiable_remote] 100% copper wire winding
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] 1 year warranty included
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
**4,810 to 21,350 NGN** (priced as material, width 1.2645, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 30%, circuit_board 10%, rubber 10%, mixed_electronic 10% (rates for circuit_board, mixed_electronic, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 11,375 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.55, which is not sure enough to price.
- 4.5kVA generator -> not proven remotely. Agent reads the rating plate.
- Elepaq brand generator -> not proven remotely. Agent will confirm at pickup.
- Petrol-powered generator -> not proven remotely. Agent will confirm at pickup.
- 100% copper wire winding -> not proven remotely. Agent opens the side cover and inspects the windings.
- 1 year warranty included -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Elepaq 4.5kva Petorl Generator 100%Copper Wire', 'category': 'generator', 'price_ngn': 275000, 'is_used': False, 'url': '/ajah/power-equipments/elepaq-4-5kva-petorl-generator-100-copper-wire-fO9HffZ6XTUlhQ61qMq9NxEp.html?page=1&pos=13&cur_pos=13&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
