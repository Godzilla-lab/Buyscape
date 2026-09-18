# Case 5iYVQxtrrQj70M6sADVjKIhY

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  14560 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.9)
- Made of: steel 60%, aluminium 20%, plastic 10%, rubber 10%
- Estimated weight: 85.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: some surface rust on metal frame, dirt and grime on engine and casing, red fuel tank shows minor scratches
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: REDMI 13C

## Two readers
- item_type agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- 9 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- RIXUAT
- CHINA
- REDMI 13C

## Chain
- **ocr** -> ok. 3 lines: RIXUAT | CHINA | REDMI 13C
- **corroborate** -> dispute. item_type agreed by both readers; brand_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; 9 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=None label=True lines=1
- **retrieval** -> empty. query='REDMI 13C IMEX diesel generator set, which consists of a diesel engine coupled to an elect' hits=[]
- **gate** -> abstain. no candidates and no model text

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5840 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6789 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 1931 ms (replayed)
- total across calls: 14560 ms; wall clock: 1567 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 20%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- read off the item's own label
- 1 lines seen by both readers
- 7 claims are still unproven, 0 are supported

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
- [unverifiable_remote] The item is an IMEX diesel generator set.
- [unverifiable_remote] The generator set consists of a diesel engine coupled to an electrical alternator.
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
**42,439 to 83,980 NGN** (priced as material, width 0.6572, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 85 kg of steel 60%, aluminium 20%, plastic 10%, rubber 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 60,775 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- The item is an IMEX diesel generator set. -> not proven remotely. Agent will confirm at pickup.
- The generator set consists of a diesel engine coupled to an electrical alternator. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '1130 Diesel Generator With Alternator 35hp', 'category': 'generator', 'price_ngn': 2900000, 'is_used': False, 'url': '/ojo/power-equipments/1130-diesel-generator-with-alternator-35hp-5iYVQxtrrQj70M6sADVjKIhY.html?page=2&pos=16&cur_pos=16&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
