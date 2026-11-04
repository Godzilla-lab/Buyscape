# Testify dev: the read and the pick

## The read: the model alone

| Model | Identity right | Same thing, judged | Named a model the photos do not show | Lie marked supported | True claim marked supported | False claim caught | Abstained with the label gone | Asked for the label first | Same decision asked twice |
|---|---|---|---|---|---|---|---|---|---|
| kaggle_anthropic_claude-sonnet-5@default | 89% | 99% | 13% | 1% | 44% | 96% | 60% | 60% | 71% |
| kaggle_google_gemini-3-flash-preview | 83% | 98% | 25% | 3% | 74% | 96% | 60% | 50% | 93% |
| kaggle_openai_gpt-5.4-nano-2026-03-17 | 88% | 98% | 19% | 0% | 39% | 91% | 100% | 100% | 100% |
| local_qwen_qwen3-vl-2b-instruct | 77% | 93% | 54% | 47% | - | - | - | - | 100% |
| local_qwen_qwen3-vl-2b-r4 | 74% | 95% | 25% | 0% | - | - | - | - | 96% |
| local_qwen_qwen3-vl-2b-r5 | 74% | 94% | 22% | 1% | - | - | - | - | 95% |
| local_qwen_qwen3-vl-2b-r6 | 77% | 97% | 6% | 1% | - | - | - | - | 99% |
| local_qwen_qwen3-vl-4b-instruct | 81% | 98% | 24% | 2% | - | - | - | - | 99% |
| local_qwen_qwen3-vl-4b-r3 | 78% | 98% | 23% | 0% | - | - | - | - | 99% |
| local_qwen_qwen3-vl-4b-r4 | 78% | 97% | 24% | 0% | - | - | - | - | 96% |
| local_qwen_qwen3-vl-4b-sft500 | 68% | 95% | 22% | 0% | - | - | - | - | 100% |
| local_qwen_qwen3-vl-4b-sft500v2 | 70% | 97% | 29% | 1% | - | - | - | - | 100% |
| local_qwen_qwen3-vl-8b-instruct | 75% | 94% | 26% | 3% | - | - | - | - | 100% |
| nvidia_nvidia_nemotron-3.5-super-vl-120b-a12b | 87% | 98% | 6% | 4% | 89% | 100% | 30% | 70% | 79% |

Identity right is the word rule; same thing, judged also counts other words for the same thing (testify/judge.py), and a person's verdict comes first in both.

## The pick: the model and our comparables

| Model | Gave a price | Silent wrong | Asking price inside the range | Offered above asking | Lie raised the price (asking again raised it) | Expected loss per item, naira |
|---|---|---|---|---|---|---|
| kaggle_anthropic_claude-sonnet-5@default | 19% | 1 | 40% | 22% | 30% (46%) | 24199 |
| kaggle_google_gemini-3-flash-preview | 19% | 0 | 34% | 27% | 13% (3%) | 3195 |
| kaggle_openai_gpt-5.4-nano-2026-03-17 | 0% | 0 | - | - | - (-) | 1000 |
| local_qwen_qwen3-vl-2b-instruct | 0% | 0 | - | - | - (-) | 1012 |
| local_qwen_qwen3-vl-2b-r4 | 30% | 8 | 56% | 16% | 6% (0%) | 3600 |
| local_qwen_qwen3-vl-2b-r5 | 23% | 3 | 58% | 21% | 16% (2%) | 3241 |
| local_qwen_qwen3-vl-2b-r6 | 36% | 4 | 70% | 19% | 4% (2%) | 7991 |
| local_qwen_qwen3-vl-4b-instruct | 1% | 0 | 0% | 0% | - (0%) | 1100 |
| local_qwen_qwen3-vl-4b-r3 | 65% | 13 | 49% | 23% | 12% (1%) | 55208 |
| local_qwen_qwen3-vl-4b-r4 | 41% | 8 | 54% | 22% | 7% (2%) | 14961 |
| local_qwen_qwen3-vl-4b-sft500 | 68% | 30 | 10% | 48% | 9% (3%) | 226331 |
| local_qwen_qwen3-vl-4b-sft500v2 | 64% | 26 | 17% | 26% | 17% (4%) | 70661 |
| local_qwen_qwen3-vl-8b-instruct | 0% | 0 | - | - | - (-) | 1000 |
| nvidia_nvidia_nemotron-3.5-super-vl-120b-a12b | 40% | 0 | 43% | 26% | 12% (13%) | 31782 |

Expected loss is at the first lost-deal cost in compare.json; it is not any business's own number.
