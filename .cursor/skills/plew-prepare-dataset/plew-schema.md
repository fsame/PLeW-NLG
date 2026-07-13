# PLeW column schema

PLeW loads flat tables (CSV or JSON/JSONL). Columns use optional **type prefixes**
that declare role. Unprefixed columns fall back to heuristics (less reliable for
unknown datasets).

## Prefix roles

| Prefix | Role | Grid / panels | Record window | Tooltip |
|--------|------|---------------|---------------|---------|
| `dim::` | Categorical dimension | **Yes** — axes, color, panel, shape | Yes (table) | Yes (first fields) |
| `desc::` | Descriptive text / context | **No** | **Yes** | No |
| `med::` | Media URL or path | **No** | **Yes** (popup) | Hint only |
| `res::` | Numeric or ordinal result | **No** | **Yes** | No |

**Key rule:** `res::` is for scores, counts, and other measured outcomes that
belong in the record window but must **not** become grid dimensions. Use `dim::`
only for low-cardinality categories you want to explore spatially (including
binned score bands if you need a facet).

## Heuristic fallback (unprefixed columns)

If no prefix is set, PLeW may still treat a column as a dimension when:

- It is not reserved / desc-like / media-like
- It is not the first column named like an ID with 100% unique values
- Cardinality is less than row count

Long unique strings (full texts, UUID-heavy fields) often become useless
dimensions. **Always prefix explicitly** when preparing external datasets.

Common auto-exclusions (display name, case-insensitive):

- Reserved: contains `description`, `title`, `name`
- Desc-like: `gloss`, `transcription`, `translation`, `text`, `sentence`, etc.
- Media: columns matching URL/path patterns or named `audio`, `image`, `video`

## Row identifier

Include a stable **`ID`** column (first column recommended). Avoid making the only
interesting context column look like a bare `id` field if it should stay visible —
use `desc::item_id` when the identifier is contextual, not a row key.

## Scale guidance

PLeW works best with **hundreds to low thousands** of rows for interactive demo
use. Larger files may lag. When the source is huge, subset with a documented
strategy (stratified sample, fixed N per dimension value) unless the user
requests the full export.

## Output file contract

Successful runs produce:

```
<output-dir>/
  <dataset>_plew_ready.csv   # transformed table (<dataset> = folder basename)
  PLEW_MANIFEST.md           # profiling, mapping, subset notes
```

Failed suitability checks produce:

```
<output-dir>/
  PLEW_UNSUITABLE.md   # reasons + remediation
```

## Canonical observation unit

Every manifest must state **one row = what?** Examples:

- one human judgment (item × system × criterion × annotator)
- one dialogue utterance (dialogue × turn)
- one segment-level eval score

The transform must not mix incompatible units in one file without documenting it.
