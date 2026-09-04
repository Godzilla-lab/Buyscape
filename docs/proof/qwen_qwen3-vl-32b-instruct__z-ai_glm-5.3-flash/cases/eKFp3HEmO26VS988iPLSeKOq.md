# Case eKFp3HEmO26VS988iPLSeKOq

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  33147 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 5%, rubber 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: Minor scuffs on red casing, Yellow sticker partially torn on front left corner
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ | CONSTANT | CE

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 19 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 19 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=3
- **grounding** -> dropped. brand
- **forensics** -> flag. the reader stated brand it could not point to in the photos
- **retrieval** -> ok. query='ELEPAQ CONSTANT CE Elepaq 5800 constant generator' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> ok. chosen=Elepaq SV6800 margin=0.6
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names sv6800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

Evidence flags: the reader stated brand it could not point to in the photos

## How sure the engine is (back office)
**Not sure enough to price: 21% on the best answer. It is probably a Elepaq SV6800 or a Elepaq SV2200, and the photos cannot separate them.**

- Identification confidence: 21% (unknown)
- Price confidence: 18%
- It is weighing: Elepaq SV6800 (0.7), Elepaq SV2200 (0.1)
- The answer names sv6800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 3 lines seen by both readers
- the reader stated brand it could not point to in the photos
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_
3. [PHOTO] Close-up of the plate on the engine block showing the engine model and serial.
   _why: nothing on the item says which model this is_

## Claims
- [unverifiable_remote] Elepaq 5800 constant generator
- [unverifiable_remote] Elepaq 5800 constant generator
- [unverifiable_remote] Elepaq 5800 constant generator
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
**6,758 to 15,475 NGN** (priced as material, width 0.7841, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, circuit_board 5%, rubber 5% (rates for circuit_board, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 10,187 NGN

Conditions attached to this price:
- Not identified: The answer names sv6800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Evidence flag: the reader stated brand it could not point to in the photos
- Elepaq 5800 constant generator -> not proven remotely. Agent will confirm at pickup.
- Elepaq 5800 constant generator -> not proven remotely. Agent will confirm at pickup.
- Elepaq 5800 constant generator -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '3.5kva 5800 Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 270000, 'is_used': False, 'url': '/ikeja/power-equipments/3-5kva-5800-elepaq-constant-generator-eKFp3HEmO26VS988iPLSeKOq.html?page=1&pos=20&cur_pos=20&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
