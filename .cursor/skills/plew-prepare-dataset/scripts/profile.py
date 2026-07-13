#!/usr/bin/env python3
"""Profile a dataset file for PLeW suitability (format-agnostic)."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path


def load_rows(path: Path) -> tuple[list[dict], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    suffix = path.suffix.lower()

    if suffix == ".csv":
        reader = csv.DictReader(text.splitlines())
        return list(reader), "csv"

    if suffix in {".json", ".jsonl", ".ndjson"}:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            rows = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
            return rows, "jsonl"

        if isinstance(parsed, list):
            return parsed, "json-array"
        if isinstance(parsed, dict):
            if "rows" in parsed and isinstance(parsed["rows"], list):
                out = []
                for item in parsed["rows"]:
                    if isinstance(item, dict) and "row" in item:
                        out.append(item["row"])
                    else:
                        out.append(item)
                return out, "hf-rows"
            return list(parsed.values()), "json-dict-values"
        return [{"value": parsed}], "json-scalar"

    if suffix == ".tsv":
        reader = csv.DictReader(text.splitlines(), delimiter="\t")
        return list(reader), "tsv"

    raise ValueError(f"Unsupported format: {suffix}")


def flatten_value(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)[:200]
    return str(v)


def profile_rows(rows: list[dict]) -> dict:
    if not rows:
        return {"row_count": 0, "columns": {}}

    keys: list[str] = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        for k in row:
            if k not in seen:
                seen.add(k)
                keys.append(k)

    columns = {}
    for key in keys:
        values = [flatten_value(r.get(key)) for r in rows if isinstance(r, dict)]
        non_empty = [v for v in values if v]
        lengths = [len(v) for v in non_empty]
        uniq = set(non_empty)
        columns[key] = {
            "non_empty": len(non_empty),
            "unique": len(uniq),
            "unique_ratio": round(len(uniq) / max(len(non_empty), 1), 3),
            "avg_len": round(sum(lengths) / max(len(lengths), 1), 1),
            "max_len": max(lengths) if lengths else 0,
            "sample": list(uniq)[:3],
        }

    return {"row_count": len(rows), "columns": columns}


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: profile.py <dataset-file>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    rows, fmt = load_rows(path)
    report = profile_rows(rows)
    report["path"] = str(path)
    report["format"] = fmt
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
