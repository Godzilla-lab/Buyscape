# Case 1tZaskvlnNM0IW2cxGQHddSL

Photos: 4  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0167  |  20450 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, plastic 30%, circuit_board 20%, glass 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 13 Pro Max
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: APPLE WARRANTY | Face ID: WORK | CONDITION: A-1 | BATTERY: 100% | VERSION: 16.3 | NO LCD WARRANTY | SN: D7YF28A0LJZS | IMEI: 358561097601222

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 13 Pro Max label=True lines=10
- **retrieval** -> ok. query='Apple iPhone 13 Pro Max APPLE WARRANTY Face ID: WORK CONDITION: A-1 BATTERY: 100% VERSION:' hits=['Apple iPhone 13 Pro', 'Apple iPhone 13 Pro Max', 'Apple iPhone 13', 'Apple iPhone 14 Pro', 'Apple iPhone 14 Pro Max']
- **identify** -> ok. chosen=Apple iPhone 13 Pro Max margin=0.8
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Apple iPhone 13 Pro (0.9)
  - Apple iPhone 13 Pro Max (0.9)
  - Apple iPhone 13 (0.7667)
  - Apple iPhone 14 Pro (0.7)
  - Apple iPhone 14 Pro Max (0.7)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads as Apple iPhone 13 Pro Max but the seller's text says 14. A Settings or About screen would settle it.

## Claims
- [unverifiable_remote] Model is iPhone 14 Pro
- [unverified] Storage capacity of 256GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Storage capacity of 128GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Available in ash colour
- [unverifiable_remote] Available in sky blue colour
- [unverifiable_remote] Item is a Direct UK import
- [unverifiable_remote] Item is used
- [unverifiable_remote] Condition is described as very good
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the phone.
- [unverified] Required evidence 'front_screen_on' was not supplied
    priced as: priced as if the worst case is true. Photo of the front with the screen switched on, showing the home screen.
- [unverified] Required evidence 'back' was not supplied
    priced as: priced as if the worst case is true. Photo of the back of the phone.
- [unverified] Required evidence 'settings_about' was not supplied
    priced as: priced as if the worst case is true. Screenshot of Settings then About, showing the model name and storage.
- [unverified] Required evidence 'imei_dial' was not supplied
    priced as: priced as if the worst case is true. Dial *#06# and screenshot the IMEI that appears.

## Price
**93 to 411 NGN** (priced as material, width 1.2628, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of aluminium 40%, plastic 30%, circuit_board 20%, glass 10% (rates for circuit_board, glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 226 NGN

Conditions attached to this price:
- Not identified: The item reads as Apple iPhone 13 Pro Max but the seller's text says 14. A Settings or About screen would settle it.
- Model is iPhone 14 Pro -> not proven remotely. Agent will confirm at pickup.
- Storage capacity of 256GB -> not proven remotely. Agent reads storage from Settings.
- Storage capacity of 128GB -> not proven remotely. Agent reads storage from Settings.
- Available in ash colour -> not proven remotely. Agent will confirm at pickup.
- Available in sky blue colour -> not proven remotely. Agent will confirm at pickup.
- Item is a Direct UK import -> not proven remotely. Agent will confirm at pickup.
- Item is used -> not proven remotely. Agent will confirm at pickup.
- Condition is described as very good -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 14 Pro 256 GB White', 'category': 'phone', 'price_ngn': 680000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-14-pro-256-gb-white-1tZaskvlnNM0IW2cxGQHddSL.html?page=1&pos=1&cur_pos=1&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
