# Case pIH0HyBnwfwDLvyCaPavJShA

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  20618 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.9)
- Made of: plastic 40%, steel 30%, circuit_board 10%, copper 10%, rubber 10%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffing on yellow casing, black frame shows slight wear
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: SERIES | POWERFUL GENERATOR

## Two readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- 7 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- SENNEI
- SIR CHUKS
- EQUITOF

## Chain
- **ocr** -> ok. 3 lines: SENNEI | SIR CHUKS | EQUITOF
- **corroborate** -> dispute. brand_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; 7 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=None label=True lines=2
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='SERIES POWERFUL GENERATOR Senwei 3.5kva Petrol Generator, available in Quantity. Wholesale' hits=['Senwei SW3500 3.5kVA', 'Lutian LT3900 3.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Senwei SW3500 margin=0.75
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5183 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 4895 ms (replayed)
- identify on z-ai/glm-5.3-flash: 7480 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3060 ms (replayed)
- total across calls: 20618 ms; wall clock: 353 ms

## Identification
Shortlist from the catalogue:
  - Senwei SW3500 3.5kVA (0.7)
  - Lutian LT3900 3.5kVA (0.3)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names sw3500, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 25% on the best answer. It is probably a Senwei SW3500 or a Kemage KM6500, and the photos cannot separate them.**

- Identification confidence: 25% (unknown)
- Price confidence: 16%
- It is weighing: Senwei SW3500 (0.85), Kemage KM6500 (0.1)
- The answer names sw3500, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 2 lines seen by both readers
- looks like a catalogue or stock image
- 9 claims are still unproven, 0 are supported

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
- [unverified] Senwei 3.5kva Petrol Generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] available in Quantity
- [unverifiable_remote] Wholesale price
- [unverifiable_remote] Sell in quality only
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
**17,974 to 41,550 NGN** (priced as material, width 0.7921, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of plastic 40%, steel 30%, circuit_board 10%, copper 10%, rubber 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 31,875 NGN

Conditions attached to this price:
- Not identified: The answer names sw3500, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Evidence flag: looks like a catalogue or stock image
- Senwei 3.5kva Petrol Generator -> not proven remotely. Agent reads the rating plate.
- available in Quantity -> not proven remotely. Agent will confirm at pickup.
- Wholesale price -> not proven remotely. Agent will confirm at pickup.
- Sell in quality only -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'SENWEI 3.5kva 3kva Petrol Generator', 'category': 'generator', 'price_ngn': 185000, 'is_used': False, 'url': '/lagos/power-equipments/senwei-3-5kva-3kva-petrol-generator-pIH0HyBnwfwDLvyCaPavJShA.html?page=2&pos=3&cur_pos=3&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
