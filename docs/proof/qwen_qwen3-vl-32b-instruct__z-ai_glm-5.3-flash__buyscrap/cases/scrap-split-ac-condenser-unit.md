# Case scrap-split-ac-condenser-unit

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  22496 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.9)
- Made of: steel 60%, plastic 30%, copper_bare 10%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: dusty surface, grime on top and sides, dark interior grilles appear dirty
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. nothing identifying was read by either
- **read_evidence** -> ok. category=split air conditioner brand=None model=None label=False lines=0
- **retrieval** -> ok. query='A scrap split AC condenser unit is available for sale. Location: Agege, Lagos State Price:' hits=['Infinix Note 50', 'Tecno Camon 50', 'Infinix Hot 50', 'Infinix Note 30', 'Infinix Note 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused
- **condition** -> not working. by the seller's own account

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 4569 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8363 ms (replayed)
- identify on z-ai/glm-5.3-flash: 6542 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3022 ms (replayed)
- total across calls: 22496 ms; wall clock: 227 ms

## Identification
Shortlist from the catalogue:
  - Infinix Note 50 (0.4)
  - Tecno Camon 50 (0.2)
  - Infinix Hot 50 (0.2)
  - Infinix Note 30 (0.2)
  - Infinix Note 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** Item is a split AC condenser unit; the shortlist contains only phones, none of which fit, and no legible label identifies any brand or model.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 18%
- Item is a split AC condenser unit; the shortlist contains only phones, none of which fit, and no legible label identifies any brand or model.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] This is a scrap split AC condenser unit.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The item is being sold as is, for parts, repair or recycling.
    priced as: assumed needs a regas. Agent checks pressures with manifold gauges
- [unverifiable_remote] The location of the item is Agege, Lagos State.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the unit.
- [unverified] Required evidence 'indoor_unit' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole indoor unit.
- [unverified] Required evidence 'outdoor_unit' was not supplied
    priced as: priced as if the worst case is true. One photo of the outdoor compressor unit.
- [unverified] Required evidence 'rating_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of the rating plate on the outdoor unit showing the model and HP.
- [unverified] Required evidence 'grille_open' was not supplied
    priced as: priced as if the worst case is true. Open the front grille of the indoor unit and photograph the filters and coil.

## Price
**17,659 to 42,850 NGN** (priced as material, width 0.8326, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, plastic 30%, copper_bare 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 33,250 NGN

Conditions attached to this price:
- Not identified: Item is a split AC condenser unit; the shortlist contains only phones, none of which fit, and no legible label identifies any brand or model.
- This is a scrap split AC condenser unit. -> not proven remotely. Agent reads the outdoor rating plate.
- The item is being sold as is, for parts, repair or recycling. -> not proven remotely. Agent checks pressures with manifold gauges.
- The location of the item is Agege, Lagos State. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Scrap split AC condenser unit', 'category': None, 'site_category': 'E-waste', 'price_ngn': 50000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/scrap-split-ac-condenser-unit/'}`
