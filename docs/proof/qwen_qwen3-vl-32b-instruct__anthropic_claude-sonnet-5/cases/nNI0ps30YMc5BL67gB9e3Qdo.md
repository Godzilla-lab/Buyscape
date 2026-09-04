# Case nNI0ps30YMc5BL67gB9e3Qdo

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0152  |  18074 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: paper 90%, plastic 10%
- Estimated weight: 30.0 kg (confidence 0.7)
- Brand read off the item: BLUE STAR
- Model read off the item: BS-9FS
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: R Series - R410A Rotary Cool Only | SPLIT AIR CONDITIONER | BLUE STAR | BS-9FS

## Chain
- **read_evidence** -> ok. category=split air conditioner brand=BLUE STAR model=BS-9FS label=True lines=4
- **retrieval** -> ok. query='BLUE STAR BS-9FS R Series - R410A Rotary Cool Only SPLIT AIR CONDITIONER BLUE STAR BS-9FS ' hits=['Samsung AR09 1HP', 'Hisense AS-09 1HP', 'LG S4-Q09 1HP']
- **identify** -> ok. chosen=Blue Star BS-9FS margin=0.95
- **abstain** -> pass. top=0.95 margin=0.95

## Identification
Shortlist from the catalogue:
  - Samsung AR09 1HP (0.2333)
  - Hisense AS-09 1HP (0.2)
  - LG S4-Q09 1HP (0.2)

**Answer: Blue Star BS-9FS R Series R410A Rotary Cool Only Split AC** (margin 0.95)

## Claims
- [unverifiable_remote] Bluestar brand
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 1HP capacity
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Split AC type
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Basic model line
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Delivers reliable and efficient cooling
    priced as: assumed not working. Agent powers the item on before payment
- [unverifiable_remote] Designed to deliver fast cooling
    priced as: assumed not working. Agent powers the item on before payment
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**576 to 3,780 NGN** (priced as material, width 1.4711, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 1,920 NGN

Conditions attached to this price:
- Bluestar brand -> not proven remotely. Weigh on the scale and photograph the display.
- 1HP capacity -> not proven remotely. Weigh on the scale and photograph the display.
- Split AC type -> not proven remotely. Weigh on the scale and photograph the display.
- Basic model line -> not proven remotely. Weigh on the scale and photograph the display.
- Delivers reliable and efficient cooling -> not proven remotely. Agent powers the item on before payment.
- Designed to deliver fast cooling -> not proven remotely. Agent powers the item on before payment.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Bluestar 1hp Basic Split Air Conditioner | Bs-9fs (Hw09cryfb1-9fs)', 'category': 'split_ac', 'price_ngn': 285000, 'is_used': False, 'url': '/ikeja/home-appliances/bluestar-1hp-basic-split-air-conditioner-bs-9fs-hw09cryfb1-9fs-nNI0ps30YMc5BL67gB9e3Qdo.html?page=1&pos=13&cur_pos=13&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
