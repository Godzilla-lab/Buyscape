# Case xdMNB5jwsl5wXNJJQSpz3z8l

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  16044 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: plastic 60%, steel 30%, carton 10%
- Estimated weight: 12.0 kg (confidence 0.7)
- Brand read off the item: Bona
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: unit appears new, still in original packaging, box slightly damaged with creases and tape marks
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Bona | AIR CONDITIONER

## Two readers
- brand_text was read by one reader and confirmed by OCR
- model_text was seen by only one reader, so it is treated as unread
- rating_text was seen by only one reader, so it is treated as unread
- serial_text was seen by only one reader, so it is treated as unread
- 6 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- KCKENRK
- Bona
- AIR CONDITIONER
- INVERTER

## Chain
- **ocr** -> ok. 4 lines: KCKENRK | Bona | AIR CONDITIONER | INVERTER
- **corroborate** -> dispute. brand_text was read by one reader and confirmed by OCR; model_text was seen by only one reader, so it is treated as unread; rating_text was seen by only one reader, so it is treated as unread; serial_text was seen by only one reader, so it is treated as unread; 6 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=split air conditioner brand=Bona model=None label=False lines=2
- **retrieval** -> empty. query='Bona Bona AIR CONDITIONER High quality solar air conditioner, 10 years warranty, very low ' hits=[]
- **gate** -> abstain. no candidates and no model text

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5295 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8173 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2576 ms (replayed)
- total across calls: 16044 ms; wall clock: 602 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 18%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- no label, plate or settings screen was legible
- 2 lines seen by both readers
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
- [unverified] High quality solar air conditioner
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverifiable_remote] 10 years warranty
- [unverifiable_remote] very low energy consumption
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
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
**1,376 to 3,600 NGN** (priced as material, width 0.8935, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of plastic 60%, steel 30%, carton 10% (rates for carton, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,592 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- High quality solar air conditioner -> not proven remotely. Agent reads the outdoor rating plate.
- 10 years warranty -> not proven remotely. Agent will confirm at pickup.
- very low energy consumption -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Solar Split Air Conditioner 1.5 Hp', 'category': 'split_ac', 'price_ngn': 440000, 'is_used': False, 'url': '/ojo/home-appliances/solar-split-air-conditioner-1-5-hp-xdMNB5jwsl5wXNJJQSpz3z8l.html?page=1&pos=8&cur_pos=8&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
