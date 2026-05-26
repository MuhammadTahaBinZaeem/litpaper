"""
Run the canonical-source migration pipeline.

Run from repository root with internet access:

    python scripts/04_fetch_gutenberg_sources.py
    python scripts/05_run_canonical_migration.py

This runner prepares the fetched plain-text files for the already verified
cleaning and validation scripts.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

CANONICAL_RAW = Path("data/raw/gutenberg_texts")
TEXT_EXTRACTED = Path("data/raw/text_extracted/gutenberg")


def run(cmd: list[str]) -> None:
    print("RUN:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def prepare_cleaner_input() -> None:
    if not CANONICAL_RAW.exists():
        raise FileNotFoundError("Missing data/raw/gutenberg_texts. Run scripts/04_fetch_gutenberg_sources.py first.")
    if TEXT_EXTRACTED.exists():
        shutil.rmtree(TEXT_EXTRACTED)
    TEXT_EXTRACTED.mkdir(parents=True, exist_ok=True)
    for src in sorted(CANONICAL_RAW.glob("*.txt")):
        shutil.copy2(src, TEXT_EXTRACTED / src.name)


def main() -> int:
    prepare_cleaner_input()
    run([sys.executable, "scripts/01_clean_texts.py"])
    run([sys.executable, "scripts/02_validate_cleaning.py"])
    run([sys.executable, "scripts/03_extract_candidate_passages.py"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
