# PLeW manifest — NeuralREG human evaluation

Prepared: 2026-07-16  
Source: [NeuralREG/humaneval](https://github.com/ThiagoCF05/NeuralREG/tree/master/humaneval)  
Output: `eval-data-processed/neuralreg_humaneval/neuralreg_humaneval_plew_ready.csv`

## Suitability

**Pass.** Per-participant human scores on three quality dimensions (fluency, grammar,
clarity) for six referring-expression generation systems, with full realizations
available per text × system.

## Observation unit

**One row = one human score** for a (text × system × criterion × participant) combination.

## Reshape operations

1. Loaded `experiment_results.json` (1,469 judgments; 61 participants; 24 texts).
2. Joined `htmls/official/text_trials/trial_info` to resolve which **system** each
   participant saw for each text (six rotated lists).
3. Joined `text_trials/{text_id}` files for model-specific realizations and gold
   `original` text.
4. Joined `participants_info.json` for English proficiency and demographics.
5. Melted `fluency`, `grammar`, `clarity` into long format (`dim::criterion`).

## Subset

None. Full release retained (4,407 rows after melt).

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `neuralreg-{n}` |
| `dim::criterion` | melted from score field names |
| `dim::score` | Likert 1–7 (grid-friendly) |
| `dim::system` | resolved from `trial_info` + stimulus list |
| `dim::text_id` | parsed from judgment `url` |
| `dim::text_size` | number of referring expressions in passage (2–7) |
| `dim::difficulty` | `critical` or `median` trial selection |
| `dim::list_id` | participant stimulus list (1–6) |
| `dim::annotator_index` | rater index within (text, system) |
| `dim::english_proficiency` | `english_proficiency_level` |
| `res::score` | same as `dim::score` |
| `desc::realization` | text rated (model-specific) |
| `desc::original` | gold realization from `original` model |
| `desc::participant_id` | raw participant id |
| `desc::participant_country` | participant country |
| `desc::participant_native_language` | participant native language |

## Systems

| `dim::system` | Description |
|---------------|-------------|
| `original` | Gold reference realizations |
| `only` | Only-names baseline |
| `ferreira` | Ferreira et al. (2016) baseline |
| `seq2seq` | Neural seq2seq |
| `catt` | Neural with content attention |
| `hieratt` | Neural with hierarchical attention |

## Suggested grid encodings

- **Grid X:** `system`
- **Grid Y:** `criterion`
- **Color:** `score`
- **Panel:** `annotator_index` or `text_id`
- **Shape:** `difficulty` or `english_proficiency`

Compare neural models against baselines; inspect whether low grammar scores cluster on
specific texts or proficiency groups.

## Known limitations

- Scores are on a 1–7 scale.
- Each participant only saw one rotated list; `dim::list_id` correlates with which
  systems they rated most often.
- `desc::participant_id` holds the raw CrowdFlower id; use `dim::annotator_index` on the grid.
- Realizations are WebNLG-style data-to-text passages with highlighted referring
  expressions in the HTML stimuli; stored text is plain verbalisation.

## Reproduce

```bash
python3 eval-data-processed/neuralreg_humaneval/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/neuralreg_humaneval/neuralreg_humaneval_plew_ready.csv
```

Raw files live under `eval-data-raw/neuralreg_humaneval/` (JSON + `text_trials/`).
