# Case aZsEbjZoqSPnCoSUgPZ2Tk1S

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0160  |  143939 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: glass 35%, aluminium 25%, mixed_electronic 30%, plastic 10%
- Estimated weight: 0.2 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **read_evidence** -> ok. category=phone brand=None model=None label=False lines=0
- **retrieval** -> ok. query='Clean Direct UK used iPhone 11 64gb
Factory unlocked 
Battery health 100% (Not Boosted)
So' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> refused. chosen=None None margin=0.4
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.4667)
  - Apple iPhone 11 Pro (0.2667)
  - Apple iPhone 11 Pro Max (0.2)
  - Apple iPhone XR (0.2)
  - Apple iPhone XS (0.2)

**Not identified: CANNOT_IDENTIFY.** No brand, model, serial or other identifying text is printed and legible on the device (OCR empty, label not legible). Camera shape, logo and colour may not be used to name a model.

## Claims
- [unverified] used iPhone 11 64gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] 64gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverified] Factory unlocked
    priced as: assumed still locked to the previous account. Seller signs out of iCloud or Google before payment
- [unverified] Battery health 100%
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverifiable_remote] Not Boosted
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverifiable_remote] used
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
**43 to 247 NGN** (priced as material, width 1.3998, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.2 kg of glass 35%, aluminium 25%, mixed_electronic 30%, plastic 10% (rates for glass, mixed_electronic, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 145 NGN

Conditions attached to this price:
- Not identified: No brand, model, serial or other identifying text is printed and legible on the device (OCR empty, label not legible). Camera shape, logo and colour may not be used to name a model.
- used iPhone 11 64gb -> not proven remotely. Agent reads storage from Settings.
- 64gb -> not proven remotely. Agent reads storage from Settings.
- Factory unlocked -> not proven remotely. Seller signs out of iCloud or Google before payment.
- Battery health 100% -> not proven remotely. Agent opens the battery health screen.
- Not Boosted -> not proven remotely. Agent opens the battery health screen.
- used -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 11 64 GB Red', 'category': 'phone', 'price_ngn': 205000, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-11-64-gb-red-aZsEbjZoqSPnCoSUgPZ2Tk1S.html?page=2&pos=8&cur_pos=8&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
