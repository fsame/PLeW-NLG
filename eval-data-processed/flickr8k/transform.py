#!/usr/bin/env python3
"""Transform Flickr8k expert and crowd caption judgments into PLeW-ready CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "flickr8k"
TEXT = RAW / "text_extracted"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
EXPERT_CSV = OUT / f"{DATASET}_plew_ready.csv"
CROWD_CSV = OUT / f"{DATASET}_plew_crowd.csv"

# Site-relative paths resolve via Hugo static/flickr8k/ (see static/flickr8k/).
# Basename also matches when users pick the images folder in the local visualizer.
MEDIA_PREFIX = "flickr8k"


def load_captions() -> dict[str, str]:
    captions: dict[str, str] = {}
    for line in (TEXT / "Flickr8k.token.txt").read_text(encoding="utf-8").splitlines():
        caption_id, text = line.split("\t", 1)
        captions[caption_id] = text
    return captions


def load_image_by_caption_set(captions: dict[str, str]) -> dict[frozenset[str], str]:
    by_image: dict[str, list[str]] = {}
    for caption_id, text in captions.items():
        image_id = caption_id.rsplit("#", 1)[0]
        by_image.setdefault(image_id, []).append(text)
    return {frozenset(texts): image for image, texts in by_image.items()}


def load_local_image_map(captions: dict[str, str]) -> dict[str, str]:
    by_caption_set = load_image_by_caption_set(captions)
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for entry in manifest:
        row_idx = entry["row_idx"]
        caption_set = frozenset(entry["captions"])
        image_id = by_caption_set.get(caption_set)
        if image_id is None:
            raise ValueError(f"No Flickr8k image match for manifest row {row_idx}")
        mapping[image_id] = f"{MEDIA_PREFIX}/flickr8k_{row_idx:02d}.jpg"  # e.g. flickr8k/flickr8k_00.jpg
    return mapping


def caption_origin(reference_image: str, caption_id: str) -> str:
    caption_image = caption_id.rsplit("#", 1)[0]
    return "same_image" if caption_image == reference_image else "cross_image"


def caption_slot(caption_id: str) -> str:
    return caption_id.rsplit("#", 1)[1]


def parse_expert(local_images: set[str], captions: dict[str, str], media_map: dict[str, str]) -> list[dict]:
    rows: list[dict] = []
    row_id = 0
    for line in (TEXT / "ExpertAnnotations.txt").read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        reference_image, caption_id, score1, score2, score3 = parts[:5]
        if reference_image not in local_images:
            continue
        caption_text = captions.get(caption_id, "")
        base = {
            "dim::demo_image": media_map[reference_image].rsplit("/", 1)[-1].replace(".jpg", ""),
            "dim::caption_origin": caption_origin(reference_image, caption_id),
            "dim::caption_slot": caption_slot(caption_id),
            "dim::split": "test",
            "desc::reference_image": reference_image,
            "desc::caption_id": caption_id,
            "desc::caption": caption_text,
            "desc::caption_image": caption_id.rsplit("#", 1)[0],
            "med::image": media_map[reference_image],
        }
        for annotator_index, score in enumerate((score1, score2, score3), start=1):
            row_id += 1
            rows.append(
                {
                    "ID": f"flickr8k-expert-{row_id:05d}",
                    "dim::annotator_index": str(annotator_index),
                    "dim::score": score,
                    "res::score": score,
                    **base,
                }
            )
    return rows


def majority_label(yes_count: int, no_count: int) -> str:
    if yes_count > no_count:
        return "yes"
    if no_count > yes_count:
        return "no"
    return "tie"


def yes_fraction_band(yes_fraction: float) -> str:
    if yes_fraction >= 0.67:
        return "high"
    if yes_fraction >= 0.34:
        return "medium"
    return "low"


def parse_crowd(local_images: set[str], captions: dict[str, str], media_map: dict[str, str]) -> list[dict]:
    rows: list[dict] = []
    row_id = 0
    for line in (TEXT / "CrowdFlowerAnnotations.txt").read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        reference_image, caption_id, yes_fraction, yes_count, no_count = parts[:5]
        if reference_image not in local_images:
            continue
        yes_count_i = int(float(yes_count))
        no_count_i = int(float(no_count))
        yes_fraction_f = float(yes_fraction)
        row_id += 1
        rows.append(
            {
                "ID": f"flickr8k-crowd-{row_id:05d}",
                "dim::demo_image": media_map[reference_image].rsplit("/", 1)[-1].replace(".jpg", ""),
                "dim::caption_origin": caption_origin(reference_image, caption_id),
                "dim::caption_slot": caption_slot(caption_id),
                "dim::majority_match": majority_label(yes_count_i, no_count_i),
                "dim::yes_fraction_band": yes_fraction_band(yes_fraction_f),
                "dim::split": "test",
                "res::yes_fraction": f"{yes_fraction_f:.6f}",
                "res::yes_count": str(yes_count_i),
                "res::no_count": str(no_count_i),
                "res::total_judgments": str(yes_count_i + no_count_i),
                "desc::reference_image": reference_image,
                "desc::caption_id": caption_id,
                "desc::caption": captions.get(caption_id, ""),
                "desc::caption_image": caption_id.rsplit("#", 1)[0],
                "med::image": media_map[reference_image],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path.name}")
    fieldnames = list(rows[0].keys())
    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    captions = load_captions()
    media_map = load_local_image_map(captions)
    local_images = set(media_map)

    expert_rows = parse_expert(local_images, captions, media_map)
    crowd_rows = parse_crowd(local_images, captions, media_map)
    write_csv(EXPERT_CSV, expert_rows)
    write_csv(CROWD_CSV, crowd_rows)

    print(f"local images: {len(local_images)}")
    print(f"{EXPERT_CSV.name} rows: {len(expert_rows)}")
    print(f"{CROWD_CSV.name} rows: {len(crowd_rows)}")
    print(f"demo images: {sorted({r['dim::demo_image'] for r in expert_rows})}")


if __name__ == "__main__":
    main()
