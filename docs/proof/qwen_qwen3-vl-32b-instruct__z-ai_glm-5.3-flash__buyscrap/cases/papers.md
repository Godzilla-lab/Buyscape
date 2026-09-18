# Case papers

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0014  |  51150 ms

## What the engine saw
- Presentation: mixed_lot
- Category: school supplies (confidence 0.9)
- Made of: paper 90%, carton 10%
- Estimated weight: 0.5 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: pages appear slightly worn and creased, some text faded or smudged
- Looks like a catalogue image: no
- Screenshot of a gallery: yes
- Text read: VICTORY BAPTIST NURSERY & PRIMARY SCHOOL | Class:  | Subject:  | Date:  | SCHOOL ANTHEM | METRIC TABLE | CAPACITY MEASURE (LIQUID VOLUME) | 10 millilitres = 1 centilitre

## Two readers
- 24 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- 4. Sanni, Saheed Adewale
- 2. Nelson, Raphael Ugochuky
- Department of Science
- Ayanlére, Joy Adunola
- Supervisor: Mr
- Faculty
- VICTORY BAPTIST NURSERY & PRIM
- Oyo State College of Agricul
- Raheem, Rofiat Omolara
- 3. Adeoye, Kaosarat Olayem
- the
- Date:

## Chain
- **ocr** -> ok. 32 lines: 4. Sanni, Saheed Adewale | 2. Nelson, Raphael Ugochuky | Department of Science | Ayanlére, Joy Adunola | Supervisor: Mr 
- **corroborate** -> dispute. 24 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=school supplies brand=None model=None label=False lines=42
- **forensics** -> flag. screenshot of a gallery rather than a photo of the item
- **gate** -> lot. priced by material, identification skipped

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 17926 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 32514 ms
- extract_claims on qwen/qwen3-vl-32b-instruct: 710 ms (replayed)
- total across calls: 51150 ms; wall clock: 32563 ms

## Identification
No catalogue candidates matched.

**Not identified: CANNOT_IDENTIFY.** This is a mixed lot, so it is priced by material and weight rather than identified.

Evidence flags: screenshot of a gallery rather than a photo of the item

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 27%
- This is a mixed lot, so it is priced by material and weight rather than identified.
- no label, plate or settings screen was legible
- 42 lines seen by both readers
- screenshot of a gallery rather than a photo of the item
- 4 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Photograph one item on its own, with nothing else in the picture.
   _why: the photos show more than one item_
2. [PHOTO] Take a new photo of the item itself, not a picture of another screen.
   _why: this is a screenshot rather than a photo of the item_
3. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**24 to 60 NGN** (priced as material, width 0.8426, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 0.5 kg of paper 90%, carton 10% (rates for carton, paper are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 30 NGN

Conditions attached to this price:
- Not identified: This is a mixed lot, so it is priced by material and weight rather than identified.
- Evidence flag: screenshot of a gallery rather than a photo of the item
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Used Papers', 'category': None, 'site_category': 'Papers', 'price_ngn': 3000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/papers/'}`
