# Case yXwtbMALuwyVsIwWckTmQIpa

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0018  |  35303 ms

## What the engine saw
- Presentation: sealed_new
- Category: mobile_phone (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 0.3 kg (confidence 0.7)
- Brand read off the item: TECNO
- Model read off the item: Camon 19 Pro
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: TECNO | CAMON | Camon 19 Pro

## Two readers
- brand_text agreed by both readers
- model_text agreed by both readers
- item_type agreed by both readers
- rating_text was seen by only one reader, so it is treated as unread

## OCR read off the photos
- TECNO
- OGENTERPRISE

## Chain
- **ocr** -> ok. 2 lines: TECNO | OGENTERPRISE
- **corroborate** -> dispute. brand_text agreed by both readers; model_text agreed by both readers; item_type agreed by both readers; rating_text was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=mobile_phone brand=TECNO model=Camon 19 Pro label=False lines=3
- **retrieval** -> ok. query='TECNO Camon 19 Pro TECNO CAMON Camon 19 Pro 6.67′′ AMOLED Display with Fingerprint on Disp' hits=['Tecno Camon 19', 'Tecno Camon 20', 'Tecno Camon 30', 'Tecno Camon 40', 'Tecno Camon 50']
- **identify** -> ok. chosen=Tecno Camon 19 margin=0.6
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 4815 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 15909 ms (replayed)
- identify on z-ai/glm-5.3-flash: 9330 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 5249 ms (replayed)
- total across calls: 35303 ms; wall clock: 1751 ms

## Identification
Shortlist from the catalogue:
  - Tecno Camon 19 (0.7667)
  - Tecno Camon 20 (0.5)
  - Tecno Camon 30 (0.5)
  - Tecno Camon 40 (0.5)
  - Tecno Camon 50 (0.5)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads as Tecno Camon 19 but the seller's text says 6. A Settings or About screen would settle it.

## How sure the engine is (back office)
**Not sure enough to price: 46% on the best answer. It is probably a Tecno Camon 19 or a Tecno Camon 19, and the photos cannot separate them.**

- Identification confidence: 46% (unsure)
- Price confidence: 14%
- It is weighing: Tecno Camon 19 (0.9), Tecno Camon 19 (0.3)
- The item reads as Tecno Camon 19 but the seller's text says 6. A Settings or About screen would settle it.
- no label, plate or settings screen was legible
- 2 lines seen by both readers
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
- [unverifiable_remote] 6.67′′ AMOLED Display
- [unverifiable_remote] AMOLED Display
- [unverifiable_remote] Fingerprint on Display
- [unverifiable_remote] 1080*2400 Resolution
- [unverifiable_remote] 32MP Front Camera
- [unverifiable_remote] Dual... front camera
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
**10 to 36 NGN** (priced as material, width 1.1142, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.3 kg of carton 100% (rates for carton are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 18 NGN

Conditions attached to this price:
- Not identified: The item reads as Tecno Camon 19 but the seller's text says 6. A Settings or About screen would settle it.
- 6.67′′ AMOLED Display -> not proven remotely. Agent will confirm at pickup.
- AMOLED Display -> not proven remotely. Agent will confirm at pickup.
- Fingerprint on Display -> not proven remotely. Agent will confirm at pickup.
- 1080*2400 Resolution -> not proven remotely. Agent will confirm at pickup.
- 32MP Front Camera -> not proven remotely. Agent will confirm at pickup.
- Dual... front camera -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Tecno Camon 20 Premier 5G 512 GB', 'category': 'phone', 'price_ngn': 500000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-tecno-camon-20-premier-5g-512-gb-yXwtbMALuwyVsIwWckTmQIpa.html?page=2&pos=16&cur_pos=16&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
