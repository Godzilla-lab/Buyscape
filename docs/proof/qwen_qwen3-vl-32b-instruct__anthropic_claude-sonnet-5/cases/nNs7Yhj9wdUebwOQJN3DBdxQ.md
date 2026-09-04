# Case nNs7Yhj9wdUebwOQJN3DBdxQ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0210  |  22765 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: plastic 70%, steel 20%, circuit_board 10%
- Estimated weight: 0.15 kg (confidence 0.9)
- Brand read off the item: G
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: G | POSTED ON LISANA

## Chain
- **read_evidence** -> ok. category=phone brand=G model=None label=False lines=2
- **retrieval** -> ok. query='G G POSTED ON LISANA Google Pixel 7a
Sleek 6.1′′ FHD+ OLED display with 90 Hz smooth visua' hits=['Google Pixel 7', 'Google Pixel 8', 'Google Pixel 9', 'Tecno Pova 6']
- **identify** -> ok. chosen=Google Pixel 7 margin=0.4
- **abstain** -> abstain. top score 0.55

## Identification
Shortlist from the catalogue:
  - Google Pixel 7 (0.7)
  - Google Pixel 8 (0.5)
  - Google Pixel 9 (0.5)
  - Tecno Pova 6 (0.2)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.55, which is not sure enough to price.

## Claims
- [unverifiable_remote] Google Pixel 7a
- [unverified] 6.1'' display
    priced as: assumed replaced screen. Agent inspects the bezel and display panel
- [unverifiable_remote] FHD+ resolution display
- [unverifiable_remote] OLED display
- [unverifiable_remote] 90 Hz refresh rate
- [unverifiable_remote] Powered by Google Tensor G2
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
**22 to 96 NGN** (priced as material, width 1.233, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.15 kg of plastic 70%, steel 20%, circuit_board 10% (rates for circuit_board, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 48 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.55, which is not sure enough to price.
- Google Pixel 7a -> not proven remotely. Agent will confirm at pickup.
- 6.1'' display -> not proven remotely. Agent inspects the bezel and display panel.
- FHD+ resolution display -> not proven remotely. Agent will confirm at pickup.
- OLED display -> not proven remotely. Agent will confirm at pickup.
- 90 Hz refresh rate -> not proven remotely. Agent will confirm at pickup.
- Powered by Google Tensor G2 -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Google Pixel 7a 128 GB White', 'category': 'phone', 'price_ngn': 275000, 'is_used': True, 'url': '/ikeja/mobile-phones/google-pixel-7a-128-gb-white-nNs7Yhj9wdUebwOQJN3DBdxQ.html?page=2&pos=4&cur_pos=4&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
