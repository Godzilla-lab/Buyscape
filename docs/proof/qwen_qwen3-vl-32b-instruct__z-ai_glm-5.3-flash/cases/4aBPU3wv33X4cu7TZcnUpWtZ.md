# Case 4aBPU3wv33X4cu7TZcnUpWtZ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  33706 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, plastic 50%, glass 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: red sticker with '2800' on back, no visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Galaxy A17 | CITY 200 | A100

## Two readers
- 1 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- alaxy
- Galoxy
- ZENTAL
- 07
- A17
- alaky
- ALI
- POSTED ON JIJI
- SHAEL TECH GLOBA
- 200
- CITY
- A100

## Chain
- **ocr** -> ok. 12 lines: alaxy | Galoxy | ZENTAL | 07 | A17 | alaky | ALI | POSTED ON JIJI | SHAEL TECH GLOBA | 200 | CITY | A100
- **corroborate** -> dispute. 1 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=phone brand=None model=None label=False lines=3
- **retrieval** -> ok. query='Galaxy A17 CITY 200 A100 Good deal 
iPhone 12pro max
256gb
84% Battery Health
Face ID 
Tru' hits=['Apple iPhone 12', 'Apple iPhone XS Max', 'Apple iPhone 11 Pro Max', 'Apple iPhone 12 Pro Max', 'Apple iPhone 13 Pro Max']
- **identify** -> ok. chosen=Apple iPhone 12 Pro Max margin=0.15
- **abstain** -> abstain. top score 0.6

## Identification
Shortlist from the catalogue:
  - Apple iPhone 12 (0.3333)
  - Apple iPhone XS Max (0.2667)
  - Apple iPhone 11 Pro Max (0.2)
  - Apple iPhone 12 Pro Max (0.2)
  - Apple iPhone 13 Pro Max (0.2)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.6, which is not sure enough to price.

## How sure the engine is (back office)
**Not sure enough to price: 28% on the best answer. It is probably a Apple iPhone 12 Pro Max or a Apple iPhone 13 Pro Max, and the photos cannot separate them.**

- Identification confidence: 28% (unknown)
- Price confidence: 14%
- It is weighing: Apple iPhone 12 Pro Max (0.6), Apple iPhone 13 Pro Max (0.45)
- The best candidate scored only 0.6, which is not sure enough to price.
- no label, plate or settings screen was legible
- 3 lines seen by both readers
- the next candidate was only 0.15 behind
- 11 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: If you have the box, photograph the label showing the model, storage and IMEI. Then, still filming, do this on the item's own screen and hold it steady so the writing can be read: open settings then About, showing the model name and storage. Then, without stopping the video: Pull out the SIM tray and photograph the open slot. Finish with: A short clip: press power, unlock, then open the camera app. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Screenshot of Settings then About, showing the model name and storage.
   _why: nothing on the item says which model this is_
3. [PHOTO] Dial *#06# and screenshot the IMEI that appears.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Has the screen or battery ever been changed?
- Is it signed out of iCloud or Google, so a new owner can set it up?

## Claims
- [unverifiable_remote] iPhone 12pro max
- [unverifiable_remote] 256gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] 84% Battery Health
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverifiable_remote] Face ID
- [unverifiable_remote] True Tone
- [unverifiable_remote] Everything working
    priced as: assumed faulty. Agent powers on and tests calls, camera and charging
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
**51 to 259 NGN** (priced as material, width 1.3406, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of aluminium 40%, plastic 50%, glass 10% (rates for glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 170 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.6, which is not sure enough to price.
- iPhone 12pro max -> not proven remotely. Agent will confirm at pickup.
- 256gb -> not proven remotely. Agent reads storage from Settings.
- 84% Battery Health -> not proven remotely. Agent opens the battery health screen.
- Face ID -> not proven remotely. Agent will confirm at pickup.
- True Tone -> not proven remotely. Agent will confirm at pickup.
- Everything working -> not proven remotely. Agent powers on and tests calls, camera and charging.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 12 Pro Max 256 GB Gold', 'category': 'phone', 'price_ngn': 450000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-12-pro-max-256-gb-gold-4aBPU3wv33X4cu7TZcnUpWtZ.html?page=1&pos=17&cur_pos=17&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
