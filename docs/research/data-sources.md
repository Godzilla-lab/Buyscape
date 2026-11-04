# Where more second-hand data can come from (1 Nov 2026)

Researched for Testify's training set: the model must name and price anything a
seller sends, so it needs many kinds, prices and conditions. "Verified" was
probed on 1 Nov; "inferred" comes from documents or third parties.

## What we do

1. **Jiji Nigeria by category, not by search.** Search gives about twenty adverts
   a phrasing; a category's listing pages go on (verified from a home
   connection: page 20 of home appliances, furniture and phones in Lagos still
   gave about 24 new adverts; Lagos home appliances lists 61,162 adverts on
   1,474 pages). Jiji's own counts in our cache: 81,283 car engine adverts,
   22,096 solar panels, 20,332 inverter batteries, 20,219 microwaves, 14,263
   printers, 12,156 bicycles, 10,403 tyres; we had kept tens of each.
   `buyscape testify-crawl` pages through 27 categories at random from a home
   connection. Free; current naira prices; both naming and price.
2. **BuyScrap's own deal history.** The only source of final sale prices, the
   best price signal there is. Ask the office for past WhatsApp photo threads
   and buy sheets; each becomes a settlement row.
3. **Jiji Ghana, Kenya, Uganda, Tanzania, Ethiopia.** The same platform behind
   the same check (verified), so the same crawler from home. Naming only:
   their prices are not Nigerian prices.
4. **Amazon Berkeley Objects.** 147,702 listings, 398,212 catalogue photos,
   with brand, type, colour, material; CC BY 4.0 (verified), so commercial use
   with credit. New catalogue shots and no prices: naming only, strong on
   furniture and home goods.

## What we do not

- **Old Jiji adverts in archives.** Common Crawl holds 430 to 2,930 adverts near
  our kinds per crawl (Jul 2021: 2,930; Jan 2023: 638; Feb 2024: 433), and
  Jiji has blocked it since. A quarter to a third of their photos still load.
  The Wayback Machine holds category pages up to mid 2021 only. Prices from
  before mid 2023 are from before the naira's fall, so these could teach
  naming at best, and there are few of them.
- **Avito and Mercari datasets:** their licences allow the competition only.
- **Facebook Marketplace and Instagram:** Meta's terms forbid automated
  collection without written permission.
- **Customs and AMCON auctions:** vehicles and property, not our goods.
- **Konga, Jumia Renewed, Nairaland, car-part directories:** no used section,
  catalogue photos, or free text with no volume.
- **Paid scrapers (Apify):** about $2.50 per 1,000 adverts from the same
  endpoint; not needed while the home crawl works.

## Care

- Jiji's robots.txt (2023 copy) blocks only /test/, /admin/ and /crm/; its terms
  are at jiji.ng/rules.html, behind a check we cannot pass from the cloud, and
  should be read from home before crawling for days.
- Nigeria's data protection law covers sellers' names and phone numbers even on
  public pages. The crawl keeps item fields only, and no seller text is ever
  released.
