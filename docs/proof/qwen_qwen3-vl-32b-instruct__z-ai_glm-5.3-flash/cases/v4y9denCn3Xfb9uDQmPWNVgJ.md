# Case v4y9denCn3Xfb9uDQmPWNVgJ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  22718 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: COROLLA
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scratches on plastic casing, some dust and grime on surface, no visible damage to engine or frame
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: COROLLA

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 13 transcribed lines was seen by only one reader, so it is treated as unread
- item_type was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- COROLLA
- CL7800E2R
- Y-12-070-7

## Chain
- **ocr** -> ok. 3 lines: COROLLA | CL7800E2R | Y-12-070-7
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 13 transcribed lines was seen by only one reader, so it is treated as unread; item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=generator brand=COROLLA model=None label=True lines=1
- **retrieval** -> empty. query='COROLLA COROLLA Corolla remote control petrol generator model cl7800E2r 100% copper coil w' hits=[]
- **gate** -> abstain. no candidates and no model text

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7018 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 12233 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3467 ms (replayed)
- total across calls: 22718 ms; wall clock: 1454 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 16%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- read off the item's own label
- 1 lines seen by both readers
- the item_type was read by only one reader and is not confirmed
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
- [unverifiable_remote] Corolla remote control petrol generator model cl7800E2r
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] with warranty one year
- [unverifiable_remote] key
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
**16,545 to 42,850 NGN** (priced as material, width 0.8858, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- Corolla remote control petrol generator model cl7800E2r -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- with warranty one year -> not proven remotely. Agent will confirm at pickup.
- key -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'COROLLA Cl7800e2r 4.5kva Petrol Gen Remote Control', 'category': 'generator', 'price_ngn': 350000, 'is_used': False, 'url': '/ojo/power-equipments/corolla-cl7800e2r-4-5kva-petrol-gen-remote-control-v4y9denCn3Xfb9uDQmPWNVgJ.html?page=1&pos=5&cur_pos=5&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
