# Case pIH0HyBnwfwDLvyCaPavJShA

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0152  |  105434 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 50%, plastic 20%, aluminium 15%, copper 10%, rubber 5%
- Estimated weight: 65.0 kg (confidence 0.4)
- Brand read off the item: SENWEI
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SENWEI

## Chain
- **read_evidence** -> ok. category=generator brand=SENWEI model=None label=False lines=1
- **retrieval** -> ok. query='SENWEI SENWEI Senwei 3.5kva Petrol Generator, available in Quantity. Wholesale price. Sell' hits=['Senwei SW3500 3.5kVA', 'Lutian LT3900 3.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> refused. chosen=None None margin=0.4
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Senwei SW3500 3.5kVA (0.7)
  - Lutian LT3900 3.5kVA (0.3)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Only the brand SENWEI is literally legible on the casing. Model, serial and rating plate are not readable (label/plate reported not legible). Seller 3.5kVA claim and the matching shortlist row are not printed on the item, so the specific model cannot be confirmed.

## Claims
- [unverifiable_remote] Senwei
- [unverified] 3.5kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Petrol Generator
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
**60,673 to 135,915 NGN** (priced as material, width 0.7655, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 65 kg of steel 50%, plastic 20%, aluminium 15%, copper 10%, rubber 5% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 102,212 NGN

Conditions attached to this price:
- Not identified: Only the brand SENWEI is literally legible on the casing. Model, serial and rating plate are not readable (label/plate reported not legible). Seller 3.5kVA claim and the matching shortlist row are not printed on the item, so the specific model cannot be confirmed.
- Senwei -> not proven remotely. Agent will confirm at pickup.
- 3.5kva -> not proven remotely. Agent reads the rating plate.
- Petrol Generator -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'SENWEI 3.5kva 3kva Petrol Generator', 'category': 'generator', 'price_ngn': 185000, 'is_used': False, 'url': '/lagos/power-equipments/senwei-3-5kva-3kva-petrol-generator-pIH0HyBnwfwDLvyCaPavJShA.html?page=2&pos=3&cur_pos=3&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
