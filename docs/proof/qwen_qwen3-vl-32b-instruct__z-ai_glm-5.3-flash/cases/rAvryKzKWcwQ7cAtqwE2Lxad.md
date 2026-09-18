# Case rAvryKzKWcwQ7cAtqwE2Lxad

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  25384 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, copper 10%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: MAXMECH
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dirt and mud on surface, some scratches on plastic casing, wet ground around unit, fuel cap appears loose
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MAXMECH

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 10 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- MMAXMECH
- C-
- MAXMECH

## Chain
- **ocr** -> ok. 3 lines: MMAXMECH | C- | MAXMECH
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 10 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=MAXMECH model=None label=True lines=1
- **retrieval** -> ok. query='MAXMECH MAXMECH Product Overview

The MAXMECH WGC-380Ei Welding Generator is a heavy-duty ' hits=['Maxmech MX3500 3.5kVA', 'Maxmech MX10000 10kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA']
- **identify** -> ok. chosen=Maxmech WGC-380Ei margin=0.75
- **abstain** -> pass. confidence=0.85 margin=0.75

## Identification
Shortlist from the catalogue:
  - Maxmech MX3500 3.5kVA (0.5)
  - Maxmech MX10000 10kVA (0.4333)
  - Thermocool TC2700 2.5kVA (0.1833)
  - Haier Thermocool HTG2700 2.5kVA (0.1833)

**Answer: Maxmech WGC-380Ei** (margin 0.75)

## How sure the engine is (back office)
**85% sure this is a Maxmech WGC-380Ei.**

- Identification confidence: 85% (certain)
- Price confidence: 0%
- It is weighing: Maxmech WGC-380Ei (0.85), Maxmech MX3500 (0.1), Maxmech MX10000 (0.1)
- read off the item's own label
- 1 lines seen by both readers
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and photograph it next to the generator.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] One photo of the whole generator from the front.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: this is needed before the price can be confirmed_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it start and run right now?
- When was it last serviced, and what was done?

## Claims
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
- [unverifiable_remote] The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine
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
**20,954 to 42,850 NGN** (priced as material, width 0.6863, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.6302 for unproven claims.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- The MAXMECH WGC-380Ei Welding Generator is a heavy-duty 2-in-1 machine -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Maxmech Wgc-380ei 300a / 2.5kva Welding Generator', 'category': 'generator', 'price_ngn': 800000, 'is_used': False, 'url': '/lagos-island-west/power-equipments/maxmech-wgc-380ei-300a-2-5kva-welding-generator-rAvryKzKWcwQ7cAtqwE2Lxad.html?page=2&pos=1&cur_pos=1&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
