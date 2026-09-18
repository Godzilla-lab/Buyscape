# Case nexus-washing-machine

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  31003 ms

## What the engine saw
- Presentation: single_unit
- Category: washing machine (confidence 0.9)
- Made of: plastic 80%, steel 20%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: NEXUS
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: dirt and grime on surface, yellowing of plastic, clothes draped over top
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: NEXUS

## Two readers
- brand_text agreed by both readers

## OCR read off the photos
- NEXUS

## Chain
- **ocr** -> ok. 1 lines: NEXUS
- **corroborate** -> agree. brand_text agreed by both readers
- **read_evidence** -> ok. category=washing machine brand=NEXUS model=None label=True lines=1
- **retrieval** -> ok. query='NEXUS NEXUS Washing machine available at Abulegba' hits=['Nexus NX-WM8 8kg twin tub', 'Nexus NX-C12 1.5HP']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Nexus NX-WM8 8kg twin tub (0.4)
  - Nexus NX-C12 1.5HP (0.38)

**Not identified: CANNOT_IDENTIFY.** Only 'NEXUS' is legible; no model or capacity marking visible, and the unit looks like a single tub washer while the only shortlist washer is a twin tub, so the match is unverified.

## How sure the engine is (back office)
**Not sure enough to price: 21% on the best answer. It is probably a Nexus NX-WM8, and the photos cannot separate them.**

- Identification confidence: 21% (unknown)
- Price confidence: 24%
- It is weighing: Nexus NX-WM8 (0.35)
- Only 'NEXUS' is legible; no model or capacity marking visible, and the unit looks like a single tub washer while the only shortlist washer is a twin tub, so the match is unverified.
- read off the item's own label
- 1 lines seen by both readers
- 5 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of the sticker with the model number, usually inside the door or on the back.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it finish a full wash and spin cycle?

## Claims
- [unverifiable_remote] Washing machine available at Abulegba
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the machine.
- [unverified] Required evidence 'overall_front' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole machine from the front with the door closed.
- [unverified] Required evidence 'rating_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of the sticker with the model number, usually inside the door or on the back.
- [unverified] Required evidence 'drum' was not supplied
    priced as: priced as if the worst case is true. Open the door and photograph the inside of the drum.

## Price
**2,089 to 3,960 NGN** (priced as material, width 0.6185, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of plastic 80%, steel 20% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,700 NGN

Conditions attached to this price:
- Not identified: Only 'NEXUS' is legible; no model or capacity marking visible, and the unit looks like a single tub washer while the only shortlist washer is a twin tub, so the match is unverified.
- Washing machine available at Abulegba -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the machine..
- Required evidence 'overall_front' was not supplied -> not proven remotely. One photo of the whole machine from the front with the door closed..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the sticker with the model number, usually inside the door or on the back..
- Required evidence 'drum' was not supplied -> not proven remotely. Open the door and photograph the inside of the drum..

## Answer key (not shown to the engine)
`{'title': 'Nexus Washing Machine', 'category': None, 'site_category': 'E-waste', 'price_ngn': 60000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/nexus-washing-machine/'}`
