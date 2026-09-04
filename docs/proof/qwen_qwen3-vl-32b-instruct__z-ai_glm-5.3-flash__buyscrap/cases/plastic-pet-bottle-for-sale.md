# Case plastic-pet-bottle-for-sale

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0005  |  6485 ms

## What the engine saw
- Presentation: mixed_lot
- Category: recyclable plastic waste (confidence 0.9)
- Made of: pet_bottle 90%, plastic 10%
- Estimated weight: 25.0 kg (confidence 0.6)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **corroborate** -> unavailable. openrouter:mistralai/mistral-small-3.2-24b-instruct failed after retries: HTTP 429: {"error":{"message":"Provider return
- **read_evidence** -> ok. category=recyclable plastic waste brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 22%
- This is a mixed lot, so it is priced by material and weight rather than identified.
- no label, plate or settings screen was legible
- only one reader saw these photos, the second was unavailable
- 6 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Move closer and photograph any label, sticker or plate so the writing is sharp.
   _why: no label was legible in the photos sent so far_

## What the seller is asked (only they know these)
- How much is there? Give kilogrammes or tons.
- Is the metal bare, or still covered in plastic, paint or rubber?
- Is it all one material, or mixed with other things?
- Does a magnet stick to it?

## Claims
- [unverifiable_remote] The items are clean and sorted PET bottles ready for weighing and pickup.
- [unverifiable_remote] Plastic PET bottle for sale in Ikosi, Ketu, Lagos State, Nigeria.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the pile.
- [unverified] Required evidence 'whole_pile' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole quantity, with a person or a car in shot so its size is clear.
- [unverified] Required evidence 'material_closeup' was not supplied
    priced as: priced as if the worst case is true. Close-up of the material itself, close enough to see whether it is bare metal, coated, painted or still in its covering.
- [unverified] Required evidence 'magnet_test' was not supplied
    priced as: priced as if the worst case is true. Hold a fridge magnet against it and photograph it. Say whether the magnet sticks.

## Price
**2,168 to 4,950 NGN** (priced as material, width 0.7815, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of pet_bottle 90%, plastic 10% (rates for pet_bottle, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,950 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- The items are clean and sorted PET bottles ready for weighing and pickup. -> not proven remotely. Agent will confirm at pickup.
- Plastic PET bottle for sale in Ikosi, Ketu, Lagos State, Nigeria. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the pile..
- Required evidence 'whole_pile' was not supplied -> not proven remotely. One photo of the whole quantity, with a person or a car in shot so its size is clear..
- Required evidence 'material_closeup' was not supplied -> not proven remotely. Close-up of the material itself, close enough to see whether it is bare metal, coated, painted or still in its covering..
- Required evidence 'magnet_test' was not supplied -> not proven remotely. Hold a fridge magnet against it and photograph it. Say whether the magnet sticks..

## Answer key (not shown to the engine)
`{'title': 'Plastic PET Bottle for Sale', 'category': None, 'site_category': 'Plastic and Rubbers', 'price_ngn': 0, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/plastic-pet-bottle-for-sale/'}`
