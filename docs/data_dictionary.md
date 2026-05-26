# Data Dictionary

This file is initialized in Step 1 and will be expanded as datasets are created.

## Current metadata layers

### `metadata/source_inventory.csv`

Inventory of all tracked raw PDFs.

Expected columns:

- `zip_path`
- `repo_target_path`
- `size_bytes`
- `sha256`
- `modified`

### `metadata/raw_file_checksums.csv`

Step 3 raw-file preservation table.

Expected columns:

- `source_path`
- `repo_target_path`
- `size_bytes`
- `pdf_pages`
- `sha256`
- `raw_available_in_session`
- `raw_committed_to_repo`
- `preservation_status`

### `metadata/extracted_text_checksums_by_id.csv`

Step 3 extracted-text checksum table using sanitized source IDs.

Expected columns:

- `source_id`
- `extraction_tool`
- `extraction_status`
- `pdf_pages`
- `text_bytes_utf8`
- `chars`
- `words`
- `sha256`
- `error_or_note`

### `metadata/text_extraction_status_summary.csv`

Compact Step 3 summary of text extraction status.

Expected columns:

- `metric`
- `value`

### `metadata/author_work_map.csv`

Step 2 author/work map.

Expected columns:

- `author_id`
- `author_name`
- `work_id`
- `work_title`
- `publication_year`
- `source_pdf`
- `source_type`
- `genre`
- `candidate_role`
- `usable_for_main_corpus`
- `inclusion_status`
- `notes`
- `extraction_priority`

### `metadata/source_item_review.csv`

Step 2 source-level review table.

Expected columns:

- `author_id`
- `author_name`
- `source_pdf`
- `filename`
- `size_bytes`
- `pdf_pages`
- `sha256`
- `step2_decision`
- `decision_reason`

### `metadata/cleaning_config.json`

Step 4 deterministic cleaning configuration.

Important fields:

- `input_dir`
- `output_dir`
- `report_path`
- `repair_simple_hyphenated_line_breaks`
- `preserve_punctuation`
- `preserve_quotes`
- `preserve_dashes`
- `preserve_dialect_spellings`
- `preserve_archaic_spellings`
- `warning_thresholds`
- `author_style_protection`

### `metadata/cleaning_report_schema.csv`

Step 4 schema for `logs/cleaning_report.csv`.

Expected columns:

- `source_text_path`
- `cleaned_text_path`
- `raw_chars`
- `cleaned_chars`
- `raw_words`
- `cleaned_words`
- `raw_lines`
- `cleaned_lines`
- `removed_artifact_lines`
- `char_loss_ratio`
- `word_loss_ratio`
- `warning_flags`

## Future datasets

The following datasets will be defined in later steps:

- `logs/cleaning_report.csv`
- `data/interim/cleaned_books/`
- `data/interim/candidate_passages.csv`
- `data/processed/original_passages.csv`
- `data/final/master_text_dataset.csv`
- `data/final/master_feature_dataset.csv`
- `data/final/master_results_dataset.csv`

## Naming rules

- `author_id`: lowercase stable identifier, e.g. `austen`, `poe`, `twain`, `wilde`, `dickens`, `shelley`.
- `work_id`: lowercase stable identifier derived from title.
- `passage_id`: stable identifier in the form `AUTHOR_WORK_####`.
- `condition`: one of `original`, `paraphrase`, `modernize`, `simplify`.

## Removed stale files

The earlier preliminary `metadata/text_extraction_manifest.csv` was removed in Step 3 because it contained stale extraction-state statuses after the source set changed. The current status is represented by `metadata/text_extraction_status_summary.csv`, `metadata/extracted_text_checksums_by_id.csv`, and `metadata/raw_file_checksums.csv`.

## Step status

Updated during Step 4. Not final.
