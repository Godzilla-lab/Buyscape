# Case 9QjGiftEi4xPrRnrbBtqQFOd

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  44318 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: FIRMAN
- Model read off the item: nothing legible
- Rating read: 5000
- Label, plate or settings screen legible: yes
- Damage noted: minor dirt and grime on surface, some scuff marks on plastic casing
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 5000 | 4200 | FIRMAN

## Two readers
- rating_text agreed by both readers
- brand_text was read by one reader and confirmed by OCR
- model_text differed between the two readers, so it is treated as unread
- 4 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- FIRMAN
- ACMASTER
- 5000
- 4200
- AC8000EZ

## Chain
- **ocr** -> ok. 5 lines: FIRMAN | ACMASTER | 5000 | 4200 | AC8000EZ
- **corroborate** -> dispute. rating_text agreed by both readers; brand_text was read by one reader and confirmed by OCR; model_text differed between the two readers, so it is treated as unread; 4 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=FIRMAN model=None label=True lines=3
- **retrieval** -> ok. query='FIRMAN 5000 5000 4200 FIRMAN Original fireman generator 5 kVA 100% copper coin' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Sumec Firman ECO8990ES 6.5kVA', 'Sumec Firman SPG8800 8.1kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=FIRMAN AC8800E2 margin=0.75
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.35)
  - Sumec Firman SPG3000 3.1kVA (0.25)
  - Sumec Firman ECO8990ES 6.5kVA (0.15)
  - Sumec Firman SPG8800 8.1kVA (0.15)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names ac8800e2, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

## How sure the engine is (back office)
**Not sure enough to price: 54% on the best answer. It is probably a FIRMAN AC8800E2 or a Sumec Firman ECO8990ES, and the photos cannot separate them.**

- Identification confidence: 54% (unsure)
- Price confidence: 18%
- It is weighing: FIRMAN AC8800E2 (0.9), Sumec Firman ECO8990ES (0.15)
- The answer names ac8800e2, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 2 lines seen by both readers
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
- [unverifiable_remote] Original fireman generator
- [unverified] 5 kVA
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% copper coin
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
**15,580 to 42,850 NGN** (priced as material, width 0.9334, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: The answer names ac8800e2, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Original fireman generator -> not proven remotely. Agent will confirm at pickup.
- 5 kVA -> not proven remotely. Agent reads the rating plate.
- 100% copper coin -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Original Fireman Generator 5 Kva 100% Copper Coin', 'category': 'generator', 'price_ngn': 735000, 'is_used': False, 'url': '/ajah/power-equipments/original-fireman-generator-5-kva-100-copper-coin-9QjGiftEi4xPrRnrbBtqQFOd.html?page=2&pos=10&cur_pos=10&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
