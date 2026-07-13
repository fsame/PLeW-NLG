# PLeW manifest — SimpEval (LENS)

Prepared: 2026-07-12  
Source: `eval-data-raw/simpeval/LENS/data/simpeval_past.csv`  
Output: `eval-data-processed/simpeval/simpeval_plew_ready.csv`

## Suitability

**Pass.** Human simplification evaluation (Rank & Rate, 0–100 overall quality) with five
raters per (source sentence × system), plus inspectable original and simplified text.
Scores are binned into five bands for grid-friendly `dim::score_band`; raw scores kept
in `res::score`.

**Marginal note:** Other files in `eval-data-raw/simpeval/LENS/data/` (`simpeval_2022.csv`
with `sentence_type`, `simplikert_2022.csv` with multi-criterion Likert) are not merged
here; they can be transformed separately if needed.

## Observation unit

**One row = one human score** for a (source sentence × system × rater) combination.

## Reshape operations

1. Loaded `simpeval_past.csv` (2,400 rows; 100 ASSET source sentences × 24 systems).
2. Subset: 20 sentences × 6 systems (seed 42), random sample without stratification.
3. Melted `rating_1`…`rating_5` (and matching z-scores) into long format
   (`dim::annotator_index` 1–5).
4. Binned 0–100 scores into `dim::score_band` (five quintile-like bands).
5. Used `processed_generation` for `desc::simplification` when present.

## Subset

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Sentences sampled | 20 of 100 |
| Systems sampled | 6 of 24 |
| Input rows after filter | 120 (sentence × system) |
| Output rows | 600 (× 5 raters) |

Full melt of entire file would be ~12,000 rows; subset keeps within demo scale.

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `simpeval-{n}` |
| `dim::system` | `system` |
| `dim::sentence_id` | `original_id` |
| `dim::annotator_index` | melted from `rating_1`…`rating_5` (1–5) |
| `dim::score_band` | binned from raw score |
| `res::score` | `rating_1`…`rating_5` (0–100) |
| `res::z_score` | matching `rating_*_z_score` |
| `desc::original` | `original` |
| `desc::simplification` | `processed_generation` (fallback `generation`) |
| `desc::generation_raw` | `generation` (uncased model output) |

## Suggested grid encodings

- **Grid X:** `system`
- **Grid Y:** `score_band` or `annotator_index`
- **Color:** `score_band` (or bin `res::score` via filters)
- **Panel:** `sentence_id` (filter recommended — 20 values)

Compare rater disagreement within (sentence, system) via `annotator_index` panels.

## Known limitations

- Scores are 0–100 (not 1–5 Likert); grid uses `dim::score_band` rather than raw score.
- `dim::sentence_id` is opaque; use record window for source and simplification text.
- Only `simpeval_past.csv` is included; 2022 splits with `sentence_type` are separate files.
- One row has empty `generation` in the raw release (~1 of 2,400).

## Reproduce

```bash
python3 eval-data-processed/simpeval/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/simpeval/simpeval_plew_ready.csv
```
