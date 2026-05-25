# Data Dictionary

This file is initialized in Step 1 and will be expanded as datasets are created.

## Expected dataset layers

### `metadata/source_inventory.csv`

Inventory of the uploaded raw PDFs.

Expected columns:

- `zip_path`
- `repo_target_path`
- `size_bytes`
- `sha256`
- `modified`

### `metadata/text_extraction_manifest.csv`

Preliminary status of text extraction from PDFs.

Expected columns:

- `source_pdf`
- `text_path`
- `status`
- `size_bytes`
- `chars`
- `words`
- `sha256`

### Future datasets

The following datasets will be defined in later steps:

- `metadata/author_work_map.csv`
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

## Step status

Initialized in Step 1. Not final.
