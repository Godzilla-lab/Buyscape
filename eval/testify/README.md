# Testify items

The benchmark set from `docs/research/testify-plan.md`. It is built for free from
data already on disk:

    uv run buyscape testify-convert

## What is here

| File | What |
|---|---|
| `items.jsonl` | One item per line: links, seller claims, answer key, hidden-risk seeds, and every recorded model pair's verdict |
| `labels.yaml` | Hand labels for the BuyScrap adverts: tier, protocol and the item in a buyer's words |
| `train_pool.jsonl` | Training data, never benchmark: dealers' brand new adverts, for teaching a model to name an item. Split `train` |

## Rules for this folder

- **Links and labels only.** Photos stay in `eval/raw/`, which is gitignored,
  and every item has `photos.public: false`.
- **No contact details.** Phone numbers and emails in seller text are
  replaced with `[phone]` and `[email]`. A test fails if one gets through.
- **The title is the answer key.** It sits under `answer` and never in the inputs.
- **Every price says what kind it is**: `asking`, `sold`, `settled` or
  `wanted`. Today every price is an asking price.
- **Risk seeds are drafts.** They come from the category protocol's claims and
  carry `reviewed: false` until a person checks them.
- **The split is fixed by a hash of the id.** About a quarter of the items
  are `dev`, so a rerun never moves an item between splits.

## Where items come from

| Source | Count | How |
|---|---|---|
| Jiji, 6 branded categories | 178 | Rebuilt from the case reports in `docs/proof` |
| BuyScrap, the tenant's own site | 56 | `uv run buyscape fetch-buyscrap` |
| Jiji, small goods and material lots, second-hand only | 207 | `uv run buyscape testify-fetch`, run from an ordinary connection |

`uv run buyscape testify-fetch --new-stock` fills the training pool: the same
52 kinds, brand new adverts only, one photo each. The two pools never share an
advert: the benchmark takes second-hand only, the pool takes new only, and
`testify-convert` drops any pool item whose id is in the benchmark.

Jiji answers cloud machines with a bot check. `testify-fetch` says so rather
than failing silently. Run it from a home or office connection, the same way
`fetch-testset` has always been run. It covers 52 kinds of item, from
torchlights and tokunbo gearboxes to okrika bales and PET bottles.
