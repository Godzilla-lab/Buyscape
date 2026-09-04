# Case kqHvMUPJMDS3ayT1QCkwlBs2

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0205  |  24384 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: paper 80%, plastic 20%
- Estimated weight: 0.5 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 13 Pro Max
- Rating read: 256GB
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: iPhone | 13 Pro Max | A2644 | 256GB | Space Black | iOS 15 | Apple

## Chain
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 13 Pro Max label=True lines=7
- **retrieval** -> ok. query='Apple iPhone 13 Pro Max 256GB iPhone 13 Pro Max A2644 256GB Space Black iOS 15 Apple Brand' hits=['Apple iPhone 13 Pro', 'Apple iPhone 13 Pro Max', 'Apple iPhone 13', 'Apple iPhone 15 Pro', 'Apple iPhone 15 Pro Max']
- **identify** -> ok. chosen=Apple iPhone 13 Pro Max margin=0.85
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Apple iPhone 13 Pro (0.9)
  - Apple iPhone 13 Pro Max (0.9)
  - Apple iPhone 13 (0.7667)
  - Apple iPhone 15 Pro (0.7)
  - Apple iPhone 15 Pro Max (0.7)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads as Apple iPhone 13 Pro Max but the seller's text says 14. A Settings or About screen would settle it.

## Claims
- [unverifiable_remote] Brand new
- [unverifiable_remote] 14pro
- [unverifiable_remote] 512gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Available in different colors
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
**19 to 66 NGN** (priced as material, width 1.0997, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.5 kg of paper 80%, plastic 20% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 34 NGN

Conditions attached to this price:
- Not identified: The item reads as Apple iPhone 13 Pro Max but the seller's text says 14. A Settings or About screen would settle it.
- Brand new -> not proven remotely. Agent will confirm at pickup.
- 14pro -> not proven remotely. Agent will confirm at pickup.
- 512gb -> not proven remotely. Agent reads storage from Settings.
- Available in different colors -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Apple iPhone 14 Pro 512 GB Purple', 'category': 'phone', 'price_ngn': 800000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-apple-iphone-14-pro-512-gb-purple-kqHvMUPJMDS3ayT1QCkwlBs2.html?page=1&pos=23&cur_pos=23&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
