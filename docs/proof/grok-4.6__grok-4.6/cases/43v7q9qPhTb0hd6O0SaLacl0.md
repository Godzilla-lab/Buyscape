# Case 43v7q9qPhTb0hd6O0SaLacl0

Photos: 3  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0154  |  162333 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: mixed_electronic 45%, glass 25%, aluminium 20%, plastic 10%
- Estimated weight: 0.2 kg (confidence 0.7)
- Brand read off the item: APPLE
- Model read off the item: nothing legible
- Rating read: 128GB
- Label, plate or settings screen legible: yes
- Damage noted: seller stickers covering the back, plastic film or wrap on edges
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 12P 128G | APPLE WARRANTY | NO LCD WARRANTY | 128G | 13PRO | 128GB

## Chain
- **read_evidence** -> ok. category=phone brand=APPLE model=None label=True lines=6
- **retrieval** -> ok. query='APPLE 128GB 12P 128G APPLE WARRANTY NO LCD WARRANTY 128G 13PRO 128GB 13 pro 128gb
Nml 13 1' hits=['Apple iPhone 13 Pro', 'Apple iPhone 13 Pro Max', 'Apple iPhone 11 Pro', 'Apple iPhone 12 Pro', 'Apple iPhone 13']
- **identify** -> refused. chosen=None None margin=0.0
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Apple iPhone 13 Pro (0.5667)
  - Apple iPhone 13 Pro Max (0.5)
  - Apple iPhone 11 Pro (0.4333)
  - Apple iPhone 12 Pro (0.4333)
  - Apple iPhone 13 (0.4333)

**Not identified: CANNOT_IDENTIFY.** Printed and handwritten labels on the device itself conflict (12P 128G vs 13PRO / 13pro 128gb). Seller text is also mixed. No single catalogue model is supported by the readable evidence.

## Claims
- [unverifiable_remote] 13 pro 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Nml 13 128gb
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
**81 to 261 NGN** (priced as material, width 1.0473, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of mixed_electronic 45%, glass 25%, aluminium 20%, plastic 10% (rates for glass, mixed_electronic, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 146 NGN

Conditions attached to this price:
- Not identified: Printed and handwritten labels on the device itself conflict (12P 128G vs 13PRO / 13pro 128gb). Seller text is also mixed. No single catalogue model is supported by the readable evidence.
- 13 pro 128gb -> not proven remotely. Agent reads storage from Settings.
- Nml 13 128gb -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 13 128 GB White', 'category': 'phone', 'price_ngn': 380000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-13-128-gb-white-43v7q9qPhTb0hd6O0SaLacl0.html?page=1&pos=2&cur_pos=2&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
