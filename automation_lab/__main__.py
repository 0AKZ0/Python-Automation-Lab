"""Command-line entry point."""
import argparse
import json
from pathlib import Path
from .core import build_report, clean_csv, write_report

def main() -> int:
    parser = argparse.ArgumentParser(description="Local CSV cleaning and quality reports")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect", help="Inspect a CSV")
    inspect.add_argument("source", type=Path)
    clean = sub.add_parser("clean", help="Clean and deduplicate a CSV")
    clean.add_argument("source", type=Path)
    clean.add_argument("--output", required=True, type=Path)
    report = sub.add_parser("report", help="Export a JSON quality report")
    report.add_argument("source", type=Path)
    report.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            result = build_report(args.source)
        elif args.command == "clean":
            result = clean_csv(args.source, args.output)
        else:
            result = write_report(args.source, args.output)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")

if __name__ == "__main__":
    raise SystemExit(main())
