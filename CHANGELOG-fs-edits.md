# Changelog – fs-edits branch

Log of changes made:

---

## Change 1: Add prefix parsing helpers

**Files modified:** `layouts/_default/example-viz.html`

**Changes:**
- Added `COLUMN_PREFIXES` constant: `dim::`, `med::`, `desc::`, `res::`
- Added `parseColumnPrefix(header)` – returns `{ type, displayName, key }` or `null`
- Added `getDisplayName(header)` – returns display name (strips prefix)
- Added `dimKey(dim)` – returns `dim.key` or `dim.name` for row lookups

**Behavior:** No change yet; helpers are unused.

---

## Change 2: Support `dim::` in analyzeDimensions


**Files modified:** `layouts/_default/example-viz.html`

**Changes:**
- Updated `analyzeDimensions` to check for `dim::` prefix first; if present, include as dimension
- Columns with `med::`, `desc::`, `res::` are excluded when prefix is present
- Dimensions now have `name` (display) and `key` (for row lookup)
- Added `key` to `mergeValueSpaces` output
- Replaced all row lookups to use `dimKey(dim)` instead of `dim.name` (dummy rows, drag-drop, filters, color/shape, modal)

**Behavior:** Columns with `dim::` prefix (e.g. `dim::Function`) are treated as dimensions. Display shows name without prefix. Existing CSVs without prefixes work unchanged.

---

## Change 3: Support `med::` for media columns

**Files modified:** `layouts/_default/example-viz.html`

**Changes:**
- Updated `isMediaRelatedColumn` to return true when header has `med::` prefix
- Updated `detectMediaColumns` to detect `med::` prefixed columns and add them to mediaColumns (using full header as key for row lookup)
- Media type inferred from display name (e.g. `med::audio_url`, `med::image_url`)
- Updated `getRowMedia` label to use `getDisplayName()` for cleaner display in media section

**Behavior:** Columns with `med::` prefix (e.g. `med::audio_url`, `med::image_url`) are treated as media. Audio/image/video show in the media section when clicking a point. Heuristic detection (audio_url, image_url, etc.) still works as fallback.

---

## Change 4: Support `desc::` and `res::`

**Files modified:** `layouts/_default/example-viz.html`

**Changes:**
- Added `shouldExcludeFromTooltip(key)` – excludes `desc::`, `res::`, `med::`, and heuristic reserved/media
- Added `shouldExcludeFromModalTable(key)` – excludes `res::` and `med::` only (`desc::` shown in modal)
- Added `getModalTitleFromRow(row)` – finds title/name from any column (including `res::title`, `res::name`)
- Updated tooltip (dummy and normal) to use `shouldExcludeFromTooltip` and `getDisplayName` for labels
- Updated modal to use `getModalTitleFromRow`, `shouldExcludeFromModalTable`, and `getDisplayName` for column labels
- Updated `validateAnchors` to use `shouldExcludeFromTooltip`

**Behavior:** 
- `desc::` columns (gloss, transcription, id): Excluded from dimensions and tooltip; shown in modal table
- `res::` columns (title, description): Excluded from dimensions, tooltip, and modal table; `res::title` and `res::name` used for modal header

---

## Change 5: Apply same changes to index.html

**Files modified:** `layouts/index.html`

**Changes:** Mirrored all Steps 1–4 in the full-editor layout (index.html): prefix helpers, dim::, med::, desc::, res::, row lookups, tooltip, modal.

---

## Change 6: Fallback for gloss/transcription/translation columns

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`

**Changes:**
- Added `DESC_LIKE_COLUMNS`: `['gloss', 'glossing', 'transcription', 'transcript', 'translation', 'meaning', 'description', 'text', 'sentence']`
- In `analyzeDimensions` fallback: exclude these column names from dimensions (even when values are not all unique)
- In `shouldExcludeFromTooltip` fallback: exclude these from tooltip

**Behavior:** Columns named gloss, glossing, transcription, transcript, translation, meaning, description, text, sentence (without prefix) are treated like `desc::` columns: excluded from dimensions and tooltip, shown in modal. Explicit prefix (`dim::gloss`) always wins over fallback.

---

## Change 7: Change behavior of the Reset All option

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`, `layouts/shortcodes/visualizer-test.html`, `layouts/_default/full-visualizer.txt`

**Changes:**
- Added confirmation dialog before `resetAllChanges()` runs
- User must confirm with "OK" to revert; "Cancel" aborts and keeps changes

**Behavior:** Clicking "Reset All" now shows a popup: "Reset all changes? All your modifications will be reverted and cannot be undone. Are you sure you want to continue?" This prevents accidental loss of work.

---

## Change 8: Filter color and shape legend values

**Timestamp:** 2026-07-11 14:20 (UTC+2)

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`

**Changes:**
- Added `rowPassesColorShapeFilters()` — hides data points whose color/shape dimension value is unchecked
- Added filter checkboxes to each row in the color and shape sidebar legends (same mechanism as grid/panel value filters via `setValueFilter`)
- Applied color/shape filters when rendering panel cells and when computing grid item counts
- Added `.legend-filter-cb` and `.legend-row-filtered-out` styles; updated legend hints

**Behavior:** Users can uncheck score/criterion (or any color/shape-encoded dimension) in the legend to hide those points from the visualization. Unchecked legend rows appear dimmed. Grid/panel value filters unchanged.

---

## Change 9: Show filtered value counts in dimension list

**Timestamp:** 2026-07-11 14:31 (UTC+2)

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`

**Changes:**
- Added `getDimensionValueCountLabel()` — returns `4 values` when all are visible, or `3 of 4 values` when some are filtered out
- Dimension sidebar meta line updates on filter changes via `updateDimensionListEncodings()`

**Behavior:** When values are hidden via grid/panel filters or color/shape legend checkboxes, the dimension list reflects how many values remain visible (e.g. criterion shows `3 of 4 values` after filtering one out).

---

## Change 10: Export/import visualization setup for reproducibility

**Timestamp:** 2026-07-11 14:43 (UTC+2)

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`

**Changes:**
- Added **Visualization setup** sidebar section with **Export setup** / **Import setup** buttons
- Setup JSON captures: dimension order, enabled dimensions, value filters, custom colors/shapes, display options (grid sizing, labels, item counts), anchor/dummy settings

**Behavior:** Export a `plew-setup-*.json` file to archive a configuration; import it to restore. Import warns if the dataset name differs but allows apply anyway. (Auto-restore on reload was added briefly, then removed in Change 11.)

---

## Change 11: Viz setup applies only on explicit import

**Timestamp:** 2026-07-11 14:55 (UTC+2)

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`

**Changes:**
- Removed automatic `localStorage` save/restore for visualization setup
- Page reload always starts from the default dimension order and filters
- Setup changes apply only when the user imports a `plew-setup-*.json` file

**Behavior:** Reload shows the original view. Export saves your tuned setup; import restores it when you choose.

---

## Change 12: Repo cleanup — PLeW-NLG demos replace legacy PLeW examples

**Timestamp:** 2026-07-12 00:29 (UTC+2)

**Files removed:**
- Legacy static media: `static/kourosh/`, `static/breach/`, `static/isaph/`, `static/visiblezoo/`, `static/zoo/`
- Legacy demo CSVs and example pages (Kourosh, zoo, ISAPh, DIA, japisaph)
- `_archive/`, `layouts/backup-index.html`, `layouts/_default/full-visualizer.txt`, `layouts/shortcodes/visualizer-test.html`

**Files added:**
- `static/data/webnlg2017_humaneval.csv`, `simpeval.csv`, `book_highlights_llm_as_a_judge.csv`
- `content/examples/webnlg2017-humaneval.md`, `simpeval.md`, `book-highlights-llm-as-a-judge.md`

**Files modified:** `README.md`, `hugo.toml`, `content/examples/_index.md`, `.gitignore`, layout titles (`PLeW-NLG`)

**Behavior:** `/examples/` lists three NLG human-eval datasets. Legacy Kourosh/zoo demos removed. Raw downloads gitignored (see `eval-data-raw/SOURCES.md` to re-fetch).

---

## Change 13: All/None toggles on value filter groups

**Timestamp:** 2026-07-12 14:49 (UTC+2)

**Files modified:** `layouts/_default/example-viz.html`, `layouts/index.html`

**Changes:**
- Added **All** / **None** buttons on each dimension group in **Filter values**
- Added the same toggles to **Color** and **Shape** legend section headers
- **All** clears the filter (show every value); **None** hides all values for that dimension

---

## Change 14: Full editor viz toolbar matches example pages

**Timestamp:** 2026-07-12 22:55 (UTC+2)

**Files modified:** `layouts/index.html`

**Changes:**
- Replaced **Uniform grid sizes** with **Unify grid sizes** + configurable outer row height (px)
- Added **Unify inner panel** + configurable inner row height (px)
- Aligned label styling dropdown labels with example pages
- Added CSS for number inputs and unified inner panel overflow
- Wired `applyUniformGrids()`, `applyUnifiedInnerPanels()`, and height helpers into render/import/export

**Behavior:** Uploading a CSV on `/` now exposes the same grid sizing controls as `/examples/...` pages.

---

## Change 15: Fix upside-down vertical axis labels

**Timestamp:** 2026-07-12 23:50 (UTC+2)

**Files modified:** `layouts/index.html`, `layouts/_default/example-viz.html`

**Changes:**
- Replaced `writing-mode: vertical-rl` + `rotate(180deg)` with rotated inner spans (`rotate(-90deg)`)
- Added `setVerticalAxisLabel()` helper for outer row labels and inner panel Y headers
- Ported `fixSnapshotLabels()` to the full editor snapshot export

**Behavior:** Left-side labels (e.g. dimension values, inner panel rows) read bottom-to-top instead of appearing upside down, in both live view and PNG snapshots.

---

## Change 16: Modal stacked vs side-by-side snapshots

**Timestamp:** 2026-07-12 23:56 (UTC+2)

**Files modified:** `layouts/index.html`, `layouts/_default/example-viz.html`

**Changes:**
- Added **📷 Stacked** and **📷 Side-by-side** buttons to the record detail modal header
- Ported `snapshotModal()` from PLeW-main (full modal capture vs fields/media split layout)

**Behavior:** Click a data point to open the modal, then export a PNG of all fields stacked or with metadata and media side by side.

---

## Change 17: Offer sibling viz setup files on Import

**Timestamp:** 2026-07-13 00:14 (UTC+2)

**Files modified:** `layouts/index.html`, `layouts/_default/example-viz.html`

**Changes:**
- On dataset load, probe the data file’s directory for `plew-setup-{basename}.json` (and `{basename}.plew-setup.json`)
- When dropping/selecting multiple files or scanning a media folder, register any co-located PLeW setup JSON files
- **Import setup** now opens a picker menu when sibling setups were found; otherwise falls back to the file chooser

**Behavior:** Save `plew-setup-seahorse.json` next to `seahorse_plew_ready.csv` — after loading the CSV, Import setup lists it for one-click apply. Single-file local picks still require manual import (browser cannot read the folder).

---

## Change 18: SEAHORSE example dataset

**Timestamp:** 2026-07-13 17:33 (UTC+2)

**Files added:**
- `static/data/seahorse.csv` (from `eval-data-processed/seahorse/seahorse_plew_ready.csv`)
- `content/examples/seahorse.md`

**Behavior:** `/examples/seahorse/` loads the multilingual summarization human-eval demo (3,856 rows).

---

## Change 19: Examples gallery grouped by NLG task

**Timestamp:** 2026-07-13 17:35 (UTC+2)

**Files modified:** `layouts/examples/list.html`, `content/examples/*.md`

**Changes:**
- Added `task` front matter to each example (`data-to-text`, `summarization`, `simplification`, `llm-as-judge`)
- Gallery page renders section headers with short task descriptions and cards underneath

**Behavior:** `/examples/` lists datasets under Data-to-text, Summarization, Text simplification, and LLM-as-judge.

---

## Change 20: SummEval example dataset

**Timestamp:** 2026-07-13 17:52 (UTC+2)

**Files added:**
- `static/data/summeval.csv` (from `eval-data-processed/summeval/summeval_plew_ready.csv`)
- `content/examples/summeval.md`

**Files modified:** `content/examples/seahorse.md` (weight 2 — SummEval listed first in Summarization)

**Behavior:** `/examples/summeval/` loads the CNN/DM summarization human-eval demo (1,920 rows).

---

## Change 21: Flickr8k on examples gallery (image captioning)

**Timestamp:** 2026-07-13 18:16 (UTC+2)

**Files modified:** `layouts/examples/list.html`, `content/examples/flickr8k.md`, `static/data/flickr8k.csv`

**Changes:**
- Added **Image captioning** section to the examples gallery
- Normalized `task` slug to `image-captioning`
- Synced published CSV from `eval-data-processed/flickr8k/flickr8k_plew_ready.csv`

**Behavior:** `/examples/flickr8k/` appears under Image captioning (345 expert judgments, 20 local JPEGs in `static/flickr8k/`).

**Behavior:** Large category lists (e.g. `mr_id`) can be bulk-selected or cleared without clicking each checkbox.