# Case 2VN7tUVvVZorGX1HLagfpZ1Z

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  35771 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 5%, rubber 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: GP ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuff marks on plastic casing, dust and grime on surface, soccer ball placed on top, not part of item
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: GP ELEPAQ | ELEPAQ | GP ELEPAQ

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 11 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- EGREENEROY
- GPELEPAQ
- GPEL

## Chain
- **ocr** -> ok. 3 lines: EGREENEROY | GPELEPAQ | GPEL
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; model_text was seen by only one reader, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 11 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=GP ELEPAQ model=None label=True lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='GP ELEPAQ GP ELEPAQ ELEPAQ GP ELEPAQ 4.5kva elepaq generator 
 copper coil 
With warranty ' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> refused. chosen=GP ELEPAQ None margin=0.15
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7095 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 14297 ms (replayed)
- identify on z-ai/glm-5.3-flash: 8404 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 5975 ms (replayed)
- total across calls: 35771 ms; wall clock: 1488 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.55)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Label shows only GP ELEPAQ with no model; seller says 4.5kVA, matching neither shortlist entry (2.5kVA/6.5kVA); no model plate or kVA figure legible in photos.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 7% on the best answer. It is probably a Elepaq SV6800 or a Elepaq SV2200, and the photos cannot separate them.**

- Identification confidence: 7% (unknown)
- Price confidence: 14%
- It is weighing: Elepaq SV6800 (0.25), Elepaq SV2200 (0.1)
- Label shows only GP ELEPAQ with no model; seller says 4.5kVA, matching neither shortlist entry (2.5kVA/6.5kVA); no model plate or kVA figure legible in photos.
- read off the item's own label
- 3 lines seen by both readers
- the next candidate was only 0.15 behind
- looks like a catalogue or stock image
- 10 claims are still unproven, 0 are supported

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
- [unverified] 4.5kva elepaq generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] elepaq generator
- [unverifiable_remote] copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] With warranty
- [unverifiable_remote] Payment on delivery with Lagos
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
**3,938 to 11,725 NGN** (priced as material, width 0.9943, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, circuit_board 5%, rubber 5% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 9,312 NGN

Conditions attached to this price:
- Not identified: Label shows only GP ELEPAQ with no model; seller says 4.5kVA, matching neither shortlist entry (2.5kVA/6.5kVA); no model plate or kVA figure legible in photos.
- Evidence flag: looks like a catalogue or stock image
- 4.5kva elepaq generator -> not proven remotely. Agent reads the rating plate.
- elepaq generator -> not proven remotely. Agent will confirm at pickup.
- copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- With warranty -> not proven remotely. Agent will confirm at pickup.
- Payment on delivery with Lagos -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '4.5kva Gp Elepaq Generator With Warranty  Copper Coil', 'category': 'generator', 'price_ngn': 275000, 'is_used': False, 'url': '/lagos/power-equipments/4-5kva-gp-elepaq-generator-with-warranty-copper-coil-2VN7tUVvVZorGX1HLagfpZ1Z.html?page=1&pos=8&cur_pos=8&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
