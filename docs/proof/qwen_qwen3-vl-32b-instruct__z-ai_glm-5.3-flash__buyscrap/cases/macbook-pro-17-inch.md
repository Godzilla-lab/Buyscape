# Case macbook-pro-17-inch

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0016  |  92105 ms

## What the engine saw
- Presentation: single_unit
- Category: laptop (confidence 0.95)
- Made of: aluminium 60%, plastic 30%, circuit_board 5%, steel 5%
- Estimated weight: 2.1 kg (confidence 0.8)
- Brand read off the item: Apple
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: screen has reflections and smudges, trackpad shows minor wear, keyboard keys appear intact, chassis shows light scuffs
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Apple

## Two readers
- brand_text agreed by both readers
- 1 transcribed lines was seen by only one reader, so it is treated as unread
- item_type was read by only one reader, so it is kept but not confirmed

## Chain
- **ocr** -> ok. 0 lines: 
- **corroborate** -> dispute. brand_text agreed by both readers; 1 transcribed lines was seen by only one reader, so it is treated as unread; item_type was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=laptop brand=Apple model=None label=False lines=1
- **retrieval** -> ok. query='Apple Apple MacBook Pro (17-inch, Late 2011) Laptops health 50% Physical damage 5% No char' hits=['Apple MacBook Pro 17-inch 2011', 'Apple MacBook Pro 13-inch 2017', 'Apple MacBook Pro 13-inch M2 2022', 'Apple MacBook Pro 14-inch M1 Pro 2021', 'Apple MacBook Pro 14-inch M3 2023']
- **identify** -> ok. chosen=Apple MacBook Pro 17-inch 2011 margin=0.8
- **abstain** -> pass. confidence=0.46 margin=0.8

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 15657 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 25108 ms (replayed)
- identify on z-ai/glm-5.3-flash: 45183 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 6157 ms (replayed)
- total across calls: 92105 ms; wall clock: 613 ms

## Identification
Shortlist from the catalogue:
  - Apple MacBook Pro 17-inch 2011 (0.6333)
  - Apple MacBook Pro 13-inch 2017 (0.5)
  - Apple MacBook Pro 13-inch M2 2022 (0.4714)
  - Apple MacBook Pro 14-inch M1 Pro 2021 (0.4714)
  - Apple MacBook Pro 14-inch M3 2023 (0.4714)

**Answer: Apple MacBook Pro 17-inch 2011** (margin 0.8)

## How sure the engine is (back office)
**Not sure enough to price: 46% on the best answer. It is probably a Apple MacBook Pro 17-inch 2011 or a Apple MacBook Pro 13-inch 2017, and the photos cannot separate them.**

- Identification confidence: 46% (unsure)
- Price confidence: 0%
- It is weighing: Apple MacBook Pro 17-inch 2011 (0.85), Apple MacBook Pro 13-inch 2017 (0.05), Apple MacBook Pro 14-inch M1 Pro 2021 (0.05)
- no label, plate or settings screen was legible
- the two readers agreed on nothing legible
- the item_type was read by only one reader and is not confirmed
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
**NO_PRICE_DATA.** Only 0 comparable asking prices were found and there is no published band for this category, so no honest range can be produced. Nothing below the 2,719 NGN floor.

Conditions attached to this price:
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
