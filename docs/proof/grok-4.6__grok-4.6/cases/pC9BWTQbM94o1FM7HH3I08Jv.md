# Case pC9BWTQbM94o1FM7HH3I08Jv

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0141  |  120065 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.92)
- Made of: mixed_electronic 55%, glass 15%, paper 15%, plastic 10%, aluminium 5%
- Estimated weight: 0.5 kg (confidence 0.55)
- Brand read off the item: SAMSUNG
- Model read off the item: S20+ 5G
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SAMSUNG | Galaxy S20+ 5G | S20 | S20+ 5G | S20 ULTRA 5G

## Chain
- **read_evidence** -> ok. category=phone brand=SAMSUNG model=S20+ 5G label=True lines=5
- **retrieval** -> ok. query='SAMSUNG S20+ 5G SAMSUNG Galaxy S20+ 5G S20 S20+ 5G S20 ULTRA 5G Samsung galaxy S20 plus 5G' hits=['Samsung Galaxy S21', 'Samsung Galaxy S22', 'Samsung Galaxy S23', 'Samsung Galaxy S24', 'Samsung Galaxy S25']
- **identify** -> ok. chosen=Samsung Galaxy S20+ 5G margin=None
- **abstain** -> pass. top=0.95 margin=None

## Identification
Shortlist from the catalogue:
  - Samsung Galaxy S21 (0.5)
  - Samsung Galaxy S22 (0.5)
  - Samsung Galaxy S23 (0.5)
  - Samsung Galaxy S24 (0.5)
  - Samsung Galaxy S25 (0.5)

**Answer: Samsung Galaxy S20+ 5G** (margin None)

## Claims
- [unverifiable_remote] Samsung galaxy S20 plus 5G
- [unverified] 256GB
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
**53,982 to 191,100 NGN** (priced as a working item, width 1.1189, method uncalibrated_wide, 2 comparable prices)

2 used asking prices, 20th to 80th percentile 192,000 to 273,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.6248 for unproven claims, floored at the scrap value 253.

Scrap floor: 253 NGN

Conditions attached to this price:
- Samsung galaxy S20 plus 5G -> not proven remotely. Agent will confirm at pickup.
- 256GB -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Samsung Galaxy S20+ 5G 256 GB Black', 'category': 'phone', 'price_ngn': 270000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-samsung-galaxy-s20-5g-256-gb-black-pC9BWTQbM94o1FM7HH3I08Jv.html?page=1&pos=7&cur_pos=7&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
