# Case xni20V5boOkoC3uXGrOYp6Ma

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0013  |  29457 ms

## What the engine saw
- Presentation: sealed_new
- Category: refrigerator (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 15.0 kg (confidence 0.6)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: DO NOT CRUSH

## Two readers
- 107 transcribed lines was seen by only one reader, so it is treated as unread
- item_type was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- REFRSGERATOR
- DO NOT CRUSH
- PRIGHT
- TRADEZONEPLUS

## Chain
- **ocr** -> ok. 4 lines: REFRSGERATOR | DO NOT CRUSH | PRIGHT | TRADEZONEPLUS
- **corroborate** -> dispute. 107 transcribed lines was seen by only one reader, so it is treated as unread; item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=refrigerator brand=None model=None label=False lines=1
- **forensics** -> flag. looks like a catalogue or stock image
- **gate** -> abstain. multiple items in frame

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 18572 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6379 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 4506 ms (replayed)
- total across calls: 29457 ms; wall clock: 2355 ms

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 18%
- The photos show more than one item, so no single item can be identified.
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- the item_type was read by only one reader and is not confirmed
- looks like a catalogue or stock image
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
3. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] The item is a Hisense AS12HB Air Conditioner.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The brand of the air conditioner is Hisense.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The item is designed to provide efficient cooling.
    priced as: assumed not working. Agent powers the item on before payment
- [unverifiable_remote] The item is intended to keep users cool and comfortable.
    priced as: assumed not working. Agent powers the item on before payment
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**270 to 1,800 NGN** (priced as material, width 1.4783, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of carton 100% (rates for carton are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 900 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Evidence flag: looks like a catalogue or stock image
- The item is a Hisense AS12HB Air Conditioner. -> not proven remotely. Weigh on the scale and photograph the display.
- The brand of the air conditioner is Hisense. -> not proven remotely. Weigh on the scale and photograph the display.
- The item is designed to provide efficient cooling. -> not proven remotely. Agent powers the item on before payment.
- The item is intended to keep users cool and comfortable. -> not proven remotely. Agent powers the item on before payment.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Hisense 1.5HP Split Air Conditioner – Powerful Cooling', 'category': 'split_ac', 'price_ngn': 315000, 'is_used': False, 'url': '/alimosho/home-appliances/hisense-1-5hp-split-air-conditioner-powerful-cooling-xni20V5boOkoC3uXGrOYp6Ma.html?page=1&pos=5&cur_pos=5&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
