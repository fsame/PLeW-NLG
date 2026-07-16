# PLeW manifest — FRANK factuality benchmark

Prepared: 2026-07-16  
Source: `eval-data-raw/frank/` ([artidoro/frank](https://github.com/artidoro/frank))  
Paper: [Pagnoni et al., NAACL 2021](https://arxiv.org/pdf/2104.13346)

## Suitability

**Pass.** FRANK ships two complementary human-evaluation tables:

| Raw file | PLeW output | Unit |
|----------|-------------|------|
| `human_annotations_sentence.json` | `frank_plew_sentence.csv` | sentence × annotator × error tag |
| `human_annotations.json` | `frank_plew_summary.csv` | article × model summary (aggregate) |

Use **sentence** for rater disagreement and per-sentence drill-down. Use **summary** for
system-level factuality and category-level error presence across a whole summary.

## Shared subset

Both outputs use the same sampled articles and models so views stay aligned.

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Articles sampled | 50 of 499 |
| Models sampled | 6 of 9 |
| Summaries retained | 146 |

---

## File 1: `frank_plew_sentence.csv`

### Observation unit

**One row = one error label** assigned by one annotator to one summary sentence.

### Reshape

1. Loaded `human_annotations_sentence.json`.
2. Joined `human_annotations.json` for `dataset` and summary-level `Factuality`.
3. Exploded `summary_sentences_annotations` (multi-label sentences → multiple rows).

### Output

**1,138 rows** (full release ≈ 15,961 exploded rows).

### Key columns

| Column | Role |
|--------|------|
| `dim::error_type`, `dim::error_group` | error tag and mapped group |
| `dim::annotator_index` | rater 1–3 |
| `dim::sentence_index` | sentence within summary |
| `desc::summary_sentence` | rated sentence |
| `res::factuality` | summary-level score (repeated) |

### Suggested grid

- **Grid X/Y:** `model` × `error_type`
- **Panel:** `annotator_index` or `article_id`
- **Filter:** exclude `NoE`

---

## File 2: `frank_plew_summary.csv`

### Observation unit

**One row = one model summary** (article × model), with aggregate human scores.

### Reshape

1. Loaded `human_annotations.json` (2,246 summaries).
2. Joined `benchmark_data.json` for article, summary, and reference text.
3. Added `dim::factuality_band` (`high` / `medium` / `low`) from `Factuality`.
4. For each error category, kept raw score in `res::` and a grid-friendly
   `dim::{category}_clear` (`yes` / `no`).

**FRANK encoding:** category score **1** = no error of that type in the summary;
**0** = that error appeared in every sentence. So `{category}_clear = yes` means
error-free for that category.

### Output

**146 rows**.

### Key columns

| Column | Role |
|--------|------|
| `dim::factuality_band` | binned overall factuality |
| `res::factuality` | continuous 0–1 score |
| `res::RelE`, `res::EntE`, … | raw category scores |
| `dim::RelE_clear`, … | `yes` if no errors of that type |
| `desc::summary`, `desc::article`, `desc::reference` | full texts |

### Suggested grid

- **Grid X/Y:** `model` × `factuality_band`
- **Color:** `Semantic_Frame_Errors_clear` or fine-grained `EntE_clear`
- **Panel:** `dataset` or `split`

---

## Error typology (sentence tags)

| Code | Label | Group |
|------|-------|-------|
| `NoE` | No error | `no_error` |
| `RelE` | Relation error | `semantic_frame` |
| `EntE` | Entity error | `semantic_frame` |
| `CircE` | Circumstantial error | `semantic_frame` |
| `OutE` | Out-of-article error | `semantic_frame` |
| `CorefE` | Coreference error | `discourse` |
| `LinkE` | Discourse link error | `discourse` |
| `GramE` | Grammar error | `content_verifiability` |
| `OtherE` / `Other` | Other error | `other` |

## Reproduce

```bash
python3 eval-data-processed/frank/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/frank/frank_plew_sentence.csv
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/frank/frank_plew_summary.csv
```

Site copies: `static/data/frank_sentence.csv`, `static/data/frank_summary.csv`.
