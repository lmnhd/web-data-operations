"""Bounded carbon-disclosure arithmetic reconciler for WS-004.

The engine evaluates only explicit, versioned evidence. It intentionally fails
closed when a factor, unit, activity breakdown, or calorific basis is missing.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = PROJECT_ROOT / "evidence" / "fixtures" / "disclosure_cases.json"
DEFAULT_FACTORS = PROJECT_ROOT / "evidence" / "factors" / "ghg_factors_2025.json"
SUPPORTED_SOURCE_FORMATS = {"ixbrl_html", "controlled_structured"}
PROHIBITED_KEYS = {
    "address",
    "companyname",
    "contact",
    "email",
    "officername",
    "personalname",
    "phone",
    "signature",
}
SIX_DP = Decimal("0.000001")


class EvidenceBoundaryError(ValueError):
    """Raised when input violates the minimized public-evidence contract."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def _normalized_key(key: str) -> str:
    return "".join(char for char in key.lower() if char.isalnum())


def enforce_evidence_boundary(value: Any, path: str = "$") -> None:
    """Reject personal/display fields before they can enter outputs."""

    if isinstance(value, dict):
        for key, item in value.items():
            if _normalized_key(str(key)) in PROHIBITED_KEYS:
                raise EvidenceBoundaryError(f"Prohibited field at {path}.{key}")
            enforce_evidence_boundary(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            enforce_evidence_boundary(item, f"{path}[{index}]")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_decimal(value: Any) -> Decimal:
    if value is None or isinstance(value, bool):
        raise InvalidOperation
    parsed = Decimal(str(value))
    if not parsed.is_finite() or parsed < 0:
        raise InvalidOperation
    return parsed


def decimal_string(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value.quantize(SIX_DP), "f")


def normalize_activity(value: Decimal, unit: str) -> Decimal:
    if unit == "kWh":
        return value
    if unit == "MWh":
        return value * Decimal("1000")
    raise KeyError("UNSUPPORTED_ACTIVITY_UNIT")


def normalize_emissions(value: Decimal, unit: str) -> Decimal:
    if unit == "tCO2e":
        return value
    if unit == "kgCO2e":
        return value / Decimal("1000")
    raise KeyError("UNSUPPORTED_EMISSIONS_UNIT")


def source_sha256(source: dict[str, Any]) -> str:
    if "sourceSha256" in source:
        supplied = source["sourceSha256"]
        if not isinstance(supplied, str) or len(supplied) != 64 or any(
            char not in "0123456789abcdefABCDEF" for char in supplied
        ):
            raise EvidenceBoundaryError(
                "sourceSha256 must be exactly 64 hexadecimal characters"
            )
        return supplied.lower()
    basis = {
        "sourceId": source.get("sourceId"),
        "sourceFormat": source.get("sourceFormat"),
        "locator": source.get("locator"),
        "sourceFingerprintBasis": source.get("sourceFingerprintBasis"),
    }
    return sha256_json(basis)


def _base_result(
    case: dict[str, Any], factor_file_sha256: str, engine_sha256: str
) -> dict[str, Any]:
    source = case.get("source") or {}
    calculation = case.get("calculation") or {}
    return {
        "caseId": case.get("caseId"),
        "fixtureKind": case.get("fixtureKind"),
        "sourceId": source.get("sourceId"),
        "sourceFormat": source.get("sourceFormat"),
        "sourceLocator": source.get("locator"),
        "sourceSha256": source_sha256(source),
        "reportingPeriodEnd": source.get("reportingPeriodEnd"),
        "inputSha256": sha256_json(case),
        "factorSetId": "UK-GHG-2025-V1-FINAL",
        "factorFileSha256": factor_file_sha256,
        "factorWorkbookSha256": None,
        "engineSha256": engine_sha256,
        "factorId": calculation.get("factorId"),
        "factorYear": calculation.get("factorYear"),
        "activityValue": calculation.get("activityValue"),
        "activityUnit": calculation.get("activityUnit"),
        "disclosedEmissionsValue": calculation.get("disclosedEmissionsValue"),
        "disclosedEmissionsUnit": calculation.get("disclosedEmissionsUnit"),
        "normalizedActivityKwh": None,
        "disclosedEmissionsTco2e": None,
        "computedEmissionsTco2e": None,
        "varianceTco2e": None,
        "toleranceTco2e": None,
        "decision": "REVIEW_REQUIRED",
        "reasonCode": None,
    }


def _review(result: dict[str, Any], reason_code: str) -> dict[str, Any]:
    result["reasonCode"] = reason_code
    return result


def evaluate_case(
    case: dict[str, Any],
    factors_document: dict[str, Any],
    factor_file_sha256: str,
    engine_sha256: str,
    tolerance_tco2e: Decimal,
) -> dict[str, Any]:
    """Evaluate one case without inferring absent evidence."""

    result = _base_result(case, factor_file_sha256, engine_sha256)
    result["factorWorkbookSha256"] = str(factors_document.get("sha256", "")).lower()
    result["toleranceTco2e"] = decimal_string(tolerance_tco2e)
    source = case.get("source") or {}
    calculation = case.get("calculation") or {}

    if source.get("sourceFormat") not in SUPPORTED_SOURCE_FORMATS:
        return _review(result, "UNSUPPORTED_SOURCE_FORMAT")

    if calculation.get("activityBreakdownAvailable") is False:
        return _review(result, "INSUFFICIENT_CALCULATION_EVIDENCE")

    if (
        calculation.get("activityCategory") == "natural_gas"
        and not calculation.get("activityBasis")
    ):
        return _review(result, "AMBIGUOUS_ACTIVITY_BASIS")

    required = (
        "activityValue",
        "activityUnit",
        "disclosedEmissionsValue",
        "disclosedEmissionsUnit",
        "factorYear",
        "factorId",
    )
    if any(calculation.get(key) in (None, "") for key in required):
        return _review(result, "INSUFFICIENT_CALCULATION_EVIDENCE")

    if calculation.get("factorYear") != 2025:
        return _review(result, "UNKNOWN_FACTOR_REFERENCE")

    factor_by_id = {
        factor["factorId"]: factor for factor in factors_document.get("factors", [])
    }
    factor = factor_by_id.get(calculation.get("factorId"))
    if factor is None:
        return _review(result, "UNKNOWN_FACTOR_REFERENCE")

    if calculation.get("activityCategory") != factor.get("activityCategory"):
        return _review(result, "FACTOR_ACTIVITY_CATEGORY_CONFLICT")

    try:
        activity = parse_decimal(calculation.get("activityValue"))
        disclosed = parse_decimal(calculation.get("disclosedEmissionsValue"))
        normalized_activity = normalize_activity(activity, calculation.get("activityUnit"))
        normalized_disclosed = normalize_emissions(
            disclosed, calculation.get("disclosedEmissionsUnit")
        )
        factor_value = parse_decimal(factor.get("factor"))
    except InvalidOperation:
        return _review(result, "INVALID_NUMERIC_INPUT")
    except KeyError as error:
        return _review(result, str(error.args[0]))

    if factor.get("emissionsUnit") != "kg CO2e":
        return _review(result, "UNSUPPORTED_FACTOR_UNIT")

    factor_activity_unit = factor.get("activityUnit")
    if factor_activity_unit not in {"kWh", "kWh (Gross CV)", "kWh (Net CV)"}:
        return _review(result, "UNSUPPORTED_FACTOR_UNIT")

    if calculation.get("activityCategory") == "natural_gas":
        expected_basis = {
            "gross_cv": "kWh (Gross CV)",
            "net_cv": "kWh (Net CV)",
        }.get(calculation.get("activityBasis"))
        if expected_basis != factor_activity_unit:
            return _review(result, "FACTOR_ACTIVITY_BASIS_CONFLICT")
    elif factor_activity_unit != "kWh":
        return _review(result, "FACTOR_ACTIVITY_UNIT_CONFLICT")

    computed = normalized_activity * factor_value / Decimal("1000")
    variance = abs(computed - normalized_disclosed)
    result.update(
        {
            "normalizedActivityKwh": decimal_string(normalized_activity),
            "disclosedEmissionsTco2e": decimal_string(normalized_disclosed),
            "computedEmissionsTco2e": decimal_string(computed),
            "varianceTco2e": decimal_string(variance),
        }
    )
    if variance <= tolerance_tco2e:
        result.update({"decision": "RECONCILED", "reasonCode": "WITHIN_TOLERANCE"})
    else:
        result.update(
            {
                "decision": "MISMATCH",
                "reasonCode": "DISCLOSED_RESULT_OUTSIDE_TOLERANCE",
            }
        )
    return result


def run_benchmark(
    cases_document: dict[str, Any],
    factors_document: dict[str, Any],
    *,
    factor_file_bytes: bytes,
    engine_file_bytes: bytes,
) -> dict[str, Any]:
    enforce_evidence_boundary(cases_document)
    tolerance = parse_decimal(cases_document.get("toleranceTco2e"))
    factor_hash = sha256_bytes(factor_file_bytes)
    engine_hash = sha256_bytes(engine_file_bytes)
    results = [
        evaluate_case(case, factors_document, factor_hash, engine_hash, tolerance)
        for case in cases_document.get("cases", [])
    ]
    counts = Counter(result["decision"] for result in results)
    summary = {
        "totalCases": len(results),
        "RECONCILED": counts["RECONCILED"],
        "MISMATCH": counts["MISMATCH"],
        "REVIEW_REQUIRED": counts["REVIEW_REQUIRED"],
    }
    run_basis = {
        "factorFileSha256": factor_hash,
        "factorWorkbookSha256": str(factors_document.get("sha256", "")).lower(),
        "engineSha256": engine_hash,
        "inputSha256": [result["inputSha256"] for result in results],
    }
    return {
        "iterationId": "WS-004",
        "runId": f"ws004-{sha256_json(run_basis)[:16]}",
        "fixtureStatus": cases_document.get("fixtureStatus"),
        "factorSetId": factors_document.get("factorSetId"),
        "factorFileSha256": factor_hash,
        "factorWorkbookSha256": str(factors_document.get("sha256", "")).lower(),
        "engineSha256": engine_hash,
        "summary": summary,
        "results": results,
        "claimBoundary": "Arithmetic reproducibility from explicit evidence only; not audit assurance, compliance, emissions truth, or production accuracy.",
    }


CSV_FIELDS = [
    "runId",
    "caseId",
    "fixtureKind",
    "sourceId",
    "sourceFormat",
    "sourceLocator",
    "sourceSha256",
    "reportingPeriodEnd",
    "inputSha256",
    "factorSetId",
    "factorFileSha256",
    "factorWorkbookSha256",
    "engineSha256",
    "factorId",
    "factorYear",
    "activityValue",
    "activityUnit",
    "disclosedEmissionsValue",
    "disclosedEmissionsUnit",
    "normalizedActivityKwh",
    "disclosedEmissionsTco2e",
    "computedEmissionsTco2e",
    "varianceTco2e",
    "toleranceTco2e",
    "decision",
    "reasonCode",
]


def write_outputs(
    run: dict[str, Any], output_json: Path | None, output_csv: Path | None
) -> None:
    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    if output_csv:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with output_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(
                {"runId": run["runId"], **result} for result in run["results"]
            )


def _select_and_override(
    document: dict[str, Any], case_id: str | None, activity_unit: str | None
) -> dict[str, Any]:
    selected = copy.deepcopy(document)
    if not case_id:
        if activity_unit:
            raise ValueError("--override-activity-unit requires --case-id")
        return selected
    matches = [case for case in selected.get("cases", []) if case.get("caseId") == case_id]
    if len(matches) != 1:
        raise ValueError(f"Unknown or duplicate case ID: {case_id}")
    selected["cases"] = matches
    if activity_unit:
        matches[0].setdefault("calculation", {})["activityUnit"] = activity_unit
    return selected


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--factors", type=Path, default=DEFAULT_FACTORS)
    parser.add_argument("--case-id")
    parser.add_argument("--override-activity-unit")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-csv", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    cases = _select_and_override(
        load_json(args.input), args.case_id, args.override_activity_unit
    )
    factors = load_json(args.factors)
    run = run_benchmark(
        cases,
        factors,
        factor_file_bytes=args.factors.read_bytes(),
        engine_file_bytes=Path(__file__).read_bytes(),
    )
    write_outputs(run, args.output_json, args.output_csv)
    print(json.dumps(run, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
