# Case toyota-prado-jeep-front-grill-and-tailight

Photos: 2  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0022  |  142860 ms

## What the engine saw
- Presentation: single_unit
- Category: headlight assembly (confidence 0.95)
- Made of: plastic 70%, steel 20%, copper_bare 10%
- Estimated weight: 3.5 kg (confidence 0.8)
- Brand read off the item: Toyota
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: minor scratches on lens surface, some rust on metal mounting brackets, dust and grime on plastic housing, Some minor scratches and dirt on the plastic and chrome surfaces., No major damage or missing parts visible.
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Toyota

## Two readers
- brand_text agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. brand_text agreed by both readers
- **read_evidence** -> ok. category=headlight assembly brand=Toyota model=None label=False lines=1
- **retrieval** -> empty. query='Toyota Toyota Prado Jeep front grill and tailight in working condition available in GRA Ik' hits=[]
- **gate** -> abstain. no candidates and no model text

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 31749 ms
- read_evidence on qwen/qwen3-vl-32b-instruct: 35395 ms
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 36321 ms
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 37226 ms
- extract_claims on qwen/qwen3-vl-32b-instruct: 2169 ms (replayed)
- total across calls: 142860 ms; wall clock: 37247 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 20%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 7 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] Prado Jeep front grill and tailight in working condition
- [unverifiable_remote] Prado Jeep front grill and tailight
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Prado Jeep front grill and tailight
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**1,552 to 5,411 NGN** (priced as material, width 1.1081, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 3.5 kg of plastic 70%, steel 20%, copper_bare 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 4,095 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- Prado Jeep front grill and tailight in working condition -> not proven remotely. Agent will confirm at pickup.
- Prado Jeep front grill and tailight -> not proven remotely. Weigh on the scale and photograph the display.
- Prado Jeep front grill and tailight -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Toyota Prado Jeep front grill and tailight', 'category': None, 'site_category': 'Scrap Car', 'price_ngn': 120000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/toyota-prado-jeep-front-grill-and-tailight/'}`
