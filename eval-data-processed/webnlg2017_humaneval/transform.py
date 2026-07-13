#!/usr/bin/env python3
"""Transform WebNLG 2017 human evaluation CSV into PLeW-ready format."""

from __future__ import annotations

import csv
import hashlib
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = (
    ROOT
    / "eval-data-raw"
    / "webnlg2017_humaneval"
    / "webnlg-human-evaluation"
    / "all_data_final_scores_anonymised.csv"
)
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

SEED = 42
MR_SAMPLE_N = 18
TEAM_SAMPLE_N = 5
CRITERIA = [
    ("fluency", "fluency"),
    ("grammaticality", "grammaticality"),
    ("semantic_adequacy", "semantic_adequacy"),
]


def mr_id(mr: str) -> str:
    digest = hashlib.sha1(mr.encode("utf-8")).hexdigest()[:8]
    return f"mr-{digest}"


def load_rows() -> list[dict]:
    with RAW.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sample_records(rows: list[dict], seed: int) -> list[dict]:
    rng = random.Random(seed)
    mrs = sorted({r["mr"] for r in rows})
    teams = sorted({r["team"] for r in rows})
    sampled_mrs = set(rng.sample(mrs, min(MR_SAMPLE_N, len(mrs))))
    sampled_teams = set(rng.sample(teams, min(TEAM_SAMPLE_N, len(teams))))
    return [r for r in rows if r["mr"] in sampled_mrs and r["team"] in sampled_teams]


def transform(rows: list[dict]) -> list[dict]:
    # Stable rater index within each (mr, system) for grid-friendly disagreement views.
    group_workers: dict[tuple[str, str], list[str]] = {}
    for rec in rows:
        key = (rec["mr"], rec["team"])
        wid = rec["X_worker_id"]
        if wid not in group_workers.setdefault(key, []):
            group_workers[key].append(wid)

    out: list[dict] = []
    row_id = 0
    for rec in rows:
        workers = group_workers[(rec["mr"], rec["team"])]
        annotator_index = str(workers.index(rec["X_worker_id"]) + 1)
        base = {
            "dim::system": rec["team"],
            "dim::category": rec["category"],
            "dim::type": rec["type"],
            "dim::triplesize": rec["triplesize"],
            "dim::systemtype": rec["systemtype"],
            "dim::mr_id": mr_id(rec["mr"]),
            "dim::annotator_index": annotator_index,
            "desc::annotator": rec["X_worker_id"],
            "desc::unit_id": rec["X_unit_id"],
            "desc::mr": rec["mr"],
            "desc::text": rec.get("text") or "",
            "res::bleu": rec["bleu"],
            "res::meteor": rec["meteor"],
            "res::ter": rec["ter"],
        }
        for criterion_key, criterion_label in CRITERIA:
            row_id += 1
            score = rec[criterion_key]
            out.append(
                {
                    "ID": f"webnlg17-{row_id:05d}",
                    "dim::criterion": criterion_label,
                    "dim::score": score,
                    "res::score": score,
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
    print(f"sampled rows (mr×team×rater): {len(sampled)}")
    print(f"{OUTPUT_CSV.name} rows: {len(plew_rows)}")
    print(f"unique mr: {len({r['dim::mr_id'] for r in plew_rows})}")
    print(f"systems: {sorted({r['dim::system'] for r in plew_rows})}")


if __name__ == "__main__":
    main()
