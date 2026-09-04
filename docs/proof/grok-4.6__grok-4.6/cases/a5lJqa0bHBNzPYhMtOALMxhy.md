# Case a5lJqa0bHBNzPYhMtOALMxhy

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0142  |  102532 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: plastic 45%, paper 30%, mixed_electronic 25%
- Estimated weight: 0.2 kg (confidence 0.55)
- Brand read off the item: NOKIA
- Model read off the item: Nokia 110
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Nokia 110 | NOKIA | For use in specific African countries* | Africa Edition

## Chain
- **read_evidence** -> ok. category=phone brand=NOKIA model=Nokia 110 label=True lines=4
- **retrieval** -> ok. query='NOKIA Nokia 110 Nokia 110 NOKIA For use in specific African countries* Africa Edition Wire' hits=['Nokia C32']
- **identify** -> ok. chosen=Nokia 110 margin=0.96
- **abstain** -> pass. top=0.98 margin=0.96

## Identification
Shortlist from the catalogue:
  - Nokia C32 (0.5)

**Answer: Nokia 110 Africa Edition** (margin 0.96)

## Claims
- [unverifiable_remote] Wireless FM
- [unverifiable_remote] Mp3 music player
- [unverifiable_remote] Camera/ video camera
- [unverifiable_remote] Support up to 32gb SD card
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the phone.
- [unverified] Required evidence 'front_screen_on' was not supplied
    priced as: priced as if the worst case is true. Photo of the front with the screen switched on, showing the home screen.
- [unverified] Required evidence 'back' was not supplied
    priced as: priced as if the worst case is true. Photo of the back of the phone.
- [unverified] Required evidence 'settings_about' was not supplied
    priced as: priced as if the worst case is true. Screenshot of Settings then About, showing the model name and storage.

## Price
**28 to 98 NGN** (priced as material, width 1.1075, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.5936 for unproven claims.

Scrap floor: 47 NGN

Conditions attached to this price:
- Wireless FM -> not proven remotely. Agent will confirm at pickup.
- Mp3 music player -> not proven remotely. Agent will confirm at pickup.
- Camera/ video camera -> not proven remotely. Agent will confirm at pickup.
- Support up to 32gb SD card -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..

## Answer key (not shown to the engine)
`{'title': 'New Nokia 110 Green', 'category': 'phone', 'price_ngn': 27000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-nokia-110-green-a5lJqa0bHBNzPYhMtOALMxhy.html?page=1&pos=8&cur_pos=8&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
