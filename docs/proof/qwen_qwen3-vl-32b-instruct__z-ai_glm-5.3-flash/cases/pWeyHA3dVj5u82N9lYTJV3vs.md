# Case pWeyHA3dVj5u82N9lYTJV3vs

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  33730 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 35.0 kg (confidence 0.7)
- Brand read off the item: DAIKIN
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: DAIKIN | SPLIT AIR CONDITIONER | INVERTER | R32 | DAIKIN | INVERTER | SPLIT AIR CONDITIONER | R32

## Two readers
- brand_text agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- R32国
- INVERTER
- DAIKIN
- sine

## Chain
- **ocr** -> ok. 4 lines: R32国 | INVERTER | DAIKIN | sine
- **corroborate** -> dispute. brand_text agreed by both readers; model_text was seen by only one reader, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=DAIKIN model=None label=False lines=8
- **retrieval** -> ok. query='DAIKIN DAIKIN SPLIT AIR CONDITIONER INVERTER R32 DAIKIN INVERTER SPLIT AIR CONDITIONER R32' hits=['Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP', 'Royal RAC12 1.5HP', 'Hisense AS-12 1.5HP', 'LG S4-Q12 1.5HP']
- **identify** -> refused. chosen=Daikin None margin=None
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 4898 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 13700 ms (replayed)
- identify on z-ai/glm-5.3-flash: 12754 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2378 ms (replayed)
- total across calls: 33730 ms; wall clock: 605 ms

## Identification
Shortlist from the catalogue:
  - Samsung AR12 1.5HP (0.3)
  - Scanfrost SFAC12 1.5HP (0.3)
  - Royal RAC12 1.5HP (0.3)
  - Hisense AS-12 1.5HP (0.26)
  - LG S4-Q12 1.5HP (0.26)

**Not identified: CANNOT_IDENTIFY.** Boxes clearly read DAIKIN split inverter R32, but no model number is legible and no Daikin entry exists in the shortlist.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 20%
- Boxes clearly read DAIKIN split inverter R32, but no model number is legible and no Daikin entry exists in the shortlist.
- no label, plate or settings screen was legible
- 8 lines seen by both readers
- 7 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] The AC is a Daikin 1.5HP Inverter model.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverifiable_remote] The AC is designed for energy efficiency.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the unit.
- [unverified] Required evidence 'indoor_unit' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole indoor unit.
- [unverified] Required evidence 'outdoor_unit' was not supplied
    priced as: priced as if the worst case is true. One photo of the outdoor compressor unit.
- [unverified] Required evidence 'rating_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of the rating plate on the outdoor unit showing the model and HP.
- [unverified] Required evidence 'grille_open' was not supplied
    priced as: priced as if the worst case is true. Open the front grille of the indoor unit and photograph the filters and coil.

## Price
**1,174 to 4,200 NGN** (priced as material, width 1.1261, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 35 kg of carton 100% (rates for carton are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,100 NGN

Conditions attached to this price:
- Not identified: Boxes clearly read DAIKIN split inverter R32, but no model number is legible and no Daikin entry exists in the shortlist.
- The AC is a Daikin 1.5HP Inverter model. -> not proven remotely. Agent reads the outdoor rating plate.
- The AC is designed for energy efficiency. -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Daikin 1.5hp Inverter Split Air Conditioner | Ftkl35 / Rkl35 (R32)', 'category': 'split_ac', 'price_ngn': 700000, 'is_used': False, 'url': '/ikeja/home-appliances/daikin-1-5hp-inverter-split-air-conditioner-ftkl35-rkl35-r32-pWeyHA3dVj5u82N9lYTJV3vs.html?page=1&pos=12&cur_pos=12&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
