# Buyscape

Remote valuation for second-hand goods. Send photos and a description, get back
what the item is, which claims the evidence supports, and a price range with the
conditions attached to it.

Built tenant-agnostic from the start. BuyScrap Nigeria is the first tenant:
Lagos scrap, appliances, generators and phones.

## Why this is hard, and what is different here

Earlier attempts at photo-based valuation failed in four ways. Quotes were cut
by a third at the doorstep, so sellers stopped trusting them. Models guessed
instead of admitting they could not tell. Identification was attempted from the
photo alone, which published work puts at 13 percent on fine-grained identity.
And the risk was pushed onto expensive hardware that never paid back.

Buyscape answers each one. Unproven claims are priced at the worst case up
front, so the pickup price can only hold or improve. Abstention is a rule
outside the model, not a request to it. The model ranks a retrieved shortlist
rather than answering alone. And the only hardware is a phone and a scale.

## Status

Phase 0: proving the pipeline on real listings before any infrastructure is
built. See `CLAUDE.md` for commands and `docs/proof/` for case reports.

**Testify**, the benchmark that grew out of it, is public on Hugging Face at
[godzilla1215/testify](https://huggingface.co/datasets/godzilla1215/testify):
910 second-hand adverts from Lagos, Abuja, Rivers and Oyo, checked photo by
photo, released as links and labels only. It scores what costs a buyer money:
pricing the wrong item, believing a claim no photo proves, offering above the
asking price, and changing the answer when asked again.

On its 679-item test split, a fine-tuned Qwen3-VL 2B small enough for one
modest GPU loses about 3,900 naira per item, against 7,415 for Claude Sonnet
5 and 55,602 for Nemotron 3.5 Super, while naming the item right 95% of the
time (Claude 99%).

**The market data**, every advert collected (15,000 and more, 29 places, with
prices, conditions and labels), is on Kaggle as links and labels at
[godzilla1215/buyscape-market-data-public](https://www.kaggle.com/datasets/godzilla1215/buyscape-market-data-public).
Jiji adverts are used with the permission of Jiji Nigeria, granted on
4 Nov 2026.

The research behind it is in `docs/research/`:

- `testify-plan.md`: what the benchmark measures and why;
- `testify-baseline-1.md` to `testify-baseline-3.md`: the first baselines, city by city;
- `fine-tuning-research.md` and `learning-loop-plan.md`: the training recipe and how settled prices feed back;
- `testify-step5.md`: the new tests and all seven training runs, with what each changed and what it cost;
- `failure-analysis.md`, `data-sources.md`, `collection-plan.md`: what the engine gets wrong and where the data comes from.

## Licence

The code is under the Apache License 2.0 (`LICENSE`). The Testify labels,
lies, schema and scores are released under CC BY 4.0 on Hugging Face. The
adverts they point to belong to their sellers and the sites that host them,
and are not covered by either licence.
