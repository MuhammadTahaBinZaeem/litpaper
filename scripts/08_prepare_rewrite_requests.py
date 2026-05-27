"""
Step 9/10 helper: prepare controlled rewrite requests JSONL.

Run from repository root after Step 8 selected passages are present:

    python scripts/08_prepare_rewrite_requests.py

Input:
- data/processed/selected_original_passages.csv
- metadata/rewrite_generation_config.json
- prompts/rewrite_system_prompt.txt
- prompts/rewrite_paraphrase_prompt.txt
- prompts/rewrite_modernize_prompt.txt
- prompts/rewrite_simplify_prompt.txt

Output:
- data/interim/rewrite_requests.jsonl
- metadata/rewrite_request_manifest.csv

This script does not call an LLM. It only prepares blinded, reproducible request
records for Step 10 generation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTED = ROOT / "data" / "processed" / "selected_original_passages.csv"
CONFIG = ROOT / "metadata" / "rewrite_generation_config.json"
PROMPT_DIR = ROOT / "prompts"
OUT_JSONL = ROOT / "data" / "interim" / "rewrite_requests.jsonl"
MANIFEST = ROOT / "metadata" / "rewrite_request_manifest.csv"

WORD_SPLIT = None


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def word_count(text: str) -> int:
    return len(text.split())


def template_for(condition: str) -> Path:
    return PROMPT_DIR / f"rewrite_{condition}_prompt.txt"


def main() -> int:
    if not SELECTED.exists():
        print(f"Missing selected passages: {SELECTED}", file=sys.stderr)
        return 1
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    system_prompt = read_text(PROMPT_DIR / "rewrite_system_prompt.txt")
    rows = read_csv(SELECTED)
    expected = int(config["expected_original_passages"])
    if len(rows) != expected:
        print(f"Expected {expected} selected passages, found {len(rows)}", file=sys.stderr)
        return 1

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    conditions = config["conditions"]
    count = 0
    manifest_rows = []
    with OUT_JSONL.open("w", encoding="utf-8") as out:
        for row in rows:
            for condition in conditions:
                prompt_path = template_for(condition)
                template = read_text(prompt_path)
                user_prompt = template.format(
                    passage_id=row["passage_id"],
                    word_count=row["word_count"],
                    text=row["text"],
                )
                request_id = f"{row['passage_id']}__{condition}"
                record = {
                    "request_id": request_id,
                    "passage_id": row["passage_id"],
                    "condition": condition,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "generation_config": {
                        "temperature": config["temperature"],
                        "top_p": config["top_p"],
                        "presence_penalty": config["presence_penalty"],
                        "frequency_penalty": config["frequency_penalty"],
                        "seed_if_available": config["seed_if_available"],
                    },
                    "source_text_sha256": sha_text(row["text"]),
                    "original_word_count": int(row["word_count"]),
                    "prompt_template_id": f"{condition}_{config['prompt_template_version']}",
                    "system_prompt_sha256": sha_text(system_prompt),
                    "user_prompt_template_sha256": sha_text(template),
                    "created_utc": datetime.now(timezone.utc).isoformat(),
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                manifest_rows.append({
                    "request_id": request_id,
                    "passage_id": row["passage_id"],
                    "condition": condition,
                    "original_word_count": row["word_count"],
                    "source_text_sha256": record["source_text_sha256"],
                    "prompt_template_id": record["prompt_template_id"],
                    "system_prompt_sha256": record["system_prompt_sha256"],
                    "user_prompt_template_sha256": record["user_prompt_template_sha256"],
                })
                count += 1

    with MANIFEST.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "request_id", "passage_id", "condition", "original_word_count", "source_text_sha256",
            "prompt_template_id", "system_prompt_sha256", "user_prompt_template_sha256",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    expected_requests = int(config["expected_requests"])
    if count != expected_requests:
        print(f"Expected {expected_requests} requests, created {count}", file=sys.stderr)
        return 1
    print(f"Prepared {count} rewrite requests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
