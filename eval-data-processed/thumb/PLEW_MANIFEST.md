# PLeW manifest — THumB 1.0 (MSCOCO)

Prepared: 2026-07-14  
Source: `eval-data-raw/thumb/mscoco_THumB-1.0.jsonl` + `eval-data-raw/thumb/mscoco_references.json`  
Output: `eval-data-processed/thumb/thumb_plew_ready.csv`

## Suitability

**Pass.** THumB 1.0 is a rubric-based human evaluation of MSCOCO image captions
([Kasai et al., NAACL 2022](https://aclanthology.org/2022.naacl-main.254/)). Five
captioning systems (Up-Down, Unified-VLP, VinVL-base, VinVL-large) plus human
reference captions are scored on **precision** and **recall** (1–5) with penalties
for fluency, conciseness, and inclusive language. 500 Karpathy-test images; images
are served via public COCO val2014 URLs so every record renders without a local
image download.

## Observation unit

**One row = one rubric score** for a (image × system × criterion) combination after
melting the five THumB dimensions.

## Reshape operations

1. Loaded `mscoco_THumB-1.0.jsonl` (2,500 rows = 500 images × 5 systems).
2. Joined `mscoco_references.json` (JSONL, 500 entries) on `seg_id` for four human
   reference captions per image.
3. Melted wide rubric columns (`P`, `R`, `Fl`, `Con`, `Inc`) into long format
   (`dim::criterion`).
4. Added `dim::is_human` from `SYS == "Human"`.
5. Kept aggregate `res::total_score` (`human_score`) on every melted row.
6. Assigned `med::image` as COCO val2014 URL (`images.cocodataset.org`).
7. Subset: 50 of 500 images sampled (seed 42); all 5 systems and all 5 criteria kept.

## Subset

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Images sampled | 50 of 500 |
| Systems | 5 of 5 (all) |
| Criteria | 5 of 5 (all) |
| Output rows | 1,250 (50 × 5 × 5) |

Full melt of the entire file would be 12,500 rows (2,500 × 5 criteria). Sampling
images keeps every system and criterion for cross-model comparison while staying
within interactive demo scale and the 50-value `dim::` cardinality cap.

## Column mapping

| Output column | Source |
|---------------|--------|
| `ID` | generated `thumb-{n}` |
| `dim::criterion` | melted rubric name |
| `dim::score` | per-criterion value (`P`, `R`, or penalty) |
| `res::score` | same value |
| `dim::model` | `SYS` |
| `dim::is_human` | `SYS == "Human"` → `human` else `model` |
| `dim::image_id` | `set_id` (Karpathy test integer id) |
| `res::total_score` | `human_score` (aggregate rubric score) |
| `med::image` | `http://images.cocodataset.org/val2014/{image}` |
| `desc::caption` | `hyp` |
| `desc::image_name` | `image` |
| `desc::seg_id` | `seg_id` |
| `desc::references` | 4 human refs joined with ` \| ` |

## Suggested grid encodings

| Role | Column |
|------|--------|
| X / Y | `dim::model`, `dim::criterion` |
| Color | `dim::score` (for precision/recall) or `dim::is_human` |
| Panel | `dim::image_id` (50 values — use as filter) |
| Record text | `desc::caption`, `desc::references` |
| Record media | `med::image` |

The headline THumB finding — human captions beat machines especially on **recall**
— reads directly off `dim::criterion` × `dim::model`, with `dim::is_human` as color.

## Known limitations

- Subset is a random sample of 50 images, not stratified by scene type.
- Penalty criteria (`fluency`, `conciseness`, `inclusive_language`) are sparse
  (mostly 0); precision and recall carry most of the signal.
- `dim::image_id` is at the 50-value cardinality cap; full 500-image export would
  need `desc::image_id` instead or panel filtering.
- Requires network access for `med::image` COCO URLs (no local image cache).
- Single adjudicated rubric score per (image × system), not per-annotator rows.

## Reproduce

```bash
python3 eval-data-processed/thumb/transform.py
python3 .cursor/skills/plew-prepare-dataset/scripts/validate_plew_csv.py \
  eval-data-processed/thumb/thumb_plew_ready.csv
```

## Citation

Kasai et al. "Transparent Human Evaluation for Image Captioning." NAACL 2022.  
[https://arxiv.org/abs/2111.08940](https://arxiv.org/abs/2111.08940)  
GitHub: [jungokasai/THumB](https://github.com/jungokasai/THumB)

Download URLs:
```
https://raw.githubusercontent.com/jungokasai/THumB/master/mscoco/mscoco_THumB-1.0.jsonl
https://raw.githubusercontent.com/jungokasai/THumB/master/mscoco/mscoco_references.json
```

Images: MSCOCO val2014 Karpathy test split via
[https://images.cocodataset.org/val2014/](https://images.cocodataset.org/val2014/)
