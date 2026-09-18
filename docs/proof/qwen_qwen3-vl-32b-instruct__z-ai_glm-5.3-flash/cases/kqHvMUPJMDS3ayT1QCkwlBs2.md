# Case kqHvMUPJMDS3ayT1QCkwlBs2

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  45627 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: paper 80%, plastic 20%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: Apple
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: Apple

## Two readers
- model_text was seen by only one reader, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 9 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed
- item_type was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- MUNICAT

## Chain
- **ocr** -> ok. 1 lines: MUNICAT
- **corroborate** -> dispute. model_text was seen by only one reader, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 9 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed; item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=phone brand=Apple model=None label=False lines=1
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='Apple Apple Brand new 14pro 512gb latest in market now 
Available in different colors 
You' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone 12', 'Apple iPhone 12 Pro']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 15099 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 14490 ms (replayed)
- identify on z-ai/glm-5.3-flash: 9332 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 6706 ms (replayed)
- total across calls: 45627 ms; wall clock: 1530 ms

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.3)
  - Apple iPhone 11 Pro (0.3)
  - Apple iPhone 11 Pro Max (0.3)
  - Apple iPhone 12 (0.3)
  - Apple iPhone 12 Pro (0.3)

**Not identified: CANNOT_IDENTIFY.** No model text is legible; box artwork resembles an iPhone 14 Pro but that is not on the shortlist, and seller claims are not label evidence.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- No model text is legible; box artwork resembles an iPhone 14 Pro but that is not on the shortlist, and seller claims are not label evidence.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the brand, item_type was read by only one reader and is not confirmed
- looks like a catalogue or stock image
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: If you have the box, photograph the label showing the model, storage and IMEI. Then, still filming, do this on the item's own screen and hold it steady so the writing can be read: open settings then About, showing the model name and storage. Then, without stopping the video: Pull out the SIM tray and photograph the open slot. Finish with: A short clip: press power, unlock, then open the camera app. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Screenshot of Settings then About, showing the model name and storage.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Has the screen or battery ever been changed?
- Is it signed out of iCloud or Google, so a new owner can set it up?

## Claims
- [unverifiable_remote] Brand new 14pro 512gb latest in market now
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 14pro 512gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 14pro 512gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] latest in market now
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
**14 to 66 NGN** (priced as material, width 1.2762, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.5 kg of paper 80%, plastic 20% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 34 NGN

Conditions attached to this price:
- Not identified: No model text is legible; box artwork resembles an iPhone 14 Pro but that is not on the shortlist, and seller claims are not label evidence.
- Evidence flag: looks like a catalogue or stock image
- Brand new 14pro 512gb latest in market now -> not proven remotely. Agent reads storage from Settings.
- 14pro 512gb -> not proven remotely. Agent reads storage from Settings.
- 14pro 512gb -> not proven remotely. Agent reads storage from Settings.
- latest in market now -> not proven remotely. Agent will confirm at pickup.
- Available in different colors -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Apple iPhone 14 Pro 512 GB Purple', 'category': 'phone', 'price_ngn': 800000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-apple-iphone-14-pro-512-gb-purple-kqHvMUPJMDS3ayT1QCkwlBs2.html?page=1&pos=23&cur_pos=23&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
