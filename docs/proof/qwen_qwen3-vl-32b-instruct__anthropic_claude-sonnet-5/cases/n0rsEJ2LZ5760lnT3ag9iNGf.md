# Case n0rsEJ2LZ5760lnT3ag9iNGf

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0145  |  20824 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.9)
- Made of: steel 70%, plastic 20%, rubber 10%
- Estimated weight: 500.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: rust on lower right panel and around vents, dents and scratches on white casing, worn paint
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **read_evidence** -> ok. category=generator brand=None model=None label=False lines=0
- **retrieval** -> empty. query='FOR SALE — 200KVA CUMMINS DIESEL GENERATOR 
Looking for a powerful, reliable and heavy-dut' hits=[]
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No brand, model, or rating plate is legible in the image. The seller's text claims Cummins 200KVA, but this cannot be visually confirmed from the photo, which only shows a generic white canopy-style generator housing with no visible manufacturer markings.

## Claims
- [unverified] 200KVA generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Cummins diesel generator
- [unverifiable_remote] Diesel generator
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
**111,300 to 233,000 NGN** (priced as material, width 0.7069, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 500 kg of steel 70%, plastic 20%, rubber 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 187,500 NGN

Conditions attached to this price:
- Not identified: No brand, model, or rating plate is legible in the image. The seller's text claims Cummins 200KVA, but this cannot be visually confirmed from the photo, which only shows a generic white canopy-style generator housing with no visible manufacturer markings.
- 200KVA generator -> not proven remotely. Agent reads the rating plate.
- Cummins diesel generator -> not proven remotely. Agent will confirm at pickup.
- Diesel generator -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Diesel Generator', 'category': 'generator', 'price_ngn': 15000000, 'is_used': True, 'url': '/ikeja/power-equipments/diesel-generator-n0rsEJ2LZ5760lnT3ag9iNGf.html?page=1&pos=4&cur_pos=4&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
