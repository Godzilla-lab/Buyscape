# Case wVYdKMzv24ZvT24fUyDVPyRs

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0209  |  27891 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: BY3200ES
- Rating read: 2.8kW/3.5kVA
- Label, plate or settings screen legible: yes
- Damage noted: Minor dust and grime on surface, Some wear on yellow paint near handle, Tire appears slightly underinflated
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | YADENI | POWER CONSTANT | MODEL NO. BY3200ES | OUTPUT: 2.8kW/3.5kVA | VOLTAGE: 220V | FREQUENCY: 50Hz | ENGINE: 178cc

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=BY3200ES label=True lines=17
- **retrieval** -> ok. query='ELEPAQ BY3200ES 2.8kW/3.5kVA ELEPAQ YADENI POWER CONSTANT MODEL NO. BY3200ES OUTPUT: 2.8kW' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA', 'Maxmech MX10000 10kVA']
- **identify** -> refused. chosen=None None margin=0.2
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.6)
  - Elepaq SV6800 6.5kVA (0.55)
  - Lutian LT3900 3.5kVA (0.3)
  - Senwei SW3500 3.5kVA (0.3)
  - Maxmech MX10000 10kVA (0.2333)

**Not identified: CANNOT_IDENTIFY.** The nameplate clearly reads brand ELEPAQ, model BY3200ES, rated 2.8kW/3.5kVA, but none of the shortlisted catalogue entries match this exact model or rating combination. The seller's claim of '10KVA' directly contradicts the legible plate rating (3.5kVA), and the shortlist's Elepaq SV2200/SV6800 models don't match the read model number or output. Insufficient consistent evidence to confidently map to any shortlist entry.

## Claims
- [unverifiable_remote] ELEPAQ 10KVA generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Built with copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] Long-lasting
- [unverifiable_remote] Delivers stable and efficient power
    priced as: assumed does not start. Agent starts the generator and runs it under load
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
**10,387 to 50,100 NGN** (priced as material, width 1.3131, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 30%, circuit_board 10%, rubber 10%, copper 10% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 34,625 NGN

Conditions attached to this price:
- Not identified: The nameplate clearly reads brand ELEPAQ, model BY3200ES, rated 2.8kW/3.5kVA, but none of the shortlisted catalogue entries match this exact model or rating combination. The seller's claim of '10KVA' directly contradicts the legible plate rating (3.5kVA), and the shortlist's Elepaq SV2200/SV6800 models don't match the read model number or output. Insufficient consistent evidence to confidently map to any shortlist entry.
- ELEPAQ 10KVA generator -> not proven remotely. Agent reads the rating plate.
- Built with copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Long-lasting -> not proven remotely. Agent will confirm at pickup.
- Delivers stable and efficient power -> not proven remotely. Agent starts the generator and runs it under load.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '10kva Elepaq Generator – Ideal for Home Appliances', 'category': 'generator', 'price_ngn': 768000, 'is_used': False, 'url': '/badagry/power-equipments/10kva-elepaq-generator-ideal-for-home-appliances-wVYdKMzv24ZvT24fUyDVPyRs.html?page=1&pos=6&cur_pos=6&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
