# Case u3zIvWmvk6hYeB72X2VJugas

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0013  |  41067 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: plastic 60%, steel 30%, copper 10%
- Estimated weight: 12.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: 3000W MAX / 2000W CONTINUOUS
- Label, plate or settings screen legible: yes
- Damage noted: minor scuffs on plastic casing, no visible dents or cracks, handles appear intact
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 2000W | OUTPUT: 3000W MAX / 2000W CONTINUOUS | FUEL TYPE: GASOLINE OR PROPANE | ENGINE: 4-STROKE, AIR-COOLED

## Two readers
- rating_text agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 15 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- VULTIPLE
- 1

## Chain
- **ocr** -> ok. 2 lines: VULTIPLE | 1
- **corroborate** -> dispute. rating_text agreed by both readers; brand_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 15 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=None label=True lines=4
- **retrieval** -> ok. query='3000W MAX / 2000W CONTINUOUS 2000W OUTPUT: 3000W MAX / 2000W CONTINUOUS FUEL TYPE: GASOLIN' hits=['Lutian LT3900 3.5kVA', 'Senwei SW3500 3.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Kemage KM6500 5.5kVA']
- **identify** -> refused. chosen=Bison None margin=0.0
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 9028 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 11539 ms (replayed)
- identify on z-ai/glm-5.3-flash: 18697 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 1803 ms (replayed)
- total across calls: 41067 ms; wall clock: 455 ms

## Identification
Shortlist from the catalogue:
  - Lutian LT3900 3.5kVA (0.3)
  - Senwei SW3500 3.5kVA (0.3)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Body shows BISON branding, but no model number is legible; all shortlist entries are different brands and their power ratings contradict the 3000W max / 2000W continuous label. Seller's 3.5kVA claim conflicts with the plate.

## How sure the engine is (back office)
**Not sure enough to price: 3% on the best answer. It is probably a Lutian LT3900 3.5kVA or a Senwei SW3500 3.5kVA, and the photos cannot separate them.**

- Identification confidence: 3% (unknown)
- Price confidence: 20%
- It is weighing: Lutian LT3900 3.5kVA (0.05), Senwei SW3500 3.5kVA (0.05)
- Body shows BISON branding, but no model number is legible; all shortlist entries are different brands and their power ratings contradict the 3000W max / 2000W continuous label. Seller's 3.5kVA claim conflicts with the plate.
- read off the item's own label
- 4 lines seen by both readers
- the next candidate was only 0.0 behind
- 7 claims are still unproven, 0 are supported

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
- [unverified] This is a bison 3.5KVA inverter generator.
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] The generator is suitable for home use.
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
**9,072 to 19,056 NGN** (priced as material, width 0.7099, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of plastic 60%, steel 30%, copper 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 14,520 NGN

Conditions attached to this price:
- Not identified: Body shows BISON branding, but no model number is legible; all shortlist entries are different brands and their power ratings contradict the 3000W max / 2000W continuous label. Seller's 3.5kVA claim conflicts with the plate.
- This is a bison 3.5KVA inverter generator. -> not proven remotely. Agent reads the rating plate.
- The generator is suitable for home use. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Bison 3.5kva Inverter Generator – Silent Fuel Efficient', 'category': 'generator', 'price_ngn': 385000, 'is_used': False, 'url': '/lekki/power-equipments/bison-3-5kva-inverter-generator-silent-fuel-efficient-u3zIvWmvk6hYeB72X2VJugas.html?page=2&pos=11&cur_pos=11&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
