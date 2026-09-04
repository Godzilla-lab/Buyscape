# Case white-shoe

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  23788 ms

## What the engine saw
- Presentation: single_unit
- Category: sneakers (confidence 0.95)
- Made of: textile 40%, plastic 30%, rubber 30%
- Estimated weight: 1.2 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- brand_text agreed by both readers
- 4 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; 4 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=sneakers brand=Nike model=None label=False lines=0
- **grounding** -> dropped. brand
- **forensics** -> flag. the reader stated brand it could not point to in the photos
- **retrieval** -> empty. query='Imported shoe available at a discount price.' hits=[]
- **gate** -> abstain. no candidates and no model text

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

Evidence flags: the reader stated brand it could not point to in the photos

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 24%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the reader stated brand it could not point to in the photos
- 5 claims are still unproven, 0 are supported

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
- [unverifiable_remote] Imported shoe available at a discount price.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**52 to 139 NGN** (priced as material, width 0.898, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 1.2 kg of textile 40%, plastic 30%, rubber 30% (rates for plastic, rubber, textile are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 68 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- Evidence flag: the reader stated brand it could not point to in the photos
- Imported shoe available at a discount price. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'White shoe', 'category': None, 'site_category': 'Premium', 'price_ngn': 50000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/white-shoe/'}`
