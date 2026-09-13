from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app import app
import demo_server


class WebAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def post(self, payload, **headers):
        return self.client.post(
            "/api/run",
            json=payload,
            headers={"Origin": "http://localhost", **headers},
        )

    def test_index_and_static_assets(self):
        index = self.client.get("/")
        self.assertEqual(index.status_code, 200)
        self.assertIn(b"Carbon Disclosure Reconciliation Desk", index.data)
        self.assertEqual(self.client.get("/app.js").status_code, 200)
        self.assertEqual(self.client.get("/style.css").status_code, 200)

    def test_config_exposes_declared_boundary_and_counts(self):
        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["cases"]), 6)
        self.assertEqual(
            data["defaultSummary"],
            {"RECONCILED": 2, "MISMATCH": 1, "REVIEW_REQUIRED": 3},
        )
        self.assertIn("not audit assurance", data["boundary"])

    def test_code_excerpt_is_actual_engine_code(self):
        response = self.client.get("/api/code")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["file"], "src/reconcile.py")
        self.assertIn("UNSUPPORTED_SOURCE_FORMAT", data["excerpt"])
        self.assertIn("AMBIGUOUS_ACTIVITY_BASIS", data["excerpt"])

    def test_default_run_reproduces_oracle_and_exports_csv(self):
        response = self.post({"caseId": None, "activityUnit": None})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(
            data["summary"],
            {
                "totalCases": 6,
                "RECONCILED": 2,
                "MISMATCH": 1,
                "REVIEW_REQUIRED": 3,
            },
        )
        self.assertEqual(data["csv"].count("\n"), 7)
        self.assertTrue(data["csv"].startswith("runId,"))
        for row in data["csv"].splitlines()[1:]:
            self.assertTrue(row.startswith(f"{data['runId']},"))
        self.assertEqual(len(data["results"]), 6)

    def test_reviewer_unit_change_reclassifies_controlled_case(self):
        response = self.post(
            {
                "caseId": "CASE-02-CONTROLLED-MWH-RECONCILED",
                "activityUnit": "kWh",
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        result = data["results"][0]
        self.assertEqual(result["normalizedActivityKwh"], "1000.000000")
        self.assertEqual(result["computedEmissionsTco2e"], "0.177000")
        self.assertEqual(result["decision"], "MISMATCH")

    def test_fail_closed_cases_remain_visible(self):
        response = self.post({"caseId": None, "activityUnit": None})
        results = {item["caseId"]: item for item in response.get_json()["results"]}
        expected = {
            "CASE-04-FILING-GAS-AMBIGUOUS": "AMBIGUOUS_ACTIVITY_BASIS",
            "CASE-05-CONTROLLED-IMAGE-ONLY": "UNSUPPORTED_SOURCE_FORMAT",
            "CASE-06-FILING-AGGREGATE-INSUFFICIENT": "INSUFFICIENT_CALCULATION_EVIDENCE",
        }
        for case_id, reason in expected.items():
            with self.subTest(case_id=case_id):
                self.assertEqual(results[case_id]["decision"], "REVIEW_REQUIRED")
                self.assertEqual(results[case_id]["reasonCode"], reason)

    def test_api_fails_closed_on_factor_activity_category_conflict(self):
        document = copy.deepcopy(demo_server.load_cases())
        case = document["cases"][0]
        case["calculation"]["activityCategory"] = "diesel"
        document["cases"] = [case]
        with patch("demo_server.load_cases", return_value=document):
            response = self.post({"caseId": case["caseId"], "activityUnit": None})
        self.assertEqual(response.status_code, 200)
        result = response.get_json()["results"][0]
        self.assertEqual(result["decision"], "REVIEW_REQUIRED")
        self.assertEqual(result["reasonCode"], "FACTOR_ACTIVITY_CATEGORY_CONFLICT")
        self.assertIsNone(result["computedEmissionsTco2e"])

    def test_api_rejects_malformed_supplied_source_sha256(self):
        document = copy.deepcopy(demo_server.load_cases())
        case = document["cases"][0]
        case["source"]["sourceSha256"] = "not-a-sha256"
        document["cases"] = [case]
        with patch("demo_server.load_cases", return_value=document):
            response = self.post({"caseId": case["caseId"], "activityUnit": None})
        self.assertEqual(response.status_code, 400)
        self.assertIn("64 hexadecimal", response.get_json()["error"])

    def test_unknown_fields_and_invalid_types_are_rejected(self):
        for payload in (
            {"extra": True},
            {"caseId": []},
            {"activityUnit": 1},
            [],
            "",
            False,
            0,
            None,
        ):
            with self.subTest(payload=payload):
                response = self.post(payload)
                self.assertEqual(response.status_code, 400)

    def test_unknown_case_and_invalid_unit_are_rejected(self):
        unknown_case = self.post({"caseId": "UNKNOWN", "activityUnit": None})
        self.assertEqual(unknown_case.status_code, 400)
        bad_unit = self.post(
            {
                "caseId": "CASE-02-CONTROLLED-MWH-RECONCILED",
                "activityUnit": "therm",
            }
        )
        self.assertEqual(bad_unit.status_code, 400)
        wrong_case = self.post(
            {
                "caseId": "CASE-01-FILING-ELECTRICITY-RECONCILED",
                "activityUnit": "MWh",
            }
        )
        self.assertEqual(wrong_case.status_code, 400)

    def test_cross_scheme_and_cross_site_posts_are_rejected(self):
        scheme = self.client.post(
            "/api/run",
            json={},
            headers={"Origin": "https://localhost"},
        )
        self.assertEqual(scheme.status_code, 403)
        cross_site = self.client.post(
            "/api/run",
            json={},
            headers={"Sec-Fetch-Site": "cross-site"},
        )
        self.assertEqual(cross_site.status_code, 403)

    def test_non_json_and_oversized_posts_are_rejected(self):
        non_json = self.client.post(
            "/api/run", data="case", content_type="text/plain"
        )
        self.assertEqual(non_json.status_code, 400)
        oversized = self.client.post(
            "/api/run",
            data=json.dumps({"caseId": "x" * 5000}),
            content_type="application/json",
        )
        self.assertEqual(oversized.status_code, 413)


if __name__ == "__main__":
    unittest.main()
