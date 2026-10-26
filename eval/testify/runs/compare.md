# Testify dev: the read and the pick

## The read: the model alone

| Model | Identity right | Named a model the photos do not show | Lie marked supported | True claim marked supported | False claim caught | Abstained with the label gone | Asked for the label first | Same decision asked twice |
|---|---|---|---|---|---|---|---|---|
| kaggle_anthropic_claude-sonnet-5@default | 89% | 13% | 1% | - | - | - | - | 71% |
| kaggle_google_gemini-3-flash-preview | 82% | 25% | 3% | 68% | 96% | - | - | 93% |
| kaggle_openai_gpt-5.4-nano-2026-03-17 | 88% | 19% | 0% | - | - | - | - | 100% |
| local_qwen_qwen3-vl-8b-instruct | 74% | 26% | 3% | - | - | - | - | 100% |
| nvidia_nvidia_nemotron-3.5-super-vl-120b-a12b | 85% | 6% | 4% | 83% | 100% | 30% | 70% | 79% |

## The pick: the model and our comparables

| Model | Gave a price | Silent wrong | Asking price inside the range | Offered above asking | Lie raised the price (asking again raised it) | Expected loss per item, naira |
|---|---|---|---|---|---|---|
| kaggle_anthropic_claude-sonnet-5@default | 19% | 1 | 40% | 22% | 30% (46%) | 24199 |
| kaggle_google_gemini-3-flash-preview | 19% | 2 | 34% | 27% | 13% (3%) | 3195 |
| kaggle_openai_gpt-5.4-nano-2026-03-17 | 0% | 0 | - | - | - (-) | 1000 |
| local_qwen_qwen3-vl-8b-instruct | 0% | 0 | - | - | - (-) | 1000 |
| nvidia_nvidia_nemotron-3.5-super-vl-120b-a12b | 40% | 3 | 43% | 26% | 12% (13%) | 31782 |

Expected loss is at the first lost-deal cost in compare.json; it is not any business's own number.
