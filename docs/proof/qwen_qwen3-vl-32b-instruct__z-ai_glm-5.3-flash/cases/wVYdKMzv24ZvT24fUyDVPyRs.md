# Case wVYdKMzv24ZvT24fUyDVPyRs

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  26465 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 45.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on yellow casing, some dust and grime on surface, tire appears intact but slightly worn
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | CE | ELEPAQ

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 15 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- ELEPAQ
- YADFENG-

## Chain
- **ocr** -> ok. 2 lines: ELEPAQ | YADFENG-
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 15 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=3
- **retrieval** -> ok. query='ELEPAQ ELEPAQ CE ELEPAQ Long-lasting ELEPAQ 10KVA generator with copper coil. Built to del' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Maxmech MX10000 10kVA', 'Kemage KM10000 10kVA']
- **identify** -> ok. chosen=ELEPAQ SV22000E1 margin=None
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7950 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8967 ms (replayed)
- identify on z-ai/glm-5.3-flash: 7047 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2501 ms (replayed)
- total across calls: 26465 ms; wall clock: 308 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)
  - Maxmech MX10000 10kVA (0.2333)
  - Kemage KM10000 10kVA (0.2333)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names sv22000e1, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

## How sure the engine is (back office)
**Not sure enough to price: 51% on the best answer. It is probably a ELEPAQ SV22000E1, and the photos cannot separate them.**

- Identification confidence: 51% (unsure)
- Price confidence: 18%
- It is weighing: ELEPAQ SV22000E1 (0.85)
- The answer names sv22000e1, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 3 lines seen by both readers
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
- [unverified] ELEPAQ 10KVA generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] generator with copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] built to deliver stable and efficient performance
    priced as: assumed does not start. Agent starts the generator and runs it under load
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
**17,955 to 77,130 NGN** (priced as material, width 1.2447, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 45 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 59,850 NGN

Conditions attached to this price:
- Not identified: The answer names sv22000e1, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- ELEPAQ 10KVA generator -> not proven remotely. Agent reads the rating plate.
- generator with copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- built to deliver stable and efficient performance -> not proven remotely. Agent starts the generator and runs it under load.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '10kva Elepaq Generator – Ideal for Home Appliances', 'category': 'generator', 'price_ngn': 768000, 'is_used': False, 'url': '/badagry/power-equipments/10kva-elepaq-generator-ideal-for-home-appliances-wVYdKMzv24ZvT24fUyDVPyRs.html?page=1&pos=6&cur_pos=6&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
