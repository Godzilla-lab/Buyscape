# Case 43v7q9qPhTb0hd6O0SaLacl0

Photos: 3  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0282  |  35102 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, plastic 40%, circuit_board 10%, glass 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 13 Pro Max
- Rating read: 128GB
- Label, plate or settings screen legible: yes
- Damage noted: Minor scuffs on the back casing, Label partially covering the camera module
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: APPLE WARRANTY | NO C.O. WARRANTY | MODEL: iPhone 13 Pro Max | IMEI: 35768710131701 | SERIAL NO: DQF2YXHJLZP | COLOR: Graphite | STORAGE: 128GB | RAM: 6GB

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 13 Pro Max label=True lines=16
- **retrieval** -> ok. query='Apple iPhone 13 Pro Max 128GB APPLE WARRANTY NO C.O. WARRANTY MODEL: iPhone 13 Pro Max IME' hits=['Apple iPhone 13 Pro', 'Apple iPhone 13 Pro Max', 'Apple iPhone 13', 'Apple iPhone 11 Pro Max', 'Apple iPhone 12 Pro Max']
- **identify** -> ok. chosen=Apple iPhone 13 Pro Max margin=0.27
- **abstain** -> abstain. top score 0.62

## Identification
Shortlist from the catalogue:
  - Apple iPhone 13 Pro (0.9)
  - Apple iPhone 13 Pro Max (0.9)
  - Apple iPhone 13 (0.7667)
  - Apple iPhone 11 Pro Max (0.6)
  - Apple iPhone 12 Pro Max (0.6)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.62, which is not sure enough to price.

## Claims
- [unverified] 13 pro 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 13 pro 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Nml 13 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Nml 13 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
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
**80 to 335 NGN** (priced as material, width 1.2286, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of aluminium 40%, plastic 40%, circuit_board 10%, glass 10% (rates for circuit_board, glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 198 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.62, which is not sure enough to price.
- 13 pro 128gb -> not proven remotely. Agent reads storage from Settings.
- 13 pro 128gb -> not proven remotely. Agent reads storage from Settings.
- Nml 13 128gb -> not proven remotely. Agent reads storage from Settings.
- Nml 13 128gb -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 13 128 GB White', 'category': 'phone', 'price_ngn': 380000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-13-128-gb-white-43v7q9qPhTb0hd6O0SaLacl0.html?page=1&pos=2&cur_pos=2&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
