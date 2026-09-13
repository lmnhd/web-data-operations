from __future__ import annotations

import copy
import csv
import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = PROJECT_ROOT / "src" / "reconcile.py"
CASES_PATH = PROJECT_ROOT / "evidence" / "fixtures" / "disclosure_cases.json"
FACTORS_PATH = PROJECT_ROOT / "evidence" / "factors" / "ghg_factors_2025.json"
ORACLE_PATH = PROJECT_ROOT / "evidence" / "fixtures" / "benchmark_oracle.json"

SPEC = importlib.util.spec_from_file_location("ws004_reconcile", ENGINE_PATH)
assert SPEC and SPEC.loader
reconcile = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reconcile)


class ReconciliationProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = reconcile.load_json(CASES_PATH)
        cls.factors = reconcile.load_json(FACTORS_PATH)
        cls.oracle = reconcile.load_json(ORACLE_PATH)
        cls.factor_bytes = FACTORS_PATH.read_bytes()
        cls.engine_bytes = ENGINE_PATH.read_bytes()

    def run_cases(self, document=None):
        return reconcile.run_benchmark(
            document or copy.deepcopy(self.cases),
            self.factors,
            factor_file_bytes=self.factor_bytes,
            engine_file_bytes=self.engine_bytes,
        )

    def case(self, case_id: str):
        return next(
            copy.deepcopy(case)
            for case in self.cases["cases"]
            if case["caseId"] == case_id
        )

    def one_case_run(self, case):
        document = copy.deepcopy(self.cases)
        document["cases"] = [case]
        return self.run_cases(document)["results"][0]

    def test_declared_six_case_oracle(self):
        run = self.run_cases()
        self.assertEqual(
            run["summary"],
            {
                "totalCases": 6,
                "RECONCILED": 2,
                "MISMATCH": 1,
                "REVIEW_REQUIRED": 3,
            },
        )
        actual = {item["caseId"]: item for item in run["results"]}
        for expected in self.oracle["cases"]:
            result = actual[expected["caseId"]]
            self.assertEqual(result["decision"], expected["expectedDecision"])
            self.assertEqual(result["reasonCode"], expected["expectedReasonCode"])
            self.assertEqual(
                result["computedEmissionsTco2e"], expected["expectedComputedTco2e"]
            )
            self.assertEqual(result["varianceTco2e"], expected["expectedVarianceTco2e"])

    def test_reconciled_filing_uses_exact_decimal_arithmetic(self):
        result = self.one_case_run(
            self.case("CASE-01-FILING-ELECTRICITY-RECONCILED")
        )
        self.assertEqual(result["normalizedActivityKwh"], "3939780.000000")
        self.assertEqual(result["computedEmissionsTco2e"], "697.341060")
        self.assertEqual(result["varianceTco2e"], "0.001060")

    def test_declared_factor_mismatch_is_not_a_compliance_claim(self):
        run = self.run_cases()
        result = next(item for item in run["results"] if item["caseId"].startswith("CASE-03"))
        self.assertEqual(result["decision"], "MISMATCH")
        self.assertEqual(result["computedEmissionsTco2e"], "73.705632")
        self.assertEqual(result["varianceTco2e"], "1.165632")
        self.assertIn("not audit assurance", run["claimBoundary"])

    def test_mwh_to_kwh_reviewer_change_is_exactly_one_thousandth(self):
        original_case = self.case("CASE-02-CONTROLLED-MWH-RECONCILED")
        changed_case = copy.deepcopy(original_case)
        changed_case["calculation"]["activityUnit"] = "kWh"
        original = self.one_case_run(original_case)
        changed = self.one_case_run(changed_case)

        self.assertEqual(Decimal(changed["normalizedActivityKwh"]), Decimal(original["normalizedActivityKwh"]) / 1000)
        self.assertEqual(Decimal(changed["computedEmissionsTco2e"]), Decimal(original["computedEmissionsTco2e"]) / 1000)
        self.assertEqual(original["decision"], "RECONCILED")
        self.assertEqual(changed["decision"], "MISMATCH")
        self.assertNotEqual(original["inputSha256"], changed["inputSha256"])
        self.assertEqual(original["sourceSha256"], changed["sourceSha256"])
        self.assertEqual(original["factorFileSha256"], changed["factorFileSha256"])
        self.assertEqual(original["engineSha256"], changed["engineSha256"])

    def test_tolerance_boundary_is_inclusive(self):
        at_boundary = self.case("CASE-02-CONTROLLED-MWH-RECONCILED")
        at_boundary["calculation"]["disclosedEmissionsValue"] = "177.01"
        beyond = copy.deepcopy(at_boundary)
        beyond["calculation"]["disclosedEmissionsValue"] = "177.010001"
        self.assertEqual(self.one_case_run(at_boundary)["decision"], "RECONCILED")
        self.assertEqual(self.one_case_run(beyond)["decision"], "MISMATCH")

    def test_ambiguous_natural_gas_basis_fails_closed(self):
        result = self.one_case_run(self.case("CASE-04-FILING-GAS-AMBIGUOUS"))
        self.assertEqual(result["decision"], "REVIEW_REQUIRED")
        self.assertEqual(result["reasonCode"], "AMBIGUOUS_ACTIVITY_BASIS")
        self.assertIsNone(result["computedEmissionsTco2e"])

    def test_aggregate_activity_without_breakdown_fails_closed(self):
        result = self.one_case_run(
            self.case("CASE-06-FILING-AGGREGATE-INSUFFICIENT")
        )
        self.assertEqual(result["reasonCode"], "INSUFFICIENT_CALCULATION_EVIDENCE")
        self.assertIsNone(result["factorId"])
        self.assertIsNone(result["computedEmissionsTco2e"])

    def test_unsupported_source_format_fails_before_calculation(self):
        result = self.one_case_run(self.case("CASE-05-CONTROLLED-IMAGE-ONLY"))
        self.assertEqual(result["reasonCode"], "UNSUPPORTED_SOURCE_FORMAT")
        self.assertIsNone(result["computedEmissionsTco2e"])

    def test_unknown_factor_year_and_id_fail_closed(self):
        unknown_year = self.case("CASE-01-FILING-ELECTRICITY-RECONCILED")
        unknown_year["calculation"]["factorYear"] = 2024
        unknown_id = self.case("CASE-01-FILING-ELECTRICITY-RECONCILED")
        unknown_id["calculation"]["factorId"] = "UNKNOWN"
        for case in (unknown_year, unknown_id):
            result = self.one_case_run(case)
            self.assertEqual(result["decision"], "REVIEW_REQUIRED")
            self.assertEqual(result["reasonCode"], "UNKNOWN_FACTOR_REFERENCE")
            self.assertIsNone(result["computedEmissionsTco2e"])

    def test_invalid_numeric_and_units_fail_closed(self):
        invalid_number = self.case("CASE-01-FILING-ELECTRICITY-RECONCILED")
        invalid_number["calculation"]["activityValue"] = "not-a-number"
        invalid_unit = self.case("CASE-01-FILING-ELECTRICITY-RECONCILED")
        invalid_unit["calculation"]["activityUnit"] = "therm"
        self.assertEqual(
            self.one_case_run(invalid_number)["reasonCode"], "INVALID_NUMERIC_INPUT"
        )
        self.assertEqual(
            self.one_case_run(invalid_unit)["reasonCode"], "UNSUPPORTED_ACTIVITY_UNIT"
        )

    def test_run_and_hashes_are_deterministic(self):
        first = self.run_cases()
        second = self.run_cases()
        self.assertEqual(first, second)
        self.assertRegex(first["runId"], r"^ws004-[0-9a-f]{16}$")
        self.assertEqual(len(first["factorFileSha256"]), 64)
        self.assertEqual(
            first["factorWorkbookSha256"],
            "8bfdb45b81ec4a88e3bdf4584637330f62e6bd09ce1940e654c5d7b7f736de94",
        )
        self.assertEqual(len(first["engineSha256"]), 64)

    def test_personal_or_display_fields_are_rejected(self):
        for prohibited_key in ("companyName", "personalName", "signature", "address", "email", "phone", "contact"):
            document = copy.deepcopy(self.cases)
            document["cases"][0]["source"][prohibited_key] = "excluded"
            with self.subTest(prohibited_key=prohibited_key):
                with self.assertRaises(reconcile.EvidenceBoundaryError):
                    self.run_cases(document)

    def test_json_and_csv_exports_agree_and_remain_minimized(self):
        run = self.run_cases()
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT / "tests") as temp_dir:
            json_path = Path(temp_dir) / "run.json"
            csv_path = Path(temp_dir) / "run.csv"
            reconcile.write_outputs(run, json_path, csv_path)
            loaded_json = json.loads(json_path.read_text(encoding="utf-8"))
            with csv_path.open(newline="", encoding="utf-8") as handle:
                loaded_csv = list(csv.DictReader(handle))

            self.assertEqual(len(loaded_csv), 6)
            self.assertEqual(
                [item["caseId"] for item in loaded_json["results"]],
                [item["caseId"] for item in loaded_csv],
            )
            self.assertEqual(
                [item["decision"] for item in loaded_json["results"]],
                [item["decision"] for item in loaded_csv],
            )
            serialized = json_path.read_text(encoding="utf-8") + csv_path.read_text(encoding="utf-8")
            for prohibited_key in reconcile.PROHIBITED_KEYS:
                self.assertNotIn(f'"{prohibited_key}"', serialized.lower())


if __name__ == "__main__":
    unittest.main()
