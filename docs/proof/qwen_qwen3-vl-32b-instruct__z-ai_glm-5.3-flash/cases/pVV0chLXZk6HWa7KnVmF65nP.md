# Case pVV0chLXZk6HWa7KnVmF65nP

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0015  |  49122 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, circuit_board 10%, rubber 10%, copper_insulated 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: AVG
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, dirt on wheels and frame, no visible damage to control panel or housing
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 1000W MAX OUTPUT | CIRCUIT BREAKER | FUEL TANK CAPACITY: 1.5L | RUNNING TIME: 3.5 HOURS @ 50% LOAD | AVG

## Two readers
- item_type agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 9 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> dispute. item_type agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 9 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=generator brand=AVG model=None label=True lines=5
- **retrieval** -> ok. query='AVG 1000W MAX OUTPUT CIRCUIT BREAKER FUEL TANK CAPACITY: 1.5L RUNNING TIME: 3.5 HOURS @ 50' hits=['Maxmech MX3500 3.5kVA', 'Maxmech MX10000 10kVA', 'Kemage KM6500 5.5kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA']
- **identify** -> refused. chosen=None None margin=0.05
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7949 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 24225 ms (replayed)
- identify on z-ai/glm-5.3-flash: 13085 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3863 ms (replayed)
- total across calls: 49122 ms; wall clock: 1507 ms

## Identification
Shortlist from the catalogue:
  - Maxmech MX3500 3.5kVA (0.55)
  - Maxmech MX10000 10kVA (0.4333)
  - Kemage KM6500 5.5kVA (0.15)
  - Lutian LT3900 3.5kVA (0.15)
  - Senwei SW3500 3.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Seller claims Maxmech 6.9kVA, but no legible model plate confirms it and no shortlist entry matches 6.9kVA; OCR text (1000W, AVG) is inconsistent and unreliable.

## How sure the engine is (back office)
**Not sure enough to price: 8% on the best answer. It is probably a Maxmech MX10000 or a Maxmech MX3500, and the photos cannot separate them.**

- Identification confidence: 8% (unknown)
- Price confidence: 14%
- It is weighing: Maxmech MX10000 (0.2), Maxmech MX3500 (0.15)
- Seller claims Maxmech 6.9kVA, but no legible model plate confirms it and no shortlist entry matches 6.9kVA; OCR text (1000W, AVG) is inconsistent and unreliable.
- read off the item's own label
- 4 lines seen by both readers
- the brand was read by only one reader and is not confirmed
- the next candidate was only 0.05 behind
- 10 claims are still unproven, 0 are supported

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
- [unverified] Brand new 6.9kva Maxmech generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] 6.9kva Maxmech generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] Maxmech generator
- [unverifiable_remote] With warranty
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
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
**5,344 to 17,600 NGN** (priced as material, width 1.0682, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 30%, circuit_board 10%, rubber 10%, copper_insulated 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 14,125 NGN

Conditions attached to this price:
- Not identified: Seller claims Maxmech 6.9kVA, but no legible model plate confirms it and no shortlist entry matches 6.9kVA; OCR text (1000W, AVG) is inconsistent and unreliable.
- Brand new 6.9kva Maxmech generator -> not proven remotely. Agent reads the rating plate.
- 6.9kva Maxmech generator -> not proven remotely. Agent reads the rating plate.
- Maxmech generator -> not proven remotely. Agent will confirm at pickup.
- With warranty -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '6.9kva Maxmech Generator 100%Copper Coil With Warranty', 'category': 'generator', 'price_ngn': 700000, 'is_used': False, 'url': '/lagos/power-equipments/6-9kva-maxmech-generator-100-copper-coil-with-warranty-pVV0chLXZk6HWa7KnVmF65nP.html?page=1&pos=15&cur_pos=15&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
