# Case cy8IDagLYa3czx0aqt91E0Ad

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  39706 ms

## What the engine saw
- Presentation: single_unit
- Category: welding generator (confidence 0.95)
- Made of: plastic 40%, steel 30%, circuit_board 10%, rubber 10%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: STAR ARC WELDING | GENERATOR-350 | STAR ARC | Star Arc Welding Generator 350 | Data/Model | Frequency: 50 Hz | Engine Model: 170F | Oil Capacity: 0.6 L

## Two readers
- brand_text agreed by both readers
- model_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- 9 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; model_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; 9 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=welding generator brand=STAR ARC WELDING model=GENERATOR-350 label=True lines=8
- **grounding** -> dropped. brand, model
- **forensics** -> flag. the reader stated brand, model it could not point to in the photos; looks like a catalogue or stock image
- **retrieval** -> ok. query='STAR ARC WELDING GENERATOR-350 STAR ARC Star Arc Welding Generator 350 Data/Model Frequenc' hits=['Tiger TG950 0.95kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA']
- **identify** -> ok. chosen=Star Arc Generator 350 margin=0.85
- **abstain** -> pass. confidence=0.47 margin=0.85

## Identification
Shortlist from the catalogue:
  - Tiger TG950 0.95kVA (0.1833)
  - Lutian LT3900 3.5kVA (0.15)
  - Senwei SW3500 3.5kVA (0.15)

**Answer: Star Arc Generator 350 Welding Generator, 3 KVA / 1.0 KW, 170F petrol engine** (margin 0.85)

Evidence flags: the reader stated brand, model it could not point to in the photos; looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 47% on the best answer. It is probably a Star Arc Generator 350 or a Lutian LT3900, and the photos cannot separate them.**

- Identification confidence: 47% (unsure)
- Price confidence: 0%
- It is weighing: Star Arc Generator 350 (0.95), Lutian LT3900 (0.1), Senwei SW3500 (0.1)
- read off the item's own label
- 8 lines seen by both readers
- the reader stated brand, model it could not point to in the photos
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

Scrap floor: 33,625 NGN

Conditions attached to this price:
- Evidence flag: the reader stated brand, model it could not point to in the photos
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
