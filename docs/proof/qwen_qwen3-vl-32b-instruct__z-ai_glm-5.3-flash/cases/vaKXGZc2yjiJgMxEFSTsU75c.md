# Case vaKXGZc2yjiJgMxEFSTsU75c

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  24635 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.95)
- Made of: carton 95%, plastic 5%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: HITACHI
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: HITACHI | AIR CONDITIONER | Outdoor Unit

## Two readers
- brand_text agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 17 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- 1
- AR CENOITOUNER
- IR CONDITIONER
- 2
- ndour Unit>
- ONDIT
- AIR CONDITIONER
- Outdoor Units

## Chain
- **ocr** -> ok. 8 lines: 1 | AR CENOITOUNER | IR CONDITIONER | 2 | ndour Unit> | ONDIT | AIR CONDITIONER | Outdoor Units
- **corroborate** -> dispute. brand_text agreed by both readers; model_text was seen by only one reader, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 17 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=HITACHI model=None label=True lines=3
- **gate** -> abstain. multiple items in frame

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6802 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 15034 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2799 ms (replayed)
- total across calls: 24635 ms; wall clock: 713 ms

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 16%
- The photos show more than one item, so no single item can be identified.
- read off the item's own label
- 3 lines seen by both readers
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] Hisense 1.5hp inverter Ac
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Hisense 1.5hp inverter Ac
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Hisense 1.5hp inverter Ac
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Hisense 1.5hp inverter Ac
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
**375 to 1,845 NGN** (priced as material, width 1.3234, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of carton 95%, plastic 5% (rates for carton, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 930 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Hisense 1.5hp inverter Ac -> not proven remotely. Agent reads the outdoor rating plate.
- Hisense 1.5hp inverter Ac -> not proven remotely. Agent reads the outdoor rating plate.
- Hisense 1.5hp inverter Ac -> not proven remotely. Agent reads the outdoor rating plate.
- Hisense 1.5hp inverter Ac -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Hisense 1.5HP Efficient Split Air Conditioner', 'category': 'split_ac', 'price_ngn': 364000, 'is_used': False, 'url': '/ayobo-ipaja/home-appliances/hisense-1-5hp-efficient-split-air-conditioner-vaKXGZc2yjiJgMxEFSTsU75c.html?page=1&pos=1&cur_pos=1&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
