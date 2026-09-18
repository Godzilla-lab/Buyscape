# Case 8mX7oiByQuax0x6ADXYvZxLN

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0006  |  18726 ms

## What the engine saw
- Presentation: single_unit
- Category: ultrasonic cleaner (confidence 0.9)
- Made of: plastic 70%, steel 20%, rubber 10%
- Estimated weight: 8.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: Dust and minor scuffs on surface, Plastic cover partially peeled back
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Bubble Clean | BRIGHT ENTERPRISE

## Two readers
- brand_text differed between the two readers, so it is treated as unread
- 6 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- HEFRIGEI
- OR
- Ffrigerador
- Wchrank/
- ifero
- Bubble
- Clean
- BRIGHT ENTERPRISE

## Chain
- **ocr** -> ok. 8 lines: HEFRIGEI | OR | Ffrigerador | Wchrank/ | ifero | Bubble | Clean | BRIGHT ENTERPRISE
- **corroborate** -> dispute. brand_text differed between the two readers, so it is treated as unread; 6 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=ultrasonic cleaner brand=None model=None label=True lines=2
- **retrieval** -> empty. query='Bubble Clean BRIGHT ENTERPRISE ￼

₦0

ACs

|

Appliances

|

Fashion

|

Furniture

Home &' hits=[]
- **gate** -> abstain. no candidates and no model text

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 27%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- read off the item's own label
- 2 lines seen by both readers
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
**1,140 to 2,048 NGN** (priced as material, width 0.5694, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 8 kg of plastic 70%, steel 20%, rubber 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 1,400 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Hisense 9kg Top Loader Automatic Washing Machine | Wt3k9022u', 'category': 'washing_machine', 'price_ngn': 350000, 'is_used': False, 'url': '/ojo/home-appliances/hisense-9kg-top-loader-automatic-washing-machine-wt3k9022u-8mX7oiByQuax0x6ADXYvZxLN.html?page=1&pos=5&cur_pos=5&ads_per_page=20&ads_count=16335&lid=_UmGsiyCR3i1GHB4'}`
