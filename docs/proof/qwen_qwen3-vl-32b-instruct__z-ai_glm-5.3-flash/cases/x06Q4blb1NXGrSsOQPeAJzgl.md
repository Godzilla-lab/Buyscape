# Case x06Q4blb1NXGrSsOQPeAJzgl

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  24972 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 5%, rubber 5%
- Estimated weight: 35.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuff marks on yellow casing, some dirt on control panel and wheels, no visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | ELEPAQ 2.8 KVA

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 13 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 13 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=2
- **grounding** -> dropped. brand
- **forensics** -> flag. the reader stated brand it could not point to in the photos
- **gate** -> abstain. multiple items in frame

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

Evidence flags: the reader stated brand it could not point to in the photos

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 18%
- The photos show more than one item, so no single item can be identified.
- read off the item's own label
- 2 lines seen by both readers
- the reader stated brand it could not point to in the photos
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_

## Claims
- [unverifiable_remote] Elepaq Constant is the original Elepaq generator
- [unverifiable_remote] has unique sound very low noise
- [unverifiable_remote] 25ltr petrol
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
**9,461 to 21,665 NGN** (priced as material, width 0.7841, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 35 kg of steel 60%, plastic 30%, circuit_board 5%, rubber 5% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 14,262 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Evidence flag: the reader stated brand it could not point to in the photos
- Elepaq Constant is the original Elepaq generator -> not proven remotely. Agent will confirm at pickup.
- has unique sound very low noise -> not proven remotely. Agent will confirm at pickup.
- 25ltr petrol -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '11kva Elepaq Constant Key Start Generator Sv22000e2', 'category': 'generator', 'price_ngn': 880000, 'is_used': False, 'url': '/ajah/power-equipments/11kva-elepaq-constant-key-start-generator-sv22000e2-x06Q4blb1NXGrSsOQPeAJzgl.html?page=1&pos=10&cur_pos=10&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
