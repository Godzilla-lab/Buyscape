# Case brown-rapping-paper

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  10741 ms

## What the engine saw
- Presentation: mixed_lot
- Category: packaging_waste (confidence 0.9)
- Made of: paper 70%, plastic 30%
- Estimated weight: 5.0 kg (confidence 0.6)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=packaging_waste brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 4413 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 5714 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 614 ms (replayed)
- total across calls: 10741 ms; wall clock: 645 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 27%
- This is a mixed lot, so it is priced by material and weight rather than identified.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 4 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
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
**293 to 690 NGN** (priced as material, width 0.8071, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 5 kg of paper 70%, plastic 30% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 360 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Brown rapping paper', 'category': None, 'site_category': 'Papers', 'price_ngn': 0, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/brown-rapping-paper/'}`
