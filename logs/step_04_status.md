# Step 4 Status Report

## Step

**Step 4 — Text Cleaning Rules and Metadata Removal**

## Status

Implemented as a deterministic, reproducible cleaning layer. Actual cleaned text generation is ready to run once extracted text files are present in `data/raw/text_extracted/` or regenerated locally from raw PDFs.

## Files created or updated

- `docs/cleaning_rules.md`
- `metadata/cleaning_config.json`
- `metadata/cleaning_report_schema.csv`
- `scripts/01_clean_texts.py`
- `docs/data_dictionary.md`
- `logs/step_04_status.md`

## What Step 4 implemented

Step 4 added a conservative cleaning protocol designed for stylometric research. The cleaner removes obvious PDF/source artifacts while preserving authorial style signals.

The cleaner is designed to preserve:

- punctuation
- quotation marks
- apostrophes
- em dashes / dash-like punctuation
- ellipses
- contractions
- archaic spelling
- dialect-like spelling
- paragraph breaks
- sentence rhythm
- long sentence structures

The cleaner explicitly avoids:

- lowercasing all text
- removing punctuation
- removing quotation marks
- standardizing dialect spelling
- modernizing spelling
- sentence-tokenizing and destructively rejoining prose
- removing semicolons/dashes/exclamation marks

## Why conservative cleaning matters

The paper studies authorial style separability. Over-cleaning would damage the exact signals needed for later experiments, especially:

- Austen's irony-bearing syntax
- Poe's punctuation intensity
- Twain's colloquial rhythm
- Wilde's aphoristic compression
- Dickens's descriptive accumulation
- Shelley's Gothic register

## Cleaning script

The cleaning script is:

```text
scripts/01_clean_texts.py
```

Expected input:

```text
data/raw/text_extracted/**/*.txt
```

Expected output:

```text
data/interim/cleaned_books/**/*.txt
```

Expected report:

```text
logs/cleaning_report.csv
```

## Cleaning report schema

The report schema is documented in:

```text
metadata/cleaning_report_schema.csv
```

It includes:

- raw and cleaned character counts
- raw and cleaned word counts
- raw and cleaned line counts
- removed artifact line count
- character-loss ratio
- word-loss ratio
- warning flags

## Current limitation

The extracted text files are not physically committed in GitHub yet. Step 3 preserved extraction checksums and status, and Step 4 now provides the deterministic cleaning layer. To run cleaning, the user must either:

1. place/regenerate extracted text files under `data/raw/text_extracted/`, or
2. add raw PDFs with Git LFS and run the preservation/extraction script before cleaning.

## Step 4 completion judgment

Step 4 is complete as a reproducible cleaning-rule and script implementation. The actual cleaned text outputs are deferred until extracted text files are present in the repo or local working tree.

## Next step

Step 5 should perform author-specific cleaning validation after the cleaner has been run on extracted texts. It should verify that cleaning did not damage punctuation, rhythm, dialogue, archaic spelling, dialect-like prose, or other style-bearing features.
