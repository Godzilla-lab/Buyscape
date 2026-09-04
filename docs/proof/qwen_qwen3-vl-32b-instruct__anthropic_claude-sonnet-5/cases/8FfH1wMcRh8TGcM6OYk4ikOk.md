# Case 8FfH1wMcRh8TGcM6OYk4ikOk

Photos: 1  |  reader: qwen/qwen3-vl-32b-instruct  |  reasoner: anthropic/claude-sonnet-5  |  cost: $0.0158  |  24350 ms

## What the engine saw
- Presentation: single_unit
- Category: generator (confidence 0.95)
- Made of: steel 60%, plastic 30%, circuit_board 5%, rubber 5%
- Estimated weight: 80.0 kg (confidence 0.7)
- Brand read off the item: FIRMAN
- Model read off the item: SDG12000SE
- Rating read: 12000W
- Label, plate or settings screen legible: yes
- Damage noted: minor scratches on casing, dust and dirt accumulation, some wear on control panel area
- Looks like a catalogue image: no
- Screenshot of a gallery: no
- Text read: FIRMAN | SDG12000SE | CHIGOLD ELECTRIC | FIRMAN | SDG12000SE | Silent | CE | 240V

## Chain
- **read_evidence** -> ok. category=generator brand=FIRMAN model=SDG12000SE label=True lines=11
- **retrieval** -> ok. query='FIRMAN SDG12000SE 12000W FIRMAN SDG12000SE CHIGOLD ELECTRIC FIRMAN SDG12000SE Silent CE 24' hits=['Sumec Firman SPG2900 2.8kVA', 'Sumec Firman SPG3000 3.1kVA', 'Maxmech MX10000 10kVA', 'Kemage KM10000 10kVA', 'Sumec Firman ECO8990ES 6.5kVA']
- **identify** -> ok. chosen=Firman SDG12000SE margin=0.9
- **abstain** -> pass. top=0.95 margin=0.9

## Identification
Shortlist from the catalogue:
  - Sumec Firman SPG2900 2.8kVA (0.35)
  - Sumec Firman SPG3000 3.1kVA (0.25)
  - Maxmech MX10000 10kVA (0.2333)
  - Kemage KM10000 10kVA (0.2333)
  - Sumec Firman ECO8990ES 6.5kVA (0.15)

**Answer: Firman SDG12000SE Diesel Generator, Silent** (margin 0.9)

## Claims
- [unverifiable_remote] Firman diesel generator
- [unverifiable_remote] Diesel generator
- [unverified] 10kva
    priced as: the smallest rating in this brand's range. Agent reads the rating plate
- [unverifiable_remote] 100% copper coin (coil)
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
**35,616 to 650,000 NGN** (priced as material, width 1.7922, method scrap_band_only, 0 comparable prices)

No usable comparable sales (0 found, 2 needed), so the range comes from the published Lagos buy band for this category, reduced by 0.4452 for unproven claims.

Scrap floor: 80,000 NGN

Conditions attached to this price:
- Firman diesel generator -> not proven remotely. Agent will confirm at pickup.
- Diesel generator -> not proven remotely. Agent will confirm at pickup.
- 10kva -> not proven remotely. Agent reads the rating plate.
- 100% copper coin (coil) -> not proven remotely. Agent opens the side cover and inspects the windings.
- Required evidence 'code_shot' was not supplied -> not proven remotely. Write the code {code} on paper and photograph it next to the generator..
- Required evidence 'overview' was not supplied -> not proven remotely. One photo of the whole generator from the front..
- Required evidence 'plate_kva' was not supplied -> not proven remotely. Close-up of the rating plate showing the kVA and model number..
- Required evidence 'side_cover_off' was not supplied -> not proven remotely. Open the side cover and photograph the alternator windings..
- Required evidence 'engine_bay' was not supplied -> not proven remotely. Photo of the engine, showing the recoil starter and carburettor..

## Answer key (not shown to the engine)
`{'title': 'Firman Diesel Generator 10kva 100% Copper Coin', 'category': 'generator', 'price_ngn': 1350000, 'is_used': False, 'url': '/ajah/power-equipments/firman-diesel-generator-10kva-100-copper-coin-8FfH1wMcRh8TGcM6OYk4ikOk.html?page=1&pos=11&cur_pos=11&ads_per_page=24&ads_count=15133&lid=Nxw8kf11TvNy7x_R'}`
