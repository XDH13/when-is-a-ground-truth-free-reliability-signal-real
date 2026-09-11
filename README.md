# ARIS REV8 public materials

This release accompanies *When Is a Ground-Truth-Free Reliability Signal Real?*
and contains the final reviewed PDF, Overleaf-ready source, original P0
artifacts, and the independent fresh-generation repetitions reported in Table 6.

## Contents

- `ARIS_REV8.pdf` — final 25-page PDF; compiled locally with MiKTeX 25.12.
- `Paper_Overleaf_REV8_FINAL.zip` — manuscript source, figures, bibliography,
  static checker, and `tab_repeat.tex`.
- `P0_FINAL_ARTIFACTS.zip` and `P0_EXPERIMENT_RESULTS.md` — original P0
  outputs and summary.
- `P0_REPEAT_FINAL_ARTIFACTS.zip` — fresh JSONL traces for MATH Qwen2.5
  3B/7B/14B and MMLU Qwen2.5 3B/7B/14B, Llama-3.1-8B and Mistral-7B; it also
  contains the repeat analysis scripts and machine-readable result JSON.
- `P0_REPEAT_RESULTS.md` — human-readable repeat summary.
- `exp4_collect.py` and `p0_mcq_collect.py` — collection scripts used by the
  MATH and MMLU repeat drivers.
- `REVIEW7_POSTREPEAT_RESULT.md` — independent post-repeat review record.

## Reproduction scope

The released runs used Ollama 0.33.3 on Windows with an NVIDIA RTX 3070 (8GB).
MATH used temperature 0.7 and a 1536-token cap. The P0 MMLU holdout used the
same temperature, three samples and two rounds, a short answer-and-confidence
prompt, and a 128-token cap. Seed `20260911` fixed item order only; it did not
seed backend sampling. The logs are therefore the audit record, not a
bit-for-bit regeneration guarantee.

The paired item-bootstrap intervals compare two archived generation traces and
do not estimate a population distribution over stochastic generations. Please
preserve that limitation when reusing these results.

## Integrity hashes (SHA-256)

```
0dd524d0f3d6f16ee0005ce790f4dadb0fc16f699752ad9bf1ef7e30941969e8  ARIS_REV8.pdf
4ab9a40d02cd4e9b6274e53f3bd09ab53b9dd14f840fa916b4c61b92eae02332  P0_FINAL_ARTIFACTS.zip
92c04abc553cbbf8f4cb492433ffbfc417ccbe503f559586ad10ef1ee859094c  P0_REPEAT_FINAL_ARTIFACTS.zip
f8b49ad4a4f6ec52d36b6dd8ce065029d4287817512b957e6f4a501fd53952f1  Paper_Overleaf_REV8_FINAL.zip
```

The release contains model outputs and scripts, not model weights or benchmark
distributions. Obtain any underlying models and benchmark data under their
respective upstream licenses.
