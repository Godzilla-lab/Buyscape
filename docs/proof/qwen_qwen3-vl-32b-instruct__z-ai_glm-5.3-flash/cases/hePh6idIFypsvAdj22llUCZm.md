# Case hePh6idIFypsvAdj22llUCZm

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  31208 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, glass 30%, plastic 20%, circuit_board 10%
- Estimated weight: 0.18 kg (confidence 0.9)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: iPhone 12

## Two readers
- model_text differed between the two readers, so it is treated as unread
- serial_text differed between the two readers, so it is treated as unread
- brand_text was seen by only one reader, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. model_text differed between the two readers, so it is treated as unread; serial_text differed between the two readers, so it is treated as unread; brand_text was seen by only one reader, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=phone brand=None model=None label=True lines=1
- **retrieval** -> ok. query='iPhone 12 * Foreign Used Grade A++*
*iPhone 12 FU 64GB & 128GB*
Neatness: 10/10
Screen: 10' hits=['Apple iPhone 12', 'Apple iPhone 12 Pro', 'Apple iPhone 12 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 12 margin=0.7
- **abstain** -> pass. confidence=0.9 margin=0.7

## Identification
Shortlist from the catalogue:
  - Apple iPhone 12 (0.4667)
  - Apple iPhone 12 Pro (0.2667)
  - Apple iPhone 12 Pro Max (0.2)
  - Apple iPhone XR (0.2)
  - Apple iPhone XS (0.2)

**Answer: Apple iPhone 12** (margin 0.7)

## How sure the engine is (back office)
**90% sure this is a Apple iPhone 12.**

- Identification confidence: 90% (certain)
- Price confidence: 40%
- It is weighing: Apple iPhone 12 (0.9), Apple iPhone 12 Pro (0.2), Apple iPhone 12 Pro Max (0.1)
- read off the item's own label
- 1 lines seen by both readers
- 12 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and take one photo with the paper next to the phone.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] Photo of the front with the screen switched on, showing the home screen.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] Photo of the back of the phone.
   _why: this is needed before the price can be confirmed_

## Claims
- [unverifiable_remote] Foreign Used Grade A++
- [unverified] iPhone 12 FU 64GB & 128GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] iPhone 12 FU 64GB & 128GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Neatness: 10/10
- [unverified] Screen: 10/10
    priced as: assumed replaced screen. Agent inspects the bezel and display panel
- [unverifiable_remote] Body: 10/10
- [unverifiable_remote] BH:...
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
**44,426 to 312,200 NGN** (priced as a working item, width 1.5017, method uncalibrated_wide, 12 comparable prices)

12 used asking prices, 20th to 80th percentile 271,000 to 446,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.3643 for unproven claims, floored at the scrap value 175.

Scrap floor: 175 NGN

Conditions attached to this price:
- Foreign Used Grade A++ -> not proven remotely. Agent will confirm at pickup.
- iPhone 12 FU 64GB & 128GB -> not proven remotely. Agent reads storage from Settings.
- iPhone 12 FU 64GB & 128GB -> not proven remotely. Agent reads storage from Settings.
- Neatness: 10/10 -> not proven remotely. Agent will confirm at pickup.
- Screen: 10/10 -> not proven remotely. Agent inspects the bezel and display panel.
- Body: 10/10 -> not proven remotely. Agent will confirm at pickup.
- BH:... -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 12 128 GB Blue', 'category': 'phone', 'price_ngn': 329999, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-12-128-gb-blue-hePh6idIFypsvAdj22llUCZm.html?page=1&pos=11&cur_pos=11&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
