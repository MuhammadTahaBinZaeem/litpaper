"""
Step 6/7 script: candidate passage extraction.

Step 6 freezes the extraction protocol and this script scaffold.
Step 7 will run this script to generate the candidate passage pool.

Purpose
-------
Extract non-overlapping, style-preserving candidate passages from cleaned texts.
The final 360-passage dataset is NOT selected here; final selection and balance
belong to Step 8.

Run
---
python scripts/03_extract_candidate_passages.py
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable

CONFIG_PATH = Path("metadata/passage_extraction_config.json")
SOURCE_ID_MAP_PATH = Path("metadata/source_id_map.csv")
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
SENT_SPLIT_RE = re.compile(r"[.!?]+")
PUNCT_CHARS = set(".,;:!?—–-\"“”‘’'…")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def word_spans(text: str) -> list[re.Match[str]]:
    return list(WORD_RE.finditer(text))


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def sentence_count(text: str) -> int:
    compact = re.sub(r"\s+", " ", text.strip())
    if not compact:
        return 0
    return len([s for s in SENT_SPLIT_RE.split(compact) if s.strip()])


def paragraph_count(text: str) -> int:
    return len([p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()])


def per_1000(count: int, word_count: int) -> float:
    return round(count / word_count * 1000, 3) if word_count else 0.0


def passage_metrics(text: str) -> dict[str, int | float]:
    toks = words(text)
    word_count = len(toks)
    sents = [s for s in SENT_SPLIT_RE.split(re.sub(r"\s+", " ", text.strip())) if s.strip()]
    sent_lens = [len(words(s)) for s in sents if words(s)]
    punctuation_total = sum(1 for c in text if c in PUNCT_CHARS)
    dialogue_marker_count = sum(text.count(ch) for ch in ['"', "“", "”", "‘", "’"])
    semicolon_count = text.count(";")
    dash_count = text.count("—") + text.count("–") + len(re.findall(r"(?<!\w)-(?!\w)", text))
    apostrophe_count = text.count("'") + text.count("’")
    long_sentence_count = sum(1 for n in sent_lens if n >= 40)
    return {
        "word_count": word_count,
        "sentence_count": len(sent_lens),
        "paragraph_count": paragraph_count(text),
        "dialogue_marker_count": dialogue_marker_count,
        "dialogue_marker_per_1000w": per_1000(dialogue_marker_count, word_count),
        "punctuation_per_1000w": per_1000(punctuation_total, word_count),
        "semicolon_per_1000w": per_1000(semicolon_count, word_count),
        "dash_per_1000w": per_1000(dash_count, word_count),
        "apostrophe_per_1000w": per_1000(apostrophe_count, word_count),
        "mean_sentence_words": round(sum(sent_lens) / len(sent_lens), 3) if sent_lens else 0.0,
        "long_sentence_ratio": round(long_sentence_count / len(sent_lens), 6) if sent_lens else 0.0,
    }


def locate_cleaned_text(cleaned_root: Path, source_path: str) -> Path | None:
    expected_name = Path(source_path).with_suffix(".txt").name
    matches = list(cleaned_root.rglob(expected_name))
    if len(matches) == 1:
        return matches[0]
    return None


def make_candidate_id(author_id: str, source_id: str, index: int) -> str:
    return f"{author_id.upper()}_{source_id.upper()}_{index:04d}"


def extract_windows(text: str, preferred_words: int, min_words: int, max_words: int, gap_words: int) -> Iterable[tuple[int, int, int, int, str]]:
    spans = word_spans(text)
    if len(spans) < min_words:
        return
    start_word = 0
    candidate_index = 1
    step = preferred_words + gap_words
    while start_word + min_words <= len(spans):
        end_word = min(start_word + preferred_words, len(spans))
        if end_word - start_word < min_words:
            break
        if end_word - start_word > max_words:
            end_word = start_word + max_words
        start_char = spans[start_word].start()
        end_char = spans[end_word - 1].end()
        passage = text[start_char:end_char].strip()
        yield candidate_index, start_word, end_word, start_char, end_char, passage
        candidate_index += 1
        start_word += step


def infer_work_fields(source_row: dict[str, str]) -> tuple[str, str]:
    # Step 7/8 will refine work boundaries for complete-works containers.
    status = source_row["main_corpus_status"]
    author = source_row["author_id"]
    if status == "eligible_container":
        return "unknown_container_section", "Unknown container section pending boundary extraction"
    return "source_level_work", "Source-level work pending final work mapping"


def main() -> None:
    config = read_json(CONFIG_PATH)
    source_rows = read_csv(SOURCE_ID_MAP_PATH)
    cleaned_root = Path(config["input_dir"])
    out_candidates = Path(config["output_candidate_passages"])
    out_metadata = Path(config["output_candidate_metadata"])
    report_path = Path(config["candidate_generation_report"])
    allowed_statuses = set(config["allowed_source_statuses"])

    out_candidates.parent.mkdir(parents=True, exist_ok=True)
    out_metadata.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    candidate_rows: list[dict[str, object]] = []
    source_report_rows: list[tuple[str, str, int, str]] = []

    for source_row in source_rows:
        source_id = source_row["source_id"]
        author_id = source_row["author_id"]
        status = source_row["main_corpus_status"]
        if status not in allowed_statuses:
            source_report_rows.append((source_id, author_id, 0, f"skipped_status_{status}"))
            continue

        cleaned_path = locate_cleaned_text(cleaned_root, source_row["source_path"])
        if cleaned_path is None:
            source_report_rows.append((source_id, author_id, 0, "missing_cleaned_text"))
            continue

        text = cleaned_path.read_text(encoding="utf-8", errors="replace")
        work_id, work_title = infer_work_fields(source_row)
        count = 0
        for idx, start_word, end_word, start_char, end_char, passage in extract_windows(
            text,
            int(config["preferred_words_per_passage"]),
            int(config["minimum_words_per_passage"]),
            int(config["maximum_words_per_passage"]),
            int(config["minimum_gap_words_same_source"]),
        ):
            m = passage_metrics(passage)
            candidate_status = "candidate_pass_length"
            exclusion_reason = ""
            if m["word_count"] < int(config["minimum_words_per_passage"]) or m["word_count"] > int(config["maximum_words_per_passage"]):
                candidate_status = "candidate_fail_length"
                exclusion_reason = "outside_hard_word_bounds"
            elif m["sentence_count"] < int(config["minimum_sentence_count"]):
                candidate_status = "candidate_fail_low_sentence_count"
                exclusion_reason = "too_few_sentences"

            candidate_rows.append({
                "candidate_id": make_candidate_id(author_id, source_id, idx),
                "source_id": source_id,
                "author_id": author_id,
                "author_name": source_row["author_name"],
                "work_id": work_id,
                "work_title": work_title,
                "source_path": source_row["source_path"],
                "candidate_index_within_source": idx,
                "start_word_index": start_word,
                "end_word_index": end_word,
                "start_char": start_char,
                "end_char": end_char,
                **m,
                "extraction_rule_version": config["extraction_rule_version"],
                "candidate_status": candidate_status,
                "exclusion_reason": exclusion_reason,
                "text": passage,
            })
            count += 1
        source_report_rows.append((source_id, author_id, count, "processed"))

    fieldnames = [
        "candidate_id", "source_id", "author_id", "author_name", "work_id", "work_title", "source_path",
        "candidate_index_within_source", "start_word_index", "end_word_index", "word_count", "sentence_count",
        "paragraph_count", "start_char", "end_char", "dialogue_marker_count", "dialogue_marker_per_1000w",
        "punctuation_per_1000w", "semicolon_per_1000w", "dash_per_1000w", "apostrophe_per_1000w",
        "mean_sentence_words", "long_sentence_ratio", "extraction_rule_version", "candidate_status",
        "exclusion_reason", "text",
    ]
    with out_candidates.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidate_rows)

    metadata_fieldnames = [name for name in fieldnames if name != "text"]
    with out_metadata.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metadata_fieldnames)
        writer.writeheader()
        for row in candidate_rows:
            writer.writerow({k: row[k] for k in metadata_fieldnames})

    author_counts: dict[str, int] = {}
    for row in candidate_rows:
        if row["candidate_status"] == "candidate_pass_length":
            author_counts[str(row["author_id"])] = author_counts.get(str(row["author_id"]), 0) + 1

    lines = [
        "# Candidate Generation Report",
        "",
        f"Total candidate rows: {len(candidate_rows)}",
        "",
        "## Passing candidates by author",
        "",
    ]
    for author_id, count in sorted(author_counts.items()):
        lines.append(f"- {author_id}: {count}")
    lines.extend(["", "## Source processing summary", ""])
    for source_id, author_id, count, status in source_report_rows:
        lines.append(f"- {source_id} / {author_id}: {count} ({status})")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {len(candidate_rows)} candidates to {out_candidates}")


if __name__ == "__main__":
    main()
