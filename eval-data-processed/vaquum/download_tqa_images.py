#!/usr/bin/env python3
"""Download the VAQUUM TQA (Visual Genome) images into eval-data-raw/vaquum/images/.

Only the 69 TQA-sourced images are fetched here; FSC-147 images are distributed
as a single Google Drive zip and must be obtained separately (see PLEW_MANIFEST.md).

Visual Genome image ids live in either the VG_100K or VG_100K_2 bucket, so both
are tried. Existing non-empty files are skipped, so this is safe to re-run.
"""

from __future__ import annotations

import csv
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMAGES_CSV = ROOT / "eval-data-raw" / "vaquum" / "images.csv"
IMAGE_DIR = ROOT / "eval-data-raw" / "vaquum" / "images"

VG_BASES = (
    "https://cs.stanford.edu/people/rak248/VG_100K/",
    "https://cs.stanford.edu/people/rak248/VG_100K_2/",
)


def fetch(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception:
        return None


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    with IMAGES_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["dataset"] == "tqa"]

    ok = skipped = failed = 0
    for row in rows:
        dst = IMAGE_DIR / row["img_name"]
        if dst.exists() and dst.stat().st_size > 0:
            skipped += 1
            continue
        for base in VG_BASES:
            data = fetch(f"{base}{row['original_img_id']}.jpg")
            if data:
                dst.write_bytes(data)
                ok += 1
                break
        else:
            failed += 1
            print(f"FAIL {row['img_name']} (vg id {row['original_img_id']})")

    print(f"tqa images: downloaded={ok} skipped={skipped} failed={failed} of {len(rows)}")


if __name__ == "__main__":
    main()
