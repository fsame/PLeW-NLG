#!/usr/bin/env python3
"""Transform book_highlights LLM-as-judge raw JSON into PLeW-ready CSV."""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "book_highlights_llm_as_a_judge"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"
OUTPUT_FAITHFULNESS_CSV = OUT / f"{DATASET}_plew_faithfulness.csv"

SEED = 42
PAIR_SAMPLE_N = 300
CRITERIA = [
    "informativeness",
    "saliency",
    "fluency_style",
    "coherence",
    "theme_adherence",
]


def resolve_winner(winner: str, a_side: str, b_side: str) -> str:
    if winner == "A":
        return a_side
    if winner == "B":
        return b_side
    return winner


def clean(val) -> str:
    if val is None:
        return ""
    if isinstance(val, float) and val != val:  # NaN
        return ""
    if isinstance(val, bool):
        return str(val)
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False)
    return str(val)


def load_preference_pairs() -> list[dict]:
    data = json.loads((RAW / "llm_judge_preference.json").read_text(encoding="utf-8"))
    return list(data.values())


def stratified_pair_sample(pairs: list[dict], n: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    by_axis: dict[str, list[dict]] = {}
    for rec in pairs:
        axis = (rec.get("metadata") or {}).get("comparison_axis", "unknown")
        by_axis.setdefault(axis, []).append(rec)

    per_axis = n // len(by_axis)
    remainder = n % len(by_axis)
    sampled: list[dict] = []
    for i, (axis, group) in enumerate(sorted(by_axis.items())):
        k = per_axis + (1 if i < remainder else 0)
        k = min(k, len(group))
        sampled.extend(rng.sample(group, k))
    return sampled


def transform_preference(pairs: list[dict]) -> list[dict]:
    rows: list[dict] = []
    row_id = 0
    for rec in pairs:
        md = rec.get("metadata") or {}
        a_side = clean(rec.get("candidate_a_source_side"))
        b_side = clean(rec.get("candidate_b_source_side"))
        pair_id = clean(rec.get("pair_id"))
        base = {
            "dim::comparison_axis": clean(md.get("comparison_axis")),
            "dim::book": clean(rec.get("book_title") or md.get("title_in_metadata_file")),
            "dim::theme": clean(rec.get("theme") or md.get("theme")),
            "dim::relation": clean(md.get("relation") or rec.get("theme")),
            "dim::candidate_a_side": a_side,
            "dim::candidate_b_side": b_side,
            "dim::sampling_mode": clean(md.get("sampling_mode")),
            "desc::pair_id": pair_id,
            "desc::book_id": clean(rec.get("book_id") or md.get("book_id_prompt")),
            "desc::book_title": clean(rec.get("book_title")),
            "desc::author": clean(rec.get("author") or md.get("author")),
            "desc::asin": clean(md.get("asin")),
            "desc::candidate_a": clean(md.get("candidate_a_text") or md.get("candidate_a")),
            "desc::candidate_b": clean(md.get("candidate_b_text") or md.get("candidate_b")),
            "desc::candidate_a_title": clean(md.get("candidate_a_title")),
            "desc::candidate_b_title": clean(md.get("candidate_b_title")),
            "desc::sample_name": clean(md.get("sample_name")),
            "res::similarity": clean(md.get("similarity")),
            "res::review_count": clean(md.get("review_count")),
        }

        criteria = dict(rec.get("criteria") or {})
        overall = rec.get("overall_preference") or {}
        criteria["overall"] = {
            "winner": overall.get("winner"),
            "confidence": overall.get("confidence"),
            "rationale": overall.get("rationale"),
            "dominant_factors": overall.get("dominant_factors"),
        }

        for criterion, judgment in criteria.items():
            row_id += 1
            winner_blind = clean(judgment.get("winner"))
            row = {
                "ID": f"bookhl-pref-{row_id:05d}",
                "dim::criterion": criterion,
                "dim::winner_blind": winner_blind,
                "dim::winner_resolved": resolve_winner(winner_blind, a_side, b_side),
                "dim::confidence": clean(judgment.get("confidence")),
                **base,
                "desc::rationale": clean(judgment.get("rationale")),
                "desc::dominant_factors": clean(judgment.get("dominant_factors")),
            }
            rows.append(row)
    return rows


def transform_faithfulness() -> list[dict]:
    data = json.loads((RAW / "llm_judge_faithfulness.json").read_text(encoding="utf-8"))
    rows: list[dict] = []
    for i, rec in enumerate(data.values(), start=1):
        rows.append(
            {
                "ID": f"bookhl-faith-{i:05d}",
                "dim::book": clean(rec.get("book_title")),
                "dim::theme": clean(rec.get("theme")),
                "dim::relation": clean(rec.get("relation")),
                "dim::system": clean(rec.get("system")),
                "dim::model": clean(rec.get("model")),
                "dim::size_label": clean(rec.get("size_label")),
                "dim::factually_accurate": clean(rec.get("factually_accurate")),
                "dim::divergence_type": clean(rec.get("divergence_type")),
                "res::severity": clean(rec.get("severity")),
                "desc::highlight_id": clean(rec.get("highlight_id")),
                "desc::pair_id": clean(rec.get("pair_id")),
                "desc::book_id": clean(rec.get("book_id")),
                "desc::book_title": clean(rec.get("book_title")),
                "desc::author": clean(rec.get("author")),
                "desc::asin": clean(rec.get("asin")),
                "desc::rationale": clean(rec.get("rationale")),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
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

    all_pairs = load_preference_pairs()
    sampled_pairs = stratified_pair_sample(all_pairs, PAIR_SAMPLE_N, SEED)
    pref_rows = transform_preference(sampled_pairs)
    faith_rows = transform_faithfulness()

    write_csv(OUTPUT_CSV, pref_rows)
    write_csv(OUTPUT_FAITHFULNESS_CSV, faith_rows)

    print(f"preference pairs sampled: {len(sampled_pairs)} of {len(all_pairs)}")
    print(f"{OUTPUT_CSV.name} rows: {len(pref_rows)}")
    print(f"{OUTPUT_FAITHFULNESS_CSV.name} rows: {len(faith_rows)}")


if __name__ == "__main__":
    main()
