# Case 7CBkGlhe7sHlzGTd4iCYyW74

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  40864 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 1.0)
- Made of: aluminium 40%, plastic 50%, glass 10%
- Estimated weight: 0.18 kg (confidence 0.9)
- Brand read off the item: Apple
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: Minor smudges and fingerprints on the back surface., No visible cracks or dents.
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: BN: 375 | Apple

## Two readers
- item_type agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- 2 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- CEEJA
- BN:3753
- GADGE
- CEEJAY GADGETS NG

## Chain
- **ocr** -> ok. 4 lines: CEEJA | BN:3753 | GADGE | CEEJAY GADGETS NG
- **corroborate** -> dispute. item_type agreed by both readers; model_text was seen by only one reader, so it is treated as unread; 2 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=phone brand=Apple model=None label=False lines=2
- **retrieval** -> ok. query='Apple BN: 375 Apple Foreign Used
iPhone 11 128gb 
Color: Red & More 
Neatness: 10/10
BH 90' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 11 margin=0.55
- **abstain** -> abstain. no label, top score 0.75

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 8389 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 15391 ms (replayed)
- identify on z-ai/glm-5.3-flash: 9720 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 7364 ms (replayed)
- total across calls: 40864 ms; wall clock: 2050 ms

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.7667)
  - Apple iPhone 11 Pro (0.5667)
  - Apple iPhone 11 Pro Max (0.5)
  - Apple iPhone XR (0.5)
  - Apple iPhone XS (0.5)

**Not identified: CANNOT_IDENTIFY.** No label, plate or settings screen was legible, and the visual match alone scored only 0.75.

## How sure the engine is (back office)
**Not sure enough to price: 31% on the best answer. It is probably a Apple iPhone 11 or a Apple iPhone XR, and the photos cannot separate them.**

- Identification confidence: 31% (unknown)
- Price confidence: 14%
- It is weighing: Apple iPhone 11 (0.75), Apple iPhone XR (0.2)
- No label, plate or settings screen was legible, and the visual match alone scored only 0.75.
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- the brand was read by only one reader and is not confirmed
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
- [unverifiable_remote] Foreign Used
- [unverified] iPhone 11 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] iPhone 11 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Color: Red & More
- [unverifiable_remote] Neatness: 10/10
- [unverifiable_remote] BH 90%+
    priced as: assumed 75 percent. Agent opens the battery health screen
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
**66 to 233 NGN** (priced as material, width 1.1157, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.18 kg of aluminium 40%, plastic 50%, glass 10% (rates for glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 153 NGN

Conditions attached to this price:
- Not identified: No label, plate or settings screen was legible, and the visual match alone scored only 0.75.
- Foreign Used -> not proven remotely. Agent will confirm at pickup.
- iPhone 11 128gb -> not proven remotely. Agent reads storage from Settings.
- iPhone 11 128gb -> not proven remotely. Agent reads storage from Settings.
- Color: Red & More -> not proven remotely. Agent will confirm at pickup.
- Neatness: 10/10 -> not proven remotely. Agent will confirm at pickup.
- BH 90%+ -> not proven remotely. Agent opens the battery health screen.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 11 128 GB Red', 'category': 'phone', 'price_ngn': 249999, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-11-128-gb-red-7CBkGlhe7sHlzGTd4iCYyW74.html?page=1&pos=21&cur_pos=21&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
