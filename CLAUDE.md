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
2. **Protocols are data.** A new category is a YAML file in `protocols/`,
   never a code change.
3. **Claims ledger.** Every seller statement is tied to the evidence that would
   prove it. Unproven claims are priced at the worst case and listed as
   conditions on the quote. A lie can never raise the remote price.
4. **Price by retrieval, never by generation.** Numbers come from observations
   with a source and a date. The model explains, it never invents.
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
    tenants/        tenant config and price lists
    eval/raw/       cached Jiji test set, never re-fetched during a run
    eval/fixtures/  recorded model calls, replayed in tests and reruns
    docs/proof/     case reports and the gate summary per model pair
    src/buyscape/   the engine

## Commands

    uv run buyscape protocols                 validate every protocol
    uv run buyscape fetch-testset             refresh the cached test set
    uv run buyscape run --reader fake --reasoner fake --limit 8
    uv run buyscape run --reader qwen/qwen3-vl-32b-instruct \
                        --reasoner google/gemini-3.8-flash
    uv run --group dev pytest

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
