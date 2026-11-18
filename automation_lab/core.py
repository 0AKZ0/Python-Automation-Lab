"""CSV cleaning and quality reporting built on the Python standard library."""
from __future__ import annotations
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

def normalize_header(value: str, index: int) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower()).strip("_")
    return value or f"column_{index + 1}"

def read_csv(path: str | Path) -> tuple[list[str], list[dict[str, str]]]:
    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"No header row found in {source}")
        original = reader.fieldnames
        headers = [normalize_header(name or "", i) for i, name in enumerate(original)]
        if len(headers) != len(set(headers)):
            raise ValueError("Column names collide after normalization")
        rows = []
        for raw in reader:
            row = {headers[i]: (raw.get(name) or "").strip() for i, name in enumerate(original)}
            if any(row.values()):
                rows.append(row)
    return headers, rows

def clean_csv(source: str | Path, destination: str | Path) -> dict[str, int]:
    headers, rows = read_csv(source)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    seen: set[tuple[str, ...]] = set()
    unique = []
    for row in rows:
        key = tuple(row[h] for h in headers)
        if key not in seen:
            seen.add(key)
            unique.append(row)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(unique)
    return {"rows_read": len(rows), "rows_written": len(unique), "duplicates_removed": len(rows) - len(unique)}

def build_report(source: str | Path) -> dict[str, Any]:
    headers, rows = read_csv(source)
    fingerprints = [tuple(row[h] for h in headers) for row in rows]
    counts = Counter(fingerprints)
    return {
        "file": Path(source).name,
        "row_count": len(rows),
        "column_count": len(headers),
        "columns": headers,
        "missing_values": {h: sum(not row[h] for row in rows) for h in headers},
        "duplicate_rows": sum(n - 1 for n in counts.values() if n > 1),
    }

def write_report(source: str | Path, destination: str | Path) -> dict[str, Any]:
    report = build_report(source)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
