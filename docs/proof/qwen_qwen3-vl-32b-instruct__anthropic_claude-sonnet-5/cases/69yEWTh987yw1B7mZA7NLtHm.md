# Case 69yEWTh987yw1B7mZA7NLtHm

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0141  |  20759 ms

## What the engine saw
- Presentation: sealed_new
- Category: split air conditioner (confidence 0.9)
- Made of: paper 90%, plastic 10%
- Estimated weight: 15.0 kg (confidence 0.7)
- Brand read off the item: MAJESTIC
- Model read off the item: nothing legible
- Rating read: none
- Label, plate or settings screen legible: no
- Damage noted: none
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: INVERTER AIR CONDITIONER | INDOOR UNIT | MAJESTIC INVERTER | OUTDOOR UNIT | INVERTER AIR CONDITIONER | MAJESTIC INVERTER | POSTED ON | STEVEN RB

## Chain
- **read_evidence** -> ok. category=split air conditioner brand=MAJESTIC model=None label=False lines=8
- **retrieval** -> ok. query='MAJESTIC INVERTER AIR CONDITIONER INDOOR UNIT MAJESTIC INVERTER OUTDOOR UNIT INVERTER AIR ' hits=['Samsung AR12 1.5HP', 'Scanfrost SFAC12 1.5HP', 'Royal RAC12 1.5HP', 'Hisense AS-12 1.5HP', 'LG S4-Q12 1.5HP']
- **identify** -> refused. chosen=None None margin=None
- **abstain** -> abstain. model refused

## Identification
Shortlist from the catalogue:
  - Samsung AR12 1.5HP (0.3)
  - Scanfrost SFAC12 1.5HP (0.3)
  - Royal RAC12 1.5HP (0.3)
  - Hisense AS-12 1.5HP (0.26)
  - LG S4-Q12 1.5HP (0.26)

**Not identified: CANNOT_IDENTIFY.** The box clearly reads 'MAXI' (or 'MAJESTIC' per OCR) Inverter Air Conditioner, not any brand in the shortlist (Samsung, Scanfrost, Royal, Hisense, LG). No model number or nameplate is legible, and none of the shortlist entries match the visible brand text, so no catalogue match can be supported by the evidence.

## Claims
- [unverifiable_remote] The item is a Maxi brand air conditioner.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] It is a 1.5hp unit.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] It is an inverter type air conditioner.
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] It is a split system air conditioner (indoor and outdoor units).
    priced as: 70 percent of the stated weight. Weigh on the scale and photograph the display
- [unverifiable_remote] The unit provides efficient cooling.
    priced as: assumed not working. Agent powers the item on before payment
- [unverifiable_remote] The unit provides consistent cooling.
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
**288 to 1,890 NGN** (priced as material, width 1.4711, method material_floor, 0 comparable prices)

This item was not identified, so it is priced as material rather than as a working item: 15 kg of paper 90%, plastic 10% (rates for paper, plastic are estimates, not published). Anything it is worth above scrap needs a clearer photo of its label or plate. The weight is an estimate from the photos and the price is settled on the scale at pickup.

Scrap floor: 960 NGN

Conditions attached to this price:
- Not identified: The box clearly reads 'MAXI' (or 'MAJESTIC' per OCR) Inverter Air Conditioner, not any brand in the shortlist (Samsung, Scanfrost, Royal, Hisense, LG). No model number or nameplate is legible, and none of the shortlist entries match the visible brand text, so no catalogue match can be supported by the evidence.
- The item is a Maxi brand air conditioner. -> not proven remotely. Weigh on the scale and photograph the display.
- It is a 1.5hp unit. -> not proven remotely. Weigh on the scale and photograph the display.
- It is an inverter type air conditioner. -> not proven remotely. Weigh on the scale and photograph the display.
- It is a split system air conditioner (indoor and outdoor units). -> not proven remotely. Weigh on the scale and photograph the display.
- The unit provides efficient cooling. -> not proven remotely. Agent powers the item on before payment.
- The unit provides consistent cooling. -> not proven remotely. Agent powers the item on before payment.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on a piece of paper and take one photo with the paper next to the item..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo showing the whole item..
- Required evidence 'label_or_plate' was not supplied -> not proven remotely. Close-up of any label, sticker or metal plate showing the brand and model..
- Required evidence 'description' was not supplied -> not proven remotely. Tell us what it is, whether it works, and roughly how heavy it is..

## Answer key (not shown to the engine)
`{'title': 'Maxi 1.5hp Inverter Split Air Conditioner', 'category': 'split_ac', 'price_ngn': 360000, 'is_used': False, 'url': '/ikeja/home-appliances/maxi-1-5hp-inverter-split-air-conditioner-69yEWTh987yw1B7mZA7NLtHm.html?page=1&pos=11&cur_pos=11&ads_per_page=19&ads_count=5405&lid=RifBWYhUFF4e2Jt3'}`
