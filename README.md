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

## Licence

The code is under the Apache License 2.0 (`LICENSE`). The Testify labels,
lies, schema and scores are released under CC BY 4.0 on Hugging Face. The
adverts they point to belong to their sellers and the sites that host them,
and are not covered by either licence.
