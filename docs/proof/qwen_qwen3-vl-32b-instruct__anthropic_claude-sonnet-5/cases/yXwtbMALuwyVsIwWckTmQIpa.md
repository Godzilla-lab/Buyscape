# Case yXwtbMALuwyVsIwWckTmQIpa

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0146  |  21019 ms

## What the engine saw
- Presentation: sealed_new
- Category: phone (confidence 0.9)
- Made of: paper 90%, plastic 10%
- Estimated weight: 0.3 kg (confidence 0.8)
- Brand read off the item: TECNO
- Model read off the item: CAMON 20
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: TECNO | CAMON 20

## Chain
- **read_evidence** -> ok. category=phone brand=TECNO model=CAMON 20 label=False lines=2
- **retrieval** -> ok. query='TECNO CAMON 20 TECNO CAMON 20 6.67′′ AMOLED Display with Fingerprint on Display
1080*2400 ' hits=['Tecno Camon 20', 'Tecno Camon 30', 'Tecno Camon 40', 'Tecno Camon 50', 'Tecno Spark 20']
- **identify** -> ok. chosen=Tecno Camon 20 margin=0.93
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Tecno Camon 20 (0.9)
  - Tecno Camon 30 (0.5)
  - Tecno Camon 40 (0.5)
  - Tecno Camon 50 (0.5)
  - Tecno Spark 20 (0.5)

**Not identified: EVIDENCE_INCOMPLETE.** The item reads as Tecno Camon 20 but the seller's text says 6. A Settings or About screen would settle it.

## Claims
- [unverifiable_remote] 6.67'' AMOLED Display
- [unverifiable_remote] Fingerprint sensor is located on the display
- [unverified] 1080*2400 Resolution
    priced as: assumed replaced screen. Agent inspects the bezel and display panel
- [unverifiable_remote] 32MP Front Camera
- [unverifiable_remote] Dual... (description cut off, unclear claim)
    priced as: assumed still locked to the previous account. Seller signs out of iCloud or Google before payment
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
**5 to 37 NGN** (priced as material, width 1.4711, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.3 kg of paper 90%, plastic 10% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 19 NGN

Conditions attached to this price:
- Not identified: The item reads as Tecno Camon 20 but the seller's text says 6. A Settings or About screen would settle it.
- 6.67'' AMOLED Display -> not proven remotely. Agent will confirm at pickup.
- Fingerprint sensor is located on the display -> not proven remotely. Agent will confirm at pickup.
- 1080*2400 Resolution -> not proven remotely. Agent inspects the bezel and display panel.
- 32MP Front Camera -> not proven remotely. Agent will confirm at pickup.
- Dual... (description cut off, unclear claim) -> not proven remotely. Seller signs out of iCloud or Google before payment.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Tecno Camon 20 Premier 5G 512 GB', 'category': 'phone', 'price_ngn': 500000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-tecno-camon-20-premier-5g-512-gb-yXwtbMALuwyVsIwWckTmQIpa.html?page=2&pos=16&cur_pos=16&ads_per_page=23&ads_count=17061&lid=REVG8QZgOnrtgxCE'}`
