#!/usr/bin/env python3
"""Transform SummEval model_annotations.aligned.jsonl into PLeW-ready format."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "summeval" / "model_annotations.aligned.jsonl"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

SEED = 42
ARTICLE_SAMPLE_N = 15
MODEL_SAMPLE_N = 4

CRITERIA = ("coherence", "consistency", "fluency", "relevance")


def article_id(article_key: str) -> str:
    digest = hashlib.sha1(article_key.encode("utf-8")).hexdigest()[:8]
    return f"art-{digest}"


def load_rows() -> list[dict]:
    rows: list[dict] = []
    with RAW.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def sample_records(rows: list[dict], seed: int) -> list[dict]:
    rng = random.Random(seed)
    article_ids = sorted({r["id"] for r in rows})
    models = sorted({r["model_id"] for r in rows})
    sampled_articles = set(rng.sample(article_ids, min(ARTICLE_SAMPLE_N, len(article_ids))))
    sampled_models = set(rng.sample(models, min(MODEL_SAMPLE_N, len(models))))
    return [
        r
        for r in rows
        if r["id"] in sampled_articles and r["model_id"] in sampled_models
    ]


def format_references(references: list[str] | None) -> str:
    if not references:
        return ""
    return " | ".join(references)


def transform(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    row_id = 0
    for rec in rows:
        base = {
            "dim::model": rec["model_id"],
            "dim::article_id": article_id(rec["id"]),
            "desc::article_id": rec["id"],
            "desc::summary": rec.get("decoded") or "",
            "desc::references": format_references(rec.get("references")),
            "desc::story_path": rec.get("filepath") or "",
        }
        annotation_groups = (
            ("expert", rec.get("expert_annotations") or []),
            ("crowd", rec.get("turker_annotations") or []),
        )
        for annotator_group, annotations in annotation_groups:
            for annotator_index, annotation in enumerate(annotations, start=1):
                for criterion in CRITERIA:
                    score = annotation.get(criterion)
                    if score is None:
                        continue
                    row_id += 1
                    out.append(
                        {
                            "ID": f"summeval-{row_id:05d}",
                            "dim::criterion": criterion,
                            "dim::annotator_group": annotator_group,
                            "dim::annotator_index": str(annotator_index),
                            "dim::score": str(score),
                            "res::score": str(score),
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
    print(f"sampled rows (article×model): {len(sampled)}")
    print(f"{OUTPUT_CSV.name} rows: {len(plew_rows)}")
    print(f"articles: {len({r['dim::article_id'] for r in plew_rows})}")
    print(f"models: {sorted({r['dim::model'] for r in plew_rows})}")


if __name__ == "__main__":
    main()
