# Case iRO7OgSsGu1ZYBzIfkJoyKOP

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  24966 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: FPG8800E2
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dust and grime on surface, scratches on casing, worn label edges
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: FPG8800E2 | 6.6 Gallon Fuel Tank | Electric Starting | OHV Engine AVR Alternator

## Two readers
- model_text agreed by both readers
- item_type agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 4 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- AN
- FPG8800E2
- 6.6 Gallon Fuel Tank
- OHV
- Electric Starting
- Engine
- AVR Alterpate

## Chain
- **ocr** -> ok. 7 lines: AN | FPG8800E2 | 6.6 Gallon Fuel Tank | OHV | Electric Starting | Engine | AVR Alterpate
- **corroborate** -> dispute. model_text agreed by both readers; item_type agreed by both readers; brand_text differed between the two readers, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 4 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=FPG8800E2 label=True lines=4
- **retrieval** -> empty. query='FPG8800E2 FPG8800E2 6.6 Gallon Fuel Tank Electric Starting OHV Engine AVR Alternator Healt' hits=[]
- **identify** -> ok. chosen=Firman FPG8800E2 margin=None
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5471 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 9859 ms (replayed)
- identify on z-ai/glm-5.3-flash: 8187 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 1449 ms (replayed)
- total across calls: 24966 ms; wall clock: 2195 ms

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The two readers disagreed about the brand and the answer's 'Firman' is not what the OCR read off the item or what the seller said. This needs a clear photo of the brand on the item.

## How sure the engine is (back office)
**Not sure enough to price: 51% on the best answer. It is probably a Firman FPG8800E2, and the photos cannot separate them.**

- Identification confidence: 51% (unsure)
- Price confidence: 22%
- It is weighing: Firman FPG8800E2 (0.85)
- The two readers disagreed about the brand and the answer's 'Firman' is not what the OCR read off the item or what the seller said. This needs a clear photo of the brand on the item.
- read off the item's own label
- 4 lines seen by both readers
- 6 claims are still unproven, 0 are supported

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
- [unverifiable_remote] Healthy and neatly used
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
**7,534 to 12,850 NGN** (priced as material, width 0.5215, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, circuit_board 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 10,250 NGN

Conditions attached to this price:
- Not identified: The two readers disagreed about the brand and the answer's 'Firman' is not what the OCR read off the item or what the seller said. This needs a clear photo of the brand on the item.
- Healthy and neatly used -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Firman 8800ez Generator', 'category': 'generator', 'price_ngn': 500000, 'is_used': True, 'url': '/lekki/power-equipments/firman-8800ez-generator-iRO7OgSsGu1ZYBzIfkJoyKOP.html?page=3&pos=4&cur_pos=4&ads_per_page=24&ads_count=15133&lid=w4bgywJfSACOHKND'}`
