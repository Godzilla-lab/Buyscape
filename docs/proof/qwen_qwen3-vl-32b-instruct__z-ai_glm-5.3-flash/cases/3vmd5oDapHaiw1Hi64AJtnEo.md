# Case 3vmd5oDapHaiw1Hi64AJtnEo

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  17143 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: SUMEC FIRMAN
- Model read off the item: SPG2500
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, no visible damage to frame or engine
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: SUMEC FIRMAN SHO2800 | POWER GENERATOR | SPG2500

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- model_text was read by one reader and confirmed by OCR
- rating_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 19 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- SPG2500
- FIRMAN
- SUMEC

## Chain
- **ocr** -> ok. 3 lines: SPG2500 | FIRMAN | SUMEC
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; model_text was read by one reader and confirmed by OCR; rating_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 19 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=SUMEC FIRMAN model=SPG2500 label=True lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='SUMEC FIRMAN SPG2500 SUMEC FIRMAN SHO2800 POWER GENERATOR SPG2500 Very clean like brand ne' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Sumec Firman ECO8990ES 6.5kVA', 'Sumec Firman SPG8800 8.1kVA']
- **identify** -> label. named from the label: SUMEC FIRMAN SPG2500, not in the catalogue
- **abstain** -> pass. confidence=0.45 from the label

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7526 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 7276 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2341 ms (replayed)
- total across calls: 17143 ms; wall clock: 1707 ms

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.5)
  - Sumec Firman SPG3000 3.1kVA (0.4)
  - Sumec Firman ECO8990ES 6.5kVA (0.3)
  - Sumec Firman SPG8800 8.1kVA (0.3)

**Answer: SUMEC FIRMAN SPG2500** (named from the item's own label; not in the catalogue)

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**45%: the photos do not say what this is.**

- Identification confidence: 45% (unsure)
- Price confidence: 0%
- named from the item's own label, which the catalogue does not list
- read off the item's own label
- 2 lines seen by both readers
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
- [unverifiable_remote] Very clean like brand new
- [unverifiable_remote] working
    priced as: assumed does not start. Agent starts the generator and runs it under load
- [unverifiable_remote] up to 6 months warranty
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
**NO_PRICE_DATA.** Only 0 comparable asking prices were found and there is no published band for this category, so no honest range can be produced. Nothing below the 33,250 NGN floor.

Conditions attached to this price:
- Evidence flag: looks like a catalogue or stock image
- Very clean like brand new -> not proven remotely. Agent will confirm at pickup.
- working -> not proven remotely. Agent starts the generator and runs it under load.
- up to 6 months warranty -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '2.5kva Gasoline Generator', 'category': 'generator', 'price_ngn': 300000, 'is_used': True, 'url': '/ikeja/power-equipments/2-5kva-gasoline-generator-3vmd5oDapHaiw1Hi64AJtnEo.html?page=2&pos=19&cur_pos=19&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
