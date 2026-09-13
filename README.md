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
- `MAIN_AUDIT_REPRO_ARTIFACTS.zip` — complete main-scale MATH Qwen logs
  (3B/7B/14B/32B), ARC/MMLU stress-test logs, and every main-text analysis
  script referenced by the manuscript.
- `verify_release.py`, `REPRODUCE.md`, `requirements.txt`, and
  `CLEAN_RECOMPUTE_RECORD.md` — an analysis-only clean-directory verification
  command, its pinned dependency, and the successful verification record.
- `REVIEW7_POSTREPEAT_RESULT.md` and `REVIEW9_REPRODUCIBILITY_RESULT.md` —
  independent review records before and after the public reproducibility fix.

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
7ddb13dc220e264c6684129d16e7f212ad87a975798eb98d34f5b017a436ff49  ARIS_REV8.pdf
4ab9a40d02cd4e9b6274e53f3bd09ab53b9dd14f840fa916b4c61b92eae02332  P0_FINAL_ARTIFACTS.zip
739f7d72532d70cecad4aa13acf6b2aeeb26545e892e5b30beff947cb5db406c  P0_REPEAT_FINAL_ARTIFACTS.zip
a102fc10bd8d5e4398c983cfdadb21680c31c6cb5af9800b40c3a77c42797026  MAIN_AUDIT_REPRO_ARTIFACTS.zip
5f6030a7a97e98d64c1716a6b44dc95513db7073bcbc0fe47185769af7aac49e  Paper_Overleaf_REV8_FINAL.zip
```

The release contains model outputs and scripts, not model weights or benchmark
distributions. Obtain any underlying models and benchmark data under their
respective upstream licenses.
