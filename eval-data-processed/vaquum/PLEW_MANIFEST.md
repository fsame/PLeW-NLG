# PLeW manifest — VAQUUM

Prepared: 2026-07-14  
Source: `eval-data-raw/vaquum/human_ratings.csv` + `eval-data-raw/vaquum/images.csv`  
Output: `eval-data-processed/vaquum/vaquum_plew_ready.csv`

## Suitability

**Pass.** VAQUUM collects human judgments of vague quantifiers grounded in images:
participants rate statements of the form *"There are [quantifier] [object] in the
image."* on a 0–100 slider, across 6 quantifier conditions (`base`, `a few`, `few`,
`some`, `many`, `a lot of`).

**Scope: TQA source only.** This export is restricted to ratings whose image comes
from the TallyQA/Visual Genome source (69 images), because those images are
downloaded locally so every record renders its image in the popup. The FSC-147
source (Google Drive only) is excluded. Result: 1,290 balanced ratings.

The design gives clean categorical facets (quantifier, count band) plus a
continuous outcome (the rating) and a working image reference — a natural fit for
PLeW's grid + record window.

**Note (off-theme):** This is a vision-grounded psycholinguistics dataset, not an
NLG system evaluation like the other `PLeW-NLG` sources. It is included as a
human-judgment visualization; there is no generated text under evaluation.

## Observation unit

**One row = one participant's 0–100 rating** of a single (quantifier × object ×
image) statement.

## Reshape operations

1. Loaded `human_ratings.csv` (20,300 rows) and `images.csv` (1,089 rows).
2. Inner join on `img_name` (match rate 100%, 0 orphans) to add the image source
   (`dataset`: fsc/tqa) and `desc::original_img_id`.
3. **Filtered to `dataset == "tqa"`** → 1,290 ratings over 69 images.
4. Data is already long form (one rating per row) — **no melt needed**.
5. Reconstructed `desc::statement` from quantifier + object (the `base` condition
   drops the quantifier word).
6. Binned continuous fields into grid facets: `dim::count_band` (from true count)
   and `dim::rating_band` (from the 0–100 rating). Exact values kept in
   `res::true_count` and `res::rating`.
7. Kept `object` as `desc::object`, not a dimension.
8. No subsetting — all 1,290 TQA rows kept (`PER_QUANTIFIER_N = None`).

## Scope / filter

| Parameter | Value |
|-----------|-------|
| Source filter | `tqa` (TallyQA / Visual Genome) |
| Subsetting | none (all TQA rows kept) |
| Quantifiers | 6 of 6, balanced (213–218 each) |
| Images | 69 (all downloaded locally) |
| Output rows | 1,290 |

FSC-147 ratings (the other ~19k rows) are excluded because those images are only
available via a Google Drive zip and were not downloaded. To include everything,
set `SOURCE_FILTER = None` in `transform.py` (and re-add a subset cap, since the
full file is 20,300 rows).

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `vaquum-{n}` |
| `dim::quantifier` | `quantifier` |
| `dim::count_band` | binned `count` (01-10 / 11-25 / 26-50 / 51-75 / 76-100) |
| `dim::rating_band` | binned `value` (0-20 / 20-40 / 40-60 / 60-80 / 80-100) |
| `dim::source` | `dataset` from `images.csv` (fsc/tqa) |
| `res::rating` | `value` (0–100) |
| `res::true_count` | `count` |
| `res::segmentation_area` | `segmentation` |
| `res::size_norm` | `size_norm` (THINGSplus; ~3% missing) |
| `med::image` | `eval-data-raw/vaquum/images/<img_name>` (see media note) |
| `desc::statement` | reconstructed from quantifier + object |
| `desc::object` | `object` |
| `desc::count_bin` | `bin` (e.g. `(40, 43]`) |
| `desc::participant` | `participant` |
| `desc::img_name` | `img_name` |
| `desc::thingsplus_id` | `thingsplus_id` |
| `desc::original_img_id` | `original_img_id` from `images.csv` |

## Suggested grid encodings

| Role | Column |
|------|--------|
| X / Y | `dim::quantifier`, `dim::count_band` |
| Color | `dim::rating_band` |
| Record text | `desc::statement`, `desc::object` |
| Record media | `med::image` |

The core question — *how do ratings of a quantifier vary with the true object
count?* — reads directly off `dim::quantifier` × `dim::count_band` colored by
`dim::rating_band` (exact rating in `res::rating`).

Note: in this TQA-only export `dim::source` is constant (`tqa`) and `dim::count_band`
spans only `01-10`/`11-25` (Visual Genome "simple" counting images have low object
counts), so neither is a useful facet here — they become informative only in a
full-source export.

## Media note

Images are not shipped with the dataset (the GitHub repo has only the two CSVs), so
they are fetched separately into `eval-data-raw/vaquum/images/`. `med::image` points
at `eval-data-raw/vaquum/images/<img_name>`.

**Status:**

- **TQA (`tqa_*.jpg`, 69 images): downloaded.** Pulled from Visual Genome
  (`VG_100K`, falling back to `VG_100K_2`) by `original_img_id`. All 69 present as
  valid JPEGs, so **every record in this export renders its image**.
- **FSC-147 (`fsc_*.jpg`, 1,020 images): not downloaded** (Google Drive-only). These
  are excluded from the export via `SOURCE_FILTER = "tqa"`, so there are no dangling
  paths in the current CSV.

To add FSC-147 later: download
[LearningToCountEverything](https://github.com/cvlab-stonybrook/LearningToCountEverything)
`images_384_VarV2` (Google Drive), then copy each `<original_img_id>.jpg` to
`eval-data-raw/vaquum/images/fsc_<original_img_id>.jpg`.

Reproduce the TQA fetch:

```bash
python3 eval-data-processed/vaquum/download_tqa_images.py
```

## Known limitations

- **TQA-only slice.** Only the 69 Visual Genome images (1,290 ratings) are included;
  the ~19k FSC-147 ratings are excluded because their images are Google Drive-only.
  This is a small, low-count-range corner of VAQUUM, not the full dataset.
- `dim::source` is constant and `dim::count_band` has only 2 values in this export
  (see grid note) — limited spatial facets; `dim::quantifier` and `dim::rating_band`
  carry the signal.
- `object` (up to 106 values dataset-wide) is kept as `desc::`, not a grid facet.
- `size_norm` / `thingsplus_id` are missing for a small fraction of rows.
- Off-theme for `PLeW-NLG` (no generated text under evaluation).

## Reproduce

```bash
python3 eval-data-processed/vaquum/download_tqa_images.py
python3 eval-data-processed/vaquum/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/vaquum/vaquum_plew_ready.csv
```

## Citation

Wong, Nouwen, Gatt. "VAQUUM: Are Vague Quantifiers Grounded in Visual Data?"
Findings of ACL 2025, pp. 11966–11982.  
[https://aclanthology.org/2025.findings-acl.619/](https://aclanthology.org/2025.findings-acl.619/)  
GitHub: [hughmee/vaquum](https://github.com/hughmee/vaquum)

Images sourced from FSC-147 (Ranjan et al., 2021 / Hobley & Prisacariu, 2023) and
TallyQA (Acharya et al., 2019); object norms from THINGSplus (Stoinski et al., 2024).

Download URLs:
```
https://raw.githubusercontent.com/hughmee/vaquum/main/data/human_ratings.csv
https://raw.githubusercontent.com/hughmee/vaquum/main/data/images.csv
```
