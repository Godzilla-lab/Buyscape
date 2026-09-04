# Case dpHX9vb2HULjkp6s3r9EQK5W

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0152  |  137858 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 50%, plastic 18%, aluminium 12%, copper 10%, rubber 8%, mixed_electronic 2%
- Estimated weight: 70.0 kg (confidence 0.45)
- Brand read off the item: ELEPAQ
- Model read off the item: TA6500
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | QUALITY GENERATOR | TA6500 | CONSTANT | CE | SV2500E3

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=TA6500 label=True lines=6
- **retrieval** -> ok. query='ELEPAQ TA6500 ELEPAQ QUALITY GENERATOR TA6500 CONSTANT CE SV2500E3 15kva elepaq generator ' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> refused. chosen=None None margin=0.05
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Not identified: CANNOT_IDENTIFY.** Housing and panel show two different model strings (TA6500 and SV2500E3) that conflict with each other and with both shortlist entries. Seller 15kVA claim also does not match the markings or the size of the unit.

## Claims
- [unverified] 15kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] elepaq generator
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
**50,055 to 142,128 NGN** (priced as material, width 0.9582, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 70 kg of steel 50%, plastic 18%, aluminium 12%, copper 10%, rubber 8%, mixed_electronic 2% (rates for mixed_electronic, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 106,820 NGN

Conditions attached to this price:
- Not identified: Housing and panel show two different model strings (TA6500 and SV2500E3) that conflict with each other and with both shortlist entries. Seller 15kVA claim also does not match the markings or the size of the unit.
- 15kva -> not proven remotely. Agent reads the rating plate.
- elepaq generator -> not proven remotely. Agent will confirm at pickup.
- 100% copper generator -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '15kva Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 700000, 'is_used': False, 'url': '/ikeja/power-equipments/15kva-elepaq-constant-generator-dpHX9vb2HULjkp6s3r9EQK5W.html?page=1&pos=22&cur_pos=22&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
