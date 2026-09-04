# Case gsbW9Vdx7tp7RvFb4wDvrF4r

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  31407 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.9)
- Made of: plastic 60%, steel 30%, circuit_board 10%
- Estimated weight: 8.5 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, no visible damage to handle or control panel
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: KM5000i | INVERTER GENERATOR

## Two readers
- model_text agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 7 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. model_text agreed by both readers; brand_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 7 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=KM5000i label=True lines=2
- **grounding** -> dropped. model
- **forensics** -> flag. the reader stated model it could not point to in the photos; looks like a catalogue or stock image
- **retrieval** -> ok. query='KM5000i INVERTER GENERATOR Kemage equipped with overload protection and low-oil shutdown, ' hits=['Kemage KM10000 10kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> ok. chosen=Kemage KM5000i margin=0.75
- **abstain** -> pass. confidence=0.47 margin=0.75

## Identification
Shortlist from the catalogue:
  - Kemage KM10000 10kVA (0.4333)
  - Kemage KM6500 5.5kVA (0.4)

**Answer: Kemage KM5000i Inverter Generator** (margin 0.75)

Evidence flags: the reader stated model it could not point to in the photos; looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 47% on the best answer. It is probably a Kemage KM5000i or a Kemage KM6500, and the photos cannot separate them.**

- Identification confidence: 47% (unsure)
- Price confidence: 0%
- It is weighing: Kemage KM5000i (0.95), Kemage KM6500 (0.2), Kemage KM10000 (0.1)
- read off the item's own label
- 2 lines seen by both readers
- the reader stated model it could not point to in the photos
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
**2,030 to 5,848 NGN** (priced as material, width 0.9693, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.6634 for unproven claims.

Scrap floor: 3,060 NGN

Conditions attached to this price:
- Evidence flag: the reader stated model it could not point to in the photos
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
