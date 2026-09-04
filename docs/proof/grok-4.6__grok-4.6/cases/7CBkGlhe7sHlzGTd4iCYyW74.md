# Case 7CBkGlhe7sHlzGTd4iCYyW74

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0160  |  153882 ms

## What the engine saw
- Presentation: single_unit
- Category: phone (confidence 0.95)
- Made of: glass 30%, mixed_electronic 45%, aluminium 20%, plastic 5%
- Estimated weight: 0.16 kg (confidence 0.65)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: 128
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: BN: 3753 | CEEJAY GADGETS | POSTED ON JIJI | CEEJAY GADGETS NG | 128

## Chain
- **read_evidence** -> ok. category=phone brand=None model=None label=True lines=5
- **retrieval** -> ok. query='128 BN: 3753 CEEJAY GADGETS POSTED ON JIJI CEEJAY GADGETS NG 128 Foreign Used
iPhone 11 12' hits=['Apple iPhone 11', 'Apple iPhone 11 Pro', 'Apple iPhone 11 Pro Max', 'Apple iPhone XR', 'Apple iPhone XS']
- **identify** -> refused. chosen=None None margin=0.3
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Apple iPhone 11 (0.4667)
  - Apple iPhone 11 Pro (0.2667)
  - Apple iPhone 11 Pro Max (0.2)
  - Apple iPhone XR (0.2)
  - Apple iPhone XS (0.2)

**Not identified: CANNOT_IDENTIFY.** Brand and model are READ fields and must be copied only from literally legible printed text. None is present on the phone (only an Apple logo, a 128 sticker, shop watermarks, and the seller's claim). Inference from logo, camera shape or colour is not allowed, so no catalogue entry can be selected.

## Claims
- [unverifiable_remote] Foreign Used
    priced as: assumed still locked to the previous account. Seller signs out of iCloud or Google before payment
- [unverifiable_remote] iPhone 11
- [unverified] 128gb
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] Color: Red
- [unverified] Neatness: 10/10
    priced as: assumed replaced screen. Agent inspects the bezel and display panel
- [unverified] BH 90%+
    priced as: assumed 75 percent. Agent opens the battery health screen
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the phone.
- [unverified] Required evidence 'front_screen_on' was not supplied
    priced as: priced as if the worst case is true. Photo of the front with the screen switched on, showing the home screen.
- [unverified] Required evidence 'back' was not supplied
    priced as: priced as if the worst case is true. Photo of the back of the phone.
- [unverified] Required evidence 'settings_about' was not supplied
    priced as: priced as if the worst case is true. Screenshot of Settings then About, showing the model name and storage.

## Price
**34 to 207 NGN** (priced as material, width 1.4256, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.16 kg of glass 30%, mixed_electronic 45%, aluminium 20%, plastic 5% (rates for glass, mixed_electronic, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 116 NGN

Conditions attached to this price:
- Not identified: Brand and model are READ fields and must be copied only from literally legible printed text. None is present on the phone (only an Apple logo, a 128 sticker, shop watermarks, and the seller's claim). Inference from logo, camera shape or colour is not allowed, so no catalogue entry can be selected.
- Foreign Used -> not proven remotely. Seller signs out of iCloud or Google before payment.
- iPhone 11 -> not proven remotely. Agent will confirm at pickup.
- 128gb -> not proven remotely. Agent reads storage from Settings.
- Color: Red -> not proven remotely. Agent will confirm at pickup.
- Neatness: 10/10 -> not proven remotely. Agent inspects the bezel and display panel.
- BH 90%+ -> not proven remotely. Agent opens the battery health screen.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..

## Answer key (not shown to the engine)
`{'title': 'Apple iPhone 11 128 GB Red', 'category': 'phone', 'price_ngn': 249999, 'is_used': True, 'url': '/ikeja/mobile-phones/apple-iphone-11-128-gb-red-7CBkGlhe7sHlzGTd4iCYyW74.html?page=1&pos=21&cur_pos=21&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
