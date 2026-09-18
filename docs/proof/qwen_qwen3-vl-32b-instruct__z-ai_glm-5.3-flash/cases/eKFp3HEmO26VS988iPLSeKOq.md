# Case eKFp3HEmO26VS988iPLSeKOq

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0013  |  30728 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: ELEPAQ | CONSTANT | CE | ELEPAQ | CONSTANT | CE

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- rating_text was seen by only one reader, so it is treated as unread
- 4 transcribed lines was seen by only one reader, so it is treated as unread

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
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; rating_text was seen by only one reader, so it is treated as unread; 4 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=6
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='ELEPAQ ELEPAQ CONSTANT CE ELEPAQ CONSTANT CE Elepaq 5800 constant generator' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> refused. chosen=Elepaq None margin=0.3
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5193 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 13809 ms (replayed)
- identify on z-ai/glm-5.3-flash: 8856 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2870 ms (replayed)
- total across calls: 30728 ms; wall clock: 1661 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Not identified: CANNOT_IDENTIFY.** Seller says 5800 Constant, which matches neither shortlist model; the rating on the red label is not legible enough to confirm the exact model number.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 10% on the best answer. It is probably a Elepaq SV6800 or a Elepaq SV2200, and the photos cannot separate them.**

- Identification confidence: 10% (unknown)
- Price confidence: 18%
- It is weighing: Elepaq SV6800 (0.35), Elepaq SV2200 (0.05)
- Seller says 5800 Constant, which matches neither shortlist model; the rating on the red label is not legible enough to confirm the exact model number.
- read off the item's own label
- 6 lines seen by both readers
- looks like a catalogue or stock image
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
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
**6,799 to 12,850 NGN** (priced as material, width 0.6158, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, circuit_board 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 10,250 NGN

Conditions attached to this price:
- Not identified: Seller says 5800 Constant, which matches neither shortlist model; the rating on the red label is not legible enough to confirm the exact model number.
- Evidence flag: looks like a catalogue or stock image
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
