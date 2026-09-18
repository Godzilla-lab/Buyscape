# Case pC9BWTQbM94o1FM7HH3I08Jv

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  18224 ms

## What the engine saw
- Presentation: sealed_new
- Category: smartphone (confidence 0.95)
- Made of: paper 80%, plastic 20%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: SAMSUNG
- Model read off the item: S20+ 5G
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: SAMSUNG | Galaxy S20 | S20+ 5G

## Two readers
- brand_text agreed by both readers
- model_text was read by one reader and confirmed by OCR

## OCR read off the photos
- 520
- ONYITEXGADGET
- S20+5G

## Chain
- **ocr** -> ok. 3 lines: 520 | ONYITEXGADGET | S20+5G
- **corroborate** -> agree. brand_text agreed by both readers; model_text was read by one reader and confirmed by OCR
- **read_evidence** -> ok. category=smartphone brand=SAMSUNG model=S20+ 5G label=True lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='SAMSUNG S20+ 5G SAMSUNG Galaxy S20 S20+ 5G Samsung galaxy S20 plus 5G 256GB available for ' hits=['Samsung Galaxy S21', 'Samsung Galaxy S22', 'Samsung Galaxy S23', 'Samsung Galaxy S24', 'Samsung Galaxy S25']
- **identify** -> label. named from the label: SAMSUNG S20+ 5G, not in the catalogue
- **abstain** -> pass. confidence=0.45 from the label

## Identification
Shortlist from the catalogue:
  - Samsung Galaxy S21 (0.5)
  - Samsung Galaxy S22 (0.5)
  - Samsung Galaxy S23 (0.5)
  - Samsung Galaxy S24 (0.5)
  - Samsung Galaxy S25 (0.5)

**Answer: SAMSUNG S20+ 5G** (named from the item's own label; not in the catalogue)

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**45%: the photos do not say what this is.**

- Identification confidence: 45% (unsure)
- Price confidence: 13%
- named from the item's own label, which the catalogue does not list
- read off the item's own label
- 3 lines seen by both readers
- looks like a catalogue or stock image
- 8 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [PHOTO] Screenshot of Settings then About, showing the model name and storage.
   _why: nothing on the item says which model this is_
3. [PHOTO] Dial *#06# and screenshot the IMEI that appears.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Has the screen or battery ever been changed?
- Is it signed out of iCloud or Google, so a new owner can set it up?

## Claims
- [unverifiable_remote] Samsung galaxy S20 plus 5G
- [unverified] 256GB
    priced as: smallest variant of this model. Agent reads storage from Settings
- [unverifiable_remote] available for sell
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and take one photo with the paper next to the phone.
- [unverified] Required evidence 'front_screen_on' was not supplied
    priced as: priced as if the worst case is true. Photo of the front with the screen switched on, showing the home screen.
- [unverified] Required evidence 'back' was not supplied
    priced as: priced as if the worst case is true. Photo of the back of the phone.
- [unverified] Required evidence 'settings_about' was not supplied
    priced as: priced as if the worst case is true. Screenshot of Settings then About, showing the model name and storage.
- [unverified] Required evidence 'imei_dial' was not supplied
    priced as: priced as if the worst case is true. Dial *#06# and screenshot the IMEI that appears.

## Price
**51,287 to 191,100 NGN** (priced as a working item, width 1.1536, method uncalibrated_wide, 2 comparable prices)

2 used asking prices, 20th to 80th percentile 192,000 to 273,000 NGN, converted to a buy range with the 0.45 to 0.7 ask-to-buy spread, then reduced by 0.5936 for unproven claims, floored at the scrap value 34.

Scrap floor: 34 NGN

Conditions attached to this price:
- Evidence flag: looks like a catalogue or stock image
- Samsung galaxy S20 plus 5G -> not proven remotely. Agent will confirm at pickup.
- 256GB -> not proven remotely. Agent reads storage from Settings.
- available for sell -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and take one photo with the paper next to the phone..
- Required evidence 'front_screen_on' was not supplied -> not proven remotely. Photo of the front with the screen switched on, showing the home screen..
- Required evidence 'back' was not supplied -> not proven remotely. Photo of the back of the phone..
- Required evidence 'settings_about' was not supplied -> not proven remotely. Screenshot of Settings then About, showing the model name and storage..
- Required evidence 'imei_dial' was not supplied -> not proven remotely. Dial *#06# and screenshot the IMEI that appears..

## Answer key (not shown to the engine)
`{'title': 'New Samsung Galaxy S20+ 5G 256 GB Black', 'category': 'phone', 'price_ngn': 270000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-samsung-galaxy-s20-5g-256-gb-black-pC9BWTQbM94o1FM7HH3I08Jv.html?page=1&pos=7&cur_pos=7&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
