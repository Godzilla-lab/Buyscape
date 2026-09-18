# Case 8FfH1wMcRh8TGcM6OYk4ikOk

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: z-ai/glm-5.3-flash  |  cost: $0.0008  |  26360 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 10%
- Estimated weight: 85.0 kg (confidence 0.7)
- Brand read off the item: FIRMAN
- Model read off the item: SDG12000SE
- Rating read: none
- Label, plate or settings screen legible: yes
- Damage noted: minor scratches on yellow casing, dust and grime on surface, some wear on control panel bezel
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: FIRMAN | SDG12000SE | FIRMAN | SDG12000SE | Silent | CE | AVR

## Two readers
- brand_text agreed by both readers
- model_text agreed by both readers
- rating_text was seen by only one reader, so it is treated as unread
- 8 transcribed lines was seen by only one reader, so it is treated as unread

## OCR read off the photos
- AVR CE
- Silent
- FIRMAN
- SDG12000SE
- Dieselbene
- S0012000SE

## Chain
- **ocr** -> ok. 6 lines: AVR CE | Silent | FIRMAN | SDG12000SE | Dieselbene | S0012000SE
- **corroborate** -> dispute. brand_text agreed by both readers; model_text agreed by both readers; rating_text was seen by only one reader, so it is treated as unread; 8 transcribed lines was seen by only one reader, so it is treated as unread
- **read_evidence** -> ok. category=generator brand=FIRMAN model=SDG12000SE label=True lines=7
- **retrieval** -> ok. query='FIRMAN SDG12000SE FIRMAN SDG12000SE FIRMAN SDG12000SE Silent CE AVR Firman diesel generato' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Maxmech MX10000 10kVA', 'Kemage KM10000 10kVA', 'Sumec Firman ECO8990ES 6.5kVA']
- **identify** -> label. named from the label: FIRMAN SDG12000SE, not in the catalogue
- **abstain** -> pass. confidence=0.9 from the label

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.35)
  - Sumec Firman SPG3000 3.1kVA (0.25)
  - Maxmech MX10000 10kVA (0.2333)
  - Kemage KM10000 10kVA (0.2333)
  - Sumec Firman ECO8990ES 6.5kVA (0.15)

**Answer: FIRMAN SDG12000SE** (named from the item's own label; not in the catalogue)

## How sure the engine is (back office)
**90% sure this is a FIRMAN SDG12000SE.**

- Identification confidence: 90% (certain)
- Price confidence: 0%
- named from the item's own label, which the catalogue does not list
- read off the item's own label
- 7 lines seen by both readers
- 7 claims are still unproven, 0 are supported

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
- [unverified] Firman diesel generator 10kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% copper coin
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
**39,464 to 650,000 NGN** (priced as material, width 1.771, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4933 for unproven claims.

Scrap floor: 80,000 NGN

Conditions attached to this price:
- Firman diesel generator 10kva -> not proven remotely. Agent reads the rating plate.
- 100% copper coin -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Firman Diesel Generator 10kva 100% Copper Coin', 'category': 'generator', 'price_ngn': 1350000, 'is_used': False, 'url': '/ajah/power-equipments/firman-diesel-generator-10kva-100-copper-coin-8FfH1wMcRh8TGcM6OYk4ikOk.html?page=1&pos=11&cur_pos=11&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
