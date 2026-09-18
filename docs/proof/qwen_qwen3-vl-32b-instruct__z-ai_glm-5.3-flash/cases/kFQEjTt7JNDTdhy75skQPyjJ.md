# Case kFQEjTt7JNDTdhy75skQPyjJ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  27221 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 1.0)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor surface scratches on yellow casing, dust and grime on control panel and frame
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: ELEPAQ | GASOLINE GENERATOR | MANUFACTURED BY CONSTANT | DC OUTLET: 12V/8A | DIMENSIONS: 650x450x450mm

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 15 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- ELEPAQ
- GASOLINE GENERATOR
- CST
- MNCONSTANT
- VADPENG—CE
- $V6000

## Chain
- **ocr** -> ok. 6 lines: ELEPAQ | GASOLINE GENERATOR | CST | MNCONSTANT | VADPENG—CE | $V6000
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 15 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=5
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='ELEPAQ ELEPAQ GASOLINE GENERATOR MANUFACTURED BY CONSTANT DC OUTLET: 12V/8A DIMENSIONS: 65' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> ok. chosen=Elepaq SV6800 margin=0.8
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7808 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 12776 ms (replayed)
- identify on z-ai/glm-5.3-flash: 5837 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 800 ms (replayed)
- total across calls: 27221 ms; wall clock: 1611 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names sv6800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 27% on the best answer. It is probably a Elepaq SV6800 or a Elepaq SV2200, and the photos cannot separate them.**

- Identification confidence: 27% (unknown)
- Price confidence: 24%
- It is weighing: Elepaq SV6800 (0.9), Elepaq SV2200 (0.1)
- The answer names sv6800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 5 lines seen by both readers
- looks like a catalogue or stock image
- 5 claims are still unproven, 0 are supported

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
**25,728 to 42,850 NGN** (priced as material, width 0.4993, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: The answer names sv6800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Evidence flag: looks like a catalogue or stock image
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Elepaq 4.5 KVA Generator', 'category': 'generator', 'price_ngn': 285000, 'is_used': False, 'url': '/lekki/power-equipments/elepaq-4-5-kva-generator-kFQEjTt7JNDTdhy75skQPyjJ.html?page=2&pos=13&cur_pos=13&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
