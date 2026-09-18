# Case 1-ton-scrap-titanium-nets-required-in-nigeria-and-china

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0014  |  43167 ms

## What the engine saw
- Presentation: mixed_lot
- Category: metal mesh scrap (confidence 0.9)
- Made of: steel 80%, plastic 20%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: tangled and crumpled, some rust visible on metal mesh
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type was read by only one reader, so it is kept but not confirmed

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=metal mesh scrap brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped
- **weight** -> stated. 1000 kg from the seller's words

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 14080 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 20172 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 8915 ms (replayed)
- total across calls: 43167 ms; wall clock: 1516 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- This is a mixed lot, so it is priced by material and weight rather than identified.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the item_type was read by only one reader and is not confirmed
- 13 claims are still unproven, 0 are supported

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
- [unverifiable_remote] The buyer is seeking approximately 1 ton (1000 kg) of scrap titanium nets.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The buyer is interested in various forms of scrap titanium netting, including industrial titanium mesh/screening used in filtration, chemical processing, or aerospace applications.
- [unverifiable_remote] Damaged or offcut titanium nets are acceptable, regardless of size or shape, as long as they are primarily titanium.
- [unverifiable_remote] Titanium alloy nets are also acceptable.
- [unverifiable_remote] Suppliers must be able to provide documentation regarding the material’s origin and composition, if possible.
- [unverifiable_remote] The buyer is seeking suppliers located in Nigeria and China.
- [unverifiable_remote] Shipping arrangements from other locations are open for discussion.
- [unverifiable_remote] Pricing will be negotiated based on the material’s purity, quantity, and condition.
    priced as: assumed mixed, and priced at the cheapest material present. Agent sorts a sample and weighs the contamination
- [unverifiable_remote] Interested suppliers should provide detailed information about available scrap titanium nets, including quantity, material composition, condition, location, photographs (if available), and quoted price.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the pile.
- [unverified] Required evidence 'whole_pile' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole quantity, with a person or a car in shot so its size is clear.
- [unverified] Required evidence 'material_closeup' was not supplied
    priced as: priced as if the worst case is true. Close-up of the material itself, close enough to see whether it is bare metal, coated, painted or still in its covering.
- [unverified] Required evidence 'magnet_test' was not supplied
    priced as: priced as if the worst case is true. Hold a fridge magnet against it and photograph it. Say whether the magnet sticks.

## Price
**126,000 to 516,000 NGN** (priced as material, width 1.215, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 1000 kg of steel 80%, plastic 20% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 420,000 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- The buyer is seeking approximately 1 ton (1000 kg) of scrap titanium nets. -> not proven remotely. Weigh on the scale and photograph the display.
- The buyer is interested in various forms of scrap titanium netting, including industrial titanium mesh/screening used in filtration, chemical processing, or aerospace applications. -> not proven remotely. Agent will confirm at pickup.
- Damaged or offcut titanium nets are acceptable, regardless of size or shape, as long as they are primarily titanium. -> not proven remotely. Agent will confirm at pickup.
- Titanium alloy nets are also acceptable. -> not proven remotely. Agent will confirm at pickup.
- Suppliers must be able to provide documentation regarding the material’s origin and composition, if possible. -> not proven remotely. Agent will confirm at pickup.
- The buyer is seeking suppliers located in Nigeria and China. -> not proven remotely. Agent will confirm at pickup.
- Shipping arrangements from other locations are open for discussion. -> not proven remotely. Agent will confirm at pickup.
- Pricing will be negotiated based on the material’s purity, quantity, and condition. -> not proven remotely. Agent sorts a sample and weighs the contamination.
- Interested suppliers should provide detailed information about available scrap titanium nets, including quantity, material composition, condition, location, photographs (if available), and quoted price. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the pile..
- Required evidence 'whole_pile' was not supplied -> not proven remotely. One photo of the whole quantity, with a person or a car in shot so its size is clear..
- Required evidence 'material_closeup' was not supplied -> not proven remotely. Close-up of the material itself, close enough to see whether it is bare metal, coated, painted or still in its covering..
- Required evidence 'magnet_test' was not supplied -> not proven remotely. Hold a fridge magnet against it and photograph it. Say whether the magnet sticks..

## Answer key (not shown to the engine)
`{'title': '1 Ton of Scrap Titanium Nets Required in Nigeria and China', 'category': None, 'site_category': 'Iron', 'price_ngn': 1000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/1-ton-scrap-titanium-nets-required-in-nigeria-and-china/'}`
