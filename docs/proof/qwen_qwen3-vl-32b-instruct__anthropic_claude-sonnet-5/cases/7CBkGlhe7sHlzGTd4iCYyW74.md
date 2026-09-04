# Case 7CBkGlhe7sHlzGTd4iCYyW74

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0160  |  18384 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, plastic 40%, circuit_board 10%, glass 10%
- Estimated weight: 0.18 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: Minor scratches on back glass, Camera module slightly raised
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: CEEJA GADGETS | BN: 3753 | CEEA GADGETS NG

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=None label=False lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='Apple CEEJA GADGETS BN: 3753 CEEA GADGETS NG Foreign Used
iPhone 11 128gb 
Color: Red & Mo' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 11 margin=0.63
- **abstain** -> abstain. no label, top score 0.78

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.7667)
  - Apple iPhone 11 Pro (0.5667)
  - Apple iPhone 11 Pro Max (0.5)
  - Apple iPhone XR (0.5)
  - Apple iPhone XS (0.5)

**Not identified: CANNOT_IDENTIFY.** No label, plate or settings screen was legible, and the visual match alone scored only 0.78.

Evidence flags: looks like a catalogue or stock image

## Claims
- [unverifiable_remote] Foreign Used
- [unverifiable_remote] iPhone 11
- [unverifiable_remote] 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Color: Red & More
- [unverifiable_remote] Neatness: 10/10
- [unverifiable_remote] BH 90%+
    priced as: assumed 75 percent. Agent opens the battery health screen
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
**86 to 301 NGN** (priced as material, width 1.1124, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.18 kg of aluminium 40%, plastic 40%, circuit_board 10%, glass 10% (rates for circuit_board, glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 178 NGN

Conditions attached to this price:
- Not identified: No label, plate or settings screen was legible, and the visual match alone scored only 0.78.
- Evidence flag: looks like a catalogue or stock image
- Foreign Used -> not proven remotely. Agent will confirm at pickup.
- iPhone 11 -> not proven remotely. Agent will confirm at pickup.
- 128gb -> not proven remotely. Agent reads storage from Settings.
- Color: Red & More -> not proven remotely. Agent will confirm at pickup.
- Neatness: 10/10 -> not proven remotely. Agent will confirm at pickup.
- BH 90%+ -> not proven remotely. Agent opens the battery health screen.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 11 128 GB Red', 'category': 'phone', 'price_ngn': 249999, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-11-128-gb-red-7CBkGlhe7sHlzGTd4iCYyW74.html?page=1&pos=21&cur_pos=21&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
