# Case macbook-pro-17-inch

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0011  |  25613 ms

## What the engine saw
- Presentation: single_unit
- Category: laptop (confidence 0.95)
- Made of: aluminium 60%, plastic 30%, circuit_board 5%, glass 5%
- Estimated weight: 2.1 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: screen has reflections and smudges, keyboard keys appear worn, trackpad shows minor scuffing
- Looks like a catalogue image: no
- Screenshot of a gallery: no

## Two readers
- brand_text agreed by both readers
- model_text was seen by only one reader, so it is treated as unread
- 1 transcribed lines was seen by only one reader, so it is treated as unread

## Chain
- **corroborate** -> dispute. brand_text agreed by both readers; model_text was seen by only one reader, so it is treated as unread; 1 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=laptop brand=Apple model=None label=False lines=0
- **grounding** -> dropped. brand
- **forensics** -> flag. the reader stated brand it could not point to in the photos
- **retrieval** -> ok. query='MacBook Pro (17-inch, Late 2011) Laptops health 50% Physical damage 5% No charger Color Gr' hits=['Apple MacBook Pro 17-inch 2011', 'Apple MacBook Pro 13-inch 2017', 'Acer Aspire 5', 'Tecno Camon 50', 'Tecno Pova 5']
- **identify** -> ok. chosen=Apple MacBook Pro 17-inch 2011 margin=0.55
- **abstain** -> abstain. no label, top score 0.75

## Identification
Shortlist from the catalogue:
  - Apple MacBook Pro 17-inch 2011 (0.3333)
  - Apple MacBook Pro 13-inch 2017 (0.2)
  - Acer Aspire 5 (0.2)
  - Tecno Camon 50 (0.2)
  - Tecno Pova 5 (0.2)

**Not identified: CANNOT_IDENTIFY.** No label, plate or settings screen was legible, and the visual match alone scored only 0.75.

Evidence flags: the reader stated brand it could not point to in the photos

## How sure the engine is (back office)
**Not sure enough to price: 16% on the best answer. It is probably a Apple MacBook Pro 17-inch 2011 or a Apple MacBook Pro 13-inch 2017, and the photos cannot separate them.**

- Identification confidence: 16% (unknown)
- Price confidence: 14%
- It is weighing: Apple MacBook Pro 17-inch 2011 (0.75), Apple MacBook Pro 13-inch 2017 (0.2)
- No label, plate or settings screen was legible, and the visual match alone scored only 0.75.
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the reader stated brand it could not point to in the photos
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Photo of the sticker on the underside showing the model, serial or service tag. Then, still filming, do this on the item's own screen and hold it steady so the writing can be read: open system Information (Windows) or About This Mac, showing the model, processor, RAM and storage. Then, without stopping the video: If the bottom panel comes off with a screwdriver, remove it and photograph the inside: RAM slots, drive and battery. Finish with: A short clip typing a few keys, moving the trackpad, and plugging the charger in so the charge light shows. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
2. [PHOTO] Photo of the sticker on the underside showing the model, serial or service tag.
   _why: nothing on the item says which model this is_
3. [PHOTO] Screenshot of System Information (Windows) or About This Mac, showing the model, processor, RAM and storage.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it stay on for more than ten minutes with the charger unplugged?
- Has it ever been dropped, or had liquid spilled on it?
- What does not work on it? Say none if everything works.

## Claims
- [unverifiable_remote] MacBook Pro (17-inch, Late 2011)
- [unverifiable_remote] Laptops health 50%
    priced as: assumed the battery only works on the charger. Agent unplugs the charger and watches the battery for two minutes
- [unverifiable_remote] Physical damage 5%
- [unverifiable_remote] No charger
- [unverifiable_remote] Color Grey
- [unverifiable_remote] Laptop has not been used for a longtime
    priced as: assumed the sticker and the system do not match. Agent matches the serial on the sticker to the serial in System Information or the BIOS
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the laptop.
- [unverified] Required evidence 'lid_open_screen_on' was not supplied
    priced as: priced as if the worst case is true. Photo of the laptop open with the screen switched on, showing the desktop.
- [unverified] Required evidence 'bottom_sticker' was not supplied
    priced as: priced as if the worst case is true. Photo of the sticker on the underside showing the model, serial or service tag.
- [unverified] Required evidence 'about_screen' was not supplied
    priced as: priced as if the worst case is true. Screenshot of System Information (Windows) or About This Mac, showing the model, processor, RAM and storage.

## Price
**991 to 4,003 NGN** (priced as material, width 1.206, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 2.1 kg of aluminium 60%, plastic 30%, circuit_board 5%, glass 5% (rates for glass, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 2,669 NGN

Conditions attached to this price:
- Not identified: No label, plate or settings screen was legible, and the visual match alone scored only 0.75.
- Evidence flag: the reader stated brand it could not point to in the photos
- MacBook Pro (17-inch, Late 2011) -> not proven remotely. Agent will confirm at pickup.
- Laptops health 50% -> not proven remotely. Agent unplugs the charger and watches the battery for two minutes.
- Physical damage 5% -> not proven remotely. Agent will confirm at pickup.
- No charger -> not proven remotely. Agent will confirm at pickup.
- Color Grey -> not proven remotely. Agent will confirm at pickup.
- Laptop has not been used for a longtime -> not proven remotely. Agent matches the serial on the sticker to the serial in System Information or the BIOS.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the laptop..
- Required evidence 'lid_open_screen_on' was not supplied -> not proven remotely. Photo of the laptop open with the screen switched on, showing the desktop..
- Required evidence 'bottom_sticker' was not supplied -> not proven remotely. Photo of the sticker on the underside showing the model, serial or service tag..
- Required evidence 'about_screen' was not supplied -> not proven remotely. Screenshot of System Information (Windows) or About This Mac, showing the model, processor, RAM and storage..

## Answer key (not shown to the engine)
`{'title': 'MacBook Pro (17-inch)', 'category': None, 'site_category': 'E-waste', 'price_ngn': 150000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/macbook-pro-17-inch/'}`
