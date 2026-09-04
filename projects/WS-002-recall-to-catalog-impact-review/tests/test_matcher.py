from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "src"
FIXTURES = PROJECT / "tests" / "fixtures"
sys.path.insert(0, str(SRC))

from catalog_matcher import ALLOWED_RECALL_FIELDS, evaluate, match_catalog  # noqa: E402


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class CatalogMatcherTests(unittest.TestCase):
    def setUp(self):
        self.recalls = load("recalls.json")

    def run_fixture(self, catalog_name="catalog.json", labels_name="expected-labels.json"):
        results = match_catalog(
            load(catalog_name), self.recalls["records"], self.recalls["provenance"]
        )
        return results, evaluate(results, load(labels_name))

    def test_baseline_reproduces_independent_labels(self):
        _, evaluation = self.run_fixture()
        self.assertEqual(evaluation["labels_total"], 8)
        self.assertEqual(evaluation["labels_failed"], 0)

    def test_expansion_benchmark_reproduces_twenty_labels(self):
        results, evaluation = self.run_fixture(
            "benchmark-catalog.json", "benchmark-labels.json"
        )
        self.assertEqual(evaluation["labels_total"], 20)
        self.assertEqual(evaluation["labels_failed"], 0)
        self.assertGreaterEqual(
            sum(row["classification"] == "review_needed" for row in results), 4
        )

    def test_all_three_queue_states_are_present(self):
        results, _ = self.run_fixture()
        self.assertEqual(
            {row["classification"] for row in results},
            {"match", "no_match", "review_needed"},
        )

    def test_conflicting_strength_routes_to_review(self):
        results, _ = self.run_fixture()
        row = next(item for item in results if item["catalog_id"] == "CAT-005")
        self.assertEqual(row["classification"], "review_needed")
        self.assertIn("strength_conflict", row["reasons"])
        self.assertEqual(row["matched_recall_number"], None)

    def test_changed_input_changes_review_to_match(self):
        baseline, _ = self.run_fixture()
        changed, evaluation = self.run_fixture(
            "catalog-changed.json", "expected-labels-changed.json"
        )
        before = next(row for row in baseline if row["catalog_id"] == "CAT-005")
        after = next(row for row in changed if row["catalog_id"] == "CAT-005")
        self.assertEqual(before["classification"], "review_needed")
        self.assertEqual(after["classification"], "match")
        self.assertEqual(after["matched_recall_number"], "D-0709-2026")
        self.assertEqual(evaluation["labels_failed"], 0)

    def test_provenance_and_fingerprint_are_attached_to_matches(self):
        results, _ = self.run_fixture()
        matched = [row for row in results if row["classification"] == "match"]
        self.assertTrue(matched)
        for row in matched:
            self.assertTrue(row["source_url"].startswith("https://api.fda.gov/"))
            self.assertEqual(len(row["content_fingerprint"]), 64)
            int(row["content_fingerprint"], 16)

    def test_review_candidates_each_retain_provenance(self):
        results, _ = self.run_fixture()
        row = next(item for item in results if item["catalog_id"] == "CAT-005")
        self.assertEqual(len(row["candidate_provenance"]), 2)
        for candidate in row["candidate_provenance"]:
            self.assertTrue(candidate["source_url"].startswith("https://api.fda.gov/"))
            self.assertEqual(len(candidate["content_fingerprint"]), 64)
            int(candidate["content_fingerprint"], 16)

    def test_fixture_persists_only_declared_fields(self):
        for recall in self.recalls["records"]:
            self.assertEqual(set(recall), ALLOWED_RECALL_FIELDS)
            self.assertNotIn("status", recall)
            self.assertNotIn("reason_for_recall", recall)

    def test_results_are_deterministic(self):
        first, _ = self.run_fixture()
        second, _ = self.run_fixture()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
