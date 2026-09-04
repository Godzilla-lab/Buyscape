# Case mlxplz68xfW3m9Ifm5tgpT65

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0131  |  18338 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: paper 90%, plastic 10%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: Google
- Model read off the item: Pixel Fold
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Pixel Fold | POSTED ON JIO | ONYITEX GADGET

## Chain
- **read_evidence** -> ok. category=phone brand=Google model=Pixel Fold label=False lines=3
- **retrieval** -> ok. query='Google Pixel Fold Pixel Fold POSTED ON JIO ONYITEX GADGET Google Pixel Fold:
- 7.6-inch OL' hits=['Google Pixel 7', 'Google Pixel 8', 'Google Pixel 9', 'Tecno Pova 5', 'Tecno Pova 6']
- **identify** -> ok. chosen=Google Pixel Fold margin=0.85
- **abstain** -> pass. top=0.9 margin=0.85

## Identification
Shortlist from the catalogue:
  - Google Pixel 7 (0.7)
  - Google Pixel 8 (0.7)
  - Google Pixel 9 (0.5)
  - Tecno Pova 5 (0.2)
  - Tecno Pova 6 (0.2)

**Answer: Google Pixel Fold** (margin 0.85)

## Claims
- [unverifiable_remote] Google Pixel Fold
- [unverifiable_remote] 7.6-inch OLED main display
- [unverifiable_remote] 5.8-inch cover screen
    priced as: assumed replaced screen. Agent inspects the bezel and display panel
- [unverifiable_remote] Tensor G2 chip
- [unverifiable_remote] 12GB RAM
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
**59,274 to 695,800 NGN** (priced as a working item, width 1.686, method uncalibrated_wide, 12 comparable prices)

12 used asking prices, 20th to 80th percentile 292,000 to 994,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.4511 for unproven claims, floored at the scrap value 32.

Scrap floor: 32 NGN

Conditions attached to this price:
- Google Pixel Fold -> not proven remotely. Agent will confirm at pickup.
- 7.6-inch OLED main display -> not proven remotely. Agent will confirm at pickup.
- 5.8-inch cover screen -> not proven remotely. Agent inspects the bezel and display panel.
- Tensor G2 chip -> not proven remotely. Agent will confirm at pickup.
- 12GB RAM -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Google Pixel Fold 512 GB Black', 'category': 'phone', 'price_ngn': 620000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-google-pixel-fold-512-gb-black-mlxplz68xfW3m9Ifm5tgpT65.html?page=1&pos=6&cur_pos=6&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
