# Case xi3EK9AeR27pR7Fqk76h00CV

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0130  |  19204 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: plastic 60%, steel 30%, circuit_board 5%, rubber 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: Perkins
- Model read off the item: SOUNDPROOF MODEL GENERATOR
- Rating read: 15kVA
- Label, plate or settings screen legible: yes
- Damage noted: minor dirt and grime on exterior, some wear on plastic casing, no visible damage to main body or lid
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Perkins | SOUNDPROOF MODEL GENERATOR | 15kVA | CHIDORI ELECTRONICS

## Chain
- **read_evidence** -> ok. category=generator brand=Perkins model=SOUNDPROOF MODEL GENERATOR label=True lines=4
- **retrieval** -> ok. query='Perkins SOUNDPROOF MODEL GENERATOR 15kVA Perkins SOUNDPROOF MODEL GENERATOR 15kVA CHIDORI ' hits=['Perkins P150 150kVA', 'Perkins P100 100kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA']
- **identify** -> refused. chosen=None None margin=0.3
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Perkins P150 150kVA (0.4333)
  - Perkins P100 100kVA (0.4333)
  - Lutian LT3900 3.5kVA (0.15)
  - Senwei SW3500 3.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** The nameplate clearly reads 'Perkins SOUNDPROOF DIESEL GENERATOR 15KVA', but none of the shortlisted catalogue entries (P150 150kVA, P100 100kVA, Lutian 3.5kVA, Senwei 3.5kVA) match this rating. No shortlist model corresponds to a 15kVA Perkins unit, so no confident catalogue match can be made.

## Claims
- [unverifiable_remote] Original Perkins diesel generator
- [unverifiable_remote] 3 phase
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] 15 kVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
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
**3,199 to 12,325 NGN** (priced as material, width 1.1755, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of plastic 60%, steel 30%, circuit_board 5%, rubber 5% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 7,187 NGN

Conditions attached to this price:
- Not identified: The nameplate clearly reads 'Perkins SOUNDPROOF DIESEL GENERATOR 15KVA', but none of the shortlisted catalogue entries (P150 150kVA, P100 100kVA, Lutian 3.5kVA, Senwei 3.5kVA) match this rating. No shortlist model corresponds to a 15kVA Perkins unit, so no confident catalogue match can be made.
- Original Perkins diesel generator -> not proven remotely. Agent will confirm at pickup.
- 3 phase -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- 15 kVA -> not proven remotely. Agent reads the rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Original Perkins Diesel Generator 3 Phase 100% Copper Coil 15 Kva', 'category': 'generator', 'price_ngn': 2450000, 'is_used': False, 'url': '/ikeja/power-equipments/original-perkins-diesel-generator-3-phase-100-copper-coil-15-kva-xi3EK9AeR27pR7Fqk76h00CV.html?page=2&pos=8&cur_pos=8&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
