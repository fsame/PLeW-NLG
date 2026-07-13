# PLeW manifest — SummEval

Prepared: 2026-07-13  
Source: `eval-data-raw/summeval/model_annotations.aligned.jsonl`  
Output: `eval-data-processed/summeval/summeval_plew_ready.csv`

## Suitability

**Pass.** Summarization human evaluation with 16 systems on 100 CNN/DailyMail articles.
Each (article × system) summary has 3 expert + 5 crowd annotators rating coherence,
consistency, fluency, and relevance on a 1–5 Likert scale. Summary text and reference
summaries are included for the record window.

**Marginal note:** Source article text is not in the release; only summaries, references,
and scores. Use `desc::story_path` or `desc::article_id` to join externally if needed.

## Observation unit

**One row = one human judgment** for a (article × system × criterion × annotator) combination.

## Reshape operations

1. Loaded `model_annotations.aligned.jsonl` (1,600 rows; 100 articles × 16 systems).
2. Subset: 15 articles × 4 models (seed 42), random sample without stratification.
3. Exploded `expert_annotations` (3) and `turker_annotations` (5) into separate rows.
4. Melted four criteria per annotator into long format (`dim::criterion`).
5. Assigned stable `dim::article_id` (8-char hash); full id in `desc::article_id`.
6. Kept raw Likert in both `dim::score` and `res::score` (cardinality 1–5).

## Subset

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Articles sampled | 15 of 100 |
| Models sampled | 4 of 16 |
| Input rows after filter | 60 (article × system) |
| Output rows | 1,920 (× 8 annotators × 4 criteria) |

Full melt of entire file would be ~51,200 rows; subset keeps within demo scale.

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `summeval-{n}` |
| `dim::model` | `model_id` |
| `dim::article_id` | hash of `id` |
| `dim::criterion` | melted criterion name |
| `dim::annotator_group` | `expert` or `crowd` (from `turker_annotations`) |
| `dim::annotator_index` | 1-based index within group |
| `dim::score` | per-criterion Likert (1–5) |
| `res::score` | same Likert value |
| `desc::article_id` | `id` |
| `desc::summary` | `decoded` |
| `desc::references` | `references` joined with ` \| ` |
| `desc::story_path` | `filepath` |

## Suggested grid encodings

| Role | Column |
|------|--------|
| X / Y | `dim::model`, `dim::criterion` |
| Color | `dim::score` or `dim::annotator_group` |
| Panel | `dim::article_id` (filter recommended — 15 values) |
| Record text | `desc::summary`, `desc::references` |

Compare expert vs crowd disagreement via `dim::annotator_group` and
`dim::annotator_index` panels within (article, model, criterion).

## Known limitations

- Source articles not included in SummEval release.
- `dim::article_id` is opaque; use record window for summary and references.
- Subset is random, not stratified by model family or article length.
- 16 model ids (M1–M22 with gaps) are opaque without external model-name mapping.

## Reproduce

```bash
python3 eval-data-processed/summeval/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/summeval/summeval_plew_ready.csv
```

## Citation

Fabbri et al. "SummEval: Re-evaluating Summarization Evaluation." TACL 2021.  
[https://github.com/Yale-LILY/SummEval](https://github.com/Yale-LILY/SummEval)

Download URL:
`https://storage.googleapis.com/sfr-summarization-repo-research/model_annotations.aligned.jsonl`
