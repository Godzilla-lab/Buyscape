# Case 6xt35N67xaVwSgpAPFeJQadk

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  67750 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: plastic 40%, steel 30%, copper 10%, paper 20%
- Estimated weight: 35.0 kg (confidence 0.7)
- Brand read off the item: Hisense
- Model read off the item: AOS-18H620A
- Rating read: 1.5HP
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Hisense | AIR CONDITIONER | Outdoor Units | Hisense | Outdoor Unit | 1.5HP | R32 | Made in China

## Chain
- **corroborate** -> unavailable. openrouter:mistralai/mistral-small-3.2-24b-instruct failed after retries: HTTP 429: {"error":{"message":"Provider return
- **read_evidence** -> ok. category=split air conditioner brand=Hisense model=AOS-18H620A label=True lines=19
- **retrieval** -> ok. query='Hisense AOS-18H620A 1.5HP Hisense AIR CONDITIONER Outdoor Units Hisense Outdoor Unit 1.5HP' hits=['Hisense AS-12 1.5HP', 'Hisense AS-09 1HP', 'Hisense AS-18 2HP', 'Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP']
- **identify** -> ok. chosen=Hisense AOS-18H620A margin=0.8
- **abstain** -> pass. confidence=0.66 margin=0.8

## Identification
Shortlist from the catalogue:
  - Hisense AS-12 1.5HP (0.64)
  - Hisense AS-09 1HP (0.4)
  - Hisense AS-18 2HP (0.38)
  - Samsung AR12 1.5HP (0.3)
  - Scanfrost SFAC12 1.5HP (0.3)

**Answer: Hisense AOS-18H620A Outdoor Unit 1.5HP R32** (margin 0.8)

## How sure the engine is (back office)
**66% sure this is a Hisense AOS-18H620A Outdoor Unit 1.5HP R32.**

- Identification confidence: 66% (likely)
- Price confidence: 0%
- It is weighing: Hisense AOS-18H620A (0.95), Hisense AS-12 1.5HP (0.15)
- read off the item's own label
- only one reader saw these photos, the second was unavailable
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and photograph it next to the unit.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] One photo of the whole indoor unit.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] One photo of the outdoor compressor unit.
   _why: this is needed before the price can be confirmed_

## Claims
- [unverified] The Hisense AS09DK Air Conditioner is designed to deliver powerful and consistent cooling for small spaces.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The Hisense AS09DK Air Conditioner is designed to deliver powerful and consistent cooling for small spaces.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The Hisense AS09DK Air Conditioner is designed to deliver powerful and consistent cooling for small spaces.
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
**19,008 to 80,000 NGN** (priced as material, width 1.2321, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4752 for unproven claims.

Scrap floor: 42,070 NGN

Conditions attached to this price:
- The Hisense AS09DK Air Conditioner is designed to deliver powerful and consistent cooling for small spaces. -> not proven remotely. Agent reads the outdoor rating plate.
- The Hisense AS09DK Air Conditioner is designed to deliver powerful and consistent cooling for small spaces. -> not proven remotely. Agent reads the outdoor rating plate.
- The Hisense AS09DK Air Conditioner is designed to deliver powerful and consistent cooling for small spaces. -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Hisense 1hp Split Air Conditioner – Powerful Cooling Performance', 'category': 'split_ac', 'price_ngn': 355000, 'is_used': False, 'url': '/ajah/home-appliances/hisense-1hp-split-air-conditioner-powerful-cooling-performance-6xt35N67xaVwSgpAPFeJQadk.html?page=1&pos=9&cur_pos=9&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
