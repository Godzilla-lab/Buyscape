# Case jRMbUhqAqIZE2pkBwQcCLDO2

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  36583 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: plastic 40%, steel 30%, circuit_board 10%, rubber 10%, mixed_electronic 10%
- Estimated weight: 12.0 kg (confidence 0.8)
- Brand read off the item: MAXMECH
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: item wrapped in plastic film, no visible damage or wear
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MAXMECH | MAXMECH

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- MAXMECH
- BAROLIDE SEMERATOR

## Chain
- **ocr** -> ok. 2 lines: MAXMECH | BAROLIDE SEMERATOR
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=MAXMECH model=None label=True lines=2
- **retrieval** -> ok. query='MAXMECH MAXMECH MAXMECH Maxmech 12kva petrol generator. 100% pure copper coil. High perfor' hits=['Maxmech MX3500 3.5kVA', 'Maxmech MX10000 10kVA']
- **identify** -> ok. chosen=Maxmech EPS 8000 margin=0.55
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Maxmech MX3500 3.5kVA (0.5)
  - Maxmech MX10000 10kVA (0.4333)

**Not identified: EVIDENCE_INCOMPLETE.** The answer states 8kva but the evidence shows 12kva.

## How sure the engine is (back office)
**Not sure enough to price: 51% on the best answer. It is probably a Maxmech EPS 8000 or a Maxmech MX10000, and the photos cannot separate them.**

- Identification confidence: 51% (unsure)
- Price confidence: 18%
- It is weighing: Maxmech EPS 8000 (0.85), Maxmech MX10000 (0.3)
- The answer states 8kva but the evidence shows 12kva.
- read off the item's own label
- 2 lines seen by both readers
- 8 claims are still unproven, 0 are supported

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
- [unverified] Maxmech 12kva petrol generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% pure copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] High performance Generator
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
**1,940 to 6,144 NGN** (priced as material, width 1.0401, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of plastic 40%, steel 30%, circuit_board 10%, rubber 10%, mixed_electronic 10% (rates for mixed_electronic, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 4,140 NGN

Conditions attached to this price:
- Not identified: The answer states 8kva but the evidence shows 12kva.
- Maxmech 12kva petrol generator -> not proven remotely. Agent reads the rating plate.
- 100% pure copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- High performance Generator -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Maxmech Peteol Generator 12kva.', 'category': 'generator', 'price_ngn': 848000, 'is_used': False, 'url': '/alimosho/power-equipments/maxmech-peteol-generator-12kva-jRMbUhqAqIZE2pkBwQcCLDO2.html?page=1&pos=23&cur_pos=23&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
