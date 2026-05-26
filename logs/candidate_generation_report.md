# Step 7 Candidate Generation Report

## Status

Candidate generation was executed locally using the committed sentence-aware Step 6 extraction scaffold.

## Overall counts

- total candidate rows: 10417
- passing length/sentence candidates: 10414
- failed length candidates: 0
- failed low-sentence candidates: 3

## Passing candidates by author

- austen: 1896 PASS
- dickens: 5242 PASS
- poe: 804 PASS
- shelley: 2265 PASS
- twain: 153 PASS
- wilde: 54 BELOW_120_TARGET

## Critical Step 7 finding

The candidate pool is large overall, but Wilde does not meet the Step 6 target of at least 120 candidate passages per author. Wilde produced only 54 passing candidates from the currently usable prose source. This is also below the eventual final target of 60 passages, so Step 8 final selection cannot honestly proceed for a balanced six-author corpus unless an additional original Wilde prose source is added or the protocol is revised.

## Output artifacts

Large candidate outputs were generated locally and packaged. Because the full candidate passage CSV includes passage text and is around 35 MB, the public GitHub connector may not reliably commit it inline. The repository preserves checksums, counts, and a local handoff archive until Git LFS or another data-release route is used.

- candidate_passages.csv SHA256: `e43248da24b4686f4fe3f4122083283054ed9ec5b0bd54ae3c3afb8d15fed4c7`
- candidate_passage_metadata.csv SHA256: `8f4dbe7c2c4d394d5c96f538ab71d782e5ea0eafe3b67cb7aa1c6c08a599a833`

## Step 7 conclusion

Step 7 was executed, but it does not fully pass the planned balance-readiness threshold because Wilde is under target. This must be resolved before honest Step 8 final passage selection.
