# Step 3 Raw Preservation Log

## Step

**Step 3 — Raw Text Preservation and Checksum Logging**

## Status

Complete for metadata-level preservation.

## What was preserved

The project now tracks **29 PDF source files**:

- 27 PDFs from the original `source.zip`
- 2 later uploaded Oscar Wilde PDFs

Because the available GitHub connector cannot stream large local binary PDF files into the repository, raw PDF preservation is performed by metadata and checksum rather than physical PDF upload.

## Preservation artifacts

- `metadata/source_inventory.csv`
- `metadata/raw_file_checksums.csv`
- `metadata/text_extraction_status_summary.csv`
- `docs/raw_source_handling.md`
- `logs/raw_preservation_log.md`

## Raw PDF binary status

Raw PDFs are **not physically committed** through this connector.

Required binary preservation route:

```bash
git lfs install
git lfs track "*.pdf"
git add .gitattributes data/raw/pdf/
git commit -m "Add raw PDF sources via Git LFS"
git push
```

## Text extraction status

A Step 3 extraction pass was performed locally using:

```text
pdftotext -layout -enc UTF-8
```

Summary:

- PDFs attempted: 29
- Successful text extractions: 29
- Failed or empty extractions: 0
- Total extracted word count: 8,245,542
- Total extracted text bytes: 44,782,448

The previous preliminary extraction manifest contained stale `not_extracted_yet` rows, so it was removed. The current compact status is stored in:

- `metadata/text_extraction_status_summary.csv`

## Important limitation

The full extracted text files are available locally in this session but are not yet physically committed as text files in GitHub. Future steps should either:

1. commit extracted text files in manageable batches, or
2. regenerate them from the raw PDFs using the documented extraction command once Git LFS raw PDFs are present.

## Step 3 conclusion

Step 3 establishes traceability for all current source PDFs by checksum and extraction status. It does not yet create cleaned research text; cleaning begins in Step 4.
