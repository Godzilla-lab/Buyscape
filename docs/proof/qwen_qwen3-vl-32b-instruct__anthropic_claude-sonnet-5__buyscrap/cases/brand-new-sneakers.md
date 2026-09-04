# Case brand-new-sneakers

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0093  |  15795 ms

## What the engine saw
- Presentation: single_unit
- Category: sneakers (confidence 0.95)
- Made of: plastic 40%, textile 30%, rubber 20%, steel 10%
- Estimated weight: 1.2 kg (confidence 0.8)
- Brand read off the item: PRIMA
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: slight scuffing on toe caps, laces slightly untied, small stain on right shoe tongue
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: PRIMA | 37 | MADE IN CHINA

## Chain
- **read_evidence** -> ok. category=sneakers brand=PRIMA model=None label=True lines=3
- **retrieval** -> ok. query='PRIMA PRIMA 37 MADE IN CHINA Brand new sneakers are available for sale. Location: Agege, L' hits=['Tecno Camon 40', 'Tecno Spark 40', 'Infinix Hot 40', 'Infinix Note 40']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Tecno Camon 40 (0.2)
  - Tecno Spark 40 (0.2)
  - Infinix Hot 40 (0.2)
  - Infinix Note 40 (0.2)

**Not identified: CANNOT_IDENTIFY.** The item is a pair of PRIMA-branded sneakers (shoes), as shown by the photos and the 'PRIMA' text legible on the insole/label, and confirmed by the seller's description. The catalogue shortlist only contains smartphone models (Tecno and Infinix phones), none of which match a shoe product. There is no valid match between the physical item and any shortlist candidate.

## Claims
- [unverifiable_remote] Brand new sneakers
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on a piece of paper and take one photo with the paper next to the item.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo showing the whole item.
- [unverified] Required evidence 'label_or_plate' was not supplied
    priced as: priced as if the worst case is true. Close-up of any label, sticker or metal plate showing the brand and model.
- [unverified] Required evidence 'description' was not supplied
    priced as: priced as if the worst case is true. Tell us what it is, whether it works, and roughly how heavy it is.

## Price
**101 to 211 NGN** (priced as material, width 0.7041, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 1.2 kg of plastic 40%, textile 30%, rubber 20%, steel 10% (rates for plastic, rubber, textile are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 130 NGN

Conditions attached to this price:
- Not identified: The item is a pair of PRIMA-branded sneakers (shoes), as shown by the photos and the 'PRIMA' text legible on the insole/label, and confirmed by the seller's description. The catalogue shortlist only contains smartphone models (Tecno and Infinix phones), none of which match a shoe product. There is no valid match between the physical item and any shortlist candidate.
- Brand new sneakers -> not proven remotely. Agent will confirm at pickup.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Brand new sneakers', 'category': None, 'site_category': 'Premium', 'price_ngn': 40000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/brand-new-sneakers/'}`
