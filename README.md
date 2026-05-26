# litpaper

Repository for the research project **Authorial Style Separability Loss in LLM-Rewritten Fiction**.

This repository contains a traceable, reproducible dataset-building and analysis pipeline for measuring how LLM rewriting affects computationally detectable author-specific literary style signals.

## Locked research direction

**Title:** Authorial Style Separability Loss in LLM-Rewritten Fiction: A Controlled Stylometric Framework for Measuring Literary Style Flattening

**Core research question:** How do controlled LLM rewriting operations affect measurable authorial style separability across lexical, syntactic, rhythmic, and distributional stylometric dimensions in public-domain fiction?

## Current canonical source layer

The preferred source layer is now **Project Gutenberg plain text**.

The earlier PDF-derived source layer remains in the repository as a legacy audit trail, but final passage selection should use the canonical Gutenberg layer.

Canonical Gutenberg registry:

```text
metadata/gutenberg_canonical_registry.csv
```

Short filename alias map:

```text
metadata/gutenberg_alias_map.csv
```

The alias map uses names such as `author1_work1`, `author1_work2`, and so on. The exact author, work title, Gutenberg ID, and URL are stored in the CSV, so file paths stay stable while provenance remains exact.

## Current pipeline status

### Legacy PDF source layer

Steps 1–7 were implemented for the originally uploaded PDF layer. That layer exposed a source-balance problem: Wilde had only 54 candidate passages, below the 120-candidate target and below the eventual 60-passage final-selection target.

The PDF-derived layer is now treated as legacy audit material only.

### Canonical Gutenberg source layer

The Gutenberg migration fixes the source-provenance and Wilde-balance problem.

Current Gutenberg Step 7 status:

```text
Austen: 395 candidates
Dickens: 471 candidates
Poe: 255 candidates
Shelley: 342 candidates
Twain: 252 candidates
Wilde: 164 candidates
Total: 1879 candidates
```

All six authors meet the minimum 120-candidate target.

### Final selected original-passage layer

Step 8 selected the balanced original-passage layer.

```text
Austen: 60 selected original passages
Dickens: 60 selected original passages
Poe: 60 selected original passages
Shelley: 60 selected original passages
Twain: 60 selected original passages
Wilde: 60 selected original passages
Total: 360 selected original passages
```

Each author contributes two works. Each work contributes 30 selected passages.

## Important generated files

### Source/provenance

```text
metadata/gutenberg_canonical_registry.csv
metadata/gutenberg_alias_map.csv
metadata/gutenberg_raw_text_checksums.csv
metadata/gutenberg_cleaned_text_checksums.csv
```

### Cleaning and validation

```text
metadata/gutenberg_cleaning_summary.csv
metadata/gutenberg_cleaning_validation_metrics.csv
metadata/gutenberg_author_summary.csv
logs/gutenberg_cleaning_report.csv
```

### Candidate generation

```text
metadata/gutenberg_candidate_generation_summary.csv
metadata/gutenberg_candidate_counts_by_author.csv
metadata/gutenberg_candidate_counts_by_source.csv
metadata/gutenberg_candidate_passage_metadata.csv
logs/gutenberg_candidate_generation_report.md
logs/step_07_gutenberg_status.md
```

### Candidate text as Markdown

The full Gutenberg candidate passage CSV contains passage text. To make the text repository-visible without fragile single-file uploads, the pipeline exports candidate text into chunked Markdown files:

```text
data/interim/gutenberg_candidate_passages_md/
```

Exporter script:

```text
scripts/06_export_gutenberg_candidates_md.py
```

### Final selected original passages

```text
scripts/07_select_final_passages.py
metadata/selection_summary.csv
metadata/selected_counts_by_author.csv
metadata/selected_counts_by_work.csv
metadata/selection_filter_report.csv
metadata/step8_output_manifest.csv
logs/step_08_status.md
```

The final selected passage text is generated locally into:

```text
data/processed/selected_original_passages.csv
data/processed/selected_passages_md/
```

## Rebuild commands

From a fresh clone with internet access:

```bash
python scripts/04_fetch_gutenberg_sources.py
python scripts/05_run_canonical_migration.py
python scripts/06_export_gutenberg_candidates_md.py
python scripts/check_gutenberg_steps_01_07_consistency.py
python scripts/07_select_final_passages.py
```

Expected Step 1–7 checker result:

```text
PASS: Gutenberg canonical Steps 1-7 are internally consistent and balance-ready.
```

Expected Step 8 result:

```text
360 selected original passages
```

## Change record

### Step 1 — Repository audit and skeleton

Created the project structure, audit documents, dependency files, source inventory, and reproducibility notes.

### Step 2 — Author/work map

Locked the six-author design and mapped candidate works for Austen, Dickens, Poe, Twain, Shelley, and Wilde.

### Step 3 — Source preservation

Generated source-level checksum and extraction metadata for the originally uploaded PDF layer. The preliminary stale extraction manifest was removed.

### Step 4 — Conservative cleaning

Added and verified a conservative text cleaner designed to preserve style-bearing signals such as punctuation, quotation, dashes, sentence rhythm, contractions, dialect-like spelling, and archaic spelling.

### Step 5 — Cleaning validation

Validated whole-source cleaned texts for style-bearing signals. A later audit corrected the legacy PDF count from 24 eligible / 5 excluded to 22 eligible / 7 excluded.

### Step 6 — Passage extraction protocol

Defined sentence-aware, non-overlapping candidate extraction with a preferred 450–650 word range, hard 400–700 word bounds, and a 150-word gap between same-source candidates.

### Step 7 — Legacy PDF candidate generation

Generated the PDF-derived candidate pool. This revealed a Wilde shortage, so the PDF layer was not accepted for final Step 8 selection.

### Step 7B — Gutenberg canonical migration

Migrated the source layer to Project Gutenberg plain text. Added canonical registry, alias map, raw checksums, cleaned checksums, validation summaries, candidate summaries, and a Gutenberg-specific consistency checker.

### Step 7C — Candidate text Markdown export

Added a script to export the full Gutenberg candidate text into chunked Markdown files so the passage text can be kept in a repository-readable form.

### Step 8 — Final balanced original-passage selection

Selected 360 original passages: 60 per author, 30 per work, across 12 canonical Gutenberg works. The selected original layer is ready for controlled rewriting conditions.

## Next step

Proceed to **Step 9 — controlled rewriting prompt protocol** for paraphrase, modernize, and simplify conditions.
