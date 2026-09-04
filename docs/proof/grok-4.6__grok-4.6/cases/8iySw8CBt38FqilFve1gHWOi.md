# Case 8iySw8CBt38FqilFve1gHWOi

Photos: 1  |  reader: grok-4.6  |  reasoner: grok-4.6  |  cost: $0.0142  |  95740 ms

## What the engine saw
- Presentation: sealed_new
- Category: washing machine (confidence 0.95)
- Made of: plastic 55%, steel 25%, stainless 10%, copper 5%, rubber 5%
- Estimated weight: 15.0 kg (confidence 0.4)
- Brand read off the item: Boscon
- Model read off the item: BOS-WM70S
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: WASHING MACHINE | Boscon | Make your life more comfortable! | MODEL NO.: BOS-WM70S | Make your washing simply easy | POSTED ON JIJI | KITCHEN PLUG | JAPAN

## Chain
- **read_evidence** -> ok. category=washing machine brand=Boscon model=BOS-WM70S label=True lines=9
- **retrieval** -> ok. query='Boscon BOS-WM70S WASHING MACHINE Boscon Make your life more comfortable! MODEL NO.: BOS-WM' hits=['Haier Thermocool TLA70 7kg top loader']
- **identify** -> ok. chosen=Boscon BOS-WM70S margin=None
- **abstain** -> pass. top=0.98 margin=None

## Identification
Shortlist from the catalogue:
  - Haier Thermocool TLA70 7kg top loader (0.1667)

**Answer: Boscon BOS-WM70S** (margin None)

## Claims
- [unverifiable_remote] Boscon single-tub washing machine
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] model BOS-WM70S
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] 7kg washing capacity
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
**3,431 to 15,060 NGN** (priced as material, width 1.2578, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3 for unproven claims.

Scrap floor: 11,437 NGN

Conditions attached to this price:
- Boscon single-tub washing machine -> not proven remotely. Weigh on the scale and photograph the display.
- model BOS-WM70S -> not proven remotely. Weigh on the scale and photograph the display.
- 7kg washing capacity -> not proven remotely. Weigh on the scale and photograph the display.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Single Tub Washing Machine 7kg Capacity. 『 Only Wash 』', 'category': 'washing_machine', 'price_ngn': 135000, 'is_used': False, 'url': '/lagos-island-west/home-appliances/single-tub-washing-machine-7kg-capacity-only-wash-8iySw8CBt38FqilFve1gHWOi.html?page=1&pos=15&cur_pos=15&ads_per_page=20&ads_count=16335&lid=_UmGsiyCR3i1GHB4'}`
