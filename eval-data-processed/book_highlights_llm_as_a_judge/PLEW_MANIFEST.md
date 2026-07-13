# PLeW manifest — Book highlights (LLM-as-judge)

Prepared: 2026-07-11  
Source: `eval-data-raw/book_highlights_llm_as_a_judge/`  
Output: `eval-data-processed/book_highlights_llm_as_a_judge/`

## Suitability

**Pass (pairwise preference).** LLM A/B judgments on generated book highlights with
five criteria plus overall preference, resolved winners, and inspectable candidate
text. **Marginal (faithfulness)** — raw file contains a single schema example only;
exported separately as `book_highlights_llm_as_a_judge_plew_faithfulness.csv` (1 row).

## Observation unit

| File | One row = |
|------|-----------|
| `book_highlights_llm_as_a_judge_plew_ready.csv` | one LLM criterion judgment for a pairwise comparison (pair × criterion, including `overall`) |
| `book_highlights_llm_as_a_judge_plew_faithfulness.csv` | one LLM faithfulness check for a single highlight |

## Reshape operations

### Pairwise preference (`llm_judge_preference.json`)

1. Loaded JSON dict (5,448 pairwise records keyed by `pair_id`).
2. Stratified subset: 300 pairs (seed 42), balanced across `comparison_axis`
   (`architecture` / `size`).
3. Melted nested `criteria` object to long format (`dim::criterion`).
4. Appended `overall` rows from `overall_preference`.
5. Resolved blind winners (`A`/`B`/`tie`/`neither`) to system labels
   (`e2e`, `pipeline`, `small`, `large`) using `candidate_*_source_side`.
6. Assigned prefixes by role (see mapping below).

### Faithfulness (`llm_judge_faithfulness.json`)

1. Loaded JSON dict (1 record).
2. Mapped scalar fields to `dim::` / `desc::` / `res::` without reshape.

## Subset

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Pairs sampled | 300 of 5,448 |
| Stratify on | `comparison_axis` (150 architecture + 150 size) |
| Criteria per pair | 6 (5 criteria + overall) |
| `book_highlights_llm_as_a_judge_plew_ready.csv` rows | 1,800 |

Full melt of all pairs would be ~32,700 rows; subset keeps within demo scale.

## Column mapping — `book_highlights_llm_as_a_judge_plew_ready.csv`

| Output column | Source |
|---------------|--------|
| `ID` | generated `bookhl-pref-{n}` |
| `dim::criterion` | melted criterion name (+ `overall`) |
| `dim::winner_blind` | `criteria[*].winner` or `overall_preference.winner` |
| `dim::winner_resolved` | resolved from winner + `candidate_*_source_side` |
| `dim::confidence` | per-criterion or overall confidence |
| `dim::comparison_axis` | `metadata.comparison_axis` |
| `dim::book` | `book_title` |
| `dim::theme` | `theme` |
| `dim::relation` | `metadata.relation` |
| `dim::candidate_a_side` | `candidate_a_source_side` |
| `dim::candidate_b_side` | `candidate_b_source_side` |
| `dim::sampling_mode` | `metadata.sampling_mode` |
| `desc::pair_id` | `pair_id` |
| `desc::book_id` | `book_id` |
| `desc::book_title` | `book_title` |
| `desc::author` | `author` |
| `desc::asin` | `metadata.asin` |
| `desc::candidate_a` | `metadata.candidate_a_text` |
| `desc::candidate_b` | `metadata.candidate_b_text` |
| `desc::candidate_a_title` | `metadata.candidate_a_title` |
| `desc::candidate_b_title` | `metadata.candidate_b_title` |
| `desc::sample_name` | `metadata.sample_name` |
| `desc::rationale` | criterion or overall rationale |
| `desc::dominant_factors` | `overall_preference.dominant_factors` (overall rows only) |
| `res::similarity` | `metadata.similarity` |
| `res::review_count` | `metadata.review_count` |

## Column mapping — `book_highlights_llm_as_a_judge_plew_faithfulness.csv`

| Output column | Source |
|---------------|--------|
| `ID` | generated `bookhl-faith-{n}` |
| `dim::book` | `book_title` |
| `dim::theme` | `theme` |
| `dim::relation` | `relation` |
| `dim::system` | `system` |
| `dim::model` | `model` |
| `dim::size_label` | `size_label` |
| `dim::factually_accurate` | `factually_accurate` |
| `dim::divergence_type` | `divergence_type` |
| `res::severity` | `severity` (1–5) |
| `desc::highlight_id` | `highlight_id` |
| `desc::pair_id` | `pair_id` (links to preference records) |
| `desc::book_id` | `book_id` |
| `desc::book_title` | `book_title` |
| `desc::author` | `author` |
| `desc::asin` | `asin` |
| `desc::rationale` | `rationale` |

## Suggested grid encodings

**Pairwise preference (`book_highlights_llm_as_a_judge_plew_ready.csv`):**

- **Grid X:** `comparison_axis`
- **Grid Y:** `criterion`
- **Color:** `winner_resolved` or `confidence`
- **Panel:** `book` or `theme` (filter recommended for dense panels)

**Faithfulness (`book_highlights_llm_as_a_judge_plew_faithfulness.csv`):**

- Demo only (1 row). Use record window; grid not meaningful until more records exist.

## Known limitations

- Source book/review text is not included — only generated highlight candidates.
- `dim::theme` mixes relation types (`author`, `previousWork`, …) with free-text
  theme labels from some books (46 values in subset).
- Faithfulness export is a schema placeholder (1 of 5,448+ potential checks).
- `pair_id` links preference and faithfulness records but only one faithfulness
  example is present in raw data.

## Reproduce

```bash
python3 eval-data-processed/book_highlights_llm_as_a_judge/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/book_highlights_llm_as_a_judge/book_highlights_llm_as_a_judge_plew_ready.csv
```
