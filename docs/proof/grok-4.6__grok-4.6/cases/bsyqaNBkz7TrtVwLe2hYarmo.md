# Case bsyqaNBkz7TrtVwLe2hYarmo

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0134  |  96362 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: mixed_electronic 50%, glass 15%, aluminium 15%, paper 15%, plastic 5%
- Estimated weight: 0.5 kg (confidence 0.65)
- Brand read off the item: Google
- Model read off the item: Pixel Fold
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Google | Pixel Fold | 25%

## Chain
- **read_evidence** -> ok. category=phone brand=Google model=Pixel Fold label=True lines=3
- **retrieval** -> ok. query='Google Pixel Fold Google Pixel Fold 25% Latest Google pixel fold 256gb 
Available in store' hits=['Google Pixel 7', 'Google Pixel 8', 'Google Pixel 9']
- **identify** -> ok. chosen=Google Pixel Fold margin=None
- **abstain** -> pass. top=0.98 margin=None

## Identification
Shortlist from the catalogue:
  - Google Pixel 7 (0.5)
  - Google Pixel 8 (0.5)
  - Google Pixel 9 (0.5)

**Answer: Google Pixel Fold** (margin None)

## Claims
- [unverifiable_remote] Latest Google pixel fold
- [unverified] 256gb
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
**82,098 to 695,800 NGN** (priced as a working item, width 1.5778, method uncalibrated_wide, 12 comparable prices)

12 used asking prices, 20th to 80th percentile 292,000 to 994,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.6248 for unproven claims, floored at the scrap value 333.

Scrap floor: 333 NGN

Conditions attached to this price:
- Latest Google pixel fold -> not proven remotely. Agent will confirm at pickup.
- 256gb -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Google Pixel Fold 256 GB White', 'category': 'phone', 'price_ngn': 530000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-google-pixel-fold-256-gb-white-bsyqaNBkz7TrtVwLe2hYarmo.html?page=1&pos=20&cur_pos=20&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
