# Case eKFp3HEmO26VS988iPLSeKOq

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  45831 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on red casing, no visible damage to control panel
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | CONSTANT | CE | OUTPUT: AC 220V/50Hz 2.5KVA | FUEL TANK CAPACITY: 10L

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- SU
- SALEPAO
- SELEPAQ
- ELEPAQ
- SASDLINE
- GERERATON
- —VAOFENG—
- CONSTANT

## Chain
- **ocr** -> ok. 8 lines: SU | SALEPAO | SELEPAQ | ELEPAQ | SASDLINE | GERERATON | —VAOFENG— | CONSTANT
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=5
- **retrieval** -> ok. query='ELEPAQ ELEPAQ CONSTANT CE OUTPUT: AC 220V/50Hz 2.5KVA FUEL TANK CAPACITY: 10L Elepaq 5800 ' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Elepaq SV2200 margin=0.55
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6581 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8004 ms (replayed)
- identify on z-ai/glm-5.3-flash: 28508 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2738 ms (replayed)
- total across calls: 45831 ms; wall clock: 515 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.6)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.2333)
  - Haier Thermocool HTG2700 2.5kVA (0.2333)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names sv2200, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

## How sure the engine is (back office)
**Not sure enough to price: 45% on the best answer. It is probably a Elepaq SV2200 or a Elepaq SV6800, and the photos cannot separate them.**

- Identification confidence: 45% (unsure)
- Price confidence: 18%
- It is weighing: Elepaq SV2200 (0.75), Elepaq SV6800 (0.2)
- The answer names sv2200, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 5 lines seen by both readers
- 8 claims are still unproven, 0 are supported

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
- [unverifiable_remote] Elepaq 5800 constant generator
- [unverifiable_remote] Elepaq 5800 constant generator
- [unverifiable_remote] Elepaq 5800 constant generator
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
**22,058 to 42,850 NGN** (priced as material, width 0.6407, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: The answer names sv2200, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Elepaq 5800 constant generator -> not proven remotely. Agent will confirm at pickup.
- Elepaq 5800 constant generator -> not proven remotely. Agent will confirm at pickup.
- Elepaq 5800 constant generator -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '3.5kva 5800 Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 270000, 'is_used': False, 'url': '/ikeja/power-equipments/3-5kva-5800-elepaq-constant-generator-eKFp3HEmO26VS988iPLSeKOq.html?page=1&pos=20&cur_pos=20&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
