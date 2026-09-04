# Case lg-washing-machine-directdrive-7kg

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0200  |  30403 ms

## What the engine saw
- Presentation: single_unit
- Category: washing machine (confidence 1.0)
- Made of: steel 40%, plastic 50%, circuit_board 5%, rubber 5%
- Estimated weight: 65.0 kg (confidence 0.8)
- Brand read off the item: LG
- Model read off the item: F1486GDP2
- Rating read: 7kg
- Label, plate or settings screen legible: yes
- Damage noted: rust stains on lower front panel and near door seal, dirt and grime on exterior surface, some discoloration on plastic casing
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: LG | INVERTER | DirectDrive 7kg F1486GDP2 | Cotton Quick | Cotton | Hand Wash (Wool) | Synthetic | Blanket

## Chain
- **read_evidence** -> ok. category=washing machine brand=LG model=F1486GDP2 label=True lines=23
- **retrieval** -> ok. query='LG F1486GDP2 7kg LG INVERTER DirectDrive 7kg F1486GDP2 Cotton Quick Cotton Hand Wash (Wool' hits=['LG T2108 8kg top loader', 'LG T2312 12kg top loader', 'LG F2J5 7kg front loader', 'LG S4-Q09 1HP', 'LG S4-Q18 2HP']
- **identify** -> ok. chosen=LG F1486GDP2 margin=0.62
- **abstain** -> pass. top=0.97 margin=0.62

## Identification
Shortlist from the catalogue:
  - LG T2108 8kg top loader (0.4333)
  - LG T2312 12kg top loader (0.4333)
  - LG F2J5 7kg front loader (0.4333)
  - LG S4-Q09 1HP (0.4)
  - LG S4-Q18 2HP (0.4)

**Answer: LG F1486GDP2 DirectDrive 7kg Front Loader** (margin 0.62)

## Claims
- [unverifiable_remote] LG DirectDrive washing machine
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 7kg capacity
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
**8,495 to 34,775 NGN** (priced as material, width 1.2146, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3991 for unproven claims.

Scrap floor: 21,287 NGN

Conditions attached to this price:
- LG DirectDrive washing machine -> not proven remotely. Weigh on the scale and photograph the display.
- 7kg capacity -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'LG Washing Machine DirectDrive 7kg', 'category': None, 'site_category': 'E-waste', 'price_ngn': 70000, 'is_used': True, 'url': 'https://www.buyscrap.com.ng/lg-washing-machine-directdrive-7kg/'}`
