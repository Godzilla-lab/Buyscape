# Case zcyInfAFXpVsgc4gBZej8tai

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0137  |  138482 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: mixed_electronic 50%, glass 25%, aluminium 15%, paper 5%, plastic 5%
- Estimated weight: 0.45 kg (confidence 0.55)
- Brand read off the item: nothing legible
- Model read off the item: GALAXY S23 ULTRA
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: GALAXY S23 ULTRA | 24 MONTHS WARRANTY

## Chain
- **read_evidence** -> ok. category=phone brand=None model=GALAXY S23 ULTRA label=True lines=2
- **retrieval** -> ok. query='GALAXY S23 ULTRA GALAXY S23 ULTRA 24 MONTHS WARRANTY Brand New Samsung Galaxy S23 Ultra 51' hits=['Samsung Galaxy S23', 'Samsung Galaxy S21', 'Samsung Galaxy S22', 'Samsung Galaxy S24', 'Samsung Galaxy S25']
- **identify** -> ok. chosen=Samsung Galaxy S23 Ultra margin=None
- **abstain** -> pass. top=0.92 margin=None

## Identification
Shortlist from the catalogue:
  - Samsung Galaxy S23 (0.9)
  - Samsung Galaxy S21 (0.5)
  - Samsung Galaxy S22 (0.5)
  - Samsung Galaxy S24 (0.5)
  - Samsung Galaxy S25 (0.5)

**Answer: Samsung Galaxy S23 Ultra** (margin None)

## Claims
- [unverifiable_remote] Brand New
- [unverifiable_remote] Samsung Galaxy S23 Ultra
- [unverified] 512GB
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
**136,765 to 511,000 NGN** (priced as a working item, width 1.1555, method uncalibrated_wide, 7 comparable prices)

7 used asking prices, 20th to 80th percentile 512,000 to 730,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.5936 for unproven claims, floored at the scrap value 298.

Scrap floor: 298 NGN

Conditions attached to this price:
- Brand New -> not proven remotely. Agent will confirm at pickup.
- Samsung Galaxy S23 Ultra -> not proven remotely. Agent will confirm at pickup.
- 512GB -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Samsung Galaxy S23 Ultra 512 GB Green', 'category': 'phone', 'price_ngn': 700000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-samsung-galaxy-s23-ultra-512-gb-green-zcyInfAFXpVsgc4gBZej8tai.html?page=2&pos=15&cur_pos=15&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
