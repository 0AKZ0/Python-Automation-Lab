# Python Automation Lab

A practical CSV automation toolkit built with Python's standard library. It normalizes messy exports, removes empty and duplicate rows, and generates data-quality reports.

## Requirements
Python 3.10+. No third-party dependencies.

## Quick start
```bash
python -m automation_lab inspect data/sales.csv
python -m automation_lab clean data/sales.csv --output output/sales_clean.csv
python -m automation_lab report data/sales.csv --output output/report.json
python -m unittest discover -s tests -v
```

## Commands
- `inspect FILE`: summarize rows, columns, missing values and duplicates.
- `clean FILE --output PATH`: normalize headers/values, skip blank rows and deduplicate.
- `report FILE --output PATH`: write a JSON quality report.

## Structure
```text
automation_lab/  # reusable processing and CLI
data/            # sample input
tests/           # unit tests
```

The tool processes files locally; it does not send data to external services. Review privacy and retention requirements before using it with sensitive datasets.

MIT License.
