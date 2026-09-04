# Case kn73bLUE7qEyoly92i3dTFvI

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0188  |  23437 ms

## What the engine saw
- Presentation: single_unit
- Category: engine_component (confidence 0.9)
- Made of: steel 60%, plastic 20%, rubber 10%, copper 10%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: some surface dirt and grime, minor corrosion on metal parts
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 135 1 1W

## Chain
- **read_evidence** -> ok. category=engine_component brand=None model=None label=False lines=1
- **retrieval** -> ok. query='135 1 1W 30kva perkins John holt generator, almost new of 950hrs run. 
With 100% warranty' hits=['Perkins P150 150kVA', 'Perkins P100 100kVA', 'Mikano MK30 30kVA']
- **identify** -> refused. chosen=None None margin=0.0
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Perkins P150 150kVA (0.4333)
  - Perkins P100 100kVA (0.4333)
  - Mikano MK30 30kVA (0.2333)

**Not identified: CANNOT_IDENTIFY.** The image shows only an engine block interior with no legible brand, model, or rating plate. The text fragment '135 1 1W' appears to be a casting or part number, not a brand/model identifier. The seller's claim of 'Perkins 30kVA' does not match any shortlist entry (Perkins options are 100/150kVA, and the 30kVA option is a different brand, Mikano). Without a visible nameplate or serial tag, there is no reliable evidence to confirm brand or model, and the shortlist entries conflict with the seller's own description.

## Claims
- [unverifiable_remote] 30kva capacity generator
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Perkins engine
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] John Holt generator (brand/distributor)
- [unverifiable_remote] Almost new condition
- [unverifiable_remote] Has run for 950 hours
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Comes with 100% warranty
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**5,962 to 25,590 NGN** (priced as material, width 1.2441, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of steel 60%, plastic 20%, rubber 10%, copper 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 19,875 NGN

Conditions attached to this price:
- Not identified: The image shows only an engine block interior with no legible brand, model, or rating plate. The text fragment '135 1 1W' appears to be a casting or part number, not a brand/model identifier. The seller's claim of 'Perkins 30kVA' does not match any shortlist entry (Perkins options are 100/150kVA, and the 30kVA option is a different brand, Mikano). Without a visible nameplate or serial tag, there is no reliable evidence to confirm brand or model, and the shortlist entries conflict with the seller's own description.
- 30kva capacity generator -> not proven remotely. Weigh on the scale and photograph the display.
- Perkins engine -> not proven remotely. Weigh on the scale and photograph the display.
- John Holt generator (brand/distributor) -> not proven remotely. Agent will confirm at pickup.
- Almost new condition -> not proven remotely. Agent will confirm at pickup.
- Has run for 950 hours -> not proven remotely. Weigh on the scale and photograph the display.
- Comes with 100% warranty -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': '30kva John Holt Perkins Generator', 'category': 'generator', 'price_ngn': 4100000, 'is_used': True, 'url': '/alimosho/power-equipments/30kva-john-holt-perkins-generator-kn73bLUE7qEyoly92i3dTFvI.html?page=2&pos=22&cur_pos=22&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
