# Case brand-new-sneakers

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  19465 ms

## What the engine saw
- Presentation: single_unit
- Category: sneakers (confidence 0.95)
- Made of: plastic 40%, textile 30%, rubber 20%, steel 10%
- Estimated weight: 1.2 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: no visible damage, shoes appear clean and unused
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- brand_text differed between the two readers, so it is treated as unread
- 2 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> dispute. brand_text differed between the two readers, so it is treated as unread; 2 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=sneakers brand=None model=None label=True lines=0
- **retrieval** -> ok. query='Brand new sneakers are available for sale. Location: Agege, Lagos State. Price: 40,000 nai' hits=['Tecno Camon 40', 'Tecno Spark 40', 'Infinix Hot 40', 'Infinix Note 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5024 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8130 ms (replayed)
- identify on z-ai/glm-5.3-flash: 5583 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 728 ms (replayed)
- total across calls: 19465 ms; wall clock: 160 ms

## Identification
Shortlist from the catalogue:
  - Tecno Camon 40 (0.2)
  - Tecno Spark 40 (0.2)
  - Infinix Hot 40 (0.2)
  - Infinix Note 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** The photos show a pair of sneakers, not any mobile phone; no shortlist entry can apply.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 27%
- The photos show a pair of sneakers, not any mobile phone; no shortlist entry can apply.
- read off the item's own label
- the two readers agreed on nothing legible
- 4 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**106 to 211 NGN** (priced as material, width 0.6588, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 1.2 kg of plastic 40%, textile 30%, rubber 20%, steel 10% (rates for plastic, rubber, textile are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 130 NGN

Conditions attached to this price:
- Not identified: The photos show a pair of sneakers, not any mobile phone; no shortlist entry can apply.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Brand new sneakers', 'category': None, 'site_category': 'Premium', 'price_ngn': 40000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/brand-new-sneakers/'}`
