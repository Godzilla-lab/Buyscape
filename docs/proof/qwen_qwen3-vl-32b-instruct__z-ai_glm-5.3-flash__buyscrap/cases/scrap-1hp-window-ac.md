# Case scrap-1hp-window-ac

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0014  |  48440 ms

## What the engine saw
- Presentation: single_unit
- Category: air conditioner (confidence 0.95)
- Made of: steel 60%, copper_bare 20%, plastic 15%, circuit_board 5%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: exposed internal components, dirt and grime on condenser coils, missing front panel, loose wiring visible, rust on metal casing
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- item_type agreed by both readers

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> agree. item_type agreed by both readers
- **read_evidence** -> ok. category=air conditioner brand=None model=None label=False lines=0
- **retrieval** -> ok. query='A scrap 1 horsepower (1HP) window AC is available for sale. Location: Agege, Lagos State P' hits=['Samsung AR09 1HP', 'Hisense AS-09 1HP', 'LG S4-Q09 1HP', 'Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP']
- **identify** -> refused. chosen=None None margin=0.0
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 7474 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 9728 ms (replayed)
- identify on z-ai/glm-5.3-flash: 28056 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 3182 ms (replayed)
- total across calls: 48440 ms; wall clock: 1333 ms

## Identification
Shortlist from the catalogue:
  - Samsung AR09 1HP (0.2333)
  - Hisense AS-09 1HP (0.2)
  - LG S4-Q09 1HP (0.2)
  - Samsung AR12 1.5HP (0.15)
  - Scanfrost SFAC12 1.5HP (0.15)

**Not identified: CANNOT_IDENTIFY.** No label, plate or brand marking is legible on the stripped unit; any brand choice would be a guess.

## How sure the engine is (back office)
**Not sure enough to price: 4% on the best answer. It is probably a Samsung AR09 or a Hisense AS-09, and the photos cannot separate them.**

- Identification confidence: 4% (unknown)
- Price confidence: 16%
- It is weighing: Samsung AR09 (0.1), Hisense AS-09 (0.1)
- No label, plate or brand marking is legible on the stripped unit; any brand choice would be a guess.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the next candidate was only 0.0 behind
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] The item is a 1 horsepower (1HP) window AC.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The item is a window AC.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] The item is described as scrap.
    priced as: assumed needs a regas. Agent checks pressures with manifold gauges
- [unverifiable_remote] The item is located in Agege, Lagos State.
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
**26,576 to 75,925 NGN** (priced as material, width 0.9629, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of steel 60%, copper_bare 20%, plastic 15%, circuit_board 5% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 58,875 NGN

Conditions attached to this price:
- Not identified: No label, plate or brand marking is legible on the stripped unit; any brand choice would be a guess.
- The item is a 1 horsepower (1HP) window AC. -> not proven remotely. Agent reads the outdoor rating plate.
- The item is a window AC. -> not proven remotely. Agent reads the outdoor rating plate.
- The item is described as scrap. -> not proven remotely. Agent checks pressures with manifold gauges.
- The item is located in Agege, Lagos State. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Scrap 1HP window AC', 'category': None, 'site_category': 'E-waste', 'price_ngn': 35000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/scrap-1hp-window-ac/'}`
