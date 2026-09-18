# Case xi3EK9AeR27pR7Fqk76h00CV

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  17960 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 45.0 kg (confidence 0.8)
- Brand read off the item: Perkins
- Model read off the item: nothing legible
- Rating read: 15kVA
- Label, plate or settings screen legible: yes
- Damage noted: minor scuff marks on casing, dirt and grime on surface, open lid with foam lining visible
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Perkins | 15kVA

## Two readers
- brand_text agreed by both readers
- rating_text agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- 3 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- 000T3
- Perkins
- SOUNDPRDOFNESE GENERITON
- 15KVA

## Chain
- **ocr** -> ok. 4 lines: 000T3 | Perkins | SOUNDPRDOFNESE GENERITON | 15KVA
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text agreed by both readers; model_text was seen by only one reader, so it is treated as unread; 3 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=Perkins model=None label=True lines=2
- **retrieval** -> ok. query='Perkins 15kVA Perkins 15kVA Original Perkins diesel generator 3 phase 100% copper coil 15 ' hits=['Perkins P150 150kVA', 'Perkins P100 100kVA', 'Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA']
- **identify** -> refused. chosen=None None margin=0.0
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5189 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 3855 ms (replayed)
- identify on z-ai/glm-5.3-flash: 5772 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3144 ms (replayed)
- total across calls: 17960 ms; wall clock: 413 ms

## Identification
Shortlist from the catalogue:
  - Perkins P150 150kVA (0.4333)
  - Perkins P100 100kVA (0.4333)
  - Lutian LT3900 3.5kVA (0.15)
  - Senwei SW3500 3.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Label clearly reads Perkins 15kVA soundproof diesel generator, but no shortlist entry matches 15kVA and no model number is legible on the plate.

## How sure the engine is (back office)
**Not sure enough to price: 5% on the best answer. It is probably a Perkins P150 or a Perkins P100, and the photos cannot separate them.**

- Identification confidence: 5% (unknown)
- Price confidence: 16%
- It is weighing: Perkins P150 (0.1), Perkins P100 (0.1)
- Label clearly reads Perkins 15kVA soundproof diesel generator, but no shortlist entry matches 15kVA and no model number is legible on the plate.
- read off the item's own label
- 2 lines seen by both readers
- the next candidate was only 0.0 behind
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
- [unverifiable_remote] Original Perkins diesel generator
- [unverifiable_remote] 3 phase
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverified] 15 kVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
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
**8,213 to 23,130 NGN** (priced as material, width 0.9518, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 45 kg of steel 60%, plastic 30%, circuit_board 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 18,450 NGN

Conditions attached to this price:
- Not identified: Label clearly reads Perkins 15kVA soundproof diesel generator, but no shortlist entry matches 15kVA and no model number is legible on the plate.
- Original Perkins diesel generator -> not proven remotely. Agent will confirm at pickup.
- 3 phase -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- 15 kVA -> not proven remotely. Agent reads the rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Original Perkins Diesel Generator 3 Phase 100% Copper Coil 15 Kva', 'category': 'generator', 'price_ngn': 2450000, 'is_used': False, 'url': '/ikeja/power-equipments/original-perkins-diesel-generator-3-phase-100-copper-coil-15-kva-xi3EK9AeR27pR7Fqk76h00CV.html?page=2&pos=8&cur_pos=8&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
