# Case 43v7q9qPhTb0hd6O0SaLacl0

Photos: 3  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0042  |  207666 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 1.0)
- Made of: aluminium 40%, plastic 30%, circuit_board 20%, glass 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: iPhone 12 Pro Max
- Rating read: 128 GB
- Label, plate or settings screen legible: yes
- Damage noted: No visible damage to back casing or camera module, Sticker with warranty information attached to back, white sticker covering back camera and part of rear panel, sticker has text and barcode, partially obscures surface, No visible damage to the back panel or camera module., Sticker on the back is slightly wrinkled.
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 12P 128 | APPLE WARRANTY | NOT TO BE USED FOR ANY OTHER PURPOSE | NO LCD WARRANTY | Model: iPhone 12 Pro Max | Serial Number: FVJH46789012 | Manufactured in China | Apple Inc.

## Two readers
- brand_text was read by one reader and confirmed by OCR
- rating_text was read by one reader and confirmed by OCR

## OCR read off the photos
- 128
- NO LCD WARRANTY
- BATTERY PASS VÉRSION TED
- FACEID WORN CONENTION
- SIMUNLOOKGRADEA
- APPLE WARRANTY
- MITE
- 12P
- NO LCD WARRANTY
- BATTERY PASS
- FACE ID WORK
- SMUNLCOK

## Chain
- **corroborate** -> unavailable. openrouter:mistralai/mistral-small-3.2-24b-instruct failed after retries: no JSON object in response: {
  "presentation"
- **ocr** -> ok. 29 lines: 128 | NO LCD WARRANTY | BATTERY PASS VÉRSION TED | FACEID WORN CONENTION | SIMUNLOOKGRADEA | APPLE WARRANTY | MITE | 12P
- **corroborate** -> agree. brand_text was read by one reader and confirmed by OCR; rating_text was read by one reader and confirmed by OCR
- **read_evidence** -> ok. category=phone brand=Apple model=iPhone 12 Pro Max label=True lines=32
- **retrieval** -> ok. query='Apple iPhone 12 Pro Max 128 GB 12P 128 APPLE WARRANTY NOT TO BE USED FOR ANY OTHER PURPOSE' hits=['Apple iPhone 12 Pro', 'Apple iPhone 12 Pro Max', 'Apple iPhone 12', 'Apple iPhone 13 Pro', 'Apple iPhone 13 Pro Max']
- **identify** -> ok. chosen=Apple iPhone 12 Pro Max margin=0.65
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 35532 ms
- read_evidence on qwen/qwen3-vl-32b-instruct: 35528 ms
- read_evidence on qwen/qwen3-vl-32b-instruct: 71294 ms
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 24710 ms
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 25070 ms
- identify on z-ai/glm-5.3-flash: 12051 ms
- extract_claims on qwen/qwen3-vl-32b-instruct: 3481 ms (replayed)
- total across calls: 207666 ms; wall clock: 291158 ms

## Identification
Shortlist from the catalogue:
  - Apple iPhone 12 Pro (0.9)
  - Apple iPhone 12 Pro Max (0.9)
  - Apple iPhone 12 (0.7667)
  - Apple iPhone 13 Pro (0.7)
  - Apple iPhone 13 Pro Max (0.7)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads as Apple iPhone 12 Pro Max but the seller's text says 13. A Settings or About screen would settle it.

## How sure the engine is (back office)
**Not sure enough to price: 38% on the best answer. It is probably a Apple iPhone 12 Pro Max or a Apple iPhone 12 Pro, and the photos cannot separate them.**

- Identification confidence: 38% (unknown)
- Price confidence: 14%
- It is weighing: Apple iPhone 12 Pro Max (0.9), Apple iPhone 12 Pro (0.25)
- The item reads as Apple iPhone 12 Pro Max but the seller's text says 13. A Settings or About screen would settle it.
- read off the item's own label
- only one reader saw these photos, the second was unavailable
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Screenshot of Settings then About, showing the model name and storage.
   _why: nothing on the item says which model this is_
2. [PHOTO] Dial *#06# and screenshot the IMEI that appears.
   _why: nothing on the item says which model this is_
3. [PHOTO] If you have the box, photograph the label showing the model, storage and IMEI.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Has the screen or battery ever been changed?
- Is it signed out of iCloud or Google, so a new owner can set it up?

## Claims
- [unverified] 13 pro 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 13 pro 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Nml 13 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Nml 13 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Nml 13 128gb
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
**68 to 291 NGN** (priced as material, width 1.243, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of aluminium 40%, plastic 30%, circuit_board 20%, glass 10% (rates for glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 198 NGN

Conditions attached to this price:
- Not identified: The item reads as Apple iPhone 12 Pro Max but the seller's text says 13. A Settings or About screen would settle it.
- 13 pro 128gb -> not proven remotely. Agent reads storage from Settings.
- 13 pro 128gb -> not proven remotely. Agent reads storage from Settings.
- Nml 13 128gb -> not proven remotely. Agent reads storage from Settings.
- Nml 13 128gb -> not proven remotely. Agent reads storage from Settings.
- Nml 13 128gb -> not proven remotely. Agent reads storage from Settings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 13 128 GB White', 'category': 'phone', 'price_ngn': 380000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-13-128-gb-white-43v7q9qPhTb0hd6O0SaLacl0.html?page=1&pos=2&cur_pos=2&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
