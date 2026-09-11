# Independent stochastic-generation replication

Each repeat uses fresh JSONL files and new Ollama generations. Fixed seeds control item order only.
Intervals below are paired item-bootstrap differences conditional on the two archived traces; they do not estimate a broader generation distribution.

| setting | original (items / conv / false / AUC) | repeat (items / conv / false / AUC) | repeat minus original AUC, 95% item-bootstrap CI |
|---|---|---|---|
| MATH / Qwen2.5-3B | 200 / 124 / 29 / 0.774 | 225 / 162 / 41 / 0.701 | -0.073 [-0.155,+0.089] |
| MATH / Qwen2.5-7B | 239 / 189 / 56 / 0.776 | 235 / 196 / 49 / 0.715 | -0.061 [-0.139,+0.042] |
| MATH / Qwen2.5-14B | 200 / 175 / 39 / 0.724 | 238 / 212 / 44 / 0.769 | +0.046 [-0.016,+0.181] |
| MMLU / Qwen2.5-3B | 200 / 199 / 70 / 0.568 | 200 / 200 / 80 / 0.521 | -0.048 [-0.111,+0.012] |
| MMLU / Qwen2.5-7B | 200 / 200 / 55 / 0.535 | 200 / 200 / 55 / 0.528 | -0.006 [-0.067,+0.051] |
| MMLU / Qwen2.5-14B | 200 / 200 / 45 / 0.566 | 200 / 200 / 44 / 0.538 | -0.028 [-0.083,+0.024] |
| MMLU / Llama-3.1-8B | 200 / 186 / 62 / 0.637 | 200 / 193 / 65 / 0.649 | +0.013 [-0.076,+0.104] |
| MMLU / Mistral-7B | 200 / 197 / 86 / 0.612 | 200 / 197 / 85 / 0.573 | -0.039 [-0.096,+0.016] |
