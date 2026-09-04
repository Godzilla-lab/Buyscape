# Case plastic-paint-rubbers-5l-21-pieces

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  22856 ms

## What the engine saw
- Presentation: mixed_lot
- Category: paint_buckets (confidence 0.95)
- Made of: plastic 90%, paint 10%
- Estimated weight: 50.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: paint splatters on buckets, dusty and dirty surfaces, some lids missing or damaged
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: FINECOAT P.O.P EMULSION PAINT

## Two readers
- brand_text was seen by only one reader, so it is treated as unread
- model_text was seen by only one reader, so it is treated as unread
- 2 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text was seen by only one reader, so it is treated as unread; model_text was seen by only one reader, so it is treated as unread; 2 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=paint_buckets brand=None model=None label=True lines=1
- **gate** -> lot. priced by material, identification skipped

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- This is a mixed lot, so it is priced by material and weight rather than identified.
- read off the item's own label
- 1 lines seen by both readers
- 11 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] Quantity: 21 pieces
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Paint rubber size: 5 Litres (L)
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Condition: Slightly Used
- [unverifiable_remote] These plastic paint rubbers can be washed and reused in homes and offices for storing water.
- [unverifiable_remote] The items are sold “as is”. Please inspect the items upon pickup.
- [unverifiable_remote] All sales are final and no returns accepted.
- [unverifiable_remote] Buyer is responsible for picking up the items at Ikeja as delivery is not included in the price.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**1,621 to 10,100 NGN** (priced as material, width 1.4467, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 50 kg of plastic 90%, paint 10% (rates for paint, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 5,250 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Quantity: 21 pieces -> not proven remotely. Weigh on the scale and photograph the display.
- Paint rubber size: 5 Litres (L) -> not proven remotely. Weigh on the scale and photograph the display.
- Condition: Slightly Used -> not proven remotely. Agent will confirm at pickup.
- These plastic paint rubbers can be washed and reused in homes and offices for storing water. -> not proven remotely. Agent will confirm at pickup.
- The items are sold “as is”. Please inspect the items upon pickup. -> not proven remotely. Agent will confirm at pickup.
- All sales are final and no returns accepted. -> not proven remotely. Agent will confirm at pickup.
- Buyer is responsible for picking up the items at Ikeja as delivery is not included in the price. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'PLASTIC PAINT RUBBERS (5L) 21 PIECES', 'category': None, 'site_category': 'Plastic and Rubbers', 'price_ngn': 250, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/plastic-paint-rubbers-5l-21-pieces/'}`
