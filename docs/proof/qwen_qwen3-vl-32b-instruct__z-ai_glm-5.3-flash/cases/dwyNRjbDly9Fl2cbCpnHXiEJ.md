# Case dwyNRjbDly9Fl2cbCpnHXiEJ

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0015  |  59967 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 5%, rubber 5%
- Estimated weight: 25.0 kg (confidence 0.8)
- Brand read off the item: nothing legible
- Model read off the item: nothing legible
- Rating read: E33KWH
- Label, plate or settings screen legible: yes
- Damage noted: some dust and minor surface wear, no visible cracks or dents
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: SUMEC | LUTIAN | E33KWH

## Two readers
- item_type agreed by both readers
- rating_text was read by one reader and confirmed by OCR
- brand_text differed between the two readers, so it is treated as unread
- model_text differed between the two readers, so it is treated as unread
- 1 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- SUMEC
- MAXI>
- POUTADLE GENERATON
- E33KWH
- WERLH
- OR
- oro
- S10ET

## Chain
- **ocr** -> ok. 8 lines: SUMEC | MAXI> | POUTADLE GENERATON | E33KWH | WERLH | OR | oro | S10ET
- **corroborate** -> dispute. item_type agreed by both readers; rating_text was read by one reader and confirmed by OCR; brand_text differed between the two readers, so it is treated as unread; model_text differed between the two readers, so it is treated as unread; 1 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=None model=None label=True lines=3
- **retrieval** -> ok. query='E33KWH SUMEC LUTIAN E33KWH 5kva maxi petrol generator set 
100% pure copper coil 
Key star' hits=['Lutian LT3900 3.5kVA', 'Thermocool TC2700 2.5kVA', 'Haier Thermocool HTG2700 2.5kVA', 'Sumec Firman SPG2900 2.8kVA', 'Sumec Firman ECO8990ES 6.5kVA']
- **identify** -> ok. chosen=Maxi E33KWH margin=0.55
- **abstain** -> pass. confidence=0.7 margin=0.55

## Timing
- read_evidence on qwen/qwen3-vl-32b-instruct: 5727 ms (replayed)
- read_evidence on mistralai/mistral-small-3.2-24b-instruct: 9021 ms (replayed)
- identify on z-ai/glm-5.3-flash: 41148 ms (replayed)
- extract_claims on qwen/qwen3-vl-32b-instruct: 4071 ms (replayed)
- total across calls: 59967 ms; wall clock: 1519 ms

## Identification
Shortlist from the catalogue:
  - Lutian LT3900 3.5kVA (0.55)
  - Thermocool TC2700 2.5kVA (0.2333)
  - Haier Thermocool HTG2700 2.5kVA (0.2333)
  - Sumec Firman SPG2900 2.8kVA (0.2)
  - Sumec Firman ECO8990ES 6.5kVA (0.2)

**Answer: Maxi E33KWH** (margin 0.55)

## How sure the engine is (back office)
**70% sure this is a Maxi E33KWH.**

- Identification confidence: 70% (likely)
- Price confidence: 0%
- It is weighing: Maxi E33KWH (0.7), Lutian LT3900 (0.15), Sumec Firman SPG2900 (0.05)
- read off the item's own label
- 2 lines seen by both readers
- 10 claims are still unproven, 0 are supported

These are stated strengths from the evidence, not calibrated probabilities. They become calibrated once settled pickup prices exist.

## What the seller is asked for next (shown in the app)
1. [PHOTO] Write the code {code} on paper and photograph it next to the generator.
   _why: this is needed before the price can be confirmed_
2. [PHOTO] One photo of the whole generator from the front.
   _why: this is needed before the price can be confirmed_
3. [PHOTO] Close-up of the rating plate showing the kVA and model number.
   _why: this is needed before the price can be confirmed_

## What the seller is asked (only they know these)
- Roughly how old is it, in years?
- Does it start and run right now?
- When was it last serviced, and what was done?

## Claims
- [unverified] 5kva maxi petrol generator set
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% pure copper coil
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverifiable_remote] Key start
- [unverifiable_remote] 15ltrs petrol tank
- [unverifiable_remote] 2.5mm copper
    priced as: assumed aluminium windings. Agent opens the side cover and inspects the windings
- [unverified] Required evidence 'code_shot' was not supplied
    priced as: priced as if the worst case is true. Write the code {code} on paper and photograph it next to the generator.
- [unverified] Required evidence 'overview' was not supplied
    priced as: priced as if the worst case is true. One photo of the whole generator from the front.
- [unverified] Required evidence 'plate_kva' was not supplied
    priced as: priced as if the worst case is true. Close-up of the rating plate showing the kVA and model number.
- [unverified] Required evidence 'side_cover_off' was not supplied
    priced as: priced as if the worst case is true. Open the side cover and photograph the alternator windings.
- [unverified] Required evidence 'engine_bay' was not supplied
    priced as: priced as if the worst case is true. Photo of the engine, showing the recoil starter and carburettor.

## Price
**10,017 to 80,000 NGN** (priced as material, width 1.5549, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.3339 for unproven claims.

Scrap floor: 30,000 NGN

Conditions attached to this price:
- 5kva maxi petrol generator set -> not proven remotely. Agent reads the rating plate.
- 100% pure copper coil -> not proven remotely. Agent opens the side cover and inspects the windings.
- Key start -> not proven remotely. Agent will confirm at pickup.
- 15ltrs petrol tank -> not proven remotely. Agent will confirm at pickup.
- 2.5mm copper -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': '5kva Maxi Petrol Generator Set 100% Copper Coil', 'category': 'generator', 'price_ngn': 470000, 'is_used': False, 'url': '/ajah/power-equipments/5kva-maxi-petrol-generator-set-100-copper-coil-dwyNRjbDly9Fl2cbCpnHXiEJ.html?page=3&pos=1&cur_pos=1&ads_per_page=24&ads_count=15133&lid=w4bgywJfSACOHKND'}`
