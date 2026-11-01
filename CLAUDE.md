# Buyscape

A tenant-agnostic remote-valuation engine for second-hand goods. Photos, clips,
screenshots and seller claims go in. Identification, evidence checks, a claims
ledger and a calibrated price range come out. BuyScrap Nigeria is tenant one.
The engine must onboard a second business by configuration alone.

## Current state

Phase 0, the offline proof. No server, no database, no API. The whole engine
runs from `buyscape run` over a cached test set and writes one markdown report
per case. Infrastructure starts only after the Phase 0 gate passes.

## The eight rules

1. **No per-category classifier.** Identification is a chain: read the item,
   retrieve candidates, rank them with the photos present, abstain by rule.
   Identity is a brand and model where the item carries one, and its type in
   a buyer's words ("2 seater sofa") where the protocol says
   `identity_by_type`: furniture, and anything with no protocol of its own.
   A sofa is never CANNOT_IDENTIFY for want of a model number.
2. **Protocols are data.** A new category is a YAML file in `protocols/`,
   never a code change.
3. **Claims ledger.** Every seller statement is tied to the evidence that would
   prove it. Unproven claims are priced at the worst case and listed as
   conditions on the quote. A lie can never raise the remote price.
4. **Price by retrieval, never by generation.** Numbers come from observations
   with a source and a date. The model explains, it never invents. When the
   used market is thin, dealers' new asking prices times the tenant's own
   `resale_fraction` is still retrieval; a model's "roughly 50,000" is not.
5. **Calibrated intervals.** Conformal calibration on settled prices once they
   exist. Until then the range is wide and says so.
6. **The human final price feeds back.** Every settlement is a calibration row.
7. **Fraud defence is structural**, not a detector: handwritten code in shot,
   perceptual hash dedup, serial cross-checks, seller trust score.
8. **Loud failures.** `CANNOT_IDENTIFY`, `NO_PRICE_DATA`, `EVIDENCE_INCOMPLETE`
   and `FRAUD_SUSPECTED` are first-class outputs. A silent wrong answer is the
   failure that killed the previous attempts at this product.

## Hidden interiors

Nothing sees through a case. Five layers instead: make the seller open it, let
the item testify through screenshots and serials, never pay for an unproven
claim, score seller trust, and have the agent open every compartment before
money moves. The promise is "nothing hidden gets priced", not "we see inside".

## Layout

    protocols/      evidence protocols, one YAML per category
    catalogue/      candidate catalogue, one CSV per category, seeded by hand
    tenants/        tenant config, price lists, and <tenant>.questions.yaml written from the office
    eval/raw/       cached Jiji test set, never re-fetched during a run
    eval/fixtures/  recorded model calls, replayed in tests and reruns
    sessions/       one folder per seller session from the web page, gitignored
    src/buyscape/ui the seller page, the back office and the bench, on stdlib http
    docs/proof/     case reports and the gate summary per model pair
    src/buyscape/   the engine
    src/buyscape/media  stills cut from seller clips, plain OpenCV, no model

## Commands

    uv run buyscape protocols                 validate every protocol
    uv run buyscape fetch-testset             refresh the cached test set
    uv run buyscape run --reader fake --reasoner fake --limit 8
    uv run buyscape run --reader qwen/qwen3-vl-32b-instruct \
                        --reasoner google/gemini-3.8-flash
    uv run buyscape run --preset balanced --budget-usd 0.5 stop once real spend hits the cap
    uv run buyscape fetch-buyscrap            cache the tenant's own adverts with photos
    uv run buyscape fetch-shops               new prices from the tenant's shops (Pointek, Slot, Jumia), for the share-of-new route
    uv run buyscape run --preset balanced --set buyscrap
    uv run buyscape spend                     every run's cost and the cost per item
    uv run buyscape testify-convert           build the Testify benchmark items, free
    uv run buyscape testify-fetch             cache Jiji small goods and material lots, from a home connection
    uv run buyscape testify-fetch --for-training --region kano   more cities as training data, never benchmark
    uv run buyscape testify-fetch --for-training --more-words --region lagos   also the makers and models the market names, for far more adverts
    uv run buyscape testify-label --market lagos --key-env GEMINI_API_1   check each item's photos, free tier
    uv run buyscape testify-construct         items with the plate taken away, and unpriceable photos, free
    uv run buyscape testify-truths            true claims a photo shows and their false twins, free
    uv run buyscape testify --model ... --split dev --variants clean,lie,truth,contra --condition witness_judge
    uv run buyscape testify --model nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b --split dev   score a model
    uv run buyscape testify-export --model human:ada --split dev --no-lies   a person sits the test at /office/testify
    uv run buyscape testify --model kaggle:google/gemini-3-flash-preview --split train --no-lies --reads-only   a teacher reads the training pool
    uv run buyscape testify-label --model kaggle:google/gemini-3.5-flash-lite --split train   the same photo check on the training pool
    uv run buyscape testify-judge --split dev --split test   judge the answers the word rules mark wrong, same thing in other words, free
    uv run buyscape testify-ocr               read every advert's photos once with the local OCR, free
    uv run buyscape testify-train-build       the fine-tuning set from those reads, never committed
    uv run buyscape testify-train-build --record-picks nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b   a teacher picks the price step first, free
    uv run buyscape ui                        seller page at /, back office at /office, staff questions at /office/questions, test bench at /bench
    uv run --group dev pytest

Keys live in `.env` and the run command loads it. Every run appends to
`docs/proof/spend.jsonl`. Replayed calls cost nothing and are not counted.

## Spending rules

- The default pair is Qwen3-VL-32B reading and GLM 5.3 Flash deciding, a
  thinking vision model at 7 cents in and 25 cents out per million tokens.
  `--preset gemini-free` is Gemini 3.8 Flash on the Google AI Studio free
  tier for when it is up. Sonnet and Opus are opt-in by preset name and never
  a default: on 4 Sep 2026 Sonnet 5 cost 1.6 cents an item.
- Never re-record what is already recorded. Replay first, pay only for the
  cases a prompt change actually invalidates.
- The default cap is 50 cents a run. Anything above that is asked for, with
  the estimated cost stated first.
- A local OCR engine (RapidOCR, `identify/ocr.py`) is a third witness for
  plate text: it confirms what one reader transcribed and never adds a fact
  of its own. It runs on the CPU, costs nothing and is never recorded.
- The reasoner is only called when there is something to rank. Three quarters
  of cases abstain and must cost nothing beyond the read.

`OPENROUTER_API_KEY` enables real model calls. Without it only recorded calls
replay, and the run says so rather than failing silently.

## Working rules

- **Never deploy without an explicit yes.** Draft deploys count as deploys.
- **No em dashes or en dashes in any shipped text**, code comments included.
- Anything tenant-specific belongs in `tenants/`, never in code. If onboarding a
  tenant needs a code change, that is a bug in the engine.
- The listing title in the test set is the answer key. It is never an input to
  the engine. Check this before trusting any accuracy number.
- Every price must carry a source and a date. If neither exists, return
  `NO_PRICE_DATA`.
- Jiji's search is literal and returns about twenty adverts per phrasing
  whatever the page number, so a type is asked for in every spelling the
  market uses (`MARKET_WORDS` in `pricing/sources.py`): "2 seater sofa",
  "2 seater couch", "2 seater sofa chair". Sets and titles carrying a number
  the type does not are not comparables for one piece.
