# Runs

One folder per model or sitting. `<split>_<market>.jsonl` holds every answer,
`.summary.json` its score, and a `.<tag>` file a second run recorded apart.

`v1/` holds the first runs, with one generic planted lie for every item and
the first retrieval. They are kept so the numbers in
`docs/research/testify-baseline-1.md` can be checked; the runs beside them
use the lies in `eval/testify/lies.yaml` and the fixed retrieval.
