# Case xkgG6hu7acapwFjS22UhqN2l

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  35988 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, copper 15%, rubber 10%, mixed_electronic 5%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, no visible rust or damage to frame, controls and labels appear intact
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: ELEPAQ | CONSTANT | CE | DISPLACEMENT: 389cc

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- 13 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- X390E
- EPAU
- ELEPAQ
- SASOLINE SENENATSS
- CONSTANT
- YADFEI

## Chain
- **ocr** -> ok. 6 lines: X390E | EPAU | ELEPAQ | SASOLINE SENENATSS | CONSTANT | YADFEI
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; 13 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=4
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='ELEPAQ ELEPAQ CONSTANT CE DISPLACEMENT: 389cc Elepaq constant 4.5kva generator' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Elepaq SV7800 margin=0.35
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.55)
  - Elepaq SV6800 6.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer names sv7800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 23% on the best answer. It is probably a Elepaq SV7800 or a Elepaq SV6800, and the photos cannot separate them.**

- Identification confidence: 23% (unknown)
- Price confidence: 18%
- It is weighing: Elepaq SV7800 (0.75), Elepaq SV6800 (0.4)
- The answer names sv7800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- read off the item's own label
- 4 lines seen by both readers
- looks like a catalogue or stock image
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it start and run right now?
- When was it last serviced, and what was done?

## Claims
- [unverified] Elepaq constant 4.5kva generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] Elepaq constant 4.5kva generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] Elepaq constant 4.5kva generator
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
**21,027 to 58,225 NGN** (priced as material, width 0.9387, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 30%, copper 15%, rubber 10%, mixed_electronic 5% (rates for mixed_electronic, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 44,250 NGN

Conditions attached to this price:
- Not identified: The answer names sv7800, which appears nowhere on the item or in the seller's words. A photo of the plate would confirm or correct it.
- Evidence flag: looks like a catalogue or stock image
- Elepaq constant 4.5kva generator -> not proven remotely. Agent reads the rating plate.
- Elepaq constant 4.5kva generator -> not proven remotely. Agent reads the rating plate.
- Elepaq constant 4.5kva generator -> not proven remotely. Agent reads the rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Elepaq Constant 4.5 Kva Generator', 'category': 'generator', 'price_ngn': 270000, 'is_used': False, 'url': '/ojo/power-equipments/elepaq-constant-4-5-kva-generator-xkgG6hu7acapwFjS22UhqN2l.html?page=1&pos=12&cur_pos=12&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
