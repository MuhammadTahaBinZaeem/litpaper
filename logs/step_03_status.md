# Step 3 Status Report

## Step

**Step 3 — Raw Text Preservation and Checksum Logging**

## Status

Complete for metadata-level preservation and reproducible local extraction.

## Files created or updated

- `metadata/raw_file_checksums.csv`
- `metadata/text_extraction_status_summary.csv`
- `logs/raw_preservation_log.md`
- `logs/step_03_status.md`
- `scripts/00_preserve_sources.py`
- `docs/raw_source_handling.md`
- `docs/repo_audit.md`
- `logs/step_01_status.md`
- `docs/data_dictionary.md`

## Consistency repair performed before Step 3

Before starting Step 3, Step 1 and Step 2 files were rechecked for stale source references.

Updated stale files included:

- `docs/raw_source_handling.md`
- `docs/repo_audit.md`
- `logs/step_01_status.md`
- `docs/data_dictionary.md`

The earlier preliminary `metadata/text_extraction_manifest.csv` was removed because it still contained stale `not_extracted_yet` entries after the Wilde source updates. Current extraction status is now represented by:

- `metadata/text_extraction_status_summary.csv`
- `logs/raw_preservation_log.md`

## Current source inventory

The project now tracks:

- 29 total PDF sources
- 27 PDFs from the original `source.zip`
- 2 later uploaded Oscar Wilde PDFs

## Raw PDF preservation status

Raw PDFs are not physically committed to the repository through the available GitHub connector because the connector does not provide direct large binary upload support.

Current preservation method:

- source paths recorded
- intended repository paths recorded
- file sizes recorded
- page counts recorded
- SHA256 checksums recorded

Physical raw-PDF preservation still requires Git LFS from a local machine.

## Text extraction status

A local extraction pass was performed using:

```text
pdftotext -layout -enc UTF-8
```

Results:

- PDFs attempted: 29
- Successful text extractions: 29
- Failed or empty extractions: 0
- Total extracted word count: 8,245,542
- Total extracted text bytes: 44,782,448

## Connector limitation encountered

A full detailed extracted-text checksum table was generated locally, but repeated attempts to commit it were blocked by the connector safety layer. To avoid leaving stale or false metadata, the older preliminary extraction manifest was deleted and replaced by a compact summary file.

The current committed source-preservation truth is:

- `metadata/raw_file_checksums.csv` for raw PDF checksums
- `metadata/text_extraction_status_summary.csv` for extraction status summary
- `logs/raw_preservation_log.md` for the human-readable preservation log
- `scripts/00_preserve_sources.py` for local regeneration

## Important source decisions preserved

- `Lord Arthur Savile’s Crime and Other Stories - Oscar Wilde - PDF Room.pdf` is accepted as the current usable Wilde prose-fiction source after extraction validation.
- `THE PICTURE OF DORIAN GRAY.pdf` is excluded because it is a retelling/adaptation, not Wilde's original prose.
- `Complete works of Oscar Wilde (1921) 6.pdf` remains excluded from the main corpus because it is drama.

## Step 3 completion judgment

Step 3 is complete at the metadata and reproducibility level. The source set is now internally consistent across Step 1, Step 2, and Step 3 documentation.

## Next step

Step 4 should define and apply deterministic cleaning rules. It must not over-clean punctuation, sentence rhythm, dialect-like prose, archaism, or other stylistic signals because those are central to the paper.
