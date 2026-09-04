# Case hePh6idIFypsvAdj22llUCZm

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0157  |  20385 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: plastic 70%, steel 20%, circuit_board 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 12
- Rating read: 128GB
- Label, plate or settings screen legible: yes
- Damage noted: Minor smudges on back cover, No visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: iPhone 12 | A2399 | Model A2399 | Serial Number: FQJW64G8T2FV | Made in China | Apple Inc. | www.apple.com | IMEI: 358052090000000

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 12 label=True lines=11
- **retrieval** -> ok. query='Apple iPhone 12 128GB iPhone 12 A2399 Model A2399 Serial Number: FQJW64G8T2FV Made in Chin' hits=['Apple iPhone 12', 'Apple iPhone 12 Pro', 'Apple iPhone 12 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 12 margin=0.9
- **abstain** -> pass. top=0.95 margin=0.9

## Identification
Shortlist from the catalogue:
  - Apple iPhone 12 (0.7667)
  - Apple iPhone 12 Pro (0.5667)
  - Apple iPhone 12 Pro Max (0.5)
  - Apple iPhone XR (0.5)
  - Apple iPhone XS (0.5)

**Answer: Apple iPhone 12 128GB** (margin 0.9)

## Claims
- [unverifiable_remote] Foreign Used Grade A++
- [unverifiable_remote] iPhone 12
- [unverifiable_remote] 64GB & 128GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Neatness: 10/10
- [unverifiable_remote] Screen: 10/10
    priced as: assumed replaced screen. Agent inspects the bezel and display panel
- [unverifiable_remote] Body: 10/10
- [unverifiable_remote] BH:...
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
**24 to 129 NGN** (priced as material, width 1.3585, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3857 for unproven claims.

Scrap floor: 64 NGN

Conditions attached to this price:
- Foreign Used Grade A++ -> not proven remotely. Agent will confirm at pickup.
- iPhone 12 -> not proven remotely. Agent will confirm at pickup.
- 64GB & 128GB -> not proven remotely. Agent reads storage from Settings.
- Neatness: 10/10 -> not proven remotely. Agent will confirm at pickup.
- Screen: 10/10 -> not proven remotely. Agent inspects the bezel and display panel.
- Body: 10/10 -> not proven remotely. Agent will confirm at pickup.
- BH:... -> not proven remotely. Agent opens the battery health screen.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 12 128 GB Blue', 'category': 'phone', 'price_ngn': 329999, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-12-128-gb-blue-hePh6idIFypsvAdj22llUCZm.html?page=1&pos=11&cur_pos=11&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
