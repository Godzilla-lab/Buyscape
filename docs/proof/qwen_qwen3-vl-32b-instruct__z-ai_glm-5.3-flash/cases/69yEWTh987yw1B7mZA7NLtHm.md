# Case 69yEWTh987yw1B7mZA7NLtHm

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0006  |  19735 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: MAXX
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: INVERTER AIR CONDITIONER | MAXX INVERTER | STEVEN RB | INVERTER AIR CONDITIONER | MAXX INVERTER

## Two readers
- model_text was seen by only one reader, so it is treated as unread
- 4 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- AIR CONDITIONER
- INVERTER
- STEVEN RB
- LIXYA
- ZOUTDOORT
- MAXISPLISIN

## Chain
- **ocr** -> ok. 6 lines: AIR CONDITIONER | INVERTER | STEVEN RB | LIXYA | ZOUTDOORT | MAXISPLISIN
- **corroborate** -> dispute. model_text was seen by only one reader, so it is treated as unread; 4 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=split air conditioner brand=MAXX model=None label=False lines=5
- **forensics** -> flag. looks like a catalogue or stock image
- **gate** -> abstain. multiple items in frame

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 22%
- The photos show more than one item, so no single item can be identified.
- no label, plate or settings screen was legible
- 5 lines seen by both readers
- the brand was read by only one reader and is not confirmed
- looks like a catalogue or stock image
- 6 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
3. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] The air conditioner is a maxi 1.5hp inverter split model.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
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
**986 to 3,000 NGN** (priced as material, width 1.0101, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of carton 100% (rates for carton are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 1,500 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Evidence flag: looks like a catalogue or stock image
- The air conditioner is a maxi 1.5hp inverter split model. -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Maxi 1.5hp Inverter Split Air Conditioner', 'category': 'split_ac', 'price_ngn': 360000, 'is_used': False, 'url': '/ikeja/home-appliances/maxi-1-5hp-inverter-split-air-conditioner-69yEWTh987yw1B7mZA7NLtHm.html?page=1&pos=11&cur_pos=11&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
