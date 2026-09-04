# Case 10-ton-scrap-plastic-circuit-boards-needed

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0013  |  75530 ms

## What the engine saw
- Presentation: mixed_lot
- Category: electronic waste (confidence 1.0)
- Made of: circuit_board 80%, plastic 15%, copper 5%
- Estimated weight: 50.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=electronic waste brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped
- **weight** -> stated. 10000 kg from the seller's words

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
- 13 claims are still unproven, 0 are supported

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
- [unverifiable_remote] The company is seeking to purchase 10 ton (10,000 kg) of scrap plastic circuit boards (PCBs).
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The material required is plastic circuit boards (PCBs).
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The PCBs must be extracted from condemned or non-functional electronic devices.
- [unverifiable_remote] Acceptable sources include laptops, desktop computers, mobile phones, televisions, and other electronic devices containing PCBs.
- [unverifiable_remote] Scrap, non-functional, or damaged PCBs are acceptable.
- [unverifiable_remote] Preferred suppliers are located in or around Lagos, Nigeria.
- [unverifiable_remote] Suppliers from other locations within Nigeria are also considered.
- [unverifiable_remote] Photographs of the PCBs are requested if available.
- [unverifiable_remote] Pricing will be negotiated based on quality and quantity.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**3,465,000 to 14,770,000 NGN** (priced as material, width 1.2399, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 10000 kg of circuit_board 80%, plastic 15%, copper 5% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 11,550,000 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- The company is seeking to purchase 10 ton (10,000 kg) of scrap plastic circuit boards (PCBs). -> not proven remotely. Weigh on the scale and photograph the display.
- The material required is plastic circuit boards (PCBs). -> not proven remotely. Weigh on the scale and photograph the display.
- The PCBs must be extracted from condemned or non-functional electronic devices. -> not proven remotely. Agent will confirm at pickup.
- Acceptable sources include laptops, desktop computers, mobile phones, televisions, and other electronic devices containing PCBs. -> not proven remotely. Agent will confirm at pickup.
- Scrap, non-functional, or damaged PCBs are acceptable. -> not proven remotely. Agent will confirm at pickup.
- Preferred suppliers are located in or around Lagos, Nigeria. -> not proven remotely. Agent will confirm at pickup.
- Suppliers from other locations within Nigeria are also considered. -> not proven remotely. Agent will confirm at pickup.
- Photographs of the PCBs are requested if available. -> not proven remotely. Agent will confirm at pickup.
- Pricing will be negotiated based on quality and quantity. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': '10 Ton Scrap Plastic Circuit Boards Needed', 'category': None, 'site_category': 'E-waste', 'price_ngn': 10000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/10-ton-scrap-plastic-circuit-boards-needed/'}`
