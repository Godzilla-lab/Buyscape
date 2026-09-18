# Case 3R6YKYsmI6DPKGwYJAgGdcKM

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  22578 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: FIRMAN
- Model read off the item: FPG-3000
- Rating read: 2800W / 3000W MAX
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on red frame, dust and grime on engine cover, no visible damage to wheels or handle
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: FIRMAN | POWER EQUIPMENT | MODEL: FPG-3000 | SERIAL NO: FPG3000123456 | OUTPUT: 2800W / 3000W MAX | VOLTAGE: 120V | FUEL TANK CAPACITY: 1.5 GAL | RUNNING TIME: 8 HRS @ 50% LOAD

## Two readers
- brand_text was read by one reader and confirmed by OCR

## OCR read off the photos
- SELEPAO
- FIRMAN

## Chain
- **corroborate** -> unavailable. no fixture for task=read_evidence key=1a9eb35eaa4ff07a2ec89741803a83fe (model=mistralai/mistral-small-3.2-24b-instruct);
- **ocr** -> ok. 2 lines: SELEPAO | FIRMAN
- **corroborate** -> agree. brand_text was read by one reader and confirmed by OCR
- **read_evidence** -> ok. category=generator brand=FIRMAN model=FPG-3000 label=True lines=14
- **retrieval** -> ok. query='FIRMAN FPG-3000 2800W / 3000W MAX FIRMAN POWER EQUIPMENT MODEL: FPG-3000 SERIAL NO: FPG300' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Sumec Firman SPG8800 8.1kVA', 'Sumec Firman ECO8990ES 6.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=FIRMAN FPG-3000 margin=0.7
- **abstain** -> abstain. seller names another generation

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7549 ms (replayed)
- identify on z-ai/glm-5.3-flash: 11345 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3684 ms (replayed)
- total across calls: 22578 ms; wall clock: 1524 ms

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.55)
  - Sumec Firman SPG3000 3.1kVA (0.5)
  - Sumec Firman SPG8800 8.1kVA (0.35)
  - Sumec Firman ECO8990ES 6.5kVA (0.3)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer rests on fpg3000, which the OCR engine did not read off the item and the seller did not say. Two readers transcribing the same code is not enough on its own. This needs a sharp photo of the label.

## How sure the engine is (back office)
**Not sure enough to price: 38% on the best answer. It is probably a FIRMAN FPG-3000 or a Sumec Firman SPG3000, and the photos cannot separate them.**

- Identification confidence: 38% (unknown)
- Price confidence: 14%
- It is weighing: FIRMAN FPG-3000 (0.9), Sumec Firman SPG3000 (0.2)
- The answer rests on fpg3000, which the OCR engine did not read off the item and the seller did not say. Two readers transcribing the same code is not enough on its own. This needs a sharp photo of the label.
- read off the item's own label
- only one reader saw these photos, the second was unavailable
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_
2. [PHOTO] Close-up of the plate on the engine block showing the engine model and serial.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it start and run right now?
- When was it last serviced, and what was done?

## Claims
- [unverifiable_remote] SUMEC FIRMAN ECO12990ES
- [unverified] 12kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% copper wire
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] 2 years warranty
- [unverifiable_remote] Automatic Starter and Manual
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
**4,334 to 12,850 NGN** (priced as material, width 0.991, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, circuit_board 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 10,250 NGN

Conditions attached to this price:
- Not identified: The answer rests on fpg3000, which the OCR engine did not read off the item and the seller did not say. Two readers transcribing the same code is not enough on its own. This needs a sharp photo of the label.
- SUMEC FIRMAN ECO12990ES -> not proven remotely. Agent will confirm at pickup.
- 12kva -> not proven remotely. Agent reads the rating plate.
- 100% copper wire -> not proven remotely. Agent opens the side cover and inspects the windings.
- 2 years warranty -> not proven remotely. Agent will confirm at pickup.
- Automatic Starter and Manual -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Eco12990es 12kva Firman 100% Copper Automatic Manual', 'category': 'generator', 'price_ngn': 890000, 'is_used': False, 'url': '/ikeja/power-equipments/eco12990es-12kva-firman-100-copper-automatic-manual-3R6YKYsmI6DPKGwYJAgGdcKM.html?page=2&pos=7&cur_pos=7&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
