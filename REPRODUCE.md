# Analysis-only reproduction

This release supports an analysis-only check: it reads archived JSONL logs and
does **not** call Ollama or generate new model outputs.

## Environment

Use Python 3.11 and install the pinned dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Alternatively, create the equivalent Conda environment:

```powershell
conda env create -f environment.yml
conda activate aris-rev8-repro
```

## One-command clean-directory check

From the directory containing this release, run:

```powershell
python verify_release.py
```

The command extracts the three archived artifact bundles into a newly created
temporary directory, recomputes the independent-repeat result and executes the
published main-text analysis scripts. It prints the temporary directory and
writes `CLEAN_RECOMPUTE_RECORD.md` in the release root. It does not alter the
archived JSONL inputs.

Expected repeat-result SHA-256 values are:

```
61fdd73a980aadbcd583ad55e26ea1b6dbb5dd8058da421c43c1ee7a2aeaf0dc  P0_REPEAT_RESULTS.md
d3d8b665282bedbd09c4fd25501dd24f8a0a9b56135325e2739280e904d39f3f  P0_REPEAT_RESULTS.json
```

The analysis-only check is intentionally distinct from fresh collection. The
scripts and exact model identifiers for a new stochastic collection are in the
repeat artifact; a new collection will not reproduce bit-for-bit traces because
Ollama sampling was not seedable.

For a fast integrity-only check that does not extract or execute analysis
scripts, run `python verify_artifact_hashes.py`.
