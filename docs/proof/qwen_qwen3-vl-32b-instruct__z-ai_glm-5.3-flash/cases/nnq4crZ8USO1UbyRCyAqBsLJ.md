# Case nnq4crZ8USO1UbyRCyAqBsLJ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  33762 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: No visible damage or wear., Clean surface, no rust or dents.
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | ELEPAQ | ON

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- 15 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- ELEPAQ
- CONSTANT
- SASCLINN SENERATEN

## Chain
- **ocr** -> ok. 3 lines: ELEPAQ | CONSTANT | SASCLINN SENERATEN
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; 15 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=3
- **retrieval** -> ok. query='ELEPAQ ELEPAQ ELEPAQ ON 100% copper
Electric and recoil starter
Circuit Breaker (Protects ' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> refused. chosen=Elepaq None margin=0.25
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 8755 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6382 ms (replayed)
- identify on z-ai/glm-5.3-flash: 16488 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2137 ms (replayed)
- total across calls: 33762 ms; wall clock: 294 ms

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Not identified: CANNOT_IDENTIFY.** Brand is legible but no model designation is readable; both shortlist Elepaq models share this yellow frame and control panel, and photo perspective alone cannot reliably separate a 2.5kVA from a 6.5kVA unit.

## How sure the engine is (back office)
**Not sure enough to price: 30% on the best answer. It is probably a Elepaq SV2200 or a Elepaq SV6800, and the photos cannot separate them.**

- Identification confidence: 30% (unknown)
- Price confidence: 18%
- It is weighing: Elepaq SV2200 (0.55), Elepaq SV6800 (0.3)
- Brand is legible but no model designation is readable; both shortlist Elepaq models share this yellow frame and control panel, and photo perspective alone cannot reliably separate a 2.5kVA from a 6.5kVA unit.
- read off the item's own label
- 3 lines seen by both readers
- the next candidate was only 0.25 behind
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
- [unverifiable_remote] 100% copper
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] Electric and recoil starter
- [unverifiable_remote] Circuit Breaker (Protects the generator and your appliances)
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
**17,416 to 42,850 NGN** (priced as material, width 0.844, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: Brand is legible but no model designation is readable; both shortlist Elepaq models share this yellow frame and control panel, and photo perspective alone cannot reliably separate a 2.5kVA from a 6.5kVA unit.
- 100% copper -> not proven remotely. Agent opens the side cover and inspects the windings.
- Electric and recoil starter -> not proven remotely. Agent will confirm at pickup.
- Circuit Breaker (Protects the generator and your appliances) -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '4.5kva Original Elepaq Constant Generator. 100% Copper 10yrs Waranty', 'category': 'generator', 'price_ngn': 295000, 'is_used': False, 'url': '/yaba/power-equipments/4-5kva-original-elepaq-constant-generator-100-copper-10yrs-waranty-nnq4crZ8USO1UbyRCyAqBsLJ.html?page=2&pos=21&cur_pos=21&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
