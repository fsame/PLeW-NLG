# Reshape patterns

Detect structural patterns in raw data and apply the matching transform **before**
role assignment. Do not hardcode benchmark-specific column names — use shape.

## Detection signals

| Signal | Typical raw shape |
|--------|-------------------|
| Nested object of scores | `{ criterion_a: { score: 3 }, criterion_b: … }` |
| Fixed score columns wide | `fluency`, `coherence`, `relevance` as separate columns |
| Annotator arrays | `[{ rater: 1, score: 4 }, { rater: 2, score: 3 }]` |
| Pairwise comparison | `candidate_a`, `candidate_b`, `winner: "A"` |
| Dialogue sequence | `utterances: [...]`, `acts: [...]`, parallel arrays |
| Multi-file | annotations file + content file sharing a key |
| Span-level markup | char/ token offsets, MQM span TSV |
| Single aggregate row | one JSON object, no population |

## Pattern → action

### Melt (wide → long)

**When:** multiple criterion/score columns, or nested criteria object.

**Action:** one output row per `(base_keys × criterion [× annotator])`.

**Add dimensions:** melted criterion name; annotator id if present.

### Explode annotators

**When:** multiple ratings per item stored as array or duplicate rows with
rater id.

**Action:** keep separate rows; `dim::annotator` or `dim::annotator_group`
(expert vs crowd) rather than averaging unless user asks for means.

### Resolve pairwise winners

**When:** blinded A/B labels with metadata mapping A/B to systems/conditions.

**Action:** compute `dim::winner_resolved` from winner + side metadata.
Store both candidate texts in `desc::`. Never plot raw `A`/`B` without axis
context (`dim::comparison_axis` or similar).

### Explode sequences

**When:** utterances/acts/emotions as parallel lists.

**Action:** one row per index `i`; `dim::turn_index` or binned position;
`desc::utterance`; categorical `dim::act`, `dim::emotion`.

### Join files

**When:** judgments separated from text/media.

**Action:** inner join on stable key; fail if match rate < threshold (e.g. 95%)
without user override. Document orphan counts in manifest.

### Aggregate spans

**When:** token/character-level error markup (MQM TSV, BIO tags).

**Action:** unless user wants span browser, aggregate to segment or document
level: error category counts, severity max/mean → `res::` or binned `dim::`.
If aggregation destroys the eval signal, mark **unsuitable** and explain.

### Bin numeric scores

**When:** continuous or many-valued numeric field needed as a facet.

**Action:** prefer raw value in `res::score`; optional `dim::score_band`
(low/med/high or Likert integer as `dim::score` when 1–5).

## Subset strategies

When row count exceeds default cap (~500–2000):

1. **Stratified:** sample N per value of lowest-cardinality planned `dim::`
2. **Head:** only if user accepts bias — document it
3. **Filter:** user-provided scope (one language pair, one model family)

Always record seed, N, and filters in `PLEW_MANIFEST.md`.
