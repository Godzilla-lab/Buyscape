# Case aprsW9ypO5nm22HwaYRamM4r

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0013  |  39771 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 18.0 kg (confidence 0.7)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: Item wrapped in plastic film, No visible damage or wear
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | CE

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 14 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- ELEPAQ
- -CONESANT
- ELOBEST D KING POWER

## Chain
- **ocr** -> ok. 3 lines: ELEPAQ | -CONESANT | ELOBEST D KING POWER
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 14 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=2
- **retrieval** -> ok. query='ELEPAQ ELEPAQ CE 1.5kva Elepaq constant generator sV 2500 
100% copper coil 
1 year warran' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> refused. chosen=ELEPAQ None margin=0.3
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6855 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 14987 ms (replayed)
- identify on z-ai/glm-5.3-flash: 14322 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3607 ms (replayed)
- total across calls: 39771 ms; wall clock: 1524 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.55)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Only 'ELEPAQ' and 'CE' are legible; no model plate text readable, and seller's stated model/rating (1.5kVA SV2500) is self-contradictory and unverified.

## How sure the engine is (back office)
**Not sure enough to price: 21% on the best answer. It is probably a Elepaq SV2200 or a Elepaq SV6800, and the photos cannot separate them.**

- Identification confidence: 21% (unknown)
- Price confidence: 16%
- It is weighing: Elepaq SV2200 (0.35), Elepaq SV6800 (0.05)
- Only 'ELEPAQ' and 'CE' are legible; no model plate text readable, and seller's stated model/rating (1.5kVA SV2500) is self-contradictory and unverified.
- read off the item's own label
- 2 lines seen by both readers
- 9 claims are still unproven, 0 are supported

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
- [unverified] 1.5kva Elepaq constant generator sV 2500
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] 1.5kva Elepaq constant generator sV 2500
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] 1 year warranty
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
**2,939 to 9,252 NGN** (priced as material, width 1.0356, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 18 kg of steel 60%, plastic 30%, circuit_board 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 7,380 NGN

Conditions attached to this price:
- Not identified: Only 'ELEPAQ' and 'CE' are legible; no model plate text readable, and seller's stated model/rating (1.5kVA SV2500) is self-contradictory and unverified.
- 1.5kva Elepaq constant generator sV 2500 -> not proven remotely. Agent reads the rating plate.
- 1.5kva Elepaq constant generator sV 2500 -> not proven remotely. Agent reads the rating plate.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- 1 year warranty -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '1.5kva Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 160000, 'is_used': False, 'url': '/ajah/power-equipments/1-5kva-elepaq-constant-generator-aprsW9ypO5nm22HwaYRamM4r.html?page=1&pos=3&cur_pos=3&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
