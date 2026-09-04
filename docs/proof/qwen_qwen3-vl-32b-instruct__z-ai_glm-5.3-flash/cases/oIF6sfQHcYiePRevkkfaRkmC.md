# Case oIF6sfQHcYiePRevkkfaRkmC

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  94615 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.95)
- Made of: paper 80%, plastic 20%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: POSTED ON Jiji | EMANTECH HUB

## Chain
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=phone brand=None model=None label=False lines=2
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='POSTED ON Jiji EMANTECH HUB Apple iPhone 17 Pro Max is Apple’s premium flagship smartphone' hits=['Apple iPhone 11 Pro Max', 'Apple iPhone 12 Pro Max', 'Apple iPhone 13 Pro Max', 'Apple iPhone 14 Pro Max', 'Apple iPhone 15 Pro Max']
- **identify** -> refused. chosen=None None margin=0.25
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 Pro Max (0.6)
  - Apple iPhone 12 Pro Max (0.6)
  - Apple iPhone 13 Pro Max (0.6)
  - Apple iPhone 14 Pro Max (0.6)
  - Apple iPhone 15 Pro Max (0.6)

**Not identified: CANNOT_IDENTIFY.** Only unboxing imagery visible: no label, no model text, and seller's claimed model is unverified and outside shortlist.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 7% on the best answer. It is probably a Apple iPhone 17 Pro Max or a Apple iPhone 15 Pro Max, and the photos cannot separate them.**

- Identification confidence: 7% (unknown)
- Price confidence: 20%
- It is weighing: Apple iPhone 17 Pro Max (0.3), Apple iPhone 15 Pro Max (0.05)
- Only unboxing imagery visible: no label, no model text, and seller's claimed model is unverified and outside shortlist.
- no label, plate or settings screen was legible
- 2 lines seen by both readers
- the next candidate was only 0.25 behind
- looks like a catalogue or stock image
- 7 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [PHOTO] Screenshot of Settings then About, showing the model name and storage.
   _why: nothing on the item says which model this is_
3. [PHOTO] Dial *#06# and screenshot the IMEI that appears.
   _why: nothing on the item says which model this is_

## Claims
- [unverifiable_remote] Apple iPhone 17 Pro Max is Apple’s premium flagship smartphone
- [unverifiable_remote] has a large 6.9-inch display
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
**23 to 66 NGN** (priced as material, width 0.9418, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.5 kg of paper 80%, plastic 20% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 34 NGN

Conditions attached to this price:
- Not identified: Only unboxing imagery visible: no label, no model text, and seller's claimed model is unverified and outside shortlist.
- Evidence flag: looks like a catalogue or stock image
- Apple iPhone 17 Pro Max is Apple’s premium flagship smartphone -> not proven remotely. Agent will confirm at pickup.
- has a large 6.9-inch display -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Apple iPhone 17 Pro Max 256 GB Orange', 'category': 'phone', 'price_ngn': 1800000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-apple-iphone-17-pro-max-256-gb-orange-oIF6sfQHcYiePRevkkfaRkmC.html?page=2&pos=12&cur_pos=12&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
