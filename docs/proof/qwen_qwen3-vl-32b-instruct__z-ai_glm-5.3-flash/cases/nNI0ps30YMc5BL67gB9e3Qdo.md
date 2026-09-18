# Case nNI0ps30YMc5BL67gB9e3Qdo

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  12936 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 45.0 kg (confidence 0.7)
- Brand read off the item: BLUE STAR
- Model read off the item: BS-9FS
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: R Series - R410A Rotary Cool Only | SPLIT AIR CONDITIONER | BLUE STAR | BS-9FS

## Two readers
- brand_text agreed by both readers
- item_type agreed by both readers
- model_text was read by one reader and confirmed by OCR
- 1 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- R Series- R410A Rotary Cool Only
- SPLIT AIR CONDITIONER
- BLUE STAR
- BS-9FS
- R Series- R4t0A Rotary Cool y
- VEEBAL
- SPLITAIR CONDITIONER

## Chain
- **ocr** -> ok. 7 lines: R Series- R410A Rotary Cool Only | SPLIT AIR CONDITIONER | BLUE STAR | BS-9FS | R Series- R4t0A Rotary Cool y | VEEBAL |
- **corroborate** -> dispute. brand_text agreed by both readers; item_type agreed by both readers; model_text was read by one reader and confirmed by OCR; 1 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=BLUE STAR model=BS-9FS label=True lines=4
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='BLUE STAR BS-9FS R Series - R410A Rotary Cool Only SPLIT AIR CONDITIONER BLUE STAR BS-9FS ' hits=['Samsung AR09 1HP', 'Hisense AS-09 1HP', 'LG S4-Q09 1HP']
- **identify** -> label. named from the label: BLUE STAR BS-9FS, not in the catalogue
- **abstain** -> pass. confidence=0.45 from the label

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 3871 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6747 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2318 ms (replayed)
- total across calls: 12936 ms; wall clock: 1746 ms

## Identification
Shortlist from the catalogue:
  - Samsung AR09 1HP (0.2333)
  - Hisense AS-09 1HP (0.2)
  - LG S4-Q09 1HP (0.2)

**Answer: BLUE STAR BS-9FS** (named from the item's own label; not in the catalogue)

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**45%: the photos do not say what this is.**

- Identification confidence: 45% (unsure)
- Price confidence: 0%
- named from the item's own label, which the catalogue does not list
- read off the item's own label
- 4 lines seen by both readers
- looks like a catalogue or stock image
- 7 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] The item is a Bluestar 1HP Basic Split AC.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverifiable_remote] The air conditioner is designed to deliver fast cooling.
    priced as: assumed not cooling, compressor unproven. Agent runs the unit and measures amps with a clamp meter
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the unit.
- [unverified] Required evidence 'indoor_unit' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole indoor unit.
- [unverified] Required evidence 'outdoor_unit' was not supplied
    priced as: priced as if the worst case is true. One photo of the outdoor compressor unit.
- [unverified] Required evidence 'rating_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of the rating plate on the outdoor unit showing the model and HP.
- [unverified] Required evidence 'grille_open' was not supplied
    priced as: priced as if the worst case is true. Open the front grille of the indoor unit and photograph the filters and coil.

## Price
**13,156 to 80,000 NGN** (priced as material, width 1.4351, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3289 for unproven claims.

Scrap floor: 40,000 NGN

Conditions attached to this price:
- Evidence flag: looks like a catalogue or stock image
- The item is a Bluestar 1HP Basic Split AC. -> not proven remotely. Agent reads the outdoor rating plate.
- The air conditioner is designed to deliver fast cooling. -> not proven remotely. Agent runs the unit and measures amps with a clamp meter.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Bluestar 1hp Basic Split Air Conditioner | Bs-9fs (Hw09cryfb1-9fs)', 'category': 'split_ac', 'price_ngn': 285000, 'is_used': False, 'url': '/ikeja/home-appliances/bluestar-1hp-basic-split-air-conditioner-bs-9fs-hw09cryfb1-9fs-nNI0ps30YMc5BL67gB9e3Qdo.html?page=1&pos=13&cur_pos=13&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
