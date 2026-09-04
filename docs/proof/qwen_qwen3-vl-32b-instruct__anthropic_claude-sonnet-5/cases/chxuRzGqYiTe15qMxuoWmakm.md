# Case chxuRzGqYiTe15qMxuoWmakm

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0144  |  21887 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: plastic 80%, steel 15%, circuit_board 5%
- Estimated weight: 0.3 kg (confidence 0.8)
- Brand read off the item: Nokia
- Model read off the item: 106 4G
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Nokia 106 4G | NOKIA

## Chain
- **read_evidence** -> ok. category=phone brand=Nokia model=106 4G label=False lines=2
- **retrieval** -> ok. query='Nokia 106 4G Nokia 106 4G NOKIA Up to 15.7 hrs/21.9 days talk/standby time
LED torch
1.8 d' hits=['Nokia C32', 'Infinix Smart 8', 'Infinix Smart 9', 'Google Pixel 7', 'Google Pixel 8']
- **identify** -> ok. chosen=Nokia 106 4G margin=0.96
- **abstain** -> pass. top=0.98 margin=0.96

## Identification
Shortlist from the catalogue:
  - Nokia C32 (0.5)
  - Infinix Smart 8 (0.2)
  - Infinix Smart 9 (0.2)
  - Google Pixel 7 (0.2)
  - Google Pixel 8 (0.2)

**Answer: Nokia 106 4G** (margin 0.96)

## Claims
- [unverifiable_remote] Up to 15.7 hrs talk time
- [unverifiable_remote] Up to 21.9 days standby time
- [unverifiable_remote] LED torch included
- [unverifiable_remote] 1.8 inch display
- [unverifiable_remote] Supports HD calls over 4G network via VoLTE
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
**41 to 130 NGN** (priced as material, width 1.0366, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.5987 for unproven claims.

Scrap floor: 69 NGN

Conditions attached to this price:
- Up to 15.7 hrs talk time -> not proven remotely. Agent will confirm at pickup.
- Up to 21.9 days standby time -> not proven remotely. Agent will confirm at pickup.
- LED torch included -> not proven remotely. Agent will confirm at pickup.
- 1.8 inch display -> not proven remotely. Agent will confirm at pickup.
- Supports HD calls over 4G network via VoLTE -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Nokia 106 Black', 'category': 'phone', 'price_ngn': 13000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-nokia-106-black-chxuRzGqYiTe15qMxuoWmakm.html?page=1&pos=13&cur_pos=13&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
