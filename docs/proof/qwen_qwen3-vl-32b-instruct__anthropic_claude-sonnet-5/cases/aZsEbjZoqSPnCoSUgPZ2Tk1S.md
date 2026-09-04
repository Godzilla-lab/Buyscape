# Case aZsEbjZoqSPnCoSUgPZ2Tk1S

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0166  |  19887 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, glass 30%, plastic 20%, circuit_board 10%
- Estimated weight: 0.18 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 11
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: minor scratches on back glass, slight wear around edges
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: POSTED ON JI | MANNY STORES

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 11 label=False lines=2
- **retrieval** -> ok. query='Apple iPhone 11 POSTED ON JI MANNY STORES Clean Direct UK used iPhone 11 64gb
Factory unlo' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 11 margin=0.7
- **abstain** -> pass. top=0.9 margin=0.7

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.7667)
  - Apple iPhone 11 Pro (0.5667)
  - Apple iPhone 11 Pro Max (0.5)
  - Apple iPhone XR (0.5)
  - Apple iPhone XS (0.5)

**Answer: Apple iPhone 11 PRODUCT(RED) 64GB** (margin 0.7)

## Claims
- [unverifiable_remote] iPhone 11
- [unverifiable_remote] 64gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Factory unlocked
    priced as: assumed still locked to the previous account. Seller signs out of iCloud or Google before payment
- [unverifiable_remote] Battery health 100% (Not Boosted)
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverifiable_remote] Used
- [unverifiable_remote] Clean Direct UK
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
**52 to 297 NGN** (priced as material, width 1.3975, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 175 NGN

Conditions attached to this price:
- iPhone 11 -> not proven remotely. Agent will confirm at pickup.
- 64gb -> not proven remotely. Agent reads storage from Settings.
- Factory unlocked -> not proven remotely. Seller signs out of iCloud or Google before payment.
- Battery health 100% (Not Boosted) -> not proven remotely. Agent opens the battery health screen.
- Used -> not proven remotely. Agent will confirm at pickup.
- Clean Direct UK -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 11 64 GB Red', 'category': 'phone', 'price_ngn': 205000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-11-64-gb-red-aZsEbjZoqSPnCoSUgPZ2Tk1S.html?page=2&pos=8&cur_pos=8&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
