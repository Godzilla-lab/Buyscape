# Case 3C6VrPuZMQvb0zCJJQIFIvif

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  27148 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 45.0 kg (confidence 0.8)
- Brand read off the item: SE-CI
- Model read off the item: SC30000
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor dust and grime on surface, no visible damage or rust
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SECI | SC30000 | GASOLINE GENERATOR | SE-CI

## Two readers
- brand_text agreed by both readers
- model_text agreed by both readers

## OCR read off the photos
- RJRA
- SE CI
- SC30000
- GASOLNE GENERATOR

## Chain
- **ocr** -> ok. 4 lines: RJRA | SE CI | SC30000 | GASOLNE GENERATOR
- **corroborate** -> agree. brand_text agreed by both readers; model_text agreed by both readers
- **read_evidence** -> ok. category=generator brand=SE-CI model=SC30000 label=True lines=4
- **retrieval** -> empty. query='SE-CI SC30000 SECI SC30000 GASOLINE GENERATOR SE-CI Senci petrol generator model sc30000 1' hits=[]
- **identify** -> ok. chosen=Senci SC30000 margin=None
- **abstain** -> pass. confidence=0.85 margin=None

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5186 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 3311 ms (replayed)
- identify on z-ai/glm-5.3-flash: 14323 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 4328 ms (replayed)
- total across calls: 27148 ms; wall clock: 319 ms

## Identification
No catalogue candidates matched.

**Answer: Senci SC30000 Gasoline generator, key start** (margin None)

## How sure the engine is (back office)
**85% sure this is a Senci SC30000 Gasoline generator, key start.**

- Identification confidence: 85% (certain)
- Price confidence: 0%
- It is weighing: Senci SC30000 (0.85)
- read off the item's own label
- 3 lines seen by both readers
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and photograph it next to the generator.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] One photo of the whole generator from the front.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: this is needed before the price can be confirmed_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it start and run right now?
- When was it last serviced, and what was done?

## Claims
- [unverifiable_remote] Senci petrol generator model sc30000
- [unverifiable_remote] 100% copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] warranty one year
- [unverifiable_remote] key start
- [unverifiable_remote] tyre
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
**NO_PRICE_DATA.** Only 0 comparable asking prices were found and there is no published band for this category, so no honest range can be produced. Nothing below the 59,850 NGN floor.

Conditions attached to this price:
- Senci petrol generator model sc30000 -> not proven remotely. Agent will confirm at pickup.
- 100% copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- warranty one year -> not proven remotely. Agent will confirm at pickup.
- key start -> not proven remotely. Agent will confirm at pickup.
- tyre -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Best Senci Petrol Generator 20kva 100% Copper Coil', 'category': 'generator', 'price_ngn': 5250000, 'is_used': False, 'url': '/lekki/power-equipments/best-senci-petrol-generator-20kva-100-copper-coil-3C6VrPuZMQvb0zCJJQIFIvif.html?page=1&pos=7&cur_pos=7&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
