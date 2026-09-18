# Case i52rWzljs8oUUAFTxvamNpo7

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  22447 ms

## What the engine saw
- Presentation: sealed_new
- Category: air_conditioner (confidence 0.9)
- Made of: carton 100%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: Kenstar
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: Kenstar | Inverter | NEXUS

## Two readers
- brand_text agreed by both readers
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- 11 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- NEXUS
- NEKUS
- E
- 159
- 8-12TF5
- Ken
- tar
- AS-12TFS
- star

## Chain
- **ocr** -> ok. 9 lines: NEXUS | NEKUS | E | 159 | 8-12TF5 | Ken | tar | AS-12TFS | star
- **corroborate** -> dispute. brand_text agreed by both readers; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; 11 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=air_conditioner brand=Kenstar model=None label=True lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **gate** -> abstain. multiple items in frame

## Identification
No catalogue candidates matched.

**Not identified: EVIDENCE_INCOMPLETE.** The photos show more than one item, so no single item can be identified.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- The photos show more than one item, so no single item can be identified.
- read off the item's own label
- 3 lines seen by both readers
- looks like a catalogue or stock image
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
3. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of the rating plate on the outdoor unit showing the model and HP. Then, without stopping the video: Open the front grille of the indoor unit and photograph the filters and coil. Finish with: A short clip with the unit running and the display lit. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it still blow cold air?
- Do you have both the indoor unit and the outdoor unit?

## Claims
- [unverified] KENSTAR 1.5HP Regular Split AC
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverifiable_remote] R410 GAS
    priced as: assumed needs a regas. Agent checks pressures with manifold gauges
- [unverified] Anti-Rust Cabinet
    priced as: assumed needs a regas. Agent checks pressures with manifold gauges
- [unverifiable_remote] Independent Dehumidification
    priced as: the smallest rating this brand sells. Agent reads the outdoor rating plate
- [unverified] Louver
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
**308 to 1,800 NGN** (priced as material, width 1.414, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of carton 100% (rates for carton are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 900 NGN

Conditions attached to this price:
- Not identified: The photos show more than one item, so no single item can be identified.
- Evidence flag: looks like a catalogue or stock image
- KENSTAR 1.5HP Regular Split AC -> not proven remotely. Agent reads the outdoor rating plate.
- R410 GAS -> not proven remotely. Agent checks pressures with manifold gauges.
- Anti-Rust Cabinet -> not proven remotely. Agent checks pressures with manifold gauges.
- Independent Dehumidification -> not proven remotely. Agent reads the outdoor rating plate.
- Louver -> not proven remotely. Agent reads the outdoor rating plate.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the unit..
- Required evidence 'indoor_unit' was not supplied -> not proven remotely. One photo of the whole indoor unit..
- Required evidence 'outdoor_unit' was not supplied -> not proven remotely. One photo of the outdoor compressor unit..
- Required evidence 'rating_plate' was not supplied -> not proven remotely. Close-up of the rating plate on the outdoor unit showing the model and HP..
- Required evidence 'grille_open' was not supplied -> not proven remotely. Open the front grille of the indoor unit and photograph the filters and coil..

## Answer key (not shown to the engine)
`{'title': 'Kenstar 1.5hp Basic Split Air Conditioner R410 Gas Ks-12tfs', 'category': 'split_ac', 'price_ngn': 355000, 'is_used': False, 'url': '/ikeja/home-appliances/kenstar-1-5hp-basic-split-air-conditioner-r410-gas-ks-12tfs-i52rWzljs8oUUAFTxvamNpo7.html?page=1&pos=14&cur_pos=14&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
