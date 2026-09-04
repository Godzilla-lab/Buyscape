# Case used-office-chair

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  18296 ms

## What the engine saw
- Presentation: single_unit
- Category: office chair (confidence 0.95)
- Made of: plastic 40%, steel 30%, textile 20%, rubber 10%
- Estimated weight: 10.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: armrests show signs of wear and slight discoloration, mesh back has minor dust and some loose threads, base and casters appear functional but slightly dusty
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=office chair brand=None model=None label=False lines=0
- **gate** -> abstain. multiple items in frame

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 27%
- The photos show more than one item, so no single item can be identified.
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
**1,637 to 2,780 NGN** (priced as material, width 0.5175, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 10 kg of plastic 40%, steel 30%, textile 20%, rubber 10% (rates for plastic, rubber, textile are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,010 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Used office chair', 'category': None, 'site_category': 'Office Chair', 'price_ngn': 10000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/used-office-chair/'}`
