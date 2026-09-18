# Case rREXiw3jnu8JE2phT7cuNXze

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  37293 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: plastic 40%, steel 30%, circuit_board 10%, rubber 10%, copper_insulated 10%
- Estimated weight: 12.0 kg (confidence 0.7)
- Brand read off the item: KEMAGE
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dirt on surface, some wear on plastic casing, white cable connected to DC outlet
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: KEMAGE

## Two readers
- brand_text agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 14 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- KEMAGE

## Chain
- **ocr** -> ok. 1 lines: KEMAGE
- **corroborate** -> dispute. brand_text agreed by both readers; model_text was seen by only one reader, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 14 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=KEMAGE model=None label=True lines=1
- **retrieval** -> ok. query='KEMAGE KEMAGE Key Feature Brand: Kemage Model: KM11000E2 AC Frequency: 50 Hz Starting Capa' hits=['Kemage KM6500 5.5kVA', 'Kemage KM10000 10kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA']
- **identify** -> refused. chosen=Kemage None margin=0.15
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 15730 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6420 ms (replayed)
- identify on z-ai/glm-5.3-flash: 11481 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3662 ms (replayed)
- total across calls: 37293 ms; wall clock: 334 ms

## Identification
Shortlist from the catalogue:
  - Kemage KM6500 5.5kVA (0.55)
  - Kemage KM10000 10kVA (0.4333)
  - Lutian LT3900 3.5kVA (0.15)
  - Senwei SW3500 3.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Only 'KEMAGE' is legible; seller's KM11000E2 is not in the shortlist and no model plate is readable, so KM10000 vs KM11000E2 cannot be distinguished.

## How sure the engine is (back office)
**Not sure enough to price: 16% on the best answer. It is probably a Kemage KM10000 or a Kemage KM6500, and the photos cannot separate them.**

- Identification confidence: 16% (unknown)
- Price confidence: 14%
- It is weighing: Kemage KM10000 (0.3), Kemage KM6500 (0.15)
- Only 'KEMAGE' is legible; seller's KM11000E2 is not in the shortlist and no model plate is readable, so KM10000 vs KM11000E2 cannot be distinguished.
- read off the item's own label
- 1 lines seen by both readers
- the next candidate was only 0.15 behind
- 10 claims are still unproven, 0 are supported

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
- [unverifiable_remote] Brand: Kemage
- [unverifiable_remote] Model: KM11000E2
- [unverifiable_remote] AC Frequency: 50 Hz
- [unverified] Starting Capacity: 8.5KVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Japan
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
**3,374 to 7,944 NGN** (priced as material, width 0.8073, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of plastic 40%, steel 30%, circuit_board 10%, rubber 10%, copper_insulated 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 6,300 NGN

Conditions attached to this price:
- Not identified: Only 'KEMAGE' is legible; seller's KM11000E2 is not in the shortlist and no model plate is readable, so KM10000 vs KM11000E2 cannot be distinguished.
- Brand: Kemage -> not proven remotely. Agent will confirm at pickup.
- Model: KM11000E2 -> not proven remotely. Agent will confirm at pickup.
- AC Frequency: 50 Hz -> not proven remotely. Agent will confirm at pickup.
- Starting Capacity: 8.5KVA -> not proven remotely. Agent reads the rating plate.
- Japan -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Kemage 230V Manual Start Gasoline Generator.', 'category': 'generator', 'price_ngn': 400000, 'is_used': False, 'url': '/lekki/power-equipments/kemage-230v-manual-start-gasoline-generator-rREXiw3jnu8JE2phT7cuNXze.html?page=2&pos=17&cur_pos=17&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
