# Case used-dry-pressing-iron-for-sale-in-lagos

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  94067 ms

## What the engine saw
- Presentation: single_unit
- Category: iron (confidence 0.95)
- Made of: plastic 60%, steel 20%, copper 10%, rubber 10%
- Estimated weight: 1.2 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: visible stains on plastic body, cracked and frayed power cord, exposed wires near plug, dented base plate
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=iron brand=None model=None label=False lines=0
- **retrieval** -> ok. query='A used dry pressing iron that is still working is available for sale. Location: Agege, Lag' hits=['Acer Aspire 5', 'Tecno Pova 5', 'Kemage KM6500 5.5kVA']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Acer Aspire 5 (0.2)
  - Tecno Pova 5 (0.2)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Item is a dry pressing iron but no brand or model is legible; shortlist (laptop, phone, generator) does not match at all.

## How sure the engine is (back office)
**Not sure enough to price: 8% on the best answer. It is probably a Unknown Dry pressing iron, and the photos cannot separate them.**

- Identification confidence: 8% (unknown)
- Price confidence: 22%
- It is weighing: Unknown Dry pressing iron (0.2)
- Item is a dry pressing iron but no brand or model is legible; shortlist (laptop, phone, generator) does not match at all.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 6 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] A used dry pressing iron is available for sale.
- [unverifiable_remote] The dry pressing iron is still working.
    priced as: assumed not working. Agent powers the item on before payment
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**594 to 1,845 NGN** (priced as material, width 1.0248, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 1.2 kg of plastic 60%, steel 20%, copper 10%, rubber 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 1,398 NGN

Conditions attached to this price:
- Not identified: Item is a dry pressing iron but no brand or model is legible; shortlist (laptop, phone, generator) does not match at all.
- A used dry pressing iron is available for sale. -> not proven remotely. Agent will confirm at pickup.
- The dry pressing iron is still working. -> not proven remotely. Agent powers the item on before payment.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Used dry pressing iron', 'category': None, 'site_category': 'E-waste', 'price_ngn': 5000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/used-dry-pressing-iron-for-sale-in-lagos/'}`
