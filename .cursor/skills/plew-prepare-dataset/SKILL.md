---
name: plew-prepare-dataset
description: >-
  Profiles an arbitrary dataset and transforms it into PLeW-ready CSV with
  dim::, desc::, med::, and res:: columns, or writes PLEW_UNSUITABLE.md with
  reasons. Use when the user asks to make data ready for PLeW, convert
  eval/annotation/human-judgment data for PLeW-NLG, assess PLeW suitability,
  or prepare a dataset for the visualization grid and record window.
disable-model-invocation: true
---

# Prepare dataset for PLeW

Transform an unknown dataset into a flat, prefixed CSV that PLeW can explore,
or reject it with explicit reasons. **Do not hardcode benchmark-specific column
names.** Infer structure from shape, cardinality, and nesting.

## Quick start

**User invocation (primary):** e.g. *"make `eval-data-raw/summeval/` ready for PLeW"*

That phrase triggers this full workflow — not the helper scripts alone.

1. Identify **raw input** under `eval-data-raw/<dataset>/` (file or folder).
2. Run profiling: `python .cursor/skills/plew-prepare-dataset/scripts/profile.py <file>`
3. Read [plew-schema.md](plew-schema.md) and [reshape-patterns.md](reshape-patterns.md).
4. Decide suitability → transform or write `PLEW_UNSUITABLE.md`.
5. Write outputs under **`eval-data-processed/<dataset>/`** (mirror the raw folder name):
   - `<dataset>_plew_ready.csv` (e.g. `webnlg2017_humaneval_plew_ready.csv`)
   - `PLEW_MANIFEST.md`
   - `transform.py` (reproducible script; read raw from `eval-data-raw/`, write processed here)
6. Validate: `python .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py eval-data-processed/<dataset>/<dataset>_plew_ready.csv`

**Naming:** `<dataset>` = the folder basename under `eval-data-processed/`. Additional
tables use `<dataset>_plew_<variant>.csv` (e.g. `book_highlights_llm_as_a_judge_plew_faithfulness.csv`).

**Do not** write processed CSVs into `eval-data-raw/` — keep raw downloads immutable.

**Reference run:** `eval-data-raw/summeval/` → `eval-data-processed/summeval/summeval_plew_ready.csv`
(1,920 rows; melted per-annotator Likert scores; subset documented). Early runs may still
live under `eval-data-raw/`; migrate when re-processing.

## PLeW column roles (must follow)

| Prefix | Use for | Grid / panels | Record window |
|--------|---------|---------------|---------------|
| `dim::` | Low-cardinality categories for axes, color, panels | **Yes** | Yes |
| `desc::` | Long text, IDs as context, rationales, source/output text | No | **Yes** |
| `med::` | Image/audio/video paths or URLs | No | **Yes** (popup) |
| `res::` | Numeric scores, counts, continuous outcomes | **No** | **Yes** |

**Important:** `res::` values are **not** panel dimensions. They appear when the
user opens a record. Put exploratory facets in `dim::` (including binned bands
like `dim::score_band` when needed). Put raw Likert integers in both
`res::score` and `dim::score` only when cardinality is small (e.g. 1–5).

See [plew-schema.md](plew-schema.md) for heuristics and scale limits.

## Workflow

Copy and track:

```
- [ ] Ingest — detect format, encoding, multi-file layout
- [ ] Profile — row count, keys, cardinality, nesting, media
- [ ] Infer observation unit — state "one row = …"
- [ ] Suitability gate — pass / marginal / fail
- [ ] Reshape — melt, join, explode, resolve pairs (see reshape-patterns.md)
- [ ] Assign prefixes — dim / desc / med / res by role, not by name
- [ ] Subset if needed — document seed and strategy
- [ ] Validate CSV — run validate_plew_csv.py
- [ ] Write manifest
```

### 1. Ingest

Support: CSV, TSV, JSON array, JSON object-of-records, JSONL, HuggingFace-style
`{ rows: [{ row: … }] }`. For folders, list files, detect primary table vs
sidecar media, plan joins.

### 2. Profile

Use `scripts/profile.py` or equivalent. For each field note:

- `unique` / `unique_ratio` — high ratio → candidate `desc::` or ID, not `dim::`
- `avg_len` / `max_len` — long strings → `desc::`
- Nesting — objects/arrays → reshape before assign
- Media extensions in values → `med::`

### 3. Infer observation unit

Declare in manifest. Examples:

- one judgment (item × generator × criterion × annotator)
- one pairwise comparison × criterion
- one utterance in a dialogue

If the file mixes units, split or warn.

### 4. Suitability gate

**Pass** when all are true:

- ≥2 `dim::` columns can be assigned with cardinality ≤50 (after binning/melt)
- ≥1 `desc::` or `med::` column for record content
- Row count manageable (default cap 500–2000 for demo unless user wants full)
- Observation unit is clear

**Marginal** — proceed with warnings in manifest:

- Only one strong dimension (suggest melt or derived dims)
- Requires join across files (document match rate)
- Pairwise/blinded labels need resolution step
- Large file — subset applied

**Fail** — write `PLEW_UNSUITABLE.md` only (no CSV):

- All columns high-cardinality text → no grid structure
- Span/token-level only with no aggregation path user accepts
- Single-row schema sample
- Aggregate-only (no row-level records to inspect)
- Join impossible or match rate catastrophic

Use this rejection template:

```markdown
# Not suitable for PLeW

## Summary
- Input: …
- Format: …
- Rows: …
- Inferred unit: …

## Reasons
1. …

## What would make it suitable
- …
```

### 5. Reshape

Apply patterns from [reshape-patterns.md](reshape-patterns.md). Prefer **long
format** when multiple criteria, annotators, or repeated judgments exist.

General role assignment (after reshape):

- **dim::** — system, model, criterion, winner (resolved), error category,
  language pair, domain, annotator group, score band, boolean flags
- **desc::** — source text, generated text, rationale, prompt, item id (context)
- **med::** — local-relative image/audio paths
- **res::** — raw scores, severity, similarity, counts, timings

Always include stable **`ID`** as first column.

Optional: `dim::dataset` when merging sources.

### 6. Subset

If profiling shows too many rows:

- Prefer **stratified** sample on a planned `dim::` column
- Record random seed, N, filters in manifest
- Do not silently truncate without documenting

### 7. Deliverables

All outputs go in **`eval-data-processed/<dataset>/`** (same basename as the raw folder).

**Success:**

- `eval-data-processed/<dataset>/<dataset>_plew_ready.csv`
- `eval-data-processed/<dataset>/PLEW_MANIFEST.md` containing:
  - raw source path(s) under `eval-data-raw/` and date
  - observation unit
  - reshape operations performed
  - column mapping table (source field → prefixed column)
  - subset strategy if any
  - suggested grid encodings (which dims for X/Y/color)
  - known limitations
  - reproduce command (`python3 eval-data-processed/<dataset>/transform.py`)
- `eval-data-processed/<dataset>/transform.py` when reshape is non-trivial

**Failure:**

- `eval-data-processed/<dataset>/PLEW_UNSUITABLE.md` only

### 8. Validate

Run `validate_plew_csv.py`. Fix errors before finishing. Warnings may remain
if documented in manifest.

## Decision hints (structure, not names)

| Profile signal | Likely role |
|----------------|-------------|
| unique_ratio > 0.9, avg_len > 80 | `desc::` |
| unique 2–30, short tokens | `dim::` |
| integers 1–5 repeated across rows | `res::` + optional `dim::` |
| URL/path ending in media ext | `med::` |
| nested map of scores | melt → `dim::criterion`, `res::score` |
| two text fields + winner A/B | resolve → `dim::winner`, `desc::` both texts |

## Anti-patterns

- Leaving long unique strings unprefixed (PLeW heuristics may treat them as dims)
- Averaging annotators without user request (loses disagreement landscape)
- Plotting blind A/B without resolving to system/condition
- Putting must-see scores only in `res::` when user needs them as grid facets
  (use binned `dim::` for the grid, keep `res::` for exact value in record)
- Hardcoding dataset-specific column names in skill logic

## Examples (patterns only)

**Multi-criterion human scores (wide or nested):** melt to long; `dim::criterion`,
`dim::system`, `dim::annotator`, `res::score`, `desc::output`.

**Pairwise LLM/human preference:** one row per pair × criterion; resolve winner;
`dim::confidence`, `desc::candidate_a`, `desc::candidate_b`, `desc::rationale`.

**Error taxonomy eval:** one row per item × error category (or per annotator);
`dim::error_type`, `dim::system`, `res::count` or `dim::present`.

**Multimodal caption eval:** join captions + judgments + image paths;
`med::image`, `desc::caption`, `dim::judgment`, `res::score`.

## Additional resources

- [plew-schema.md](plew-schema.md) — prefix semantics and PLeW heuristics
- [reshape-patterns.md](reshape-patterns.md) — melt/join/explode decision tree
- `scripts/profile.py` — quick cardinality report
- `scripts/validate_plew_csv.py` — post-transform checks
