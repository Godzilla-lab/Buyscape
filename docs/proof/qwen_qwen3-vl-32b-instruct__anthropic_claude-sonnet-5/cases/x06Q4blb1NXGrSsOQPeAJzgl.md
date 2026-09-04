# Case x06Q4blb1NXGrSsOQPeAJzgl

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0143  |  21616 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: EP-6500
- Rating read: 6500W
- Label, plate or settings screen legible: yes
- Damage noted: Minor scuffs on plastic casing, Some dirt on surface, Wires exposed at front panel, not fully enclosed
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | POWER GENERATOR | 6500W | MODEL: EP-6500 | SERIAL NO: 1234567890 | INPUT: 120V / 60Hz | OUTPUT: 120V / 60Hz | MAX POWER: 6500W

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=EP-6500 label=True lines=18
- **retrieval** -> ok. query='ELEPAQ EP-6500 6500W ELEPAQ POWER GENERATOR 6500W MODEL: EP-6500 SERIAL NO: 1234567890 INP' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> ok. chosen=Elepaq EP-6500 margin=0.65
- **abstain** -> pass. top=0.9 margin=0.65

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Answer: Elepaq EP-6500** (margin 0.65)

## Claims
- [unverifiable_remote] Elepaq Constant is the original Elepaq generator
- [unverifiable_remote] Has unique sound with very low noise
- [unverifiable_remote] 25ltr petrol (fuel tank capacity)
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
**22,970 to 50,100 NGN** (priced as material, width 0.7426, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.6634 for unproven claims.

Scrap floor: 34,625 NGN

Conditions attached to this price:
- Elepaq Constant is the original Elepaq generator -> not proven remotely. Agent will confirm at pickup.
- Has unique sound with very low noise -> not proven remotely. Agent will confirm at pickup.
- 25ltr petrol (fuel tank capacity) -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '11kva Elepaq Constant Key Start Generator Sv22000e2', 'category': 'generator', 'price_ngn': 880000, 'is_used': False, 'url': '/ajah/power-equipments/11kva-elepaq-constant-key-start-generator-sv22000e2-x06Q4blb1NXGrSsOQPeAJzgl.html?page=1&pos=10&cur_pos=10&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
