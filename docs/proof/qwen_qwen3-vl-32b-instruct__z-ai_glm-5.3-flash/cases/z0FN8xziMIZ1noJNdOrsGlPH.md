# Case z0FN8xziMIZ1noJNdOrsGlPH

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  15676 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.9)
- Made of: plastic 70%, steel 20%, circuit_board 10%
- Estimated weight: 15.0 kg (confidence 0.8)
- Brand read off the item: Panasonic
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Panasonic

## Two readers
- brand_text agreed by both readers
- item_type was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- HOME APPLIANCES

## Chain
- **ocr** -> ok. 1 lines: HOME APPLIANCES
- **corroborate** -> agree. brand_text agreed by both readers; item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=split air conditioner brand=Panasonic model=None label=False lines=1
- **gate** -> abstain. multiple items in frame

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 4103 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6464 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 5109 ms (replayed)
- total across calls: 15676 ms; wall clock: 1246 ms

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- The photos show more than one item, so no single item can be identified.
- no label, plate or settings screen was legible
- 1 lines seen by both readers
- the item_type was read by only one reader and is not confirmed
- 11 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] Uk used Panasonic 2hp air conditioners
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Panasonic 2hp air conditioners
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Panasonic 2hp air conditioners
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverifiable_remote] with the remotes
- [unverifiable_remote] indoor hangers
- [unverifiable_remote] water hoses
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
**1,527 to 5,190 NGN** (priced as material, width 1.0903, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of plastic 70%, steel 20%, circuit_board 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 3,750 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Uk used Panasonic 2hp air conditioners -> not proven remotely. Agent reads the outdoor rating plate.
- Panasonic 2hp air conditioners -> not proven remotely. Agent reads the outdoor rating plate.
- Panasonic 2hp air conditioners -> not proven remotely. Agent reads the outdoor rating plate.
- with the remotes -> not proven remotely. Agent will confirm at pickup.
- indoor hangers -> not proven remotely. Agent will confirm at pickup.
- water hoses -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Low Voltage Panasonic 1.5hp Split Air Conditioner Pod', 'category': 'split_ac', 'price_ngn': 190000, 'is_used': True, 'url': '/lagos-island-west/home-appliances/low-voltage-panasonic-1-5hp-split-air-conditioner-pod-z0FN8xziMIZ1noJNdOrsGlPH.html?page=2&pos=19&cur_pos=19&ads_per_page=19&ads_count=5405&lid=0XmBf5MruhjkTPrH'}`
