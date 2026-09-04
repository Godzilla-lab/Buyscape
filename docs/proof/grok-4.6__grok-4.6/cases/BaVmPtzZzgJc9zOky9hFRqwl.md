# Case BaVmPtzZzgJc9zOky9hFRqwl

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0130  |  126929 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.92)
- Made of: mixed_electronic 40%, glass 25%, plastic 25%, aluminium 10%
- Estimated weight: 0.35 kg (confidence 0.55)
- Brand read off the item: Galaxy
- Model read off the item: A17
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Galaxy | A17

## Chain
- **read_evidence** -> ok. category=phone brand=Galaxy model=A17 label=False lines=2
- **retrieval** -> ok. query='Galaxy A17 Galaxy A17 SAMSUNG GALAXY A17 256GB 8GB RAM' hits=['Samsung Galaxy S21', 'Samsung Galaxy S22', 'Samsung Galaxy S23', 'Samsung Galaxy S24', 'Samsung Galaxy S25']
- **identify** -> ok. chosen=Samsung Galaxy A17 margin=None
- **abstain** -> pass. top=0.95 margin=None

## Identification
Shortlist from the catalogue:
  - Samsung Galaxy S21 (0.5)
  - Samsung Galaxy S22 (0.5)
  - Samsung Galaxy S23 (0.5)
  - Samsung Galaxy S24 (0.5)
  - Samsung Galaxy S25 (0.5)

**Answer: Samsung Galaxy A17** (margin None)

## Claims
- [unverifiable_remote] SAMSUNG GALAXY A17
- [unverified] 256GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 8GB RAM
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
**94 to 335 NGN** (priced as material, width 1.118, method scrap_band_only, 1 comparable prices)

No usable comparable sales (1 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.5311 for unproven claims.

Scrap floor: 178 NGN

Conditions attached to this price:
- SAMSUNG GALAXY A17 -> not proven remotely. Agent will confirm at pickup.
- 256GB -> not proven remotely. Agent reads storage from Settings.
- 8GB RAM -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Samsung Galaxy A17 256 GB Gray', 'category': 'phone', 'price_ngn': 370000, 'is_used': False, 'url': '/apapa/mobile-phones/new-samsung-galaxy-a17-256-gb-gray-BaVmPtzZzgJc9zOky9hFRqwl.html?page=2&pos=20&cur_pos=20&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
