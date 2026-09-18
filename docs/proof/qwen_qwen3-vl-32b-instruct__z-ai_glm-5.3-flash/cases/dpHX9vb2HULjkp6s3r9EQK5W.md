# Case dpHX9vb2HULjkp6s3r9EQK5W

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  64338 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 40%, plastic 30%, copper 15%, rubber 10%, glass 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: ELEPAQ
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scuff marks on plastic casing, some dust and grime on engine components, tire appears slightly worn but intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: ELEPAQ

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 16 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- ELEPAQ

## Chain
- **ocr** -> ok. 1 lines: ELEPAQ
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 16 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=ELEPAQ model=None label=True lines=1
- **retrieval** -> ok. query='ELEPAQ ELEPAQ 15kva elepaq generator 100% copper generator' hits=['Elepaq SV2200 2.5kVA', 'Elepaq SV6800 6.5kVA']
- **identify** -> ok. chosen=Elepaq SV22000E margin=0.5
- **abstain** -> abstain. top score 0.6

## Identification
Shortlist from the catalogue:
  - Elepaq SV2200 2.5kVA (0.5)
  - Elepaq SV6800 6.5kVA (0.5)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.6, which is not sure enough to price.

## How sure the engine is (back office)
**Not sure enough to price: 36% on the best answer. It is probably a Elepaq SV22000E or a Elepaq SV6800, and the photos cannot separate them.**

- Identification confidence: 36% (unknown)
- Price confidence: 18%
- It is weighing: Elepaq SV22000E (0.6), Elepaq SV6800 (0.1)
- The best candidate scored only 0.6, which is not sure enough to price.
- read off the item's own label
- 1 lines seen by both readers
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
- [unverified] 15kva elepaq generator
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] elepaq generator
- [unverifiable_remote] 100% copper generator
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
**20,337 to 56,412 NGN** (priced as material, width 0.9401, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 40%, plastic 30%, copper 15%, rubber 10%, glass 5% (rates for glass, plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 43,400 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.6, which is not sure enough to price.
- 15kva elepaq generator -> not proven remotely. Agent reads the rating plate.
- elepaq generator -> not proven remotely. Agent will confirm at pickup.
- 100% copper generator -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '15kva Elepaq Constant Generator', 'category': 'generator', 'price_ngn': 700000, 'is_used': False, 'url': '/ikeja/power-equipments/15kva-elepaq-constant-generator-dpHX9vb2HULjkp6s3r9EQK5W.html?page=1&pos=22&cur_pos=22&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
