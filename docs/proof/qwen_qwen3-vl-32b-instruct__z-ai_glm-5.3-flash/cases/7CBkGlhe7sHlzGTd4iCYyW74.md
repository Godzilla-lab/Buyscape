# Case 7CBkGlhe7sHlzGTd4iCYyW74

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  42535 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: aluminium 40%, plastic 40%, glass 10%, circuit_board 10%
- Estimated weight: 0.2 kg (confidence 0.9)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: Red back cover with minor smudges and fingerprints, Camera module appears intact, no visible cracks
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: BN: 3753

## Two readers
- brand_text was seen by only one reader, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- 2 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text was seen by only one reader, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; 2 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=phone brand=None model=None label=False lines=1
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='BN: 3753 Foreign Used
iPhone 11 128gb 
Color: Red & More 
Neatness: 10/10
BH 90%+' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> ok. chosen=Apple iPhone 11 margin=0.65
- **abstain** -> abstain. confidence 0.36: no label, plate or settings screen was legible; 1 lines seen by both readers; looks like a catalogue or stock image

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.4667)
  - Apple iPhone 11 Pro (0.2667)
  - Apple iPhone 11 Pro Max (0.2)
  - Apple iPhone XR (0.2)
  - Apple iPhone XS (0.2)

**Not identified: EVIDENCE_INCOMPLETE.** The evidence only supports this answer at 36 percent, which is a guess. One clear photo of the label would settle it.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 22% on the best answer. It is probably a Apple iPhone 11 or a Apple iPhone XR, and the photos cannot separate them.**

- Identification confidence: 22% (unknown)
- Price confidence: 14%
- It is weighing: Apple iPhone 11 (0.85), Apple iPhone XR (0.2)
- The evidence only supports this answer at 36 percent, which is a guess. One clear photo of the label would settle it.
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- looks like a catalogue or stock image
- 11 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: If you have the box, photograph the label showing the model, storage and IMEI. Then, still filming, do this on the item's own screen and hold it steady so the writing can be read: open settings then About, showing the model name and storage. Then, without stopping the video: Pull out the SIM tray and photograph the open slot. Finish with: A short clip: press power, unlock, then open the camera app. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Screenshot of Settings then About, showing the model name and storage.
   _why: nothing on the item says which model this is_

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
**85 to 335 NGN** (priced as material, width 1.1868, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of aluminium 40%, plastic 40%, glass 10%, circuit_board 10% (rates for circuit_board, glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 198 NGN

Conditions attached to this price:
- Not identified: The evidence only supports this answer at 36 percent, which is a guess. One clear photo of the label would settle it.
- Evidence flag: looks like a catalogue or stock image
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
