# PLeW manifest — Flickr8k

Prepared: 2026-07-13  
Source: `eval-data-raw/flickr8k/text_extracted/` (ExpertAnnotations, CrowdFlowerAnnotations, Flickr8k.token.txt), `eval-data-raw/flickr8k/manifest.json`, `eval-data-raw/flickr8k/images/`  
Output: `eval-data-processed/flickr8k/flickr8k_plew_ready.csv`, `eval-data-processed/flickr8k/flickr8k_plew_crowd.csv`

## Suitability

**Pass.** Multimodal image-caption human evaluation with expert Likert scores (1–4)
and crowd yes/no aggregate judgments. Caption text and local image paths are joined
for the record window.

**Marginal note:** Only 20 of 8,092 Flickr8k images are stored locally (~650 KB demo
subset from the HF `intro/flickr8k` test split). Judgments are filtered to those 20
reference images so every row has `med::image`. Full corpus caption/judgment files
remain in `eval-data-raw/` for future expansion.

## Observation unit

**Expert file (`flickr8k_plew_ready.csv`):** one row = one expert judgment for a
(reference image × candidate caption × annotator) triple.

**Crowd file (`flickr8k_plew_crowd.csv`):** one row = one aggregated CrowdFlower
judgment for a (reference image × candidate caption) pair.

## Reshape operations

1. Loaded caption lookup from `Flickr8k.token.txt` (40,461 caption ids).
2. Mapped 20 local JPEGs to original image ids via `manifest.json` caption-set matching.
3. Filtered expert and crowd annotations to the 20 reference images with local media.
4. Expert: exploded three annotator score columns into long format (`dim::annotator_index`).
5. Crowd: kept one row per pair; derived `dim::majority_match` and `dim::yes_fraction_band`.
6. Joined caption text on `<image>.jpg#<0-4>` caption id.
7. Tagged `dim::caption_origin` as `same_image` vs `cross_image` (ranking-style pairs).

## Subset

| Parameter | Value |
|-----------|-------|
| Scope | 20 demo images with local JPEGs only |
| Expert input pairs | 115 (reference image × candidate caption) |
| Expert output rows | 345 (× 3 annotators) |
| Crowd output rows | 1,010 |
| Split tag | `test` (all demo images are from test split) |

No random subsampling applied within the 20-image demo scope.

## Column mapping — expert (`flickr8k_plew_ready.csv`)

| Output column | Source |
|---------------|--------|
| `ID` | generated `flickr8k-expert-{n}` |
| `dim::demo_image` | local basename without extension (`flickr8k_00` … `flickr8k_19`) |
| `dim::annotator_index` | expert column 3–5 (1-based) |
| `dim::score` | expert Likert 1–4 |
| `dim::caption_origin` | derived: caption image == reference image |
| `dim::caption_slot` | caption number 0–4 from caption id |
| `dim::split` | constant `test` |
| `res::score` | same Likert value |
| `desc::reference_image` | ExpertAnnotations col 1 |
| `desc::caption_id` | ExpertAnnotations col 2 |
| `desc::caption` | Flickr8k.token.txt lookup |
| `desc::caption_image` | image filename from caption id |
| `med::image` | `flickr8k/flickr8k_{nn}.jpg` (served from `static/flickr8k/`) |

## Column mapping — crowd (`flickr8k_plew_crowd.csv`)

| Output column | Source |
|---------------|--------|
| `ID` | generated `flickr8k-crowd-{n}` |
| `dim::demo_image` | same as expert |
| `dim::caption_origin` | derived |
| `dim::caption_slot` | derived |
| `dim::majority_match` | derived from yes/no counts (`yes` / `no` / `tie`) |
| `dim::yes_fraction_band` | binned from col 3 (`low` / `medium` / `high`) |
| `dim::split` | constant `test` |
| `res::yes_fraction` | CrowdFlowerAnnotations col 3 |
| `res::yes_count` | col 4 |
| `res::no_count` | col 5 |
| `res::total_judgments` | yes + no |
| `desc::*` / `med::image` | same join as expert |

## Suggested grid encodings

### Expert

| Role | Column |
|------|--------|
| X / Y | `dim::score`, `dim::annotator_index` |
| Color | `dim::caption_origin` or `dim::caption_slot` |
| Panel | `dim::demo_image` |
| Record | `desc::caption`, `med::image` |

Compare expert disagreement via `dim::annotator_index` within (demo_image, caption).

### Crowd

| Role | Column |
|------|--------|
| X / Y | `dim::majority_match`, `dim::yes_fraction_band` |
| Color | `dim::caption_origin` |
| Panel | `dim::demo_image` |
| Record | `desc::caption`, `med::image`, `res::yes_fraction` |

## Known limitations

- Only 20 reference images have local `med::image` paths; full 8k corpus not bundled.
- Expert annotations are ranking-style: most pairs are cross-image captions, not the
  five reference captions for the image.
- Crowd and expert are in separate CSVs (different observation units).
- `med::image` uses root-relative paths under `static/flickr8k/` (Hugo) or matches by
  basename when loading the CSV locally with the image folder via **Select media folder**.
- Crowd variant: `static/data/flickr8k_crowd.csv` (1,010 rows).
- Non-commercial research use only (University of Illinois Flickr8k terms).

## Reproduce

```bash
python3 eval-data-processed/flickr8k/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/flickr8k/flickr8k_plew_ready.csv
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/flickr8k/flickr8k_plew_crowd.csv
```

## Citation

Hodosh, Young, Hockenmaier. "Framing Image Description as a Ranking Task: Data,
Models and Evaluation Metrics." JAIR 2013.

Download URL (text/annotations):
`https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip`
