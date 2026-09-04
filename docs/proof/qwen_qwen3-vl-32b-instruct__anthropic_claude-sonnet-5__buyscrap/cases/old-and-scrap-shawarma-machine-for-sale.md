# Case old-and-scrap-shawarma-machine-for-sale

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0203  |  31687 ms

## What the engine saw
- Presentation: single_unit
- Category: industrial heater or oven (confidence 0.7)
- Made of: steel 70%, copper 20%, plastic 10%
- Estimated weight: 15.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: rust and corrosion on metal surfaces, dirt and grime buildup, worn and frayed power cord
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **read_evidence** -> ok. category=industrial heater or oven brand=None model=None label=False lines=0
- **retrieval** -> empty. query='A client has a used and locally made shawarma machine that uses gas. The last known condit' hits=[]
- **identify** -> ok. chosen=Unbranded Locally-made gas shawarma machine margin=None
- **abstain** -> abstain. top score 0.4

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.4, which is not sure enough to price.

## Claims
- [unverifiable_remote] Used shawarma machine
- [unverifiable_remote] Locally made
- [unverifiable_remote] Uses gas
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Last known condition is that it works perfectly okay
    priced as: assumed not working. Agent powers the item on before payment
- [unverifiable_remote] This wasn't tested
- [unverifiable_remote] The item is sold as scrap
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**10,620 to 45,570 NGN** (priced as material, width 1.244, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of steel 70%, copper 20%, plastic 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 35,400 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.4, which is not sure enough to price.
- Used shawarma machine -> not proven remotely. Agent will confirm at pickup.
- Locally made -> not proven remotely. Agent will confirm at pickup.
- Uses gas -> not proven remotely. Weigh on the scale and photograph the display.
- Last known condition is that it works perfectly okay -> not proven remotely. Agent powers the item on before payment.
- This wasn't tested -> not proven remotely. Agent will confirm at pickup.
- The item is sold as scrap -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Old and scrap shawarma machine for sale', 'category': None, 'site_category': 'Industrial Machines', 'price_ngn': 50000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/old-and-scrap-shawarma-machine-for-sale/'}`
