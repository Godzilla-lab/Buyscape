# Case aprsW9ypO5nm22HwaYRamM4r

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0191  |  39885 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 18.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: V-6000E
- Rating read: MAX POWER 6000W, RATED POWER 5000W, FUEL TANK CAPACITY 15L, RUNNING TIME 8H
- Label, plate or settings screen legible: yes
- Damage noted: Item is wrapped in plastic film, No visible damage or wear
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | V-6000E | CE | OUTPUT AC 230V 50Hz | MAX POWER 6000W | RATED POWER 5000W | FUEL TANK CAPACITY 15L | RUNNING TIME 8H

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=V-6000E label=True lines=15
- **retrieval** -> ok. query='ELEPAQ V-6000E MAX POWER 6000W, RATED POWER 5000W, FUEL TANK CAPACITY 15L, RUNNING TIME 8H' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Elepaq V-6000E margin=0.6
- **abstain** -> pass. top=0.75 margin=0.6

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.55)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Answer: Elepaq V-6000E** (margin 0.6)

## Claims
- [unverifiable_remote] Elepaq brand generator
- [unverifiable_remote] Model designation 'SV 2500'
- [unverified] 1.5kVA rated capacity
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Constant (not just peak) power generator
- [unverifiable_remote] 100% copper coil winding
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
**12,054 to 80,000 NGN** (priced as material, width 1.4762, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4018 for unproven claims.

Scrap floor: 30,000 NGN

Conditions attached to this price:
- Elepaq brand generator -> not proven remotely. Agent will confirm at pickup.
- Model designation 'SV 2500' -> not proven remotely. Agent will confirm at pickup.
- 1.5kVA rated capacity -> not proven remotely. Agent reads the rating plate.
- Constant (not just peak) power generator -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil winding -> not proven remotely. Agent opens the side cover and inspects the windings.
- 1 year warranty included -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '1.5kva Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 160000, 'is_used': False, 'url': '/ajah/power-equipments/1-5kva-elepaq-constant-generator-aprsW9ypO5nm22HwaYRamM4r.html?page=1&pos=3&cur_pos=3&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
