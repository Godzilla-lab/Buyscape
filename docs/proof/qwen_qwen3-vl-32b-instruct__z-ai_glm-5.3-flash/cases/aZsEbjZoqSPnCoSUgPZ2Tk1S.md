# Case aZsEbjZoqSPnCoSUgPZ2Tk1S

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  28489 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 1.0)
- Made of: aluminium 40%, glass 30%, plastic 20%, circuit_board 10%
- Estimated weight: 0.18 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: minor scratches on back glass, faint smudges and fingerprints
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MANNY STORES | Apple

## Two readers
- model_text was seen by only one reader, so it is treated as unread
- 1 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- MANNY STORES

## Chain
- **ocr** -> ok. 1 lines: MANNY STORES
- **corroborate** -> dispute. model_text was seen by only one reader, so it is treated as unread; 1 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=phone brand=Apple model=None label=False lines=2
- **retrieval** -> ok. query='Apple MANNY STORES Apple Clean Direct UK used iPhone 11 64gb
Factory unlocked 
Battery hea' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 11 margin=0.7
- **abstain** -> pass. confidence=0.61 margin=0.7

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.7667)
  - Apple iPhone 11 Pro (0.5667)
  - Apple iPhone 11 Pro Max (0.5)
  - Apple iPhone XR (0.5)
  - Apple iPhone XS (0.5)

**Answer: Apple iPhone 11 PRODUCT RED, 64GB (seller stated)** (margin 0.7)

## How sure the engine is (back office)
**Not sure enough to price: 61% on the best answer. It is probably a Apple iPhone 11 or a Apple iPhone XR, and the photos cannot separate them.**

- Identification confidence: 61% (unsure)
- Price confidence: 0%
- It is weighing: Apple iPhone 11 (0.9), Apple iPhone XR (0.2), Apple iPhone 11 Pro (0.05)
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- the brand was read by only one reader and is not confirmed
- 10 claims are still unproven, 0 are supported

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
- [unverified] Clean Direct UK used iPhone 11 64gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Clean Direct UK used iPhone 11 64gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Factory unlocked
    priced as: assumed still locked to the previous account. Seller signs out of iCloud or Google before payment
- [unverifiable_remote] Battery health 100% (Not Boosted)
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverifiable_remote] Sold with a...
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
**48 to 243 NGN** (priced as material, width 1.3301, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 163 NGN

Conditions attached to this price:
- Clean Direct UK used iPhone 11 64gb -> not proven remotely. Agent reads storage from Settings.
- Clean Direct UK used iPhone 11 64gb -> not proven remotely. Agent reads storage from Settings.
- Factory unlocked -> not proven remotely. Seller signs out of iCloud or Google before payment.
- Battery health 100% (Not Boosted) -> not proven remotely. Agent opens the battery health screen.
- Sold with a... -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 11 64 GB Red', 'category': 'phone', 'price_ngn': 205000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-11-64-gb-red-aZsEbjZoqSPnCoSUgPZ2Tk1S.html?page=2&pos=8&cur_pos=8&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
