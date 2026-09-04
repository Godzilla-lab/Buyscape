# Case CA2VNggUjKw9a4P5FnwvlS59

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0177  |  24789 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 30%, plastic 50%, circuit_board 10%, glass 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 13 Pro Max
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: No visible damage to back panel or camera module, Minor smudges on glass back
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: iPhone 13 Pro Max | A2466 | MLLQ3LL/A | Made in China | Model: A2466 | IMEI: 358740090000000 | Serial Number: FVJH2W2GZT | Apple Inc.

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 13 Pro Max label=True lines=9
- **retrieval** -> ok. query='Apple iPhone 13 Pro Max iPhone 13 Pro Max A2466 MLLQ3LL/A Made in China Model: A2466 IMEI:' hits=['Apple iPhone 13 Pro', 'Apple iPhone 13 Pro Max', 'Apple iPhone 13', 'Apple iPhone 14', 'Apple iPhone 11 Pro Max']
- **identify** -> ok. chosen=Apple iPhone 13 Pro Max margin=0.9
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Apple iPhone 13 Pro (0.9)
  - Apple iPhone 13 Pro Max (0.9)
  - Apple iPhone 13 (0.7667)
  - Apple iPhone 14 (0.6333)
  - Apple iPhone 11 Pro Max (0.6)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads as Apple iPhone 13 Pro Max but the seller's text says 14. A Settings or About screen would settle it.

## Claims
- [unverifiable_remote] iPhone 14 Pro
- [unverifiable_remote] 128GB storage capacity
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 98% battery health
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverifiable_remote] Dual SIM capability
- [unverifiable_remote] Gold color
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
**81 to 279 NGN** (priced as material, width 1.0966, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of aluminium 30%, plastic 50%, circuit_board 10%, glass 10% (rates for circuit_board, glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 160 NGN

Conditions attached to this price:
- Not identified: The item reads as Apple iPhone 13 Pro Max but the seller's text says 14. A Settings or About screen would settle it.
- iPhone 14 Pro -> not proven remotely. Agent will confirm at pickup.
- 128GB storage capacity -> not proven remotely. Agent reads storage from Settings.
- 98% battery health -> not proven remotely. Agent opens the battery health screen.
- Dual SIM capability -> not proven remotely. Agent will confirm at pickup.
- Gold color -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 14 Pro 128 GB Gold', 'category': 'phone', 'price_ngn': 580000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-14-pro-128-gb-gold-CA2VNggUjKw9a4P5FnwvlS59.html?page=1&pos=9&cur_pos=9&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
