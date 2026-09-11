# P0 experiment results

## Heterogeneous agents on MATH

Round 1 reuses fixed draws from matched homogeneous runs; round 2 is newly generated after cross-family answer exchange.

| configuration | total | converged / false | within-Level agreement AUC | status |
|---|---:|---:|---:|---|
| Qwen3+Llama8+Mistral7 | 196 | 76 / 13 | 0.615 [0.490,0.734] | UNDERPOWERED |
| Qwen7+Llama8+Mistral7 | 199 | 93 / 20 | 0.779 [0.671,0.869] | OK |
| Qwen14+Llama8+Mistral7 | 197 | 83 / 20 | 0.727 [0.630,0.814] | OK |

## Disjoint MMLU holdout

The pool is disjoint from the original 150-item MMLU pool and uses a generic MCQ prompt shared by all five models.

| model | total | converged / false | within-tier agreement AUC | status | MATH minus MMLU |
|---|---:|---:|---:|---|---:|
| Qwen2.5-3B | 200 | 199 / 70 | 0.568 [0.511,0.629] | OK | +0.205 [+0.105,+0.303] |
| Qwen2.5-7B | 200 | 200 / 55 | 0.535 [0.487,0.586] | OK | +0.241 [+0.146,+0.326] |
| Qwen2.5-14B | 200 | 200 / 45 | 0.566 [0.521,0.622] | OK | +0.158 [+0.055,+0.257] |
| Llama-3.1-8B | 200 | 186 / 62 | 0.637 [0.572,0.702] | OK | +0.047 [-0.061,+0.150] |
| Mistral-7B | 200 | 197 / 86 | 0.612 [0.562,0.666] | OK | +0.116 [-0.028,+0.249] |

All intervals are item-level stratified bootstrap intervals. A cell with fewer than 15 false-consensus cases is labelled UNDERPOWERED and is not interpreted.
