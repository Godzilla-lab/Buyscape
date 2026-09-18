# Case cy8IDagLYa3czx0aqt91E0Ad

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  27097 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 1.0)
- Made of: steel 40%, plastic 50%, circuit_board 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: STAR ARC WELDING
- Model read off the item: GENERATOR-350
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: STAR ARC WELDING GENERATOR-350 | STAR ARC | STAR ARC WELDING GENERATOR 350 | Data/Model | AC Rated Output: 3 kVA / 2.5 kW | Frequency: 50 Hz | Engine Model: 170 F/P | Max. Output: 3 kVA

## Two readers
- brand_text agreed by both readers
- model_text agreed by both readers
- item_type agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- 5 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- STAR ARC WELDING
- GENERATOR-350
- SPECIFICATION
- MCKENNYTOOLS &HARDWARE
- AC Rated Output
- Engine Model.
- Max Output.
- Data/Model
- Frequency
- e pe
- Displacement.
- Fuel Tank Capacity.

## Chain
- **ocr** -> ok. 25 lines: STAR ARC WELDING | GENERATOR-350 | SPECIFICATION | MCKENNYTOOLS &HARDWARE | AC Rated Output | Engine Model. | Max Output
- **corroborate** -> dispute. brand_text agreed by both readers; model_text agreed by both readers; item_type agreed by both readers; rating_text differed between the two readers, so it is treated as unread; 5 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=STAR ARC WELDING model=GENERATOR-350 label=True lines=11
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='STAR ARC WELDING GENERATOR-350 STAR ARC WELDING GENERATOR-350 STAR ARC STAR ARC WELDING GE' hits=['Tiger TG950 0.95kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA', 'Lutian LT3900 3.5kVA']
- **identify** -> label. named from the label: STAR ARC WELDING GENERATOR-350, not in the catalogue
- **abstain** -> pass. confidence=0.45 from the label

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6924 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 17128 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3045 ms (replayed)
- total across calls: 27097 ms; wall clock: 2063 ms

## Identification
Shortlist from the catalogue:
  - Tiger TG950 0.95kVA (0.1833)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)
  - Lutian LT3900 3.5kVA (0.15)

**Answer: STAR ARC WELDING GENERATOR-350** (named from the item's own label; not in the catalogue)

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**45%: the photos do not say what this is.**

- Identification confidence: 45% (unsure)
- Price confidence: 0%
- named from the item's own label, which the catalogue does not list
- read off the item's own label
- 11 lines seen by both readers
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
- [unverified] AC Rated Output is 3 KVA/1.0 KW
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Max. Output is 7 HP
- [unverifiable_remote] Engine Model is 170 F/P
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
**17,808 to 80,000 NGN** (priced as material, width 1.2717, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.5936 for unproven claims.

Scrap floor: 30,000 NGN

Conditions attached to this price:
- Evidence flag: looks like a catalogue or stock image
- AC Rated Output is 3 KVA/1.0 KW -> not proven remotely. Agent reads the rating plate.
- Max. Output is 7 HP -> not proven remotely. Agent will confirm at pickup.
- Engine Model is 170 F/P -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Star Arc Welding Generator 350a', 'category': 'generator', 'price_ngn': 450000, 'is_used': False, 'url': '/lagos-island-west/power-equipments/star-arc-welding-generator-350a-cy8IDagLYa3czx0aqt91E0Ad.html?page=3&pos=3&cur_pos=3&ads_per_page=24&ads_count=15133&lid=w4bgywJfSACOHKND'}`
