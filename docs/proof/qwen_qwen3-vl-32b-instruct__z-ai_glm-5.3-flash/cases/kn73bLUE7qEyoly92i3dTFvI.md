# Case kn73bLUE7qEyoly92i3dTFvI

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  31801 ms

## What the engine saw
- Presentation: single_unit
- Category: engine_component (confidence 0.9)
- Made of: steel 60%, plastic 20%, rubber 10%, copper 10%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: some surface dirt and grime, minor oil residue on components
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- 1 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. 1 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=engine_component brand=None model=None label=True lines=0
- **retrieval** -> ok. query='30kva perkins John holt generator, almost new of 950hrs run. 
With 100% warranty' hits=['Perkins P150 150kVA', 'Perkins P100 100kVA', 'Mikano MK30 30kVA']
- **identify** -> refused. chosen=None None margin=0.1
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Perkins P150 150kVA (0.4333)
  - Perkins P100 100kVA (0.4333)
  - Mikano MK30 30kVA (0.2333)

**Not identified: CANNOT_IDENTIFY.** No legible brand, model or rating text on engine or plate; seller's 30kVA Perkins claim unverifiable and no 30kVA Perkins in shortlist.

## How sure the engine is (back office)
**Not sure enough to price: 7% on the best answer. It is probably a Mikano MK30 or a Perkins P100, and the photos cannot separate them.**

- Identification confidence: 7% (unknown)
- Price confidence: 16%
- It is weighing: Mikano MK30 (0.15), Perkins P100 (0.05)
- No legible brand, model or rating text on engine or plate; seller's 30kVA Perkins claim unverifiable and no 30kVA Perkins in shortlist.
- read off the item's own label
- the two readers agreed on nothing legible
- the next candidate was only 0.1 behind
- 9 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## Claims
- [unverifiable_remote] 30kva perkins John holt generator
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] perkins John holt generator
- [unverifiable_remote] almost new of 950hrs run
- [unverifiable_remote] almost new of 950hrs run
- [unverifiable_remote] With 100% warranty
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**9,229 to 25,590 NGN** (priced as material, width 0.9397, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of steel 60%, plastic 20%, rubber 10%, copper 10% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 19,875 NGN

Conditions attached to this price:
- Not identified: No legible brand, model or rating text on engine or plate; seller's 30kVA Perkins claim unverifiable and no 30kVA Perkins in shortlist.
- 30kva perkins John holt generator -> not proven remotely. Weigh on the scale and photograph the display.
- perkins John holt generator -> not proven remotely. Agent will confirm at pickup.
- almost new of 950hrs run -> not proven remotely. Agent will confirm at pickup.
- almost new of 950hrs run -> not proven remotely. Agent will confirm at pickup.
- With 100% warranty -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': '30kva John Holt Perkins Generator', 'category': 'generator', 'price_ngn': 4100000, 'is_used': True, 'url': '/alimosho/power-equipments/30kva-john-holt-perkins-generator-kn73bLUE7qEyoly92i3dTFvI.html?page=2&pos=22&cur_pos=22&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
