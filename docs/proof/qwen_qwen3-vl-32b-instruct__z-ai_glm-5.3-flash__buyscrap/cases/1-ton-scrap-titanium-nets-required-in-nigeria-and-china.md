# Case 1-ton-scrap-titanium-nets-required-in-nigeria-and-china

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0012  |  55985 ms

## What the engine saw
- Presentation: mixed_lot
- Category: metal mesh scrap (confidence 0.9)
- Made of: steel 80%, plastic 20%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: tangled and crumpled, some rust visible on metal parts
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- brand_text was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=metal mesh scrap brand=None model=None label=False lines=0
- **gate** -> lot. priced by material, identification skipped
- **weight** -> stated. 1000 kg from the seller's words

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
- [unverifiable_remote] The buyer is seeking approximately 1 ton (1000 kg) of scrap titanium nets.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The buyer is interested in various forms of scrap titanium netting, including industrial titanium mesh/screening, damaged or offcut titanium nets, and titanium alloy nets.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The condition of the scrap titanium nets can be scrap, damaged, or offcut material.
- [unverifiable_remote] The buyer is seeking suppliers located in Nigeria and China.
- [unverifiable_remote] Suppliers must be able to provide documentation regarding the material’s origin and composition, if possible.
- [unverifiable_remote] Pricing will be negotiated based on the material’s purity, quantity, and condition.
    priced as: assumed not working. Agent powers the item on before payment
- [unverifiable_remote] Interested suppliers are requested to provide detailed information about their available scrap titanium nets, including quantity, material composition, condition, location, photographs (if available), and quoted price.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**126,000 to 516,000 NGN** (priced as material, width 1.215, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 1000 kg of steel 80%, plastic 20% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 420,000 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- The buyer is seeking approximately 1 ton (1000 kg) of scrap titanium nets. -> not proven remotely. Weigh on the scale and photograph the display.
- The buyer is interested in various forms of scrap titanium netting, including industrial titanium mesh/screening, damaged or offcut titanium nets, and titanium alloy nets. -> not proven remotely. Weigh on the scale and photograph the display.
- The condition of the scrap titanium nets can be scrap, damaged, or offcut material. -> not proven remotely. Agent will confirm at pickup.
- The buyer is seeking suppliers located in Nigeria and China. -> not proven remotely. Agent will confirm at pickup.
- Suppliers must be able to provide documentation regarding the material’s origin and composition, if possible. -> not proven remotely. Agent will confirm at pickup.
- Pricing will be negotiated based on the material’s purity, quantity, and condition. -> not proven remotely. Agent powers the item on before payment.
- Interested suppliers are requested to provide detailed information about their available scrap titanium nets, including quantity, material composition, condition, location, photographs (if available), and quoted price. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': '1 Ton of Scrap Titanium Nets Required in Nigeria and China', 'category': None, 'site_category': 'Iron', 'price_ngn': 1000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/1-ton-scrap-titanium-nets-required-in-nigeria-and-china/'}`
