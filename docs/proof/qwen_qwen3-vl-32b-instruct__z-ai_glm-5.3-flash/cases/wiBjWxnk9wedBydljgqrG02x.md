# Case wiBjWxnk9wedBydljgqrG02x

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  29959 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.95)
- Made of: plastic 60%, steel 30%, copper_bare 10%
- Estimated weight: 35.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor dust and grime on surface, some scratches on plastic casing
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 5 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> dispute. item_type agreed by both readers; brand_text differed between the two readers, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 5 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=None model=None label=True lines=0
- **retrieval** -> ok. query='The Haier Thermocool Supercool Premium Split Air Conditioner is everything one could want ' hits=['Haier Thermocool HSU-12 1.5HP']
- **identify** -> ok. chosen=Haier Thermocool HSU-12 1.5HP margin=None
- **abstain** -> abstain. top score 0.55

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6635 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8658 ms (replayed)
- identify on z-ai/glm-5.3-flash: 13229 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 1437 ms (replayed)
- total across calls: 29959 ms; wall clock: 1265 ms

## Identification
Shortlist from the catalogue:
  - Haier Thermocool HSU-12 1.5HP (0.38)

**Not identified: CANNOT_IDENTIFY.** The best candidate scored only 0.55, which is not sure enough to price.

## How sure the engine is (back office)
**Not sure enough to price: 26% on the best answer. It is probably a Haier Thermocool HSU-12 1.5HP, and the photos cannot separate them.**

- Identification confidence: 26% (unknown)
- Price confidence: 24%
- It is weighing: Haier Thermocool HSU-12 1.5HP (0.55)
- The best candidate scored only 0.55, which is not sure enough to price.
- read off the item's own label
- the two readers agreed on nothing legible
- 5 claims are still unproven, 0 are supported

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
**32,770 to 55,580 NGN** (priced as material, width 0.5163, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 35 kg of plastic 60%, steel 30%, copper_bare 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 42,350 NGN

Conditions attached to this price:
- Not identified: The best candidate scored only 0.55, which is not sure enough to price.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': '1.5hp Thermocool Split Air Conditioner for Sale', 'category': 'split_ac', 'price_ngn': 238000, 'is_used': True, 'url': '/yaba/home-appliances/1-5hp-thermocool-split-air-conditioner-for-sale-wiBjWxnk9wedBydljgqrG02x.html?page=2&pos=17&cur_pos=17&ads_per_page=19&ads_count=5405&lid=0XmBf5MruhjkTPrH'}`
