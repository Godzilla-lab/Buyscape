# Case 6xt35N67xaVwSgpAPFeJQadk

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0156  |  24986 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.95)
- Made of: plastic 40%, steel 30%, copper 15%, paper 15%
- Estimated weight: 25.0 kg (confidence 0.7)
- Brand read off the item: Hisense
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: Hisense | AIR CONDITIONER | Outdoor Units | Hisense | Outdoor Unit

## Chain
- **read_evidence** -> ok. category=split air conditioner brand=Hisense model=None label=True lines=5
- **retrieval** -> ok. query='Hisense Hisense AIR CONDITIONER Outdoor Units Hisense Outdoor Unit The Hisense AS09DK Air ' hits=['Hisense AS-09 1HP', 'Hisense AS-12 1.5HP', 'Hisense AS-18 2HP']
- **identify** -> ok. chosen=Hisense AS-09 1HP margin=0.55
- **abstain** -> pass. top=0.7 margin=0.55

## Identification
Shortlist from the catalogue:
  - Hisense AS-09 1HP (0.4)
  - Hisense AS-12 1.5HP (0.38)
  - Hisense AS-18 2HP (0.38)

**Answer: Hisense AS-09 1HP AS09DK** (margin 0.55)

## Claims
- [unverifiable_remote] The item is a Hisense AS09DK Air Conditioner
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Designed to deliver powerful and consistent cooling
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] Suitable for small (rooms/spaces)
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
**12,742 to 55,500 NGN** (priced as material, width 1.2531, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 42,475 NGN

Conditions attached to this price:
- The item is a Hisense AS09DK Air Conditioner -> not proven remotely. Weigh on the scale and photograph the display.
- Designed to deliver powerful and consistent cooling -> not proven remotely. Weigh on the scale and photograph the display.
- Suitable for small (rooms/spaces) -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Hisense 1hp Split Air Conditioner – Powerful Cooling Performance', 'category': 'split_ac', 'price_ngn': 355000, 'is_used': False, 'url': '/ajah/home-appliances/hisense-1hp-split-air-conditioner-powerful-cooling-performance-6xt35N67xaVwSgpAPFeJQadk.html?page=1&pos=9&cur_pos=9&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
