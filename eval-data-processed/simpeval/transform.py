#!/usr/bin/env python3
"""Transform SimpEval (LENS simpeval_past.csv) into PLeW-ready format."""

from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "simpeval" / "LENS" / "data" / "simpeval_past.csv"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

SEED = 42
SENTENCE_SAMPLE_N = 20
SYSTEM_SAMPLE_N = 6
RATER_COLUMNS = [
    ("rating_1", "rating_1_z_score"),
    ("rating_2", "rating_2_z_score"),
    ("rating_3", "rating_3_z_score"),
    ("rating_4", "rating_4_z_score"),
    ("rating_5", "rating_5_z_score"),
]


def score_band(score: str) -> str:
    value = int(float(score))
    if value <= 20:
        return "0-20"
    if value <= 40:
        return "21-40"
    if value <= 60:
        return "41-60"
    if value <= 80:
        return "61-80"
    return "81-100"


def load_rows() -> list[dict]:
    with RAW.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sample_records(rows: list[dict], seed: int) -> list[dict]:
    rng = random.Random(seed)
    sentence_ids = sorted({r["original_id"] for r in rows})
    systems = sorted({r["system"] for r in rows})
    sampled_sentences = set(rng.sample(sentence_ids, min(SENTENCE_SAMPLE_N, len(sentence_ids))))
    sampled_systems = set(rng.sample(systems, min(SYSTEM_SAMPLE_N, len(systems))))
    return [
        r
        for r in rows
        if r["original_id"] in sampled_sentences and r["system"] in sampled_systems
    ]


def transform(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    row_id = 0
    for rec in rows:
        simplification = rec.get("processed_generation") or rec.get("generation") or ""
        base = {
            "dim::system": rec["system"],
            "dim::sentence_id": rec["original_id"],
            "desc::original": rec["original"],
            "desc::simplification": simplification,
            "desc::generation_raw": rec.get("generation") or "",
        }
        for annotator_index, (rating_col, z_col) in enumerate(RATER_COLUMNS, start=1):
            score = rec[rating_col]
            row_id += 1
            out.append(
                {
                    "ID": f"simpeval-{row_id:05d}",
                    "dim::annotator_index": str(annotator_index),
                    "dim::score_band": score_band(score),
                    "res::score": score,
                    "res::z_score": rec.get(z_col) or "",
                    **base,
                }
            )
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys())
    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows = load_rows()
    sampled = sample_records(all_rows, SEED)
    plew_rows = transform(sampled)
    write_csv(OUTPUT_CSV, plew_rows)

    print(f"input rows: {len(all_rows)}")
    print(f"sampled rows (sentence×system): {len(sampled)}")
    print(f"{OUTPUT_CSV.name} rows: {len(plew_rows)}")
    print(f"sentences: {len({r['dim::sentence_id'] for r in plew_rows})}")
    print(f"systems: {sorted({r['dim::system'] for r in plew_rows})}")


if __name__ == "__main__":
    main()
