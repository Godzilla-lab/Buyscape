# Case rAvryKzKWcwQ7cAtqwE2Lxad

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0014  |  29703 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 5%, rubber 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: MAXMECH
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dirt and mud on body and frame, some rust visible on metal parts, worn rubber wheels, fuel cap appears loose or missing
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MAXMECH

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 11 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- MMAXMECH
- C-
- MAXMECH

## Chain
- **ocr** -> ok. 3 lines: MMAXMECH | C- | MAXMECH
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 11 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=MAXMECH model=None label=True lines=1
- **retrieval** -> ok. query='MAXMECH MAXMECH Product Overview

The MAXMECH WGC-380Ei Welding Generator is a heavy-duty ' hits=['Maxmech MX3500 3.5kVA', 'Maxmech MX10000 10kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA']
- **identify** -> ok. chosen=Maxmech WGC-380i margin=0.5
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6894 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 11127 ms (replayed)
- identify on z-ai/glm-5.3-flash: 7735 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3947 ms (replayed)
- total across calls: 29703 ms; wall clock: 1610 ms

## Identification
Shortlist from the catalogue:
  - Maxmech MX3500 3.5kVA (0.5)
  - Maxmech MX10000 10kVA (0.4333)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names wgc380i, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

## How sure the engine is (back office)
**Not sure enough to price: 42% on the best answer. It is probably a Maxmech WGC-380i or a Maxmech MX3500, and the photos cannot separate them.**

- Identification confidence: 42% (unsure)
- Price confidence: 16%
- It is weighing: Maxmech WGC-380i (0.7), Maxmech MX3500 (0.2)
- The answer names wgc380i, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 1 lines seen by both readers
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_
3. [PHOTO] Close-up of the plate on the engine block showing the engine model and serial.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it start and run right now?
- When was it last serviced, and what was done?

## Claims
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the generator.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole generator from the front.
- [unverified] Required evidence 'plate_kva' was not supplied
    priced as: priced as if the worst case is true. Close-up of the rating plate showing the kVA and model number.
- [unverified] Required evidence 'side_cover_off' was not supplied
    priced as: priced as if the worst case is true. Open the side cover and photograph the alternator windings.
- [unverified] Required evidence 'engine_bay' was not supplied
    priced as: priced as if the worst case is true. Photo of the engine, showing the recoil starter and carburettor.

## Price
**5,868 to 11,725 NGN** (priced as material, width 0.6657, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, circuit_board 5%, rubber 5% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 9,312 NGN

Conditions attached to this price:
- Not identified: The answer names wgc380i, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Maxmech Wgc-380ei 300a / 2.5kva Welding Generator', 'category': 'generator', 'price_ngn': 800000, 'is_used': False, 'url': '/lagos-island-west/power-equipments/maxmech-wgc-380ei-300a-2-5kva-welding-generator-rAvryKzKWcwQ7cAtqwE2Lxad.html?page=2&pos=1&cur_pos=1&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
