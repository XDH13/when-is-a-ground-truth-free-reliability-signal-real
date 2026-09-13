"""Verify the immutable public artifact hashes listed in README.md."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "ARIS_REV8.pdf": "7ddb13dc220e264c6684129d16e7f212ad87a975798eb98d34f5b017a436ff49",
    "P0_FINAL_ARTIFACTS.zip": "4ab9a40d02cd4e9b6274e53f3bd09ab53b9dd14f840fa916b4c61b92eae02332",
    "P0_REPEAT_FINAL_ARTIFACTS.zip": "739f7d72532d70cecad4aa13acf6b2aeeb26545e892e5b30beff947cb5db406c",
    "MAIN_AUDIT_REPRO_ARTIFACTS.zip": "a102fc10bd8d5e4398c983cfdadb21680c31c6cb5af9800b40c3a77c42797026",
    "Paper_Overleaf_REV8_FINAL.zip": "5f6030a7a97e98d64c1716a6b44dc95513db7073bcbc0fe47185769af7aac49e",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    failures = []
    for name, expected in EXPECTED.items():
        actual = digest(ROOT / name)
        status = "PASS" if actual == expected else "FAIL"
        print(f"{status}  {name}")
        if actual != expected:
            failures.append(name)
    if failures:
        raise SystemExit(f"hash mismatch: {', '.join(failures)}")


if __name__ == "__main__":
    main()
