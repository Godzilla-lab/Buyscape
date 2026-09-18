# Case gsbW9Vdx7tp7RvFb4wDvrF4r

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  21884 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: plastic 70%, steel 20%, circuit_board 10%
- Estimated weight: 8.5 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: KM5000I
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, no visible damage to engine or controls
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: KM5000I | INVERTER GENERATOR | ENGINE: OHV 4-STROKE 79CC

## Two readers
- model_text agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- KM5000i

## Chain
- **ocr** -> ok. 1 lines: KM5000i
- **corroborate** -> dispute. model_text agreed by both readers; brand_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=KM5000I label=True lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='KM5000I KM5000I INVERTER GENERATOR ENGINE: OHV 4-STROKE 79CC Kemage equipped with overload' hits=['Kemage KM10000 10kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Kemage KM5000I margin=None
- **abstain** -> pass. confidence=0.47 margin=None

## Identification
Shortlist from the catalogue:
  - Kemage KM10000 10kVA (0.4333)
  - Kemage KM6500 5.5kVA (0.4)

**Answer: Kemage KM5000I Inverter generator, OHV 4-stroke 79cc** (margin None)

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 47% on the best answer. It is probably a Kemage KM5000I, and the photos cannot separate them.**

- Identification confidence: 47% (unsure)
- Price confidence: 0%
- It is weighing: Kemage KM5000I (0.95)
- read off the item's own label
- 3 lines seen by both readers
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
- [unverifiable_remote] Kemage equipped with overload protection
- [unverifiable_remote] Kemage equipped with low-oil shutdown
- [unverifiable_remote] The Kemage 5000 helps protect both...
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
**1,409 to 2,941 NGN** (priced as material, width 0.7039, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.6634 for unproven claims.

Scrap floor: 2,125 NGN

Conditions attached to this price:
- Evidence flag: looks like a catalogue or stock image
- Kemage equipped with overload protection -> not proven remotely. Agent will confirm at pickup.
- Kemage equipped with low-oil shutdown -> not proven remotely. Agent will confirm at pickup.
- The Kemage 5000 helps protect both... -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Kemage 5000i 4.5kva Low-Noise Inverter Generator', 'category': 'generator', 'price_ngn': 480000, 'is_used': False, 'url': '/ajah/power-equipments/kemage-5000i-4-5kva-low-noise-inverter-generator-gsbW9Vdx7tp7RvFb4wDvrF4r.html?page=2&pos=6&cur_pos=6&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
