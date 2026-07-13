# PLeW manifest — SEAHORSE

Prepared: 2026-07-12  
Source: `eval-data-raw/seahorse/seahorse_data/validation.tsv`  
Output: `eval-data-processed/seahorse/seahorse_plew_ready.csv`

## Suitability

**Pass.** Multilingual summarization human evaluation with Yes/No/Unsure ratings
along six quality dimensions, multiple systems, and inspectable summary text.
Articles are not bundled in the raw TSV (retrieve via `gem_id` from GEM); summaries
are included.

**Marginal note:** When `question1` (comprehensibility) is `No`, SEAHORSE omits
ratings for questions 2–6. The transform keeps only non-empty answers (no imputation).

## Observation unit

**One row = one human rating** for a (article × model × criterion) combination.
Each input TSV row is one worker rating for one (gem_id, model) pair; criteria are
melted to long format.

## Reshape operations

1. Loaded validation split TSV (8,968 rows; 3,712 unique `gem_id`; 9 models).
2. Subset: 50 `gem_id` × 6 models (seed 42), random sample without stratification.
3. Melted `question1`–`question6` into long format (`dim::criterion`).
4. Parsed `dim::dataset` from `gem_id` prefix (xsum, xlsum_*, mlsum_*, wiki_lingua_*).
5. Assigned stable `dim::article_id` (8-char hash); full id in `desc::gem_id`.
6. Mapped Yes/No/Unsure to `dim::rating` and numeric `res::rating_code` (1 / 0 / 0.5).

## Subset

| Parameter | Value |
|-----------|-------|
| Split used | validation only (not train/test) |
| Seed | 42 |
| Articles sampled | 50 of 3,712 |
| Models sampled | 1shot, finetuned, mt5_small, mt5_small_250steps, mt5_xxl, t5_xxl (6 of 9) |
| Input rows after filter | 96 (gem_id × model) |
| Output rows | 531 (melted criteria) |

Full validation melt would be ~49,353 rows; subset keeps within demo scale.

## Criterion mapping

| Source column | `dim::criterion` |
|---------------|------------------|
| question1 | comprehensibility |
| question2 | repetition |
| question3 | grammar |
| question4 | attribution |
| question5 | main_ideas |
| question6 | conciseness |

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `seahorse-{n}` |
| `dim::criterion` | melted question name |
| `dim::rating` | Yes / No / Unsure |
| `dim::model` | `model` |
| `dim::worker_lang` | `worker_lang` |
| `dim::dataset` | parsed from `gem_id` |
| `dim::article_id` | hash of `gem_id` |
| `desc::gem_id` | `gem_id` |
| `desc::summary` | `summary` |
| `res::rating_code` | 1 / 0 / 0.5 |

## Suggested grid encodings

| Role | Column |
|------|--------|
| X / Y | `dim::model`, `dim::criterion` |
| Color | `dim::rating` |
| Panel | `dim::dataset` or `dim::worker_lang` |
| Record text | `desc::summary`, `desc::gem_id` |

## Known limitations

- Source articles not included; join via GEM using `desc::gem_id` if needed.
- `duplicates/` split not used (overlap with train/dev/test per SEAHORSE README).
- Train (60K) and test (18K) splits available but not transformed here.

## Reproduce

```bash
python3 eval-data-processed/seahorse/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/seahorse/seahorse_plew_ready.csv
```

## Citation

Clark et al. SEAHORSE: A Multilingual, Multifaceted Dataset for Summarization
Evaluation. EMNLP 2023. [https://arxiv.org/abs/2305.13194](https://arxiv.org/abs/2305.13194)

License: CC BY 4.0
