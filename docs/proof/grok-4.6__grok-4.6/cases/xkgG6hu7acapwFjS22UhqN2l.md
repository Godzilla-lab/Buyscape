# Case xkgG6hu7acapwFjS22UhqN2l

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0149  |  108006 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 45%, aluminium 25%, copper 12%, plastic 13%, rubber 5%
- Estimated weight: 45.0 kg (confidence 0.5)
- Brand read off the item: ELEPAQ
- Model read off the item: Y4000W
- Rating read: Y4000W
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | GASOLINE GENERATOR | GT | Y4000W | CE | CONSTANT

## Chain
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=Y4000W label=True lines=6
- **retrieval** -> ok. query='ELEPAQ Y4000W Y4000W ELEPAQ GASOLINE GENERATOR GT Y4000W CE CONSTANT Elepaq constant 4.5kv' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=ELEPAQ Y4000W margin=0.0
- **abstain** -> abstain. top score 0.0

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.55)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.0, which is not sure enough to price.

## Claims
- [unverifiable_remote] Elepaq
- [unverified] constant 4.5kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] 4.5kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] generator
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
**44,054 to 117,378 NGN** (priced as material, width 0.9084, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 45 kg of steel 45%, aluminium 25%, copper 12%, plastic 13%, rubber 5% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 87,322 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.0, which is not sure enough to price.
- Elepaq -> not proven remotely. Agent will confirm at pickup.
- constant 4.5kva -> not proven remotely. Agent reads the rating plate.
- 4.5kva -> not proven remotely. Agent reads the rating plate.
- generator -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Elepaq Constant 4.5 Kva Generator', 'category': 'generator', 'price_ngn': 270000, 'is_used': False, 'url': '/ojo/power-equipments/elepaq-constant-4-5-kva-generator-xkgG6hu7acapwFjS22UhqN2l.html?page=1&pos=12&cur_pos=12&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
