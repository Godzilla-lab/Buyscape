# Case kGZvShsoiHYofl7VVl239rVc

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  30580 ms

## What the engine saw
- Presentation: single_unit
- Category: electric motor (confidence 0.95)
- Made of: steel 70%, copper 20%, plastic 10%
- Estimated weight: 50.0 kg (confidence 0.8)
- Brand read off the item: MAX ELECTRON
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scratches on casing, some dust and dirt accumulation, no visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: MAX ELECTRON

## Two readers
- brand_text was read by one reader and confirmed by OCR
- model_text differed between the two readers, so it is treated as unread
- rating_text differed between the two readers, so it is treated as unread
- serial_text differed between the two readers, so it is treated as unread
- 16 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- 23
- MAO
- LECTRON

## Chain
- **ocr** -> ok. 3 lines: 23 | MAO | LECTRON
- **corroborate** -> dispute. brand_text was read by one reader and confirmed by OCR; model_text differed between the two readers, so it is treated as unread; rating_text differed between the two readers, so it is treated as unread; serial_text differed between the two readers, so it is treated as unread; 16 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=electric motor brand=MAX ELECTRON model=None label=True lines=1
- **retrieval** -> ok. query='MAX ELECTRON MAX ELECTRON 30kva Alternator coil with warranty one year three phase and sin' hits=['Mikano MK30 30kVA']
- **identify** -> refused. chosen=None None margin=0.4
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Mikano MK30 30kVA (0.2333)

**Not identified: CANNOT_IDENTIFY.** Label states MAX ELECTRON, conflicting with shortlisted Mikano; no legible model number, so no single model is supported.

## How sure the engine is (back office)
**Not sure enough to price: 24% on the best answer. It is probably a MAX ELECTRON unknown 30kVA alternator or a Mikano MK30 30kVA, and the photos cannot separate them.**

- Identification confidence: 24% (unknown)
- Price confidence: 20%
- It is weighing: MAX ELECTRON unknown 30kVA alternator (0.5), Mikano MK30 30kVA (0.1)
- Label states MAX ELECTRON, conflicting with shortlisted Mikano; no legible model number, so no single model is supported.
- read off the item's own label
- the two readers agreed on nothing legible
- 7 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] 30kva Alternator coil
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] warranty one year
- [unverifiable_remote] three phase and single phase available
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**44,745 to 151,900 NGN** (priced as material, width 1.0898, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 50 kg of steel 70%, copper 20%, plastic 10% (rates for plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 118,000 NGN

Conditions attached to this price:
- Not identified: Label states MAX ELECTRON, conflicting with shortlisted Mikano; no legible model number, so no single model is supported.
- 30kva Alternator coil -> not proven remotely. Weigh on the scale and photograph the display.
- warranty one year -> not proven remotely. Agent will confirm at pickup.
- three phase and single phase available -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': '☆¤30kva Alternator Coil Three Phase and Single Phase Avail', 'category': 'generator', 'price_ngn': 875000, 'is_used': False, 'url': '/ojo/power-equipments/30kva-alternator-coil-three-phase-and-single-phase-avail-kGZvShsoiHYofl7VVl239rVc.html?page=1&pos=9&cur_pos=9&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
