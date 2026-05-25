# Step 1 Repository Audit

## Project

**Repository:** `MuhammadTahaBinZaeem/litpaper`  
**Default branch:** `main`  
**Visibility:** public  
**Research title:** *Authorial Style Separability Loss in LLM-Rewritten Fiction: A Controlled Stylometric Framework for Measuring Literary Style Flattening*

## Step 1 purpose

Step 1 establishes the repository as a reproducible research workspace. It does **not** perform cleaning, passage extraction, rewriting, feature extraction, or analysis. Its job is to preserve the current source-state information, create the project skeleton, and define the rules for the remaining 19 steps.

## Current repository state before Step 1 hardening

The repository was initialized with:

- `README.md`
- `metadata/source_inventory.csv`
- `metadata/text_extraction_manifest.csv`
- `docs/raw_source_handling.md`

These files record the uploaded source archive inventory and the current limitation that large binary PDFs could not be uploaded through the available GitHub connector.

## Uploaded source archive summary

The uploaded archive inspected in this session was:

- Local file: `/mnt/data/source.zip`
- Files found: 27 PDFs
- Total uncompressed PDF bytes: 162,141,311
- Top-level archive folder: `source/`
- Author folders detected:
  - `austenJane/`
  - `CharlesDicken/`
  - `EdgarPoe/`
  - `Marktwain/`
  - `Marryshelly/`
  - `Oscarwilde/`

The detailed file-level inventory is stored in:

- `metadata/source_inventory.csv`

## Raw PDF status

Raw PDFs are **not yet committed into the repository**. The available GitHub connector in this chat can write UTF-8 text files but does not expose a direct local binary-file upload action for large PDFs. Because of this, Step 1 preserves traceability through file names, sizes, timestamps, and SHA256 checksums rather than pretending the PDF upload succeeded.

Recommended raw-PDF preservation route:

```bash
git lfs install
git lfs track "*.pdf"
mkdir -p data/raw/pdf
unzip source.zip -d /tmp/litpaper_source
rsync -av /tmp/litpaper_source/source/ data/raw/pdf/
git add .gitattributes data/raw/pdf metadata/source_inventory.csv
git commit -m "Add raw PDF sources via Git LFS"
git push
```

## Text extraction status

A preliminary local extraction attempt produced text-status metadata for the PDFs. The extraction status is stored in:

- `metadata/text_extraction_manifest.csv`

Important: Step 1 does not treat these extracted texts as final research data. Text extraction, cleaning, and validation are handled later in the pipeline.

## Project skeleton added in Step 1

The repository is organized around this intended structure:

```text
data/
  raw/
    pdf/
    text_extracted/
  interim/
  processed/
    original_passages/
    rewrites/
    features/
  final/
metadata/
scripts/
notebooks/
results/
  tables/
  figures/
logs/
docs/
```

Because Git does not track empty directories, `.gitkeep` files are used where necessary.

## Research direction locked for the repository

The repository is for one paper only:

> **Authorial Style Separability Loss in LLM-Rewritten Fiction: A Controlled Stylometric Framework for Measuring Literary Style Flattening**

Core research question:

> How do controlled LLM rewriting operations affect measurable authorial style separability across lexical, syntactic, rhythmic, and distributional stylometric dimensions in public-domain fiction?

Mandatory methods:

- Burrows’ Delta
- function-word analysis
- sentence-length distributions
- POS distributions
- inter-author distance
- statistical testing
- author-specific literary interpretation

Locked main authors:

- Jane Austen
- Edgar Allan Poe
- Mark Twain
- Oscar Wilde
- Charles Dickens
- Mary Shelley

Locked rewriting tasks:

1. Paraphrase
2. Modernize
3. Simplify

Summarization is not part of the main experiment because it introduces a major length confound.

## Step 1 completion criteria

Step 1 is complete when the repository contains:

- project README
- raw source inventory
- raw source handling note
- text extraction status manifest
- repository audit
- 20-step pipeline protocol
- initial data dictionary stub
- reproducibility stub
- directory skeleton
- environment/dependency stub
- clear statement of what has and has not been uploaded

## Step 1 limitations

- Raw PDFs are inventoried but not physically uploaded through this connector.
- Text extraction metadata is preliminary and not final.
- No cleaned corpus exists yet.
- No final passage dataset exists yet.
- No LLM rewrites exist yet.
- No stylometric features or results exist yet.

## Next step

Step 2 should create the formal author-work map from the source inventory and decide which works are eligible for the main six-author corpus.
