# Case rREXiw3jnu8JE2phT7cuNXze

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0197  |  28333 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: plastic 40%, steel 30%, circuit_board 10%, rubber 10%, aluminium 10%
- Estimated weight: 12.0 kg (confidence 0.8)
- Brand read off the item: KEMAGE
- Model read off the item: nothing legible
- Rating read: 1000W
- Label, plate or settings screen legible: yes
- Damage noted: minor dirt and grime on surface, some scuff marks on plastic casing, no visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: KEMAGE | GENUINE QUALITY | 1000W GENERATOR | PETROL POWERED GENERATOR | OUTPUT: 1000W | VOLTAGE: 230V | FUEL TANK CAPACITY: 3.5L | ENGINE: 4-STROKE

## Chain
- **read_evidence** -> ok. category=generator brand=KEMAGE model=None label=True lines=14
- **retrieval** -> ok. query='KEMAGE 1000W KEMAGE GENUINE QUALITY 1000W GENERATOR PETROL POWERED GENERATOR OUTPUT: 1000W' hits=['Kemage KM6500 5.5kVA', 'Kemage KM10000 10kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA', 'Thermocool TC2700 2.5kVA']
- **identify** -> refused. chosen=None None margin=0.05
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Kemage KM6500 5.5kVA (0.55)
  - Kemage KM10000 10kVA (0.4333)
  - Lutian LT3900 3.5kVA (0.3)
  - Senwei SW3500 3.5kVA (0.3)
  - Thermocool TC2700 2.5kVA (0.1833)

**Not identified: CANNOT_IDENTIFY.** The nameplate clearly reads KEMAGE, 1000W output, 3.5L tank, 12kg, 4-stroke recoil-start unit — a small portable genset. The seller's claimed model (KM11000E2, 8.5KVA) is inconsistent with these printed specs, and none of the shortlisted models (KM6500 5.5kVA, KM10000 10kVA, etc.) match a 1000W/12kg unit. No legible model number appears on the plate itself, so I cannot confidently map this to any specific catalogue entry.

## Claims
- [unverifiable_remote] Brand: Kemage
- [unverifiable_remote] Model: KM11000E2
- [unverifiable_remote] AC Frequency: 50 Hz
- [unverifiable_remote] Starting Capacity: 8.5KVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Japan (implied origin or manufacturing standard)
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
**3,503 to 11,544 NGN** (priced as material, width 1.0687, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of plastic 40%, steel 30%, circuit_board 10%, rubber 10%, aluminium 10% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 6,540 NGN

Conditions attached to this price:
- Not identified: The nameplate clearly reads KEMAGE, 1000W output, 3.5L tank, 12kg, 4-stroke recoil-start unit — a small portable genset. The seller's claimed model (KM11000E2, 8.5KVA) is inconsistent with these printed specs, and none of the shortlisted models (KM6500 5.5kVA, KM10000 10kVA, etc.) match a 1000W/12kg unit. No legible model number appears on the plate itself, so I cannot confidently map this to any specific catalogue entry.
- Brand: Kemage -> not proven remotely. Agent will confirm at pickup.
- Model: KM11000E2 -> not proven remotely. Agent will confirm at pickup.
- AC Frequency: 50 Hz -> not proven remotely. Agent will confirm at pickup.
- Starting Capacity: 8.5KVA -> not proven remotely. Agent reads the rating plate.
- Japan (implied origin or manufacturing standard) -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Kemage 230V Manual Start Gasoline Generator.', 'category': 'generator', 'price_ngn': 400000, 'is_used': False, 'url': '/lekki/power-equipments/kemage-230v-manual-start-gasoline-generator-rREXiw3jnu8JE2phT7cuNXze.html?page=2&pos=17&cur_pos=17&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
