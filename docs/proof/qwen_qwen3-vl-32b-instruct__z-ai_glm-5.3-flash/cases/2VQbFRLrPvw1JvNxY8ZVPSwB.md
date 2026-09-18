# Case 2VQbFRLrPvw1JvNxY8ZVPSwB

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0010  |  21622 ms

## What the engine saw
- Presentation: sealed_new
- Category: computer (confidence 0.9)
- Made of: paper 90%, plastic 10%
- Estimated weight: 12.0 kg (confidence 0.7)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: yes
- Screenshot of a gallery: no
- Text read: UN 3481 | DASHLINK INTEGRATED SYSTEM | Intel Inside

## Two readers
- item_type agreed by both readers
- brand_text differed between the two readers, so it is treated as unread
- 4 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- Q
- UN 3481
- 112-

## Chain
- **ocr** -> ok. 3 lines: Q | UN 3481 | 112-
- **corroborate** -> dispute. item_type agreed by both readers; brand_text differed between the two readers, so it is treated as unread; 4 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=computer brand=None model=None label=True lines=3
- **forensics** -> flag. looks like a catalogue or stock image
- **retrieval** -> ok. query='UN 3481 DASHLINK INTEGRATED SYSTEM Intel Inside Hp probook 440 g10 intel core i7 13th gen ' hits=['HP 2000', 'HP ProBook 450 G7', 'HP 250 G7', 'HP Pavilion 15', 'HP EliteBook 840 G5']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5007 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 6610 ms (replayed)
- identify on z-ai/glm-5.3-flash: 5804 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 4201 ms (replayed)
- total across calls: 21622 ms; wall clock: 1267 ms

## Identification
Shortlist from the catalogue:
  - HP 2000 (0.5)
  - HP ProBook 450 G7 (0.4333)
  - HP 250 G7 (0.4333)
  - HP Pavilion 15 (0.4333)
  - HP EliteBook 840 G5 (0.3)

**Not identified: CANNOT_IDENTIFY.** Sealed HP box shows only HP and Intel logos; no model marking legible, and the seller's claimed ProBook 440 G10 is not in the shortlist and cannot be verified from the packaging.

Evidence flags: looks like a catalogue or stock image

## How sure the engine is (back office)
**0%: the photos do not say what this is.**

- Identification confidence: 0% (unknown)
- Price confidence: 14%
- Sealed HP box shows only HP and Intel logos; no model marking legible, and the seller's claimed ProBook 440 G10 is not in the shortlist and cannot be verified from the packaging.
- read off the item's own label
- 3 lines seen by both readers
- looks like a catalogue or stock image
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Take your own photo of the actual item you are selling.
   _why: this looks like a catalogue picture, not the real unit_
2. [VIDEO] Record one video, up to thirty seconds, in one take. Start by showing the whole item slowly from every side. Then hold the camera still and close for three seconds: Close-up of any label, sticker or metal plate showing the brand and model. Then, without stopping the video: If it opens without tools, open it and photograph the inside. Keep filming the whole time. Do not cut between clips.
   _why: two readings of these photos disagreed about what is written on the item_
3. [PHOTO] Close-up of any label, sticker or metal plate showing the brand and model.
   _why: nothing on the item says which model this is_

## What the seller is asked (only they know these)
- How much of it is there? Give the weight in kilogrammes or tons if you know it.
- Does it still work?
- Roughly how old is it, in years?

## Claims
- [unverifiable_remote] Hp probook 440 g10
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] intel core i7 13th gen (up to 5.0 ghz)
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 8gb ddr4 ram
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 512gb ssd
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 14.0’’
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] backlit
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
**230 to 1,512 NGN** (priced as material, width 1.4711, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 12 kg of paper 90%, plastic 10% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 768 NGN

Conditions attached to this price:
- Not identified: Sealed HP box shows only HP and Intel logos; no model marking legible, and the seller's claimed ProBook 440 G10 is not in the shortlist and cannot be verified from the packaging.
- Evidence flag: looks like a catalogue or stock image
- Hp probook 440 g10 -> not proven remotely. Weigh on the scale and photograph the display.
- intel core i7 13th gen (up to 5.0 ghz) -> not proven remotely. Weigh on the scale and photograph the display.
- 8gb ddr4 ram -> not proven remotely. Weigh on the scale and photograph the display.
- 512gb ssd -> not proven remotely. Weigh on the scale and photograph the display.
- 14.0’’ -> not proven remotely. Weigh on the scale and photograph the display.
- backlit -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'New Laptop HP ProBook 440 8GB Intel Core I7 SSD 512GB', 'category': 'laptop', 'price_ngn': 1065000, 'is_used': False, 'url': '/ikeja/computers-and-laptops/new-laptop-hp-probook-440-8gb-intel-core-i7-ssd-512gb-2VQbFRLrPvw1JvNxY8ZVPSwB.html?page=1&pos=19&cur_pos=19&ads_per_page=23&ads_count=32886&lid=TO3fbyjARcku0HMx'}`
