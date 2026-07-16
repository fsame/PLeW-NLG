#!/usr/bin/env python3
"""Transform VAQUUM (vague quantifiers with human judgments) into PLeW-ready format.

Raw:
  eval-data-raw/vaquum/human_ratings.csv  — one row per participant rating (0-100)
    of a statement "There are [quantifier] [object] in the image."
  eval-data-raw/vaquum/images.csv         — per-image metadata (adds source dataset
    fsc/tqa and original image id), joined on img_name.

Output: one row per human rating (already long form; no melt needed). Restricted to
the TQA (Visual Genome) image source, whose 69 images are downloaded locally so every
record renders in the popup. The 1,290 TQA ratings are within demo scale, so no
subsetting is applied.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "vaquum"
RATINGS = RAW / "human_ratings.csv"
IMAGES = RAW / "images.csv"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

SEED = 42
# Keep only ratings whose image comes from this source (images downloaded locally).
# Set to None to include every source.
SOURCE_FILTER = "tqa"
# Rows to keep per quantifier after filtering; None keeps all.
PER_QUANTIFIER_N = None

# Relative location where the (externally sourced) images live.
IMAGE_DIR = "eval-data-raw/vaquum/images"


def count_band(count: int) -> str:
    if count <= 10:
        return "01-10"
    if count <= 25:
        return "11-25"
    if count <= 50:
        return "26-50"
    if count <= 75:
        return "51-75"
    return "76-100"


def rating_band(value: float) -> str:
    if value < 20:
        return "0-20"
    if value < 40:
        return "20-40"
    if value < 60:
        return "40-60"
    if value < 80:
        return "60-80"
    return "80-100"


def statement(quantifier: str, obj: str) -> str:
    # "base" condition presents the sentence with no quantifier.
    if quantifier == "base":
        return f"There are {obj} in the image."
    return f"There are {quantifier} {obj} in the image."


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stratified_sample(rows: list[dict], key: str, n: int | None, seed: int) -> list[dict]:
    if n is None:
        return rows
    rng = random.Random(seed)
    buckets: dict[str, list[dict]] = {}
    for r in rows:
        buckets.setdefault(r[key], []).append(r)
    out: list[dict] = []
    for value in sorted(buckets):
        bucket = buckets[value]
        out.extend(bucket if len(bucket) <= n else rng.sample(bucket, n))
    return out


def transform(ratings: list[dict], images: list[dict]) -> list[dict]:
    img_meta = {im["img_name"]: im for im in images}
    if SOURCE_FILTER is not None:
        ratings = [
            r for r in ratings
            if img_meta.get(r["img_name"], {}).get("dataset") == SOURCE_FILTER
        ]
    sampled = stratified_sample(ratings, "quantifier", PER_QUANTIFIER_N, SEED)

    out: list[dict] = []
    for i, rec in enumerate(sampled, start=1):
        img = img_meta.get(rec["img_name"], {})
        obj = rec["object"]
        quantifier = rec["quantifier"]
        count = int(rec["count"])
        value = float(rec["value"])
        out.append(
            {
                "ID": f"vaquum-{i:05d}",
                "dim::quantifier": quantifier,
                "dim::count_band": count_band(count),
                "dim::rating_band": rating_band(value),
                "dim::source": img.get("dataset", ""),
                "res::rating": f"{value:g}",
                "res::true_count": str(count),
                "res::segmentation_area": rec.get("segmentation", ""),
                "res::size_norm": rec.get("size_norm", ""),
                "med::image": f"{IMAGE_DIR}/{rec['img_name']}",
                "desc::statement": statement(quantifier, obj),
                "desc::object": obj,
                "desc::count_bin": rec.get("bin", ""),
                "desc::participant": rec["participant"],
                "desc::img_name": rec["img_name"],
                "desc::thingsplus_id": rec.get("thingsplus_id", ""),
                "desc::original_img_id": img.get("original_img_id", ""),
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
    ratings = load_csv(RATINGS)
    images = load_csv(IMAGES)
    rows = transform(ratings, images)
    write_csv(OUTPUT_CSV, rows)

    print(f"input ratings: {len(ratings)}")
    print(f"{OUTPUT_CSV.name} rows: {len(rows)}")
    print(f"quantifiers: {sorted({r['dim::quantifier'] for r in rows})}")
    print(f"count bands: {sorted({r['dim::count_band'] for r in rows})}")
    print(f"rating bands: {sorted({r['dim::rating_band'] for r in rows})}")
    print(f"sources: {sorted({r['dim::source'] for r in rows})}")


if __name__ == "__main__":
    main()
