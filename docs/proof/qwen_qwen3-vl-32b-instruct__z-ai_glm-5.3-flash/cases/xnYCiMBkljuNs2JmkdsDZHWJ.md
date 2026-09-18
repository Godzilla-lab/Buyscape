# Case xnYCiMBkljuNs2JmkdsDZHWJ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  35739 ms

## What the engine saw
- Presentation: single_unit
- Category: inverter generator (confidence 0.95)
- Made of: steel 40%, plastic 35%, circuit_board 15%, rubber 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: BECTRODES
- Model read off the item: nothing legible
- Rating read: 5.6kVA, 5.0kW
- Label, plate or settings screen legible: yes
- Damage noted: box is slightly creased and scuffed, generator casing has minor scratches
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: 5.6kVA | Max power | Rated power | DIGITAL INVERTER TECHNOLOGY | ULTRA COMPACT SIZE | INVERTER GENERATOR | TWO WIRE AUTO START | PREMIUM QUALITY

## Two readers
- rating_text agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- 6 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- 5.6kVA
- INVERTER GENERATOR
- 5.0kVA
- Max power
- AUTO START
- TWO WIRS
- PREMUM
- OUALITY
- Rated power
- - DIGITAL INVERTER TECHNOLOSY
- D15
- BC7800IES

## Chain
- **ocr** -> ok. 18 lines: 5.6kVA | INVERTER GENERATOR | 5.0kVA | Max power | AUTO START | TWO WIRS | PREMUM | OUALITY | Rated power | - DIGITAL IN
- **corroborate** -> dispute. rating_text agreed by both readers; model_text was seen by only one reader, so it is treated as unread; 6 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=inverter generator brand=BECTRODES model=None label=True lines=11
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='BECTRODES 5.6kVA, 5.0kW 5.6kVA Max power Rated power DIGITAL INVERTER TECHNOLOGY ULTRA COM' hits=['Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Senci SC7800IES margin=0.85
- **abstain** -> abstain. confidence 0.36: read off the item's own label; 9 lines seen by both readers; the brand was read by only one reader and is not confirmed; looks like a catalogue or stock image

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 16326 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 11348 ms (replayed)
- identify on z-ai/glm-5.3-flash: 4988 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3077 ms (replayed)
- total across calls: 35739 ms; wall clock: 549 ms

## Identification
Shortlist from the catalogue:
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The evidence only supports this answer at 36 percent, which is a guess. One clear photo of the label would settle it.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 22% on the best answer. It is probably a Senci SC7800IES or a Kemage KM6500, and the photos cannot separate them.**

- Identification confidence: 22% (unknown)
- Price confidence: 16%
- It is weighing: Senci SC7800IES (0.9), Kemage KM6500 (0.05)
- The evidence only supports this answer at 36 percent, which is a guess. One clear photo of the label would settle it.
- read off the item's own label
- 9 lines seen by both readers
- the brand was read by only one reader and is not confirmed
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
- [unverifiable_remote] Brand new Senci petrol inverter generator
- [unverifiable_remote] Model SC7800IES
- [unverifiable_remote] Complete 5/5.6KVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Soundproof technology
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
**5,075 to 11,575 NGN** (priced as material, width 0.7808, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 35%, circuit_board 15%, rubber 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 9,000 NGN

Conditions attached to this price:
- Not identified: The evidence only supports this answer at 36 percent, which is a guess. One clear photo of the label would settle it.
- Evidence flag: looks like a catalogue or stock image
- Brand new Senci petrol inverter generator -> not proven remotely. Agent will confirm at pickup.
- Model SC7800IES -> not proven remotely. Agent will confirm at pickup.
- Complete 5/5.6KVA -> not proven remotely. Agent reads the rating plate.
- Soundproof technology -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Sc7800ies Senci 5/5.6kva Two Wire Auto Start Petrol Inverter Generator', 'category': 'generator', 'price_ngn': 850000, 'is_used': False, 'url': '/ojo/power-equipments/sc7800ies-senci-5-5-6kva-two-wire-auto-start-petrol-inverter-generator-xnYCiMBkljuNs2JmkdsDZHWJ.html?page=2&pos=18&cur_pos=18&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
