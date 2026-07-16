#!/usr/bin/env python3
"""Transform THumB 1.0 MSCOCO image-captioning rubric scores into PLeW-ready format.

Raw:
  eval-data-raw/thumb/mscoco_THumB-1.0.jsonl   — one row per (image × system) with
    precision/recall (1–5) and fluency/conciseness/inclusive-language penalties.
  eval-data-raw/thumb/mscoco_references.json   — JSONL of 4 human reference captions
    per image (joined on seg_id).

Output: one row per (image × system × criterion) after melting the five rubric scores.
Images are referenced via public COCO val2014 URLs (no local download required).
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "thumb"
SCORES = RAW / "mscoco_THumB-1.0.jsonl"
REFS = RAW / "mscoco_references.json"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

SEED = 42
IMAGE_SAMPLE_N = 50

COCO_IMAGE_URL = "http://images.cocodataset.org/val2014/{image}"

# Source field -> criterion label for melt.
CRITERIA = (
    ("P", "precision"),
    ("R", "recall"),
    ("Fl", "fluency"),
    ("Con", "conciseness"),
    ("Inc", "inclusive_language"),
)


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_references(path: Path) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            refs[rec["seg_id"]] = rec.get("refs") or []
    return refs


def sample_images(rows: list[dict], n: int, seed: int) -> set[str]:
    rng = random.Random(seed)
    images = sorted({r["image"] for r in rows})
    return set(rng.sample(images, min(n, len(images))))


def format_references(refs: list[str]) -> str:
    return " | ".join(refs)


def transform(rows: list[dict], references: dict[str, list[str]]) -> list[dict]:
    keep = sample_images(rows, IMAGE_SAMPLE_N, SEED)
    subset = [r for r in rows if r["image"] in keep]

    out: list[dict] = []
    row_id = 0
    for rec in subset:
        model = rec["SYS"]
        base = {
            "dim::model": model,
            "dim::is_human": "human" if model == "Human" else "model",
            "dim::image_id": str(rec["set_id"]),
            "res::total_score": str(rec["human_score"]),
            "med::image": COCO_IMAGE_URL.format(image=rec["image"]),
            "desc::caption": rec["hyp"],
            "desc::image_name": rec["image"],
            "desc::seg_id": rec["seg_id"],
            "desc::references": format_references(references.get(rec["seg_id"], [])),
        }
        for field, criterion in CRITERIA:
            score = rec[field]
            row_id += 1
            score_str = f"{score:g}"
            out.append(
                {
                    "ID": f"thumb-{row_id:05d}",
                    "dim::criterion": criterion,
                    "dim::score": score_str,
                    "res::score": score_str,
                    **base,
                }
            )
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows = load_jsonl(SCORES)
    references = load_references(REFS)
    plew_rows = transform(all_rows, references)
    write_csv(OUTPUT_CSV, plew_rows)

    print(f"input rows: {len(all_rows)}")
    print(f"{OUTPUT_CSV.name} rows: {len(plew_rows)}")
    print(f"images: {len({r['dim::image_id'] for r in plew_rows})}")
    print(f"models: {sorted({r['dim::model'] for r in plew_rows})}")
    print(f"criteria: {sorted({r['dim::criterion'] for r in plew_rows})}")


if __name__ == "__main__":
    main()
