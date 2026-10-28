# What each partner publishes, checked before any email

Rule: take what a company publishes on its own website first. Email only for
what is missing. Checked on 14 October 2026.

| Company | Website | Robots | Public data found | Used | Email still needed for |
|---|---|---|---|---|---|
| V-Martins Recycling | vmartinsrecyclingcompany.com | Allows all | **Price list dated October 2026**: iron, copper, brass, 4 aluminium grades, scrap cars, generators, ACs | Yes: `tenants/scrap_index_lagos.yaml` | Nothing yet |
| Scrapays | scrapays.com | No robots file | A recyclables page built to show prices, but the price list came back empty. Lists the materials it buys: PET, HDPE, LDPE, PP, ABS, paperboard, aluminium, iron, copper, brass, batteries | Material list only | Prices per kilo, past collections |
| Ecobarter | ecobarter.africa | Allows all | Impact totals and stories. No price list on the site. Prices live in its app, in points | No | Prices per kilo, past collections |
| Hinckley Group | hinckley.com.ng | Allows all except admin | Company pages only: HP, Dell, Lenovo and Canon service centre, and Nigeria's first registered e-waste recycler. No prices or intake data | No | E-waste intake weights and values |
| Pakam | pakam.ng | Names Google, Bing and Twitter only | Not read: its robots file names only those crawlers, so others are not invited | No | Prices per kilo, past collections |
| Credlock | credlock.com | Allows all | The domain shows a parked "lander" page, so it may not be Credlock's site | No | Find the real site first |
| Cars45 | cars45.com | Allows most | Not read: every page sits behind a CAPTCHA | No | Inspection reports |
| Konga | konga.com | Allows product pages | Not read: its terms load by script and could not be checked | No | Permission for new prices |
| Jiji | jiji.ng | Blocks this machine | Fetched from a home connection with `testify-fetch` | Yes | Bulk access, if the home fetch is not enough |

## New-price shops, checked on 28 October 2026

BuyScrap's own site still lists the same 56 adverts cached on 14 October, so
nothing new there. These shops sell new goods, so their prices are for the
"dealers' new price times `resale_fraction`" route when used adverts are thin.
Today that route uses only the dealers' new stock on Jiji. Only robots files
were read; no shop page was fetched.

| Shop | Website | Robots | What it could add |
|---|---|---|---|
| Jumia | jumia.com.ng | Allows product and category pages; blocks filters, search and its app API | New prices for phones, appliances, TVs, generators |
| Slot | slot.ng | Allows all but cart, checkout and profile | New prices for phones, laptops, accessories |
| Pointek | pointekonline.com | Allows all but admin and cart; has a sitemap | New prices for electronics |
| Kara | kara.com.ng | Timed out | Not known |
| Autochek | autochek.africa | Sends visitors to a welcome page | Used car prices, if the listings are reachable |
| Badili | badili.africa | No robots file; the site is an app | Refurbished phone prices by grade, if reachable |
| Nairaland | nairaland.com | Blocks this machine, like Jiji | Forum adverts, from a home connection only |

## Press figures, not used

Articles quote per-kilo prices for plastics: PET at 250 a kilo from pickers
and 500 to 600 to recyclers, HDPE 300 to 350, PP 250 to 300 (Nairametrics,
July 2025). They are more than 240 days old, past the index's age limit, and
they are a journalist's report rather than a buyer's schedule. They are noted
here as a sense check on the derived plastic rates, which look low.

## What changed in the index

- Iron and steel: 500-600 to 400-500 a kilo
- Bare copper: 10,000-13,000 to 12,000-14,000
- Brass: 7,000-7,500 to 7,500-8,000
- Aluminium: 2,000-3,000 to 1,500-2,500, now with four grades
- Stainless and lead: dropped from the October list, so moved to estimates
- Generators and ACs: unchanged
