# Case white-shoe

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0226  |  23869 ms

## What the engine saw
- Presentation: single_unit
- Category: sneakers (confidence 0.95)
- Made of: textile 40%, plastic 30%, rubber 20%, steel 10%
- Estimated weight: 1.0 kg (confidence 0.8)
- Brand read off the item: Nike
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: 试穿请保留，折毁不退换 | 日常穿着时请移除此标签 | 3007.5

## Chain
- **read_evidence** -> ok. category=sneakers brand=Nike model=None label=True lines=3
- **retrieval** -> ok. query='Nike 试穿请保留，折毁不退换 日常穿着时请移除此标签 3007.5 Imported shoe available at a discount price.' hits=['Tecno Pova 5', 'Kemage KM6500 5.5kVA']
- **identify** -> refused. chosen=Nike None margin=None
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Tecno Pova 5 (0.2)
  - Kemage KM6500 5.5kVA (0.15)

**Not identified: CANNOT_IDENTIFY.** Image and text confirm brand 'Nike' (swoosh logo visible on tag) and shows a white low-top leather sneaker, but no model name/text (e.g. 'Air Force 1') is legible on the tag or shoe itself — only care instructions and a numeric code (3007.5) are readable. Neither shortlist entry (Tecno Pova 5, a phone; Kemage KM6500, a generator) matches this item at all, a shoe. Per rules, I cannot pick from an unrelated shortlist, and the brand alone is insufficient to state a specific model without visible text confirming it.

## Claims
- [unverifiable_remote] The item is a shoe.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The shoe is imported.
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**55 to 166 NGN** (priced as material, width 1.0013, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 1 kg of textile 40%, plastic 30%, rubber 20%, steel 10% (rates for plastic, rubber, textile are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 102 NGN

Conditions attached to this price:
- Not identified: Image and text confirm brand 'Nike' (swoosh logo visible on tag) and shows a white low-top leather sneaker, but no model name/text (e.g. 'Air Force 1') is legible on the tag or shoe itself — only care instructions and a numeric code (3007.5) are readable. Neither shortlist entry (Tecno Pova 5, a phone; Kemage KM6500, a generator) matches this item at all, a shoe. Per rules, I cannot pick from an unrelated shortlist, and the brand alone is insufficient to state a specific model without visible text confirming it.
- The item is a shoe. -> not proven remotely. Weigh on the scale and photograph the display.
- The shoe is imported. -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'White shoe', 'category': None, 'site_category': 'Premium', 'price_ngn': 50000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/white-shoe/'}`
