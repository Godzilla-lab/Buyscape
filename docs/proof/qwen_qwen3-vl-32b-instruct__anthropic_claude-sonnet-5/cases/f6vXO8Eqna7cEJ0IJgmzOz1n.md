# Case f6vXO8Eqna7cEJ0IJgmzOz1n

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0138  |  18803 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.9)
- Made of: plastic 70%, paper 30%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: S10+
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: S10+ | ONYTEX GADGETZ

## Chain
- **read_evidence** -> ok. category=phone brand=None model=S10+ label=False lines=2
- **retrieval** -> ok. query='S10+ S10+ ONYTEX GADGETZ Brand new Samsung galaxy S10+ now available at low cost dm for yo' hits=['Samsung Galaxy S21', 'Samsung Galaxy S22', 'Samsung Galaxy S23', 'Samsung Galaxy S24', 'Samsung Galaxy S25']
- **identify** -> ok. chosen=Samsung Galaxy S10+ margin=0.85
- **abstain** -> pass. top=0.9 margin=0.85

## Identification
Shortlist from the catalogue:
  - Samsung Galaxy S21 (0.5)
  - Samsung Galaxy S22 (0.5)
  - Samsung Galaxy S23 (0.5)
  - Samsung Galaxy S24 (0.5)
  - Samsung Galaxy S25 (0.5)

**Answer: Samsung Galaxy S10+** (margin 0.85)

## Claims
- [unverifiable_remote] Brand new Samsung Galaxy S10+
- [unverifiable_remote] Brand new
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
**64,418 to 161,000 NGN** (priced as a working item, width 0.8569, method uncalibrated_wide, 6 comparable prices)

6 used asking prices, 20th to 80th percentile 205,000 to 230,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.6983 for unproven claims, floored at the scrap value 44.

Scrap floor: 44 NGN

Conditions attached to this price:
- Brand new Samsung Galaxy S10+ -> not proven remotely. Agent will confirm at pickup.
- Brand new -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Samsung Galaxy S10 Plus 128 GB Black', 'category': 'phone', 'price_ngn': 270000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-samsung-galaxy-s10-plus-128-gb-black-f6vXO8Eqna7cEJ0IJgmzOz1n.html?page=1&pos=5&cur_pos=5&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
