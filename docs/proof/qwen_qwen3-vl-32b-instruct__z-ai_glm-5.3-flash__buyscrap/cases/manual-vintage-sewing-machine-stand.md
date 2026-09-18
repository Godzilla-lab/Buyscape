# Case manual-vintage-sewing-machine-stand

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0015  |  77471 ms

## What the engine saw
- Presentation: single_unit
- Category: sewing machine (confidence 0.9)
- Made of: steel 70%, wood 30%
- Estimated weight: 15.0 kg (confidence 0.8)
- Brand read off the item: YANKEE
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: rust on metal parts, chipped paint on frame, dusty and grimy surface, worn pedal mechanism
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: YANKEE

## Two readers
- item_type agreed by both readers
- 1 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> dispute. item_type agreed by both readers; 1 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=sewing machine brand=YANKEE model=None label=False lines=1
- **retrieval** -> ok. query='YANKEE YANKEE A scrap manual vintage sewing machine stand with cast iron legs and treadle ' hits=['Infinix Note 30', 'Tecno Camon 30', 'Tecno Spark 30', 'Infinix Hot 30', 'Infinix Note 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused
- **condition** -> not working. by the seller's own account

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 19981 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 19840 ms (replayed)
- identify on z-ai/glm-5.3-flash: 28437 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 9213 ms (replayed)
- total across calls: 77471 ms; wall clock: 1493 ms

## Identification
Shortlist from the catalogue:
  - Infinix Note 30 (0.4)
  - Tecno Camon 30 (0.2)
  - Tecno Spark 30 (0.2)
  - Infinix Hot 30 (0.2)
  - Infinix Note 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** Item is a vintage treadle sewing machine stand; shortlist contains only phones, and no model name is legible beyond 'YANKEE'.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 16%
- Item is a vintage treadle sewing machine stand; shortlist contains only phones, and no model name is legible beyond 'YANKEE'.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the brand was read by only one reader and is not confirmed
- 9 claims are still unproven, 0 are supported

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
- [unverifiable_remote] A scrap manual vintage sewing machine stand with cast iron legs and treadle mechanism is available for sale.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The stand has cast iron legs.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The stand includes a treadle mechanism.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Quantity: Two (2) stands are available.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The item is being sold as is, for parts, repair or recycling.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**1,602 to 6,570 NGN** (priced as material, width 1.2159, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of steel 70%, wood 30% (rates for wood are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 5,340 NGN

Conditions attached to this price:
- Not identified: Item is a vintage treadle sewing machine stand; shortlist contains only phones, and no model name is legible beyond 'YANKEE'.
- A scrap manual vintage sewing machine stand with cast iron legs and treadle mechanism is available for sale. -> not proven remotely. Weigh on the scale and photograph the display.
- The stand has cast iron legs. -> not proven remotely. Weigh on the scale and photograph the display.
- The stand includes a treadle mechanism. -> not proven remotely. Weigh on the scale and photograph the display.
- Quantity: Two (2) stands are available. -> not proven remotely. Weigh on the scale and photograph the display.
- The item is being sold as is, for parts, repair or recycling. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Manual vintage sewing machine stand', 'category': None, 'site_category': 'Industrial Machines', 'price_ngn': 30000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/manual-vintage-sewing-machine-stand/'}`
