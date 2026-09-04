# Case planet-old-tv-indoor-antenna

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0130  |  22946 ms

## What the engine saw
- Presentation: single_unit
- Category: tv_antenna (confidence 0.95)
- Made of: plastic 60%, steel 30%, copper 10%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: PLANET
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, antenna elements appear intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: PLANET | UHF - VHF - FM | TV INDOOR ANTENNA

## Chain
- **read_evidence** -> ok. category=tv_antenna brand=PLANET model=None label=True lines=3
- **retrieval** -> empty. query='PLANET PLANET UHF - VHF - FM TV INDOOR ANTENNA The old TV indoor Antenna might still be wo' hits=[]
- **identify** -> refused. chosen=Planet None margin=None
- **abstain** -> abstain. model refused

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** Brand 'PLANET' and product type (UHF/VHF/FM indoor TV antenna) are clearly legible, but no specific model number or code is printed on the item, and no catalogue entries were provided to match against.

## Claims
- [unverifiable_remote] The item is a TV indoor antenna.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The antenna is old.
- [unverifiable_remote] The antenna might still be working.
    priced as: assumed not working. Agent powers the item on before payment
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**181 to 794 NGN** (priced as material, width 1.2558, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.5 kg of plastic 60%, steel 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 605 NGN

Conditions attached to this price:
- Not identified: Brand 'PLANET' and product type (UHF/VHF/FM indoor TV antenna) are clearly legible, but no specific model number or code is printed on the item, and no catalogue entries were provided to match against.
- The item is a TV indoor antenna. -> not proven remotely. Weigh on the scale and photograph the display.
- The antenna is old. -> not proven remotely. Agent will confirm at pickup.
- The antenna might still be working. -> not proven remotely. Agent powers the item on before payment.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Planet old TV Indoor Antenna', 'category': None, 'site_category': 'E-waste', 'price_ngn': 1300, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/planet-old-tv-indoor-antenna/'}`
