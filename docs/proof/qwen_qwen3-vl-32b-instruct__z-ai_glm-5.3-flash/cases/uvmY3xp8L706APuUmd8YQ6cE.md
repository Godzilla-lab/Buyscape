# Case uvmY3xp8L706APuUmd8YQ6cE

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  48182 ms

## What the engine saw
- Presentation: single_unit
- Category: portable generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: Minor scuffing on yellow casing, Box is slightly creased and worn
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: SENWEI | RUN ON GASOLINE | PORTABLE GENERATOR | SV6200 | USA STANDARD | SENWEI | MODEL: SV6200 | OUTPUT: 6200W

## Two readers
- brand_text agreed by both readers
- model_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- 16 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; model_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; 16 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=portable generator brand=SENWEI model=SV6200 label=True lines=8
- **grounding** -> dropped. brand, model
- **forensics** -> flag. the reader stated brand, model it could not point to in the photos; looks like a catalogue or stock image
- **retrieval** -> ok. query='SENWEI RUN ON GASOLINE PORTABLE GENERATOR SV6200 USA STANDARD SENWEI MODEL: SV6200 OUTPUT:' hits=['Senwei SW3500 3.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA', 'Lutian LT3900 3.5kVA']
- **identify** -> ok. chosen=Senwei SV6200 margin=0.75
- **abstain** -> pass. confidence=0.47 margin=0.75

## Identification
Shortlist from the catalogue:
  - Senwei SW3500 3.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)
  - Lutian LT3900 3.5kVA (0.15)

**Answer: Senwei SV6200 Portable gasoline generator, 6200W** (margin 0.75)

Evidence flags: the reader stated brand, model it could not point to in the photos; looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 47% on the best answer. It is probably a Senwei SV6200 or a Senwei SW3500, and the photos cannot separate them.**

- Identification confidence: 47% (unsure)
- Price confidence: 0%
- It is weighing: Senwei SV6200 (0.95), Senwei SW3500 (0.2)
- read off the item's own label
- 8 lines seen by both readers
- the reader stated brand, model it could not point to in the photos
- looks like a catalogue or stock image
- 11 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate showing the kVA and model number. Then, without stopping the video: Open the side cover and photograph the alternator windings. Finish with: A short clip of the generator starting and running. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: nothing on the item says which model this is_

## Claims
- [unverified] Original 4.5kva Senwei Generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] Original 4.5kva Senwei Generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverified] Original 4.5kva Senwei Generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% Corper
- [unverifiable_remote] 5yrs warranty
- [unverifiable_remote] Power one inverter Ac, one...
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
**12,222 to 80,000 NGN** (priced as material, width 1.4699, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4074 for unproven claims.

Scrap floor: 30,000 NGN

Conditions attached to this price:
- Evidence flag: the reader stated brand, model it could not point to in the photos
- Evidence flag: looks like a catalogue or stock image
- Original 4.5kva Senwei Generator -> not proven remotely. Agent reads the rating plate.
- Original 4.5kva Senwei Generator -> not proven remotely. Agent reads the rating plate.
- Original 4.5kva Senwei Generator -> not proven remotely. Agent reads the rating plate.
- 100% Corper -> not proven remotely. Agent will confirm at pickup.
- 5yrs warranty -> not proven remotely. Agent will confirm at pickup.
- Power one inverter Ac, one... -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Original 4.5kva Senwei Generator(Sv6200) 100% Corper. 5yrs Warranty', 'category': 'generator', 'price_ngn': 230000, 'is_used': False, 'url': '/yaba/power-equipments/original-4-5kva-senwei-generator-sv6200-100-corper-5yrs-warranty-uvmY3xp8L706APuUmd8YQ6cE.html?page=2&pos=23&cur_pos=23&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
