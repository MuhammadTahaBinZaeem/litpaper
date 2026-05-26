# Raw source handling note

The original uploaded `source.zip` contained 27 PDF files totaling 162,141,311 bytes. Two additional Oscar Wilde PDFs were uploaded later, bringing the current tracked source inventory to **29 PDF files**.

The GitHub connector available in this chat can create/update UTF-8 text files, but it does not expose a direct local binary-file streaming upload action for large PDFs.

For traceability, this repository stores:

1. `metadata/source_inventory.csv` — exact source paths, planned repository paths, byte sizes, modification timestamps/notes, and SHA256 checksums for all tracked PDFs.
2. `metadata/raw_file_checksums.csv` — Step 3 raw-file preservation checksum table with page counts and preservation status.
3. `metadata/text_extraction_manifest.csv` — current text extraction status for all tracked PDFs.
4. `metadata/extracted_text_checksums.csv` — Step 3 extracted-text checksum table.

Recommended raw-PDF preservation route outside this connector:

```bash
mkdir -p data/raw/pdf
unzip source.zip -d /tmp/litpaper_source
rsync -av /tmp/litpaper_source/source/ data/raw/pdf/
# manually copy the two later Wilde PDFs into data/raw/pdf/Oscarwilde/
git lfs install
git lfs track "*.pdf"
git add .gitattributes data/raw/pdf metadata/source_inventory.csv metadata/raw_file_checksums.csv
git commit -m "Add raw PDF sources via Git LFS"
git push
```

For the actual research pipeline, text extracted from the PDFs should be used as the computational source, while the raw PDFs remain auditable by checksum.

## Current source status after Step 3

- Current tracked PDFs: 29
- Original ZIP PDFs: 27
- Later uploaded Wilde PDFs: 2
- Raw PDFs physically uploaded to GitHub through connector: no, binary upload unsupported by connector
- Raw PDF traceability status: inventoried by path, size, page count, and SHA256 checksum
- Text extraction tool used in Step 3: `pdftotext -layout -enc UTF-8`
- Text extraction status after Step 3: 29/29 extracted locally and checksummed

## Important source decisions

- `Lord Arthur Savile’s Crime and Other Stories - Oscar Wilde - PDF Room.pdf` is accepted as a usable Wilde prose-fiction source after extraction validation.
- `THE PICTURE OF DORIAN GRAY.pdf` is excluded because it is an Oxford Bookworms retelling by Jill Nevile, not Wilde's original prose.
- `Complete works of Oscar Wilde (1921) 6.pdf` remains excluded from the main corpus because it is a drama volume.
