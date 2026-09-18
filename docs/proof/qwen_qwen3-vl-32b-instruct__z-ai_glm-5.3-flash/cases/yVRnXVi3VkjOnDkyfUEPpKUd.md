# Case yVRnXVi3VkjOnDkyfUEPpKUd

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  40981 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: carton 95%, plastic 5%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: Hisense
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Hisense | AIR CONDITIONER | Inverter 12000 BTU | 2 YEAR WARRANTY | Split Air Conditioner | 12000 BTU | R32 Refrigerant | Model: HSC-12000I

## Two readers
- brand_text agreed by both readers
- rating_text differed between the two readers, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 6 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- Energy
- OLG
- Hieer
- XE
- 2
- AIR CONDITIONER
- Indonr Waite

## Chain
- **ocr** -> ok. 7 lines: Energy | OLG | Hieer | XE | 2 | AIR CONDITIONER | Indonr Waite
- **corroborate** -> dispute. brand_text agreed by both readers; rating_text differed between the two readers, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 6 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=Hisense model=None label=True lines=18
- **retrieval** -> ok. query='Hisense Hisense AIR CONDITIONER Inverter 12000 BTU 2 YEAR WARRANTY Split Air Conditioner 1' hits=['Hisense AS-12 1.5HP', 'Hisense AS-09 1HP', 'Hisense AS-18 2HP', 'Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP']
- **identify** -> ok. chosen=Hisense HSC-12000I margin=0.6
- **abstain** -> abstain. seller names another generation

## Identification
Shortlist from the catalogue:
  - Hisense AS-12 1.5HP (0.51)
  - Hisense AS-09 1HP (0.4)
  - Hisense AS-18 2HP (0.38)
  - Samsung AR12 1.5HP (0.15)
  - Scanfrost SFAC12 1.5HP (0.15)

**Not identified: EVIDENCE_INCOMPLETE.** The answer rests on hsc12000i, which the OCR engine did not read off the item and the seller did not say. Two readers transcribing the same code is not enough on its own. This needs a sharp photo of the label.

## How sure the engine is (back office)
**Not sure enough to price: 54% on the best answer. It is probably a Hisense HSC-12000I or a Hisense AS-12 1.5HP, and the photos cannot separate them.**

- Identification confidence: 54% (unsure)
- Price confidence: 16%
- It is weighing: Hisense HSC-12000I (0.9), Hisense AS-12 1.5HP (0.3)
- The answer rests on hsc12000i, which the OCR engine did not read off the item and the seller did not say. Two readers transcribing the same code is not enough on its own. This needs a sharp photo of the label.
- read off the item's own label
- 18 lines seen by both readers
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverifiable_remote] The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice
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
**626 to 3,075 NGN** (priced as material, width 1.3234, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of carton 95%, plastic 5% (rates for carton, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 1,550 NGN

Conditions attached to this price:
- Not identified: The answer rests on hsc12000i, which the OCR engine did not read off the item and the seller did not say. Two readers transcribing the same code is not enough on its own. This needs a sharp photo of the label.
- The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice -> not proven remotely. Agent reads the outdoor rating plate.
- The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice -> not proven remotely. Agent reads the outdoor rating plate.
- The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice -> not proven remotely. Agent reads the outdoor rating plate.
- The Hisense 1.5 HP Inverter AC is an excellent, energy-saving choice -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Hisense Inverter Ac 1.5hp – Fast Cooling Split Air Conditioner', 'category': 'split_ac', 'price_ngn': 374000, 'is_used': False, 'url': '/gbagada/home-appliances/hisense-inverter-ac-1-5hp-fast-cooling-split-air-conditioner-yVRnXVi3VkjOnDkyfUEPpKUd.html?page=1&pos=7&cur_pos=7&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
