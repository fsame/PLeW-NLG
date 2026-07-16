#!/usr/bin/env python3
"""Transform NeuralREG human evaluation JSON into PLeW-ready format."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "eval-data-raw" / "neuralreg_humaneval"
OUT = Path(__file__).resolve().parent
DATASET = OUT.name
OUTPUT_CSV = OUT / f"{DATASET}_plew_ready.csv"

MODELS = ["original", "only", "ferreira", "seq2seq", "catt", "hieratt"]
CRITERIA = ["fluency", "grammar", "clarity"]


def load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        payload = json.load(f)
    return payload["RECORDS"]


def parse_trial_info(path: Path) -> dict[str, dict]:
    mapping: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("-") or line.startswith("text_id"):
            continue
        parts = re.split(r"\s{2,}", line)
        if len(parts) < 9:
            continue
        text_id, size, difficulty = parts[0], parts[1], parts[2]
        lists = parts[3:9]
        mapping[text_id] = {
            "size": size,
            "difficulty": difficulty,
            "lists": {str(i + 1): lists[i] for i in range(6)},
        }
    return mapping


def parse_text_trials(path: Path) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped in MODELS:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = stripped
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def load_texts(text_trials_dir: Path) -> dict[str, dict[str, str]]:
    texts: dict[str, dict[str, str]] = {}
    for path in sorted(text_trials_dir.iterdir()):
        if path.name == "trial_info" or path.is_dir():
            continue
        texts[path.name] = parse_text_trials(path)
    return texts


def load_participants(path: Path) -> dict[str, dict]:
    return {row["id"]: row for row in load_json(path)}


def parse_url(url: str) -> tuple[str, str]:
    match = re.match(r"list(\d+)/(\d+)\.php$", url)
    if not match:
        raise ValueError(f"Unexpected url format: {url}")
    return match.group(1), match.group(2)


def transform() -> list[dict]:
    results = load_json(RAW / "experiment_results.json")
    participants = load_participants(RAW / "participants_info.json")
    trial_info = parse_trial_info(RAW / "text_trials" / "trial_info")
    texts = load_texts(RAW / "text_trials")

    group_participants: dict[tuple[str, str], list[str]] = {}
    for rec in results:
        list_num, text_id = parse_url(rec["url"])
        system = trial_info[text_id]["lists"][list_num]
        key = (text_id, system)
        pid = rec["participant_id"]
        if pid not in group_participants.setdefault(key, []):
            group_participants[key].append(pid)

    out: list[dict] = []
    row_id = 0
    for rec in results:
        list_num, text_id = parse_url(rec["url"])
        if rec["list_id"] != list_num:
            raise ValueError(
                f"list_id mismatch for participant {rec['participant_id']}: "
                f"{rec['list_id']} vs {list_num}"
            )

        trial = trial_info[text_id]
        system = trial["lists"][list_num]
        text_variants = texts[text_id]
        realization = text_variants.get(system, "")
        original = text_variants.get("original", "")

        participant = participants.get(rec["participant_id"], {})
        annotator_index = group_participants[(text_id, system)].index(rec["participant_id"]) + 1
        base = {
            "dim::system": system,
            "dim::text_id": text_id,
            "dim::text_size": trial["size"],
            "dim::difficulty": trial["difficulty"],
            "dim::list_id": list_num,
            "dim::annotator_index": str(annotator_index),
            "dim::english_proficiency": participant.get("english_proficiency_level", ""),
            "desc::realization": realization,
            "desc::original": original,
            "desc::participant_id": rec["participant_id"],
            "desc::participant_country": participant.get("country", ""),
            "desc::participant_native_language": participant.get("native_language", ""),
        }

        for criterion in CRITERIA:
            score = rec[criterion]
            row_id += 1
            out.append(
                {
                    "ID": f"neuralreg-{row_id:05d}",
                    "dim::criterion": criterion,
                    "dim::score": score,
                    "res::score": score,
                    **base,
                }
            )
    return out


def main() -> None:
    rows = transform()
    fieldnames = list(rows[0].keys())
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
