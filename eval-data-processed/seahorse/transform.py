#!/usr/bin/env python3
"""Transform SEAHORSE validation TSV into PLeW-ready format."""

from __future__ import annotations

import csv
import hashlib
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "seahorse" / "seahorse_data" / "validation.tsv"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

SEED = 42
GEM_ID_SAMPLE_N = 500
MODEL_SAMPLE_N = 6

CRITERIA = [
    ("question1", "comprehensibility"),
    ("question2", "repetition"),
    ("question3", "grammar"),
    ("question4", "attribution"),
    ("question5", "main_ideas"),
    ("question6", "conciseness"),
]

RATING_SCORE = {"Yes": "1", "No": "0", "Unsure": "0.5"}


def article_id(gem_id: str) -> str:
    digest = hashlib.sha1(gem_id.encode("utf-8")).hexdigest()[:8]
    return f"art-{digest}"


def parse_dataset(gem_id: str) -> str:
    if gem_id.startswith("xsum-"):
        return "xsum"
    if gem_id.startswith("mlsum_"):
        return gem_id.split("-", 1)[0]
    if gem_id.startswith("xlsum_"):
        if "-validation-" in gem_id:
            return gem_id.split("-validation-", 1)[0]
        return gem_id.rsplit("-", 2)[0]
    if gem_id.startswith("wiki_lingua_"):
        if "-val-" in gem_id:
            return gem_id.split("-val-", 1)[0]
        return gem_id.rsplit("-", 2)[0]
    return gem_id.rsplit("-", 2)[0]


def load_rows() -> list[dict]:
    with RAW.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def sample_records(rows: list[dict], seed: int) -> list[dict]:
    rng = random.Random(seed)
    gem_ids = sorted({r["gem_id"] for r in rows})
    models = sorted({r["model"] for r in rows})
    sampled_gem_ids = set(rng.sample(gem_ids, min(GEM_ID_SAMPLE_N, len(gem_ids))))
    sampled_models = set(rng.sample(models, min(MODEL_SAMPLE_N, len(models))))
    return [
        r
        for r in rows
        if r["gem_id"] in sampled_gem_ids and r["model"] in sampled_models
    ]


def transform(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    row_id = 0
    for rec in rows:
        base = {
            "dim::model": rec["model"],
            "dim::worker_lang": rec["worker_lang"],
            "dim::dataset": parse_dataset(rec["gem_id"]),
            "dim::article_id": article_id(rec["gem_id"]),
            "desc::gem_id": rec["gem_id"],
            "desc::summary": rec["summary"],
        }
        for question_col, criterion_label in CRITERIA:
            rating = (rec.get(question_col) or "").strip()
            if not rating:
                continue
            row_id += 1
            out.append(
                {
                    "ID": f"seahorse-{row_id:05d}",
                    "dim::criterion": criterion_label,
                    "dim::rating": rating,
                    "res::rating_code": RATING_SCORE.get(rating, ""),
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
    print(f"sampled rows (gem_id×model): {len(sampled)}")
    print(f"{OUTPUT_CSV.name} rows: {len(plew_rows)}")
    print(f"articles: {len({r['dim::article_id'] for r in plew_rows})}")
    print(f"models: {sorted({r['dim::model'] for r in plew_rows})}")
    print(f"datasets: {sorted({r['dim::dataset'] for r in plew_rows})}")


if __name__ == "__main__":
    main()
