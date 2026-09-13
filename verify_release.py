"""Clean-directory, analysis-only verification for the public release."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARCHIVES = [
    "P0_FINAL_ARTIFACTS.zip",
    "P0_REPEAT_FINAL_ARTIFACTS.zip",
    "MAIN_AUDIT_REPRO_ARTIFACTS.zip",
]
SCRIPTS = [
    "p0_repeat_analyze.py",
    "_fwer_r1.py",
    "invu_significance.py",
    "invu4_within.py",
    "theory_32b.py",
    "theory_32b_v2.py",
    "thresh_perf.py",
    "thresh_sensitivity.py",
    "_arc4pt.py",
]
EXPECTED = {
    "P0_REPEAT_RESULTS.md": "61fdd73a980aadbcd583ad55e26ea1b6dbb5dd8058da421c43c1ee7a2aeaf0dc",
    "P0_REPEAT_RESULTS.json": "d3d8b665282bedbd09c4fd25501dd24f8a0a9b56135325e2739280e904d39f3f",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="aris-recompute-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ARCHIVES:
            with zipfile.ZipFile(ROOT / name) as archive:
                archive.extractall(tmp)
        # This tiny, documented compatibility module closes the only historical
        # import used by exp4_within.py.
        shutil.copy2(ROOT / "exp0_analyze.py", tmp / "exp0_analyze.py")

        records: list[str] = []
        for script in SCRIPTS:
            run = subprocess.run(
                [sys.executable, script], cwd=tmp, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            (tmp / f"{script}.stdout.txt").write_text(run.stdout, encoding="utf-8")
            if run.returncode:
                raise RuntimeError(f"{script} failed with exit {run.returncode}\n{run.stdout}")
            records.append(f"- PASS: `{script}`")

        hashes = {name: sha256(tmp / name) for name in EXPECTED}
        mismatch = [name for name, value in hashes.items() if value != EXPECTED[name]]
        if mismatch:
            raise RuntimeError(f"unexpected repeat-result hash: {mismatch}")

        report = [
            "# Clean analysis-only recomputation record",
            "",
            f"- UTC timestamp: `{datetime.now(timezone.utc).isoformat()}`",
            f"- Python: `{sys.version.split()[0]}`",
            "- Mode: clean temporary directory; archived inputs only; no Ollama call.",
            "- Result: PASS.",
            "",
            "## Executed scripts",
            *records,
            "",
            "## Recomputed repeat-result hashes",
            *[f"- `{value}`  `{name}`" for name, value in hashes.items()],
            "",
            "The temporary directory is deleted after a successful verification.",
        ]
        (ROOT / "CLEAN_RECOMPUTE_RECORD.md").write_text("\n".join(report) + "\n", encoding="utf-8")
        print("CLEAN_RECOMPUTE_PASS")
        for name, value in hashes.items():
            print(value, name)


if __name__ == "__main__":
    main()
