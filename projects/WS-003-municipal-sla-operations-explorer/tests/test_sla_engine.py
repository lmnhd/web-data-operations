"""Automated tests for Municipal 311 SLA Calculation Engine (WS-003)."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sla_engine import (
    evaluate_dataset,
    evaluate_record,
    export_evaluated_records_csv,
    parse_iso_timestamp,
    DEFAULT_CATEGORY_SLA_DAYS,
)

FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures" if (PROJECT_ROOT / "tests" / "fixtures" / "toronto_311_sample.json").is_file() else PROJECT_ROOT / "evidence" / "fixtures"


class TestSLAEngine(unittest.TestCase):

    def test_benchmark_oracle_reproduction(self) -> None:
        sample_path = FIXTURES_DIR / "toronto_311_sample.json"
        oracle_path = FIXTURES_DIR / "benchmark_oracle.json"

        with sample_path.open("r", encoding="utf-8") as f:
            records = json.load(f)
        with oracle_path.open("r", encoding="utf-8") as f:
            oracle = json.load(f)

        ref_dt = parse_iso_timestamp(oracle["reference_now"])
        result = evaluate_dataset(records, reference_now=ref_dt)

        self.assertEqual(result["total_records"], oracle["expected_total_records"])
        self.assertEqual(result["status_summary"], oracle["expected_summary_counts"])

        evaluated_map = {r["service_request_id"]: r for r in result["evaluated_records"]}
        expected_map = oracle["expected_classifications"]

        for req_id, exp in expected_map.items():
            self.assertIn(req_id, evaluated_map, f"Missing request {req_id} in evaluated results")
            item = evaluated_map[req_id]
            self.assertEqual(
                item["sla_status"],
                exp["sla_status"],
                f"Mismatch for {req_id}: expected sla_status {exp['sla_status']}, got {item['sla_status']}",
            )
            self.assertEqual(
                item["lifecycle_state"],
                exp["lifecycle_state"],
                f"Mismatch for {req_id}: expected lifecycle {exp['lifecycle_state']}, got {item['lifecycle_state']}",
            )
            self.assertEqual(
                item["reason_code"],
                exp["reason_code"],
                f"Mismatch for {req_id}: expected reason {exp['reason_code']}, got {item['reason_code']}",
            )

    def test_reviewer_threshold_adjustment_scenario(self) -> None:
        """Reviewer scenario: Adjust Pothole Repair SLA target from 5 days to 3 days."""
        sample_path = FIXTURES_DIR / "toronto_311_sample.json"
        oracle_path = FIXTURES_DIR / "benchmark_oracle.json"

        with sample_path.open("r", encoding="utf-8") as f:
            records = json.load(f)
        with oracle_path.open("r", encoding="utf-8") as f:
            oracle = json.load(f)

        ref_dt = parse_iso_timestamp(oracle["reference_now"])

        adjusted_rules = dict(DEFAULT_CATEGORY_SLA_DAYS)
        adjusted_rules["Pothole Repair"] = 3

        baseline_res = evaluate_dataset(records, reference_now=ref_dt)
        adjusted_res = evaluate_dataset(records, rules=adjusted_rules, reference_now=ref_dt)

        item_001_base = next(r for r in baseline_res["evaluated_records"] if r["service_request_id"] == "SR-311-001")
        item_001_adj = next(r for r in adjusted_res["evaluated_records"] if r["service_request_id"] == "SR-311-001")

        self.assertEqual(item_001_base["sla_status"], "COMPLIANT")
        self.assertEqual(item_001_adj["sla_status"], "SLA_BREACHED")
        self.assertEqual(item_001_adj["reason_code"], "CLOSED_AFTER_SLA_TARGET")

    def test_incomplete_timestamp_edge_case(self) -> None:
        bad_record = {
            "service_request_id": "SR-BAD-999",
            "service_name": "Pothole Repair",
            "ward": "Ward 10 - Spadina-Fort York",
            "created_date": "INVALID_STAMP",
            "target_date": None,
            "closed_date": None,
            "status": "OPEN",
        }
        evaluated = evaluate_record(bad_record)
        self.assertEqual(evaluated["sla_status"], "INCOMPLETE_DATA_REVIEW")
        self.assertEqual(evaluated["lifecycle_state"], "DATA_ERROR")
        self.assertEqual(evaluated["reason_code"], "INVALID_CREATED_TIMESTAMP")

    def test_malformed_closed_timestamp_routes_to_review(self) -> None:
        record = {
            "service_request_id": "SR-BAD-CLOSED",
            "service_name": "Pothole Repair",
            "ward": "Ward 10 - Spadina-Fort York",
            "created_date": "2026-08-01T12:00:00Z",
            "target_date": "2026-08-06T12:00:00Z",
            "closed_date": "NOT-A-TIMESTAMP",
            "status": "CLOSED",
        }
        evaluated = evaluate_record(record)
        self.assertEqual(evaluated["sla_status"], "INCOMPLETE_DATA_REVIEW")
        self.assertEqual(evaluated["reason_code"], "INVALID_CLOSED_TIMESTAMP")

    def test_closure_before_creation_routes_to_review(self) -> None:
        record = {
            "service_request_id": "SR-REVERSED",
            "service_name": "Pothole Repair",
            "ward": "Ward 10 - Spadina-Fort York",
            "created_date": "2026-08-02T12:00:00Z",
            "target_date": "2026-08-07T12:00:00Z",
            "closed_date": "2026-08-01T12:00:00Z",
            "status": "CLOSED",
        }
        evaluated = evaluate_record(record)
        self.assertEqual(evaluated["sla_status"], "INCOMPLETE_DATA_REVIEW")
        self.assertEqual(evaluated["reason_code"], "CLOSED_BEFORE_CREATED")
        self.assertIsNone(evaluated["duration_days"])

    def test_unknown_category_routes_to_review(self) -> None:
        record = {
            "service_request_id": "SR-UNKNOWN",
            "service_name": "Unmapped Service",
            "ward": "Ward 10 - Spadina-Fort York",
            "created_date": "2026-08-01T12:00:00Z",
            "target_date": None,
            "closed_date": None,
            "status": "OPEN",
        }
        evaluated = evaluate_record(record, reference_now=parse_iso_timestamp("2026-08-02T12:00:00Z"))
        self.assertEqual(evaluated["sla_status"], "INCOMPLETE_DATA_REVIEW")
        self.assertEqual(evaluated["reason_code"], "UNKNOWN_SERVICE_CATEGORY")
        self.assertIsNone(evaluated["sla_target_days"])

    def test_future_creation_routes_to_review(self) -> None:
        record = {
            "service_request_id": "SR-FUTURE",
            "service_name": "Pothole Repair",
            "ward": "Ward 10 - Spadina-Fort York",
            "created_date": "2026-08-03T12:00:00Z",
            "target_date": None,
            "closed_date": None,
            "status": "OPEN",
        }
        evaluated = evaluate_record(record, reference_now=parse_iso_timestamp("2026-08-02T12:00:00Z"))
        self.assertEqual(evaluated["sla_status"], "INCOMPLETE_DATA_REVIEW")
        self.assertEqual(evaluated["reason_code"], "CREATED_AFTER_REFERENCE_TIME")

    def test_invalid_target_timestamp_routes_to_review(self) -> None:
        record = {
            "service_request_id": "SR-BAD-TARGET",
            "service_name": "Pothole Repair",
            "ward": "Ward 10 - Spadina-Fort York",
            "created_date": "2026-08-01T12:00:00Z",
            "target_date": "NOT-A-TIMESTAMP",
            "closed_date": None,
            "status": "OPEN",
        }
        evaluated = evaluate_record(record, reference_now=parse_iso_timestamp("2026-08-02T12:00:00Z"))
        self.assertEqual(evaluated["sla_status"], "INCOMPLETE_DATA_REVIEW")
        self.assertEqual(evaluated["reason_code"], "INVALID_TARGET_TIMESTAMP")

    def test_csv_and_json_export(self) -> None:
        sample_path = FIXTURES_DIR / "toronto_311_sample.json"
        oracle_path = FIXTURES_DIR / "benchmark_oracle.json"

        with sample_path.open("r", encoding="utf-8") as f:
            records = json.load(f)
        with oracle_path.open("r", encoding="utf-8") as f:
            oracle = json.load(f)

        ref_dt = parse_iso_timestamp(oracle["reference_now"])
        result = evaluate_dataset(records, reference_now=ref_dt)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            csv_out = tmp_path / "evaluated_out.csv"
            json_out = tmp_path / "evaluated_out.json"

            export_evaluated_records_csv(result["evaluated_records"], csv_out)
            with json_out.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            self.assertTrue(csv_out.is_file())
            self.assertTrue(json_out.is_file())

            with csv_out.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 15)
                self.assertEqual(rows[0]["fixture_kind"], "synthetic_sla_scenario")
                self.assertIn("fingerprint", rows[0])
                self.assertIn("reason_code", rows[0])


if __name__ == "__main__":
    unittest.main()

