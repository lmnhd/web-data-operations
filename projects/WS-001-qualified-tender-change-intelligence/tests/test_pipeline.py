from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

from fetch_sanitized_record import sanitize_package  # noqa: E402
from tender_pipeline import extract_releases, normalize_release, run_pipeline  # noqa: E402


class TenderPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads((PROJECT / "tests/fixtures/release-package.json").read_text(encoding="utf-8"))
        cls.profile = json.loads((PROJECT / "examples/qualification-profile.json").read_text(encoding="utf-8"))
        cls.result = run_pipeline(
            cls.payload,
            cls.profile,
            "fixture://ws-001/release-package",
            "2026-09-03T00:00:00Z",
        )

    def test_update_tag_is_not_treated_as_material_change(self) -> None:
        unchanged = next(
            row for row in self.result["queues"]["rejected"] if row["ocid"] == "ocds-demo-unchanged"
        )
        self.assertEqual([], unchanged["changes"])
        self.assertEqual(["NO_MATERIAL_CHANGE"], unchanged["reason_codes"])

    def test_qualified_material_change_is_accepted(self) -> None:
        accepted = self.result["queues"]["accepted"]
        self.assertEqual(1, len(accepted))
        self.assertEqual("ocds-demo-qualified-change", accepted[0]["ocid"])
        self.assertEqual("tender.tenderPeriod.endDate", accepted[0]["changes"][0]["field"])

    def test_unqualified_change_is_rejected_with_reason(self) -> None:
        rejected = next(
            row for row in self.result["queues"]["rejected"] if row["ocid"] == "ocds-demo-unqualified-change"
        )
        self.assertIn("CLASSIFICATION_NOT_ALLOWED", rejected["reason_codes"])

    def test_missing_required_evidence_routes_to_review(self) -> None:
        review = self.result["queues"]["review-needed"]
        self.assertEqual(1, len(review))
        self.assertEqual(["MISSING_CLASSIFICATION"], review[0]["reason_codes"])

    def test_normalization_excludes_contacts_and_free_text(self) -> None:
        first = extract_releases(self.payload)[0]
        normalized = normalize_release(first, "fixture://source", "2026-09-03T00:00:00Z")
        encoded = json.dumps(normalized)
        self.assertNotIn("contactPoint", encoded)
        self.assertNotIn("Excluded Person", encoded)
        self.assertNotIn("description", encoded)
        self.assertIn("content_fingerprint", normalized["provenance"])
        self.assertEqual(normalized["ocid"], normalized["provenance"]["process_id"])

    def test_summary_uses_diff_derived_counts(self) -> None:
        self.assertEqual(4, self.result["summary"]["update_tagged_comparisons"])
        self.assertEqual(3, self.result["summary"]["material_change_comparisons"])
        self.assertEqual(4, self.result["summary"]["comparisons"])

    def test_sanitized_capture_is_replayable_without_excluded_fields(self) -> None:
        sanitized = sanitize_package(
            self.payload,
            "https://www.find-tender.service.gov.uk/api/1.0/ocdsRecordPackages/example",
            "2026-09-03T00:00:00Z",
        )
        persisted_records = json.dumps(sanitized["records"])
        self.assertNotIn("Excluded Person", persisted_records)
        self.assertNotIn("contactPoint", persisted_records)
        self.assertEqual(1, sanitized["capture"]["requestCount"])
        replay = run_pipeline(sanitized, self.profile, sanitized["capture"]["sourceUrl"], sanitized["capture"]["retrievedAt"])
        self.assertEqual(self.result["summary"], replay["summary"])


if __name__ == "__main__":
    unittest.main()
