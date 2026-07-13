#!/usr/bin/env python3
"""Validate a PLeW-ready CSV against prefix and dimension rules."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

MAX_ROWS_DEFAULT = 5000
MAX_DIM_CARDINALITY = 50
MIN_DIM_COLUMNS = 2


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_plew_csv.py <dataset_plew_ready.csv> [max_rows]", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else MAX_ROWS_DEFAULT

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    headers = reader.fieldnames or []
    errors: list[str] = []
    warnings: list[str] = []

    if not rows:
        errors.append("CSV has no data rows")

    dim_cols = [h for h in headers if h.startswith("dim::")]
    desc_cols = [h for h in headers if h.startswith("desc::")]
    med_cols = [h for h in headers if h.startswith("med::")]
    res_cols = [h for h in headers if h.startswith("res::")]
    bare = [h for h in headers if not h.startswith(("dim::", "desc::", "med::", "res::")) and h != "ID"]

    if len(dim_cols) < MIN_DIM_COLUMNS:
        errors.append(f"Need at least {MIN_DIM_COLUMNS} dim:: columns; found {len(dim_cols)}")

    if not desc_cols and not med_cols:
        warnings.append("No desc:: or med:: columns — record window may be empty")

    if bare:
        warnings.append(f"Unprefixed columns (may become auto-dims): {bare}")

    if len(rows) > max_rows:
        warnings.append(f"Row count {len(rows)} exceeds recommended max {max_rows}")

    for col in dim_cols:
        vals = {r.get(col, "") for r in rows}
        vals.discard("")
        if len(vals) > MAX_DIM_CARDINALITY:
            errors.append(f"{col} has {len(vals)} unique values (max {MAX_DIM_CARDINALITY})")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN: {w}")
        sys.exit(1)

    print("OK")
    print(f"  rows: {len(rows)}")
    print(f"  dim:: ({len(dim_cols)}): {', '.join(c.replace('dim::', '') for c in dim_cols)}")
    print(f"  desc:: ({len(desc_cols)}), med:: ({len(med_cols)}), res:: ({len(res_cols)})")
    for w in warnings:
        print(f"  WARN: {w}")


if __name__ == "__main__":
    main()
