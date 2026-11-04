# The learning loop: an open valuation system that gets better with use

## In one paragraph

Anyone who buys second-hand goods, a scrap dealer in Ikeja or a phone
trade-in desk, should be able to run Buyscape on their own website or
WhatsApp number. A seller sends photos and gets an offer. Staff go to the
pickup, find the real price, and type it into the back office. Today that
price is saved and then forgotten. This plan makes every saved price teach
the system: the next similar item is priced from it the same day, the range
narrows as prices pile up, and the reading model is retrained on what staff
corrected. The more a business uses it, the better it prices for that
business.

## The example that drives the design

The system quotes 2,000 naira for a bag of copper offcuts. At the pickup the
agent finds clean bright copper, weighs it and pays 20,000. On the back
office the agent types 20,000 and picks a reason: "the photos made it look
dirtier than it was".

What should happen next:

1. **Today:** the next seller with copper offcuts in that city is priced
   with this 20,000 as a dated, sourced observation, alongside the market
   prices. No retraining, no waiting.
2. **This month:** once a few dozen copper settlements exist, the range for
   copper is set from how far quotes have missed settled prices, so it says
   honestly how sure it is.
3. **Next retrain:** the photos, what the agent found and the reason become
   a training example, so the reading model learns that this look is clean
   copper.

The model still never writes a price (rule 4). It learns to read better.
The price improves because the system has better observations to retrieve
and a better measure of its own error.

## What already exists

| Piece | Where | State |
|---|---|---|
| Seller page: photos, protocol questions, offer | `ui/seller.html`, `POST /api/sessions` | Works |
| Back office with a Settle button | `ui/office.html`, `POST /api/office/sessions/<id>/settle` | Works, behind a staff token |
| Every settlement saved as a row | `UiStore.settle` in `ui/sessions.py`, writes `sessions/settlements.jsonl` | Works |
| Off-machine backup of sessions and settlements | `ui/archive.py`, a private Hugging Face dataset | Works |
| An observation type for settled prices | `Observation(kind="settled")` in `pricing/sources.py` | Defined, never filled |
| Tenant config, price lists, protocols as data | `tenants/`, `protocols/` | Works; a second tenant needs no code |
| One-box deploy | `Dockerfile` | Builds; never deployed without a yes |
| Benchmark to test any new model | Testify, `buyscape testify` | Works |

What is missing is everything that reads `settlements.jsonl` back. Nothing
does today.

## The four layers of learning

Each layer works on its own and is useful with very little data. They are
built in this order.

### Layer 1: a settled price is the best comparable (same day)

- On settle, the row becomes an `Observation` with `kind="settled"`, the
  source `settlement:<tenant>:<session id>`, the date it was paid, the
  category, and the identity the agent confirmed.
- Retrieval looks at the tenant's own settlements first, then the market
  adverts. A settled price is a sold price, so it does not get the
  asking-to-buying discount (`ASK_TO_BUY`) that adverts get.
- Old settlements count less, and stop counting after a set age per
  category in the tenant file (`settled_max_age_days`), because Nigerian
  prices move fast.
- One settlement cannot move a quote alone: it joins the median with the
  rest. An outlier waits for a second staff member to confirm it (see
  Guards).
- `ASK_TO_BUY` and `resale_fraction` are corrected per category from the
  ratio of settled price to asking price, once a category has 20 or more
  settlements. The engine comment already promises this.

### Layer 2: staff say what the item really was

The Settle form grows three fields, all optional except the reason when the
price differs a lot:

- **What it really was:** kind, brand, model, as the agent saw it in hand.
- **What we found:** works, faulty, parts missing, heavier or lighter than
  said, cleaner or dirtier than it looked.
- **Why the price differed:** wrong item, hidden fault, seller's claim was
  false, the photos misled us, the market moved, the quote was simply off.

That turns each settlement into a labelled error. A wrong-item settlement
adds a row to `catalogue/`. A "seller's claim was false" settlement lowers
the seller's trust score (rule 7). A "photos misled us" settlement is the
best training example there is.

### Layer 3: honest ranges (rule 5)

- Per category, once it has 30 settlements, the range is set by split
  conformal calibration on the ratio of settled price to the quote's
  middle. Below 30 the range stays wide and says so, as it does now.
- The back office shows the coverage: of the last 50 settled items, how
  many fell inside their quoted range. It should match the stated level.
- Settlements also become the settled-price labels Testify is missing (its
  card's first limit), with the tenant's consent.

### Layer 4: the reading model is retrained, and must earn its place

- Every N settlements (start with 500), export the settled sessions as
  training examples: photos, the seller's words, and a target read that
  uses the agent's confirmed identity and findings. The price is never a
  target.
- Retrain the small open model from the fine-tuning plan
  (`docs/research/fine-tuning-research.md`) on these plus the earlier
  training set.
- **It ships only if it wins** on both Testify `dev` and the newest 20% of
  settlements it was not trained on: no rise in silent wrong answers, no
  lie effect beyond noise, and better identity accuracy. Otherwise the
  current model stays and the report says why.
- Each tenant file names the model it runs (`model_key`), so going back is
  one line.

## Guards

| Risk | Guard |
|---|---|
| A seller types a price to raise their own offer | Only staff with the office token can settle. The seller never touches it |
| A typing slip (2,000,000 for 20,000) | A settlement more than 5 times or less than a fifth of the quote needs a reason, and waits for a second staff member before it enters retrieval |
| A dishonest staff member | Every settlement records who entered it. The back office shows each person's settled-to-quote pattern |
| A wrong row cannot be taken back | Settlements are only added, never edited. A mistake is a new row that voids the old one, with a reason |
| One business's prices leak to another | Each tenant's settlements stay its own. Sharing into a common pool is a tenant setting, off by default |
| Faces, phone numbers, homes in photos | Training export blurs faces and drops phone numbers and full serials, as the Testify release already checks |
| The model learns to please, not to be right | Layer 4's gate is a fixed benchmark plus held-out settlements, not the latest week's feedback |
| A lie raises the price | The claims ledger stays: unproven claims are priced at worst case before any learned number is used |

## Making it usable by anyone

1. **A licence.** The repo has none yet, so nobody may legally reuse the
   code. Apache 2.0 is the usual choice for code a company would build on.
   The Testify data is already CC BY 4.0. This is the owner's decision.
2. **One command to run.** `docker run` with a tenant file and a staff token
   mounted. A short guide: write `tenants/<you>.yaml`, add price lists, start
   the box. Onboarding needing code is a bug (CLAUDE.md).
3. **A documented API.** The routes exist; they need versioned paths
   (`/api/v1/...`), a key per tenant, and an OpenAPI file:
   - `POST /api/v1/sessions` start a session
   - `POST /api/v1/sessions/<id>/photos` add photos
   - `POST /api/v1/sessions/<id>/submit` get the offer, or the proof still needed
   - `POST /api/v1/sessions/<id>/settle` staff enter the real price and findings
   - `GET /api/v1/settlements` export a tenant's own settlements
4. **A website widget.** One script tag on a shop's page opens the seller
   page in a panel, with the tenant's name and colours from its file.
5. **A WhatsApp adapter.** A webhook for the WhatsApp Business Cloud API.
   Photos in, the protocol's questions out as messages, the offer back as a
   message, and a link for anything a chat cannot do. It needs a business
   number from Meta and a public address, so it is a deploy and waits for
   an explicit yes. It is built and tested first against recorded webhook
   calls, for free.
6. **A learning page in the back office.** Settlements per category, quote
   against settled price, range coverage, the reasons staff gave, what
   changed this week, and which model is running.

## Phases and the check that ends each one

| Phase | Work | Done when |
|---|---|---|
| A | Layer 1, the reason field, outlier hold, void rows | A test settles a copper lot at 20,000 and the next copper quote cites `settlement:...` with its date |
| B | Layer 2 fields, catalogue rows from corrections, trust score update | A test corrects an identity and the next session finds the item |
| C | Versioned API, per-tenant keys, OpenAPI file, widget, licence | A second, made-up tenant runs end to end with a YAML file and no code change |
| D | Layer 3 calibration and the learning page | Coverage on held-out settlements is within 5 points of the stated level, shown on the page |
| E | WhatsApp adapter on recorded webhooks | A recorded chat goes from photos to offer in tests. A live number only after a yes |
| F | Layer 4 export, retrain, gate, rollback | A retrained model is accepted or refused by the gate, with the report written either way |

A to C need no new data and can be built now. D needs about 30 settlements
in a category. F needs the first fine-tuned model from the Testify plan and
a few hundred settlements.

## What this means for Testify

Testify measures whether a model is honest before it meets real sellers.
The learning loop is what happens after. They meet in two places: Testify
is the gate every retrained model must pass, and the tenants' settlements,
shared with consent, become the settled-price labels that make Testify v0.2
a measure of real selling prices, not asking prices.
