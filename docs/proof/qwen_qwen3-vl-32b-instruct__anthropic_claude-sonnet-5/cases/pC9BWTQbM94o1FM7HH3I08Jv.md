# Case pC9BWTQbM94o1FM7HH3I08Jv

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0106  |  14554 ms

## What the engine saw
- Presentation: sealed_new
- Category: smartphone (confidence 0.95)
- Made of: paper 80%, plastic 20%
- Estimated weight: 0.5 kg (confidence 0.9)
- Brand read off the item: SAMSUNG
- Model read off the item: S20+ 5G
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: box appears slightly scuffed and creased
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SAMSUNG | Galaxy S20 | S20+ 5G

## Chain
- **read_evidence** -> ok. category=smartphone brand=SAMSUNG model=S20+ 5G label=True lines=3
- **retrieval** -> ok. query='SAMSUNG S20+ 5G SAMSUNG Galaxy S20 S20+ 5G Samsung galaxy S20 plus 5G 256GB available for ' hits=['Samsung Galaxy S21', 'Samsung Galaxy S22', 'Samsung Galaxy S23', 'Samsung Galaxy S24', 'Samsung Galaxy S25']
- **identify** -> ok. chosen=Samsung Galaxy S20+ margin=0.9
- **abstain** -> pass. top=0.95 margin=0.9

## Identification
Shortlist from the catalogue:
  - Samsung Galaxy S21 (0.5)
  - Samsung Galaxy S22 (0.5)
  - Samsung Galaxy S23 (0.5)
  - Samsung Galaxy S24 (0.5)
  - Samsung Galaxy S25 (0.5)

**Answer: Samsung Galaxy S20+ 5G** (margin 0.9)

## Claims
- [unverifiable_remote] Samsung Galaxy S20 Plus 5G
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 256GB storage capacity
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
**13 to 66 NGN** (priced as material, width 1.3178, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3991 for unproven claims.

Scrap floor: 34 NGN

Conditions attached to this price:
- Samsung Galaxy S20 Plus 5G -> not proven remotely. Weigh on the scale and photograph the display.
- 256GB storage capacity -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'New Samsung Galaxy S20+ 5G 256 GB Black', 'category': 'phone', 'price_ngn': 270000, 'is_used': False, 'url': '/ikeja/mobile-phones/new-samsung-galaxy-s20-5g-256-gb-black-pC9BWTQbM94o1FM7HH3I08Jv.html?page=1&pos=7&cur_pos=7&ads_per_page=24&ads_count=17061&lid=s6u6iV4wdGHElRC1'}`
