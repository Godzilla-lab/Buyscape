# Case yVRnXVi3VkjOnDkyfUEPpKUd

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  18136 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: paper 90%, plastic 10%
- Estimated weight: 30.0 kg (confidence 0.7)
- Brand read off the item: Hisense
- Model read off the item: HSC-12H
- Rating read: 12000 BTU/h
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Hisense | AIR CONDITIONER | Inverter 12000 | 2 YEARS WARRANTY | Energy Efficiency Rating: 5 Stars | Split Air Conditioner | Model: HSC-12H | Serial No: 123456789

## Chain
- **corroborate** -> unavailable. openrouter:mistralai/mistral-small-3.2-24b-instruct failed after retries: HTTP 429: {"error":{"message":"Provider return
- **read_evidence** -> ok. category=split air conditioner brand=Hisense model=HSC-12H label=True lines=15
- **retrieval** -> ok. query='Hisense HSC-12H 12000 BTU/h Hisense AIR CONDITIONER Inverter 12000 2 YEARS WARRANTY Energy' hits=['Hisense AS-12 1.5HP', 'Hisense AS-09 1HP', 'Hisense AS-18 2HP', 'Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP']
- **identify** -> ok. chosen=Hisense HSC-12H margin=0.6
- **abstain** -> pass. confidence=0.63 margin=0.6

## Identification
Shortlist from the catalogue:
  - Hisense AS-12 1.5HP (0.51)
  - Hisense AS-09 1HP (0.4)
  - Hisense AS-18 2HP (0.38)
  - Samsung AR12 1.5HP (0.15)
  - Scanfrost SFAC12 1.5HP (0.15)

**Answer: Hisense HSC-12H Inverter 12000 BTU/h Split Air Conditioner** (margin 0.6)

## How sure the engine is (back office)
**Not sure enough to price: 63% on the best answer. It is probably a Hisense HSC-12H or a Hisense AS-12, and the photos cannot separate them.**

- Identification confidence: 63% (unsure)
- Price confidence: 0%
- It is weighing: Hisense HSC-12H (0.9), Hisense AS-12 (0.3)
- read off the item's own label
- only one reader saw these photos, the second was unavailable
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and photograph it next to the unit.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] One photo of the whole indoor unit.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] One photo of the outdoor compressor unit.
   _why: this is needed before the price can be confirmed_

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
**16,156 to 80,000 NGN** (priced as material, width 1.3279, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4039 for unproven claims.

Scrap floor: 40,000 NGN

Conditions attached to this price:
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
