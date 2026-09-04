# Case dpHX9vb2HULjkp6s3r9EQK5W

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0157  |  29961 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, aluminium 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: TAMARIN
- Rating read: 6.5KVA
- Label, plate or settings screen legible: yes
- Damage noted: minor scuff marks on plastic casing, yellow paint slightly faded, tire appears worn but intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | POWER GENERATOR | TAMARIN | 6.5KVA | SILENT TYPE | DC 12V 8.5A | AC 230V 50Hz | OUTPUT: 6.5KVA

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=TAMARIN label=True lines=16
- **retrieval** -> ok. query='ELEPAQ TAMARIN 6.5KVA ELEPAQ POWER GENERATOR TAMARIN 6.5KVA SILENT TYPE DC 12V 8.5A AC 230' hits=['Elepaq SV6800 6.5kVA', 'Elepaq SV2200 2.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Elepaq TAMARIN margin=0.6
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Elepaq SV6800 6.5kVA (0.6)
  - Elepaq SV2200 2.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads 6.5kva but the seller says 15kva. A clear photo of the rating plate on this exact unit would settle it.

## Claims
- [unverifiable_remote] 15kva elepaq generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Elepaq brand generator
- [unverifiable_remote] 100% copper generator
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
**6,853 to 25,100 NGN** (priced as material, width 1.1421, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 30%, circuit_board 10%, rubber 10%, aluminium 10% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 14,625 NGN

Conditions attached to this price:
- Not identified: The item reads 6.5kva but the seller says 15kva. A clear photo of the rating plate on this exact unit would settle it.
- 15kva elepaq generator -> not proven remotely. Agent reads the rating plate.
- Elepaq brand generator -> not proven remotely. Agent will confirm at pickup.
- 100% copper generator -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '15kva Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 700000, 'is_used': False, 'url': '/ikeja/power-equipments/15kva-elepaq-constant-generator-dpHX9vb2HULjkp6s3r9EQK5W.html?page=1&pos=22&cur_pos=22&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
