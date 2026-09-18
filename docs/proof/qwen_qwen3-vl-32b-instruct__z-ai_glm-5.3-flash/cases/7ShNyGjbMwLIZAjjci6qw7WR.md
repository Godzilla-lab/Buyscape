# Case 7ShNyGjbMwLIZAjjci6qw7WR

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0007  |  15942 ms

## What the engine saw
- Presentation: single_unit
- Category: battery charger (confidence 0.9)
- Made of: plastic 60%, steel 30%, circuit_board 5%, rubber 5%
- Estimated weight: 12.0 kg (confidence 0.7)
- Brand read off the item: QISA
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: minor scuffs on yellow casing, no visible damage to controls or display
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: DC ON | AC CHARGER | QISA

## Two readers
- model_text was seen by only one reader, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread
- brand_text was read by only one reader, so it is kept but not confirmed

## OCR read off the photos
- DCON
- OFF
- AC CNAN
- POSTED ON JIJI
- AMA
- SOSO
- HUB

## Chain
- **ocr** -> ok. 7 lines: DCON | OFF | AC CNAN | POSTED ON JIJI | AMA | SOSO | HUB
- **corroborate** -> dispute. model_text was seen by only one reader, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread; brand_text was read by only one reader, so it is kept but not confirmed
- **read_evidence** -> ok. category=battery charger brand=QISA model=None label=False lines=3
- **retrieval** -> empty. query='QISA DC ON AC CHARGER QISA Qasa spg-500va is a 500watts solar generator with a 78000mah ba' hits=[]
- **gate** -> abstain. no candidates and no model text

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5512 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 8438 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 1992 ms (replayed)
- total across calls: 15942 ms; wall clock: 445 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 22%
- No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- no label, plate or settings screen was legible
- 2 lines seen by both readers
- the brand was read by only one reader and is not confirmed
- 6 claims are still unproven, 0 are supported

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
- [unverifiable_remote] Qasa spg-500va is a 500watts solar generator
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The solar generator has a 78000mah battery
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
**1,209 to 4,116 NGN** (priced as material, width 1.0917, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of plastic 60%, steel 30%, circuit_board 5%, rubber 5% (rates for plastic, rubber are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 3,030 NGN

Conditions attached to this price:
- Not identified: No catalogue entry matched what was read and no model string was legible on the item, so there is nothing to rank.
- Qasa spg-500va is a 500watts solar generator -> not proven remotely. Weigh on the scale and photograph the display.
- The solar generator has a 78000mah battery -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Gaza 500wtt Solar Generator (Heavy Duty)', 'category': 'generator', 'price_ngn': 385000, 'is_used': False, 'url': '/lekki/power-equipments/gaza-500wtt-solar-generator-heavy-duty-7ShNyGjbMwLIZAjjci6qw7WR.html?page=2&pos=15&cur_pos=15&ads_per_page=23&ads_count=15133&lid=jDmK55nggeXBjrth'}`
