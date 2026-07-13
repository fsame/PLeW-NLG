# PLeW manifest — WebNLG 2017 human evaluation

Prepared: 2026-07-11  
Source: `eval-data-raw/webnlg2017_humaneval/webnlg-human-evaluation/all_data_final_scores_anonymised.csv`  
Output: `eval-data-processed/webnlg2017_humaneval/webnlg2017_humaneval_plew_ready.csv`

## Suitability

**Pass.** Per-rater human scores on three quality dimensions (fluency, grammaticality,
semantic adequacy) for multiple WebNLG 2017 systems, with meaning representations and
generated text in the same file.

## Observation unit

**One row = one human score** for a (MR × system × criterion × rater) combination.

## Reshape operations

1. Loaded anonymised per-rater CSV (6,111 rows; 223 unique MRs × 10 systems).
2. Subset: 18 MRs × 5 systems (seed 42), random sample without stratification.
3. Melted `fluency`, `grammaticality`, `semantic_adequacy` into long format
   (`dim::criterion`).
4. Assigned stable `dim::mr_id` (8-char hash) for grid use; full MR kept in `desc::mr`.
5. Assigned `dim::annotator_index` (1…n) within each (MR, system) group; CrowdFlower
   worker id in `desc::annotator`.

## Subset

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| MRs sampled | 18 of 223 |
| Systems sampled | adapt, baseline, pkuwriter, tilburg-nmt, webnlg (5 of 10) |
| Input rows after filter | 256 (MR × system × rater) |
| Output rows | 768 (× 3 criteria) |

Full melt of entire file would be ~18,333 rows; subset keeps within demo scale.

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `webnlg17-{n}` |
| `dim::criterion` | melted from score column names |
| `dim::score` | Likert 1–3 (grid-friendly) |
| `dim::system` | `team` |
| `dim::category` | `category` (DBpedia domain) |
| `dim::type` | `type` (`seen` / `unseen`) |
| `dim::triplesize` | `triplesize` |
| `dim::systemtype` | `systemtype` (neural, template, human, …) |
| `dim::mr_id` | hash of `mr` |
| `dim::annotator_index` | rater index within (MR, system) |
| `res::score` | same as `dim::score` |
| `res::bleu` | `bleu` |
| `res::meteor` | `meteor` |
| `res::ter` | `ter` |
| `desc::mr` | `mr` (RDF triples, `<br>`-separated) |
| `desc::text` | `text` (generated verbalisation) |
| `desc::annotator` | `X_worker_id` |
| `desc::unit_id` | `X_unit_id` |

## Suggested grid encodings

- **Grid X:** `system`
- **Grid Y:** `criterion`
- **Color:** `score`
- **Panel:** `category` or `mr_id` (filter recommended for dense panels)

Compare `webnlg` (human reference) against neural/template systems on semantics vs fluency.

## Known limitations

- Scores are on a 1–3 scale (not 1–5).
- `dim::mr_id` is opaque; use record window for MR and generated text.
- Some rows have empty `desc::text` in the raw release (~25 of 6,111 full file).
- Automatic metrics (`res::bleu`, etc.) are system-level constants per row, not per-rater.

## Reproduce

```bash
python3 eval-data-processed/webnlg2017_humaneval/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/webnlg2017_humaneval/webnlg2017_humaneval_plew_ready.csv
```
