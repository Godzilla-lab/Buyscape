# Case 1tZaskvlnNM0IW2cxGQHddSL

Photos: 4  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0036  |  217383 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 1.0)
- Made of: aluminium 40%, glass 30%, plastic 20%, circuit_board 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: No visible damage to back panel or camera module, Minor smudges on glass back
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: APPLE WARRANTY | Apple Inc. | Apple | Designed by Apple in California | FACE ID WORK

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- serial_text differed between the two readers, so it is treated as unread
- 30 transcribed lines was seen by only one reader, so it is treated as unread
- item_type was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- NO LCD WARRANTY
- BATTERY PASS VERSION 18 0
- FACEID WORK CONDITION
- SIMUNLOCK
- APPLEWARRANTY
- GRADEA++
- m9 2005
- MM
- NO LCD WARRANTY
- MAPHIZ
- 256G
- APPLE WARRANTY

## Chain
- **ocr** -> ok. 17 lines: NO LCD WARRANTY | BATTERY PASS VERSION 18 0 | FACEID WORK CONDITION | SIMUNLOCK | APPLEWARRANTY | GRADEA++ | m9 2005 | M
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; serial_text differed between the two readers, so it is treated as unread; 30 transcribed lines was seen by only one reader, so it is treated as unread; item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=phone brand=Apple model=None label=True lines=5
- **retrieval** -> ok. query='Apple APPLE WARRANTY Apple Inc. Apple Designed by Apple in California FACE ID WORK 14 pro ' hits=['Apple iPhone 14 Pro', 'Apple iPhone 14 Pro Max', 'Apple iPhone 11 Pro', 'Apple iPhone 12 Pro', 'Apple iPhone 13 Pro']
- **identify** -> ok. chosen=Apple iPhone 14 Pro margin=0.35
- **abstain** -> pass. confidence=0.6 margin=0.35

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 14963 ms (replayed)
- read_evidence on qwen/qwen3-vl-32b-instruct: 14631 ms (replayed)
- read_evidence on qwen/qwen3-vl-32b-instruct: 15357 ms (replayed)
- read_evidence on qwen/qwen3-vl-32b-instruct: 14595 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 21156 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 16418 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 16565 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 24036 ms (replayed)
- identify on z-ai/glm-5.3-flash: 68964 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 10698 ms (replayed)
- total across calls: 217383 ms; wall clock: 2661 ms

## Identification
Shortlist from the catalogue:
  - Apple iPhone 14 Pro (0.5667)
  - Apple iPhone 14 Pro Max (0.5)
  - Apple iPhone 11 Pro (0.4333)
  - Apple iPhone 12 Pro (0.4333)
  - Apple iPhone 13 Pro (0.4333)

**Answer: Apple iPhone 14 Pro 256GB** (margin 0.35)

## How sure the engine is (back office)
**Not sure enough to price: 60% on the best answer. It is probably a Apple iPhone 14 Pro or a Apple iPhone 13 Pro, and the photos cannot separate them.**

- Identification confidence: 60% (unsure)
- Price confidence: 40%
- It is weighing: Apple iPhone 14 Pro (0.75), Apple iPhone 13 Pro (0.4), Apple iPhone 14 Pro Max (0.3)
- read off the item's own label
- 5 lines seen by both readers
- the item_type was read by only one reader and is not confirmed
- 13 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and take one photo with the paper next to the phone.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] Photo of the front with the screen switched on, showing the home screen.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] Photo of the back of the phone.
   _why: this is needed before the price can be confirmed_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Has the screen or battery ever been changed?
- Is it signed out of iCloud or Google, so a new owner can set it up?

## Claims
- [unverified] 14 pro 256gb 680k
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 14 pro 256gb 680k
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] 14 pro 256gb 680k
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 128gb 640k
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] 128gb 640k
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Available on ash and sky blue
- [unverifiable_remote] Direct UK used in very good condition
- [unverifiable_remote] Direct UK used in very good condition
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
**84,510 to 490,000 NGN** (priced as a working item, width 1.4116, method uncalibrated_wide, 12 comparable prices)

12 used asking prices, 20th to 80th percentile 626,000 to 700,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.3 for unproven claims, floored at the scrap value 181.

Scrap floor: 181 NGN

Conditions attached to this price:
- 14 pro 256gb 680k -> not proven remotely. Agent reads storage from Settings.
- 14 pro 256gb 680k -> not proven remotely. Agent reads storage from Settings.
- 14 pro 256gb 680k -> not proven remotely. Agent reads storage from Settings.
- 128gb 640k -> not proven remotely. Agent reads storage from Settings.
- 128gb 640k -> not proven remotely. Agent reads storage from Settings.
- Available on ash and sky blue -> not proven remotely. Agent will confirm at pickup.
- Direct UK used in very good condition -> not proven remotely. Agent will confirm at pickup.
- Direct UK used in very good condition -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 14 Pro 256 GB White', 'category': 'phone', 'price_ngn': 680000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-14-pro-256-gb-white-1tZaskvlnNM0IW2cxGQHddSL.html?page=1&pos=1&cur_pos=1&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
