# Case oQBJS6OOE3PiyhnNlndH0gFN

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  36938 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 25%, circuit_board 10%, rubber 5%
- Estimated weight: 35.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dust and grime on surface, some minor scratches on plastic casing, exposed engine components show signs of use
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: FIRMAN

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 5 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 5 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=FIRMAN model=None label=True lines=1
- **grounding** -> dropped. brand
- **forensics** -> flag. the reader stated brand it could not point to in the photos
- **retrieval** -> ok. query='FIRMAN Brand New complete 15kva Firman petrol generator 2 cylinder engine with warranty tw' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Sumec Firman ECO8990ES 6.5kVA']
- **identify** -> ok. chosen=Firman FPG15000E margin=0.75
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.4)
  - Sumec Firman SPG3000 3.1kVA (0.25)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Sumec Firman ECO8990ES 6.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names fpg15000e, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

Evidence flags: the reader stated brand it could not point to in the photos

## How sure the engine is (back office)
**Not sure enough to price: 27% on the best answer. It is probably a Firman FPG15000E or a Sumec Firman ECO8990ES, and the photos cannot separate them.**

- Identification confidence: 27% (unknown)
- Price confidence: 14%
- It is weighing: Firman FPG15000E (0.9), Sumec Firman ECO8990ES (0.15)
- The answer names fpg15000e, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 1 lines seen by both readers
- the reader stated brand it could not point to in the photos
- 11 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_
3. [PHOTO] Close-up of the plate on the engine block showing the engine model and serial.
   _why: nothing on the item says which model this is_

## Claims
- [unverified] Brand New complete 15kva Firman petrol generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 2 cylinder engine
- [unverifiable_remote] petrol generator
- [unverified] 15kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] with warranty two years
- [unverifiable_remote] key start
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
**7,610 to 28,350 NGN** (priced as material, width 1.1534, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 35 kg of steel 60%, plastic 25%, circuit_board 10%, rubber 5% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 16,712 NGN

Conditions attached to this price:
- Not identified: The answer names fpg15000e, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Evidence flag: the reader stated brand it could not point to in the photos
- Brand New complete 15kva Firman petrol generator -> not proven remotely. Agent reads the rating plate.
- 2 cylinder engine -> not proven remotely. Agent will confirm at pickup.
- petrol generator -> not proven remotely. Agent will confirm at pickup.
- 15kva -> not proven remotely. Agent reads the rating plate.
- with warranty two years -> not proven remotely. Agent will confirm at pickup.
- key start -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Brand New Complete 15kva Firman Petrol Gene 2 Cylinder Engin', 'category': 'generator', 'price_ngn': 2800000, 'is_used': False, 'url': '/ajah/power-equipments/brand-new-complete-15kva-firman-petrol-gene-2-cylinder-engin-oQBJS6OOE3PiyhnNlndH0gFN.html?page=1&pos=2&cur_pos=2&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
