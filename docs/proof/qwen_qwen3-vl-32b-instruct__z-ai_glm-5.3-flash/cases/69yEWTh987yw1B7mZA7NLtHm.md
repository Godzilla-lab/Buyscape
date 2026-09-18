# Case 69yEWTh987yw1B7mZA7NLtHm

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  25481 ms

## What the engine saw
- Presentation: sealed_new
- Category: air conditioner (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: INVERTER AIR CONDITIONER | MAJESTY INVERTER | INVERTER AIR CONDITIONER | MAJESTY INVERTER

## Two readers
- item_type agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- 4 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- AIR CONDITIONER
- INVERTER
- STEVEN RB
- LIXYA
- ZOUTDOORT
- MAXISPLISIN

## Chain
- **ocr** -> ok. 6 lines: AIR CONDITIONER | INVERTER | STEVEN RB | LIXYA | ZOUTDOORT | MAXISPLISIN
- **corroborate** -> dispute. item_type agreed by both readers; brand_text differed between the two readers, so it is treated as unread; 4 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=air conditioner brand=None model=None label=False lines=4
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='INVERTER AIR CONDITIONER MAJESTY INVERTER INVERTER AIR CONDITIONER MAJESTY INVERTER The ma' hits=['Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP', 'Royal RAC12 1.5HP', 'Hisense AS-12 1.5HP', 'LG S4-Q12 1.5HP']
- **identify** -> ok. chosen=Maxi Majesty Inverter 1.5HP margin=0.8
- **abstain** -> abstain. confidence 0.38: no label, plate or settings screen was legible; 4 lines seen by both readers; looks like a catalogue or stock image

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 4956 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 9188 ms (replayed)
- identify on z-ai/glm-5.3-flash: 9038 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 2299 ms (replayed)
- total across calls: 25481 ms; wall clock: 1898 ms

## Identification
Shortlist from the catalogue:
  - Samsung AR12 1.5HP (0.3)
  - Scanfrost SFAC12 1.5HP (0.3)
  - Royal RAC12 1.5HP (0.3)
  - Hisense AS-12 1.5HP (0.26)
  - LG S4-Q12 1.5HP (0.26)

**Not identified: EVIDENCE_INCOMPLETE.** The evidence only supports this answer at 38 percent, which is a guess. One clear photo of the label would settle it.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**Not sure enough to price: 23% on the best answer. It is probably a Maxi Majesty Inverter 1.5HP or a Scanfrost SFAC12 1.5HP, and the photos cannot separate them.**

- Identification confidence: 23% (unknown)
- Price confidence: 20%
- It is weighing: Maxi Majesty Inverter 1.5HP (0.9), Scanfrost SFAC12 1.5HP (0.1)
- The evidence only supports this answer at 38 percent, which is a guess. One clear photo of the label would settle it.
- no label, plate or settings screen was legible
- 4 lines seen by both readers
- looks like a catalogue or stock image
- 7 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of the rating plate on the outdoor unit showing the model and HP.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] The air conditioner is a maxi 1.5hp inverter split model.
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverifiable_remote] The air conditioner is designed to provide efficient, consistent cooling.
    priced as: assumed not cooling, compressor unproven. Agent runs the unit and measures amps with a clamp meter
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
**493 to 3,000 NGN** (priced as material, width 1.4351, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 25 kg of carton 100% (rates for carton are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 1,500 NGN

Conditions attached to this price:
- Not identified: The evidence only supports this answer at 38 percent, which is a guess. One clear photo of the label would settle it.
- Evidence flag: looks like a catalogue or stock image
- The air conditioner is a maxi 1.5hp inverter split model. -> not proven remotely. Agent reads the outdoor rating plate.
- The air conditioner is designed to provide efficient, consistent cooling. -> not proven remotely. Agent runs the unit and measures amps with a clamp meter.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Maxi 1.5hp Inverter Split Air Conditioner', 'category': 'split_ac', 'price_ngn': 360000, 'is_used': False, 'url': '/ikeja/home-appliances/maxi-1-5hp-inverter-split-air-conditioner-69yEWTh987yw1B7mZA7NLtHm.html?page=1&pos=11&cur_pos=11&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
