# Case 10-ton-scrap-plastic-circuit-boards-needed

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  45223 ms

## What the engine saw
- Presentation: mixed_lot
- Category: electronic waste (confidence 1.0)
- Made of: circuit_board 80%, plastic 15%, copper_bare 5%
- Estimated weight: 50.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: broken components, chipped edges, exposed traces
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type agreed by both readers
- **read_evidence** -> ok. category=electronic waste brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped
- **weight** -> stated. 10000 kg from the seller's words

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 19789 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 25434 ms (replayed)
- total across calls: 45223 ms; wall clock: 1781 ms

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
2. [PHOTO] Move closer and photograph any label, sticker or plate so the writing is sharp.
   _why: no label was legible in the photos sent so far_

## What the seller is asked (only they know these)
- How much is there? Give kilogrammes or tons.
- Is the metal bare, or still covered in plastic, paint or rubber?
- Is it all one material, or mixed with other things?
- Does a magnet stick to it?

## Claims
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the pile.
- [unverified] Required evidence 'whole_pile' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole quantity, with a person or a car in shot so its size is clear.
- [unverified] Required evidence 'material_closeup' was not supplied
    priced as: priced as if the worst case is true. Close-up of the material itself, close enough to see whether it is bare metal, coated, painted or still in its covering.
- [unverified] Required evidence 'magnet_test' was not supplied
    priced as: priced as if the worst case is true. Hold a fridge magnet against it and photograph it. Say whether the magnet sticks.

## Price
**9,407,475 to 14,770,000 NGN** (priced as material, width 0.4436, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 10000 kg of circuit_board 80%, plastic 15%, copper_bare 5% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 11,550,000 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the pile..
- Required evidence 'whole_pile' was not supplied -> not proven remotely. One photo of the whole quantity, with a person or a car in shot so its size is clear..
- Required evidence 'material_closeup' was not supplied -> not proven remotely. Close-up of the material itself, close enough to see whether it is bare metal, coated, painted or still in its covering..
- Required evidence 'magnet_test' was not supplied -> not proven remotely. Hold a fridge magnet against it and photograph it. Say whether the magnet sticks..

## Answer key (not shown to the engine)
`{'title': '10 Ton Scrap Plastic Circuit Boards Needed', 'category': None, 'site_category': 'E-waste', 'price_ngn': 10000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/10-ton-scrap-plastic-circuit-boards-needed/'}`
