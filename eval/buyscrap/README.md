# Real BuyScrap listings

Photos of what people actually try to sell. This is the honest benchmark: the
Jiji set is four tidy categories, this is the real distribution.

## How to add them

Drop the image files into `eval/buyscrap/media/`, any filenames. Then run:

    uv run buyscape run --raw eval/buyscrap --mode record

Images pasted into a chat never touch the filesystem, so they have to be saved
here by hand once.

## What the first batch showed

Nineteen photos, and only two of them fit the four categories the engine was
built for. The rest is the point of the product.

| What it is | Priced how | Notes |
|---|---|---|
| Ideal Topstar sewing machine | unit | Brand legible on the body, so OCR identifies it |
| Two taped black plastic units with cords | unit | Nothing legible, poor light |
| Sony flat screen TV with remotes and adapter | unit | Front shot only, no plate |
| Sony TV rear panel | unit | A review site's studio image, not the seller's TV |
| LG CRT television | unit | A screenshot of a phone gallery app, not a photo |
| LG DirectDrive 6/3kg washer dryer | unit | Model and capacity legible on the fascia |
| Linksys Hydra Pro 6 router, boxed | sealed new | Prices off retail, not off condition |
| Stack of school exercise paper | lot | Paper by weight |
| Old hi-fi stack | unit | Blurred, nothing legible |
| Standing fan, rusted | unit | Nothing legible |
| Sacks of PET bottles | lot | Plastic by weight |
| Wrecked vacuum tanker truck | unit | Vehicle, needs the open-every-compartment protocol |
| Pile of circuit boards | lot | E-waste board grade by weight |
| Mesh and wire offcuts | lot | Ferrous by weight |
| Heap of car parts: driveshafts, steering rack, condenser, starter | lot | Mixed metals by weight |
| Window air conditioner, rear view | unit | Dirty, no plate in frame |
| Office chair | unit | No maker visible |
| LG monitor and keyboard | unit | Brand legible on the bezel |
| Camera lens | unit | Markings not legible at this angle |

## What that changes

1. **Lots outnumber units.** Bottles, boards, mesh, car parts and paper have no
   model to find. They are priced by material, weight and contamination. Asking
   "what model is this" is the wrong question, and an engine that asks it will
   either guess or refuse.
2. **The generic protocol is the main road**, not the fallback.
3. **Fraud signals are already present at roughly one in ten**: one stock photo
   lifted from a review site, one screenshot of a gallery app.
4. **Capture conditions are the binding constraint.** Dark rooms, blur, single
   angles, no plate in frame on most items.
5. **Sealed new stock is a third path**, priced off retail with the only real
   question being whether the box has been opened.
