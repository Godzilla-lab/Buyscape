# Case 10-tons-of-scrap-titanium-boards-required-in-nigeria-and-china

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0017  |  55590 ms

## What the engine saw
- Presentation: single_unit
- Category: industrial plate (confidence 0.9)
- Made of: steel 90%, plastic 10%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: rust stains on surface, chipped corner, dirt and grime
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type agreed by both readers
- **read_evidence** -> ok. category=industrial plate brand=None model=None label=False lines=0
- **retrieval** -> ok. query='A collaborative venture between a leading Chinese industrial manufacturer and a Nigerian r' hits=['Tecno Spark 10']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused
- **weight** -> stated. 10000 kg from the seller's words

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 20483 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 11567 ms (replayed)
- identify on z-ai/glm-5.3-flash: 14091 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 9449 ms (replayed)
- total across calls: 55590 ms; wall clock: 1718 ms

## Identification
Shortlist from the catalogue:
  - Tecno Spark 10 (0.2)

**Not identified: CANNOT_IDENTIFY.** Photos show dark metal sheets/boards, not a phone; no legible label, and the only shortlist entry (Tecno Spark 10) is a handset with no supporting evidence. Material composition (titanium vs other metal) cannot be verified visually.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- Photos show dark metal sheets/boards, not a phone; no legible label, and the only shortlist entry (Tecno Spark 10) is a handset with no supporting evidence. Material composition (titanium vs other metal) cannot be verified visually.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 13 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] The buyer is seeking approximately 10 tons (10,000 kg) of scrap titanium boards.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The buyer is interested in industrial titanium plates/sheets discarded or surplus from manufacturing, aerospace, or chemical processing.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The buyer accepts damaged or offcut titanium boards of any size or shape, provided they are primarily titanium.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Used titanium cladding/panels from construction or other applications are acceptable.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Titanium alloy boards are also acceptable.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] High titanium content is preferred.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Suppliers must be able to provide documentation regarding material origin and composition, if possible.
- [unverifiable_remote] The buyer is seeking suppliers in both Nigeria and China.
- [unverifiable_remote] Suppliers are requested to provide detailed information about their available scrap titanium nets, including quantity, material composition, condition, location, photographs (if available), and quoted price.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**1,380,000 to 5,580,000 NGN** (priced as material, width 1.2069, method material_floor, 0 comparable prices)

The weight is estimated from the photos, so this price is settled on the scale at pickup.

This item was not identified, so it is priced as material rather than as a working item: 10000 kg of steel 90%, plastic 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 4,600,000 NGN

Conditions attached to this price:
- Not identified: Photos show dark metal sheets/boards, not a phone; no legible label, and the only shortlist entry (Tecno Spark 10) is a handset with no supporting evidence. Material composition (titanium vs other metal) cannot be verified visually.
- The buyer is seeking approximately 10 tons (10,000 kg) of scrap titanium boards. -> not proven remotely. Weigh on the scale and photograph the display.
- The buyer is interested in industrial titanium plates/sheets discarded or surplus from manufacturing, aerospace, or chemical processing. -> not proven remotely. Weigh on the scale and photograph the display.
- The buyer accepts damaged or offcut titanium boards of any size or shape, provided they are primarily titanium. -> not proven remotely. Weigh on the scale and photograph the display.
- Used titanium cladding/panels from construction or other applications are acceptable. -> not proven remotely. Weigh on the scale and photograph the display.
- Titanium alloy boards are also acceptable. -> not proven remotely. Weigh on the scale and photograph the display.
- High titanium content is preferred. -> not proven remotely. Weigh on the scale and photograph the display.
- Suppliers must be able to provide documentation regarding material origin and composition, if possible. -> not proven remotely. Agent will confirm at pickup.
- The buyer is seeking suppliers in both Nigeria and China. -> not proven remotely. Agent will confirm at pickup.
- Suppliers are requested to provide detailed information about their available scrap titanium nets, including quantity, material composition, condition, location, photographs (if available), and quoted price. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': '10 Tons of Scrap Titanium Boards Required in Nigeria and China', 'category': None, 'site_category': 'Iron', 'price_ngn': 10000000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/10-tons-of-scrap-titanium-boards-required-in-nigeria-and-china/'}`
