# Step 2 Status Report

## Step

**Step 2 — Corpus Inventory and Author-Work Map**

## Status

Complete, with one important source gap.

## Files created

- `metadata/author_work_map.csv`
- `metadata/source_item_review.csv`
- `docs/corpus_selection_rationale.md`
- `logs/step_02_status.md`

## What Step 2 did

Step 2 converted the uploaded source inventory into a formal author/work map for the six-author literary corpus.

The main corpus remains focused on English prose fiction, not poetry, drama, essays, travel writing, letters, biography, or mixed editorial matter.

## Locked target authors

- Jane Austen
- Edgar Allan Poe
- Mark Twain
- Oscar Wilde
- Charles Dickens
- Mary Shelley

## Target corpus size

The intended original corpus remains:

```text
6 authors × 60 passages = 360 original passages
```

Each passage should later be extracted at approximately:

```text
450–650 words
```

## Main work candidates after Step 2

| Author | Main candidate works/status |
|---|---|
| Jane Austen | `Pride and Prejudice`, `Emma` from complete-works PDF |
| Charles Dickens | `Great Expectations`, `Oliver Twist` from individual PDFs |
| Edgar Allan Poe | selected prose fiction tales from complete-works PDF |
| Mark Twain | `Adventures of Huckleberry Finn` from uploaded volume |
| Mary Shelley | `Frankenstein` 1818 and `The Last Man` from complete-works PDF |
| Oscar Wilde | **source gap:** current PDF appears to be drama, not prose fiction |

## Major finding

The uploaded Oscar Wilde PDF appears to be a drama volume beginning with `Lady Windermere's Fan`. Since the main corpus is prose fiction, this source is not suitable for the main study.

Required fix before final passage extraction:

```text
Add a public-domain prose fiction source for Oscar Wilde, preferably The Picture of Dorian Gray.
```

Desired backup:

```text
Lord Arthur Savile's Crime and Other Stories
```

## Other notes

- Austen, Shelley, and Poe are stored as complete/container PDFs, so later steps must extract internal work boundaries.
- Dickens has many individual PDFs and is source-rich.
- Twain appears to have one usable main source, `Huckleberry Finn`; a second Twain work would improve balance but is not strictly required if 60 passages can be extracted cleanly.
- Some Dickens short works or previously failed extraction files need rechecking in Step 3/Step 4.

## Step 2 completion judgment

Step 2 is complete because the repository now contains a formal author-work map, source-level decisions, and corpus-selection rationale.

The project may proceed to Step 3, but Wilde should be treated as a known source gap until a proper prose-fiction source is added.
