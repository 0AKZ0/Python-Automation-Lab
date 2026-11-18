import csv
import tempfile
import unittest
from pathlib import Path
from automation_lab.core import build_report, clean_csv, read_csv

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "input.csv"
        self.source.write_text(" Customer Name ,Amount\nAna,10\nAna,10\n,,\n", encoding="utf-8")
    def tearDown(self):
        self.temp.cleanup()
    def test_normalizes_headers_and_skips_blank_rows(self):
        headers, rows = read_csv(self.source)
        self.assertEqual(headers, ["customer_name", "amount"])
        self.assertEqual(len(rows), 2)
    def test_clean_deduplicates(self):
        output = self.root / "out" / "clean.csv"
        result = clean_csv(self.source, output)
        self.assertEqual(result["duplicates_removed"], 1)
        with output.open(encoding="utf-8", newline="") as handle:
            self.assertEqual(len(list(csv.DictReader(handle))), 1)
    def test_report_counts_duplicates(self):
        self.assertEqual(build_report(self.source)["duplicate_rows"], 1)

if __name__ == "__main__":
    unittest.main()
