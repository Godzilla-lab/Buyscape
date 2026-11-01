# Testify test: the read and the pick

## The read: the model alone

| Model | Identity right | Named a model the photos do not show | Lie marked supported | True claim marked supported | False claim caught | Abstained with the label gone | Asked for the label first | Same decision asked twice |
|---|---|---|---|---|---|---|---|---|
| local_qwen_qwen3-vl-2b-r4 | 74% | 13% | 1% | - | - | - | - | - |
| local_qwen_qwen3-vl-2b-r5 | 75% | 13% | 1% | - | - | - | - | - |
| local_qwen_qwen3-vl-4b-r4 | 77% | 11% | 1% | - | - | - | - | - |

## The pick: the model and our comparables

| Model | Gave a price | Silent wrong | Asking price inside the range | Offered above asking | Lie raised the price (asking again raised it) | Expected loss per item, naira |
|---|---|---|---|---|---|---|
| local_qwen_qwen3-vl-2b-r4 | 31% | 20 | 52% | 14% | 6% (-) | 3873 |
| local_qwen_qwen3-vl-2b-r5 | 21% | 16 | 56% | 16% | 6% (-) | 3850 |
| local_qwen_qwen3-vl-4b-r4 | 36% | 26 | 48% | 25% | 6% (-) | 11301 |

Expected loss is at the first lost-deal cost in compare.json; it is not any business's own number.
