# Testify test: the read and the pick

## The read: the model alone

| Model | Identity right | Same thing, judged | Named a model the photos do not show | Lie marked supported | True claim marked supported | False claim caught | Abstained with the label gone | Asked for the label first | Same decision asked twice |
|---|---|---|---|---|---|---|---|---|---|
| kaggle_anthropic_claude-sonnet-5@default | 85% | 99% | 2% | - | - | - | - | - | - |
| local_qwen_qwen3-vl-2b-r4 | 74% | 94% | 13% | 1% | - | - | - | - | - |
| local_qwen_qwen3-vl-2b-r5 | 75% | 95% | 13% | 1% | - | - | - | - | - |
| local_qwen_qwen3-vl-4b-r4 | 77% | 94% | 11% | 1% | - | - | - | - | - |

Identity right is the word rule; same thing, judged also counts other words for the same thing (testify/judge.py), and a person's verdict comes first in both.

## The pick: the model and our comparables

| Model | Gave a price | Silent wrong | Asking price inside the range | Offered above asking | Lie raised the price (asking again raised it) | Expected loss per item, naira |
|---|---|---|---|---|---|---|
| kaggle_anthropic_claude-sonnet-5@default | 18% | 3 | 41% | 18% | - (-) | 4306 |
| local_qwen_qwen3-vl-2b-r4 | 31% | 20 | 52% | 14% | 6% (-) | 3873 |
| local_qwen_qwen3-vl-2b-r5 | 21% | 16 | 56% | 16% | 6% (-) | 3850 |
| local_qwen_qwen3-vl-4b-r4 | 36% | 26 | 48% | 25% | 6% (-) | 11301 |

Expected loss is at the first lost-deal cost in compare.json; it is not any business's own number.
