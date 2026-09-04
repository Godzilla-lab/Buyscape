# Case rAvryKzKWcwQ7cAtqwE2Lxad

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0194  |  28399 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: MAXMECH
- Model read off the item: MS-2600
- Rating read: 2.6KVA
- Label, plate or settings screen legible: yes
- Damage noted: dirt and mud on surface, some rust visible on frame, worn plastic cover, fuel cap appears loose or missing
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MAXMECH | MS-2600 | GENERATOR | 2.6KVA | AC 220V 50Hz | DC 12V 8A | OUTPUT POWER: 2.6KVA | ENGINE: OHV 4-STROKE

## Chain
- **read_evidence** -> ok. category=generator brand=MAXMECH model=MS-2600 label=True lines=10
- **retrieval** -> ok. query='MAXMECH MS-2600 2.6KVA MAXMECH MS-2600 GENERATOR 2.6KVA AC 220V 50Hz DC 12V 8A OUTPUT POWE' hits=['Maxmech MX3500 3.5kVA', 'Maxmech MX10000 10kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA']
- **identify** -> ok. chosen=MAXMECH MS-2600 margin=0.8
- **abstain** -> pass. top=0.9 margin=0.8

## Identification
Shortlist from the catalogue:
  - Maxmech MX3500 3.5kVA (0.5)
  - Maxmech MX10000 10kVA (0.4333)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)

**Answer: MAXMECH MS-2600 2.6KVA** (margin 0.8)

## Claims
- [unverifiable_remote] The product is a MAXMECH WGC-380Ei Welding Generator.
- [unverifiable_remote] It is a heavy-duty machine.
- [unverifiable_remote] It is a 2-in-1 machine.
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
**19,902 to 80,000 NGN** (priced as material, width 1.2031, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.6634 for unproven claims.

Scrap floor: 34,625 NGN

Conditions attached to this price:
- The product is a MAXMECH WGC-380Ei Welding Generator. -> not proven remotely. Agent will confirm at pickup.
- It is a heavy-duty machine. -> not proven remotely. Agent will confirm at pickup.
- It is a 2-in-1 machine. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Maxmech Wgc-380ei 300a / 2.5kva Welding Generator', 'category': 'generator', 'price_ngn': 800000, 'is_used': False, 'url': '/lagos-island-west/power-equipments/maxmech-wgc-380ei-300a-2-5kva-welding-generator-rAvryKzKWcwQ7cAtqwE2Lxad.html?page=2&pos=1&cur_pos=1&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
