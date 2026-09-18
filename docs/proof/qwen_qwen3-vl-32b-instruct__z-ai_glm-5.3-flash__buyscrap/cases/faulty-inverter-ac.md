# Case faulty-inverter-ac

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0009  |  22253 ms

## What the engine saw
- Presentation: single_unit
- Category: split air conditioner (confidence 0.9)
- Made of: plastic 40%, steel 30%, copper 20%, mixed_electronic 10%
- Estimated weight: 35.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: Dusty exterior, Yellowing plastic casing, Minor scratches on front panel, Handwritten red numbers '14,570' on side
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Inverter

## Two readers
- brand_text differed between the two readers, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- 10 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> dispute. brand_text differed between the two readers, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; 10 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=None model=None label=True lines=1
- **retrieval** -> empty. query='Inverter Faulty inverter AC available for sale. Location: Oshodi, Lagos State Price: 60,00' hits=[]
- **gate** -> abstain. no candidates and no model text
- **condition** -> not working. by the seller's own account

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 6778 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 13246 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2229 ms (replayed)
- total across calls: 22253 ms; wall clock: 197 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 18%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- read off the item's own label
- 1 lines seen by both readers
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] Faulty inverter AC available for sale.
    priced as: assumed needs a regas. Agent checks pressures with manifold gauges
- [unverifiable_remote] Location: Oshodi, Lagos State
- [unverifiable_remote] Price: 60,000 naira
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
**46,953 to 105,070 NGN** (priced as material, width 0.7646, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 35 kg of plastic 40%, steel 30%, copper 20%, mixed_electronic 10% (rates for mixed_electronic, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 79,100 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- Faulty inverter AC available for sale. -> not proven remotely. Agent checks pressures with manifold gauges.
- Location: Oshodi, Lagos State -> not proven remotely. Agent will confirm at pickup.
- Price: 60,000 naira -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Faulty Inverter AC', 'category': None, 'site_category': 'E-waste', 'price_ngn': 60000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/faulty-inverter-ac/'}`
