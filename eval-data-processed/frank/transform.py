#!/usr/bin/env python3
"""Transform FRANK human annotations into PLeW-ready format."""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "frank"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_SENTENCE_CSV = OUT / f"{DATASET}_plew_sentence.csv"
OUTPUT_SUMMARY_CSV = OUT / f"{DATASET}_plew_summary.csv"

SEED = 42
HASH_SAMPLE_N = 50
MODEL_SAMPLE_N = 6

ANNOTATOR_KEYS = ["annotator_0", "annotator_1", "annotator_2"]

ERROR_GROUPS = {
    "NoE": "no_error",
    "RelE": "semantic_frame",
    "EntE": "semantic_frame",
    "CircE": "semantic_frame",
    "OutE": "semantic_frame",
    "CorefE": "discourse",
    "LinkE": "discourse",
    "GramE": "content_verifiability",
    "OtherE": "other",
    "Other": "other",
}

ERROR_LABELS = {
    "NoE": "No error",
    "RelE": "Relation error",
    "EntE": "Entity error",
    "CircE": "Circumstantial error",
    "OutE": "Out-of-article error",
    "CorefE": "Coreference error",
    "LinkE": "Discourse link error",
    "GramE": "Grammar error",
    "OtherE": "Other error",
    "Other": "Other error",
}

SUMMARY_CATEGORY_FIELDS = [
    "Semantic_Frame_Errors",
    "Discourse_Errors",
    "Content_Verifiability_Errors",
    "RelE",
    "EntE",
    "CircE",
    "OutE",
    "GramE",
    "CorefE",
    "LinkE",
    "Other",
]


def load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def article_id(hash_value: str) -> str:
    return f"art-{hash_value[:8]}"


def factuality_band(score: float) -> str:
    if score >= 0.8:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"


def category_clear(score: float) -> str:
    # FRANK summary scores: 1 = no error of this type, 0 = error in every sentence.
    return "yes" if float(score) >= 1.0 else "no"


def sample_key(rec: dict) -> tuple[str, str]:
    return rec["hash"], rec["model_name"]


def sample_records(records: list[dict], seed: int) -> list[dict]:
    rng = random.Random(seed)
    hashes = sorted({rec["hash"] for rec in records})
    models = sorted({rec["model_name"] for rec in records})
    sampled_hashes = set(rng.sample(hashes, min(HASH_SAMPLE_N, len(hashes))))
    sampled_models = set(rng.sample(models, min(MODEL_SAMPLE_N, len(models))))
    return [
        rec
        for rec in records
        if rec["hash"] in sampled_hashes and rec["model_name"] in sampled_models
    ]


def benchmark_lookup() -> dict[tuple[str, str], dict]:
    rows = load_json(RAW / "benchmark_data.json")
    return {sample_key(rec): rec for rec in rows}


def transform_sentence(
    records: list[dict],
    summaries: dict[tuple[str, str], dict],
) -> list[dict]:
    out: list[dict] = []
    row_id = 0
    for rec in records:
        summary = summaries[sample_key(rec)]
        base = {
            "dim::model": rec["model_name"],
            "dim::dataset": summary["dataset"],
            "dim::split": rec["split"],
            "dim::article_id": article_id(rec["hash"]),
            "res::factuality": summary["Factuality"],
            "desc::summary": rec["summary"],
            "desc::reference": rec["reference"],
            "desc::article": rec["article"],
            "desc::hash": rec["hash"],
        }
        for sentence_index, (sentence_text, ann_block) in enumerate(
            zip(rec["summary_sentences"], rec["summary_sentences_annotations"], strict=True),
            start=1,
        ):
            for annotator_key, tags in ann_block.items():
                annotator_index = str(ANNOTATOR_KEYS.index(annotator_key) + 1)
                for error_type in tags:
                    row_id += 1
                    out.append(
                        {
                            "ID": f"frank-sent-{row_id:05d}",
                            "dim::error_type": error_type,
                            "dim::error_group": ERROR_GROUPS.get(error_type, "other"),
                            "dim::sentence_index": str(sentence_index),
                            "dim::annotator_index": annotator_index,
                            "desc::error_label": ERROR_LABELS.get(error_type, error_type),
                            "desc::summary_sentence": sentence_text,
                            **base,
                        }
                    )
    return out


def transform_summary(
    records: list[dict],
    benchmark: dict[tuple[str, str], dict],
) -> list[dict]:
    out: list[dict] = []
    for row_id, rec in enumerate(records, start=1):
        key = sample_key(rec)
        texts = benchmark[key]
        factuality = float(rec["Factuality"])
        row = {
            "ID": f"frank-sum-{row_id:05d}",
            "dim::model": rec["model_name"],
            "dim::dataset": rec["dataset"],
            "dim::split": rec["split"],
            "dim::article_id": article_id(rec["hash"]),
            "dim::factuality_band": factuality_band(factuality),
            "res::factuality": rec["Factuality"],
            "desc::summary": texts["summary"],
            "desc::reference": texts["reference"],
            "desc::article": texts["article"],
            "desc::hash": rec["hash"],
        }
        for field in SUMMARY_CATEGORY_FIELDS:
            score = rec[field]
            row[f"res::{field}"] = score
            row[f"dim::{field}_clear"] = category_clear(score)
        out.append(row)
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def main() -> None:
    summary_rows = load_json(RAW / "human_annotations.json")
    sentence_rows = load_json(RAW / "human_annotations_sentence.json")
    benchmark = benchmark_lookup()
    summaries = {sample_key(rec): rec for rec in summary_rows}

    sampled_sentence = sample_records(sentence_rows, SEED)
    sampled_keys = {sample_key(rec) for rec in sampled_sentence}
    sampled_summary = [rec for rec in summary_rows if sample_key(rec) in sampled_keys]

    write_csv(OUTPUT_SENTENCE_CSV, transform_sentence(sampled_sentence, summaries))
    write_csv(OUTPUT_SUMMARY_CSV, transform_summary(sampled_summary, benchmark))


if __name__ == "__main__":
    main()
