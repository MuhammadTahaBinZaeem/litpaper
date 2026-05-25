# Raw source handling note

The uploaded `source.zip` contains 27 PDF files totaling 162,141,311 bytes. The GitHub connector available in this chat can create/update UTF-8 text files, but it does not expose a direct local binary-file streaming upload action for large PDFs.

For traceability, this repository stores:

1. `metadata/source_inventory.csv` — exact ZIP paths, planned repository paths, byte sizes, modification timestamps, and SHA256 checksums for all PDFs.
2. `metadata/text_extraction_manifest.csv` — extracted-text status and checksums for text extracted from the PDFs where extraction completed.

Recommended raw-PDF preservation route outside this connector:

```bash
mkdir -p data/raw/pdf
unzip source.zip -d /tmp/litpaper_source
rsync -av /tmp/litpaper_source/source/ data/raw/pdf/
git lfs install
git lfs track "*.pdf"
git add .gitattributes data/raw/pdf metadata/source_inventory.csv
git commit -m "Add raw PDF sources via Git LFS"
git push
```

For the actual research pipeline, text extracted from the PDFs should be used as the computational source, while the raw PDFs remain auditable by checksum.

## Current extraction status from this session

- Source PDFs in ZIP: 27
- Total raw PDF bytes: 162,141,311
- Text files extracted locally before timeout: 23
- PDFs not extracted locally yet: Austen complete works, Mark Twain complete works, Mary Shelley complete works, Oscar Wilde complete works
- Some short Dickens PDFs appear as empty/failed in the extraction manifest and should be rechecked in Step 1/Step 4.
