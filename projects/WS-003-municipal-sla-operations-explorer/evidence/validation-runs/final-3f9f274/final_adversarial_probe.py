from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
PROJECT = ROOT / "projects" / "WS-003-municipal-sla-operations-explorer"
RUN_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PROJECT / "src"))

from app import app  # noqa: E402
from demo_server import default_rules, load_fixture, run_demo  # noqa: E402
from sla_engine import evaluate_dataset, evaluate_record, parse_iso_timestamp  # noqa: E402


def api_case(client, name: str, *, json_body=None, raw=None, content_type=None, headers=None):
    kwargs = {"headers": headers or {"Origin": "http://localhost"}}
    if raw is not None:
        kwargs["data"] = raw
        if content_type is not None:
            kwargs["content_type"] = content_type
    else:
        kwargs["json"] = json_body
    response = client.post("/api/run", **kwargs)
    try:
        body = response.get_json()
    except Exception:
        body = response.get_data(as_text=True)
    return {"name": name, "status": response.status_code, "body": body}


def edge_record(name: str, **overrides):
    record = {
        "service_request_id": f"EDGE-{name}",
        "service_name": "Pothole Repair",
        "ward": "Ward Edge",
        "created_date": "2026-08-01T12:00:00Z",
        "target_date": "2026-08-06T12:00:00Z",
        "closed_date": None,
        "status": "OPEN",
    }
    record.update(overrides)
    result = evaluate_record(
        record,
        reference_now=parse_iso_timestamp("2026-08-08T12:00:00Z"),
    )
    return {
        "name": name,
        "input": record,
        "sla_status": result["sla_status"],
        "lifecycle_state": result["lifecycle_state"],
        "reason_code": result["reason_code"],
        "duration_days": result["duration_days"],
        "margin_days": result["margin_days"],
    }


def main() -> None:
    client = app.test_client()
    cases = []

    for value, label in [
        ([], "empty_array"),
        ("", "empty_string"),
        (False, "false"),
        (0, "zero"),
        (None, "null"),
        ([1], "truthy_array"),
        ("x", "truthy_string"),
        (1, "truthy_number"),
        (True, "truthy_boolean"),
    ]:
        cases.append(api_case(client, f"rules_{label}", json_body={"rules": value}))

    for value, label in [
        (1.5, "fractional"),
        (True, "boolean_true"),
        (False, "boolean_false"),
        (0, "below_range_zero"),
        (-1, "below_range_negative"),
        (31, "above_range"),
        ("3", "numeric_string"),
        (None, "null_value"),
    ]:
        cases.append(
            api_case(
                client,
                f"rule_value_{label}",
                json_body={"rules": {"Pothole Repair": value}},
            )
        )

    cases.extend(
        [
            api_case(client, "unknown_rule_key", json_body={"rules": {"Unmapped Service": 5}}),
            api_case(client, "empty_rule_object", json_body={"rules": {}}),
            api_case(client, "missing_rules_key", json_body={}),
            api_case(client, "valid_default_rules", json_body={"rules": default_rules()}),
            api_case(
                client,
                "valid_strict_rules",
                json_body={
                    "rules": {
                        "Pothole Repair": 3,
                        "Streetlight Maintenance": 2,
                        "Tree Trimming": 5,
                        "Garbage Collection": 1,
                    }
                },
            ),
            api_case(client, "malformed_json", raw=b'{"rules":', content_type="application/json"),
            api_case(client, "empty_json_body", raw=b"", content_type="application/json"),
            api_case(client, "top_level_array", json_body=[]),
            api_case(client, "top_level_string", json_body="x"),
            api_case(client, "top_level_false", json_body=False),
            api_case(client, "non_json_content_type", raw=b'{"rules":{}}', content_type="text/plain"),
            api_case(
                client,
                "oversized_json_body",
                json_body={"rules": {}, "padding": "x" * 9000},
            ),
            api_case(
                client,
                "cross_origin",
                json_body={"rules": {}},
                headers={"Origin": "https://evil.example"},
            ),
            api_case(
                client,
                "sec_fetch_cross_site",
                json_body={"rules": {}},
                headers={"Origin": "http://localhost", "Sec-Fetch-Site": "cross-site"},
            ),
            api_case(
                client,
                "same_origin",
                json_body={"rules": {}},
                headers={"Origin": "http://localhost"},
            ),
            api_case(client, "origin_absent", json_body={"rules": {}}, headers={}),
            api_case(
                client,
                "scheme_mismatch_same_host",
                json_body={"rules": {}},
                headers={"Origin": "https://localhost"},
            ),
        ]
    )

    expected_400 = {
        case["name"]
        for case in cases
        if case["name"].startswith("rules_")
        or case["name"].startswith("rule_value_")
        or case["name"]
        in {
            "unknown_rule_key",
            "malformed_json",
            "empty_json_body",
            "top_level_array",
            "top_level_string",
            "top_level_false",
            "non_json_content_type",
        }
    }
    expected_200 = {
        "empty_rule_object",
        "missing_rules_key",
        "valid_default_rules",
        "valid_strict_rules",
        "same_origin",
        "origin_absent",
        "scheme_mismatch_same_host",
    }
    expected_403 = {"cross_origin", "sec_fetch_cross_site"}
    expected_413 = {"oversized_json_body"}

    api_failures = []
    for case in cases:
        expected = (
            400
            if case["name"] in expected_400
            else 200
            if case["name"] in expected_200
            else 403
            if case["name"] in expected_403
            else 413
            if case["name"] in expected_413
            else None
        )
        case["expected_status"] = expected
        case["pass"] = case["status"] == expected
        if not case["pass"]:
            api_failures.append(case["name"])

    named = {case["name"]: case for case in cases}
    for scenario, expected_summary in [
        ("valid_default_rules", {"COMPLIANT": 8, "AT_RISK": 1, "SLA_BREACHED": 5, "INCOMPLETE_DATA_REVIEW": 1}),
        ("valid_strict_rules", {"COMPLIANT": 0, "AT_RISK": 1, "SLA_BREACHED": 13, "INCOMPLETE_DATA_REVIEW": 1}),
    ]:
        actual = named[scenario]["body"].get("status_summary") if isinstance(named[scenario]["body"], dict) else None
        named[scenario]["expected_summary"] = expected_summary
        named[scenario]["summary_pass"] = actual == expected_summary
        if actual != expected_summary:
            api_failures.append(f"{scenario}_summary")

    strict_001 = next(
        item
        for item in named["valid_strict_rules"]["body"]["evaluated_records"]
        if item["service_request_id"] == "SR-311-001"
    )
    strict_001_pass = strict_001["sla_status"] == "SLA_BREACHED" and strict_001["reason_code"] == "CLOSED_AFTER_SLA_TARGET"
    if not strict_001_pass:
        api_failures.append("strict_SR-311-001")

    edges = [
        edge_record("invalid_created", created_date="BAD"),
        edge_record("invalid_target", target_date="BAD"),
        edge_record("target_before_created", target_date="2026-07-31T12:00:00Z"),
        edge_record("invalid_closed", closed_date="BAD", status="CLOSED"),
        edge_record("missing_closed", closed_date=None, status="CLOSED"),
        edge_record("closed_before_created", closed_date="2026-07-31T12:00:00Z", status="CLOSED"),
        edge_record("future_created", created_date="2026-08-09T12:00:00Z", target_date=None),
        edge_record("unknown_category", service_name="Unmapped Service"),
        edge_record("unknown_status", status="NONSENSE"),
        edge_record("open_with_closed_timestamp", status="OPEN", closed_date="2026-08-02T12:00:00Z"),
        edge_record("in_progress_with_closed_timestamp", status="IN_PROGRESS", closed_date="2026-08-02T12:00:00Z"),
        edge_record("closed_after_reference_time", status="CLOSED", closed_date="2026-08-09T12:00:00Z"),
    ]

    fixture = load_fixture()
    reference = parse_iso_timestamp("2026-08-08T12:00:00Z")
    result_a = evaluate_dataset(deepcopy(fixture), reference_now=reference)
    result_b = evaluate_dataset(deepcopy(fixture), reference_now=reference)
    engine_deterministic = result_a == result_b
    fingerprint_set_a = {item["fingerprint"] for item in result_a["evaluated_records"]}
    fingerprint_set_b = {item["fingerprint"] for item in result_b["evaluated_records"]}
    fingerprints_deterministic = fingerprint_set_a == fingerprint_set_b and len(fingerprint_set_a) == 15

    changed_fixture = deepcopy(fixture)
    changed_fixture[0]["ward"] = "Ward Changed"
    changed = evaluate_dataset(changed_fixture, reference_now=reference)
    changed_input_fingerprint = (
        result_a["evaluated_records"][0]["fingerprint"] != changed["evaluated_records"][0]["fingerprint"]
    )

    default_001 = next(item for item in result_a["evaluated_records"] if item["service_request_id"] == "SR-311-001")
    strict_run = run_demo(
        {
            "Pothole Repair": 3,
            "Streetlight Maintenance": 2,
            "Tree Trimming": 5,
            "Garbage Collection": 1,
        }
    )
    strict_demo_001 = next(item for item in strict_run["evaluated_records"] if item["service_request_id"] == "SR-311-001")

    export_json = json.loads((RUN_DIR / "final-export.json").read_text(encoding="utf-8"))
    with (RUN_DIR / "final-export.csv").open("r", encoding="utf-8", newline="") as stream:
        export_csv = list(csv.DictReader(stream))
    required_fields = {"fixture_kind", "reason_code", "fingerprint"}
    json_export_ok = (
        export_json["total_records"] == 15
        and export_json["status_summary"] == {"COMPLIANT": 8, "AT_RISK": 1, "SLA_BREACHED": 5, "INCOMPLETE_DATA_REVIEW": 1}
        and all(required_fields <= set(row) for row in export_json["evaluated_records"])
        and all(row["fixture_kind"] == "synthetic_sla_scenario" for row in export_json["evaluated_records"])
    )
    csv_export_ok = (
        len(export_csv) == 15
        and all(required_fields <= set(row) for row in export_csv)
        and all(row["fixture_kind"] == "synthetic_sla_scenario" for row in export_csv)
    )
    fingerprint_format_ok = all(re.fullmatch(r"[0-9a-f]{16}", row["fingerprint"]) for row in export_csv)
    export_fingerprint_sets_match = (
        {row["fingerprint"] for row in export_csv}
        == {row["fingerprint"] for row in export_json["evaluated_records"]}
        == fingerprint_set_a
    )
    forbidden_field_fragments = ("resident_name", "private_address", "postal", "intersection", "email", "phone", "contact")
    exported_keys = {key.lower() for row in export_json["evaluated_records"] for key in row}
    privacy_field_ok = not any(fragment in key for key in exported_keys for fragment in forbidden_field_fragments)
    serialized_exports = json.dumps(export_json, sort_keys=True).lower() + json.dumps(export_csv, sort_keys=True).lower()
    privacy_value_ok = not re.search(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", serialized_exports)

    fixture_test_bytes = (PROJECT / "tests/fixtures/toronto_311_sample.json").read_bytes()
    fixture_evidence_bytes = (PROJECT / "evidence/fixtures/toronto_311_sample.json").read_bytes()
    oracle_test_bytes = (PROJECT / "tests/fixtures/benchmark_oracle.json").read_bytes()
    oracle_evidence_bytes = (PROJECT / "evidence/fixtures/benchmark_oracle.json").read_bytes()

    output = {
        "api_cases": cases,
        "api_failures": api_failures,
        "strict_SR-311-001": {
            "sla_status": strict_001["sla_status"],
            "reason_code": strict_001["reason_code"],
            "pass": strict_001_pass,
        },
        "engine_edges": edges,
        "determinism": {
            "engine_results_equal": engine_deterministic,
            "fingerprints_deterministic_unique_15": fingerprints_deterministic,
            "changed_input_changes_fingerprint": changed_input_fingerprint,
            "default_SR-311-001": [default_001["sla_status"], default_001["reason_code"]],
            "strict_SR-311-001": [strict_demo_001["sla_status"], strict_demo_001["reason_code"]],
        },
        "exports": {
            "json_ok": json_export_ok,
            "csv_ok": csv_export_ok,
            "fingerprint_format_ok": fingerprint_format_ok,
            "fingerprint_sets_match": export_fingerprint_sets_match,
            "privacy_field_ok": privacy_field_ok,
            "privacy_value_ok": privacy_value_ok,
            "fixture_copies_identical": fixture_test_bytes == fixture_evidence_bytes,
            "fixture_sha256": hashlib.sha256(fixture_test_bytes).hexdigest(),
            "oracle_copies_identical": oracle_test_bytes == oracle_evidence_bytes,
            "oracle_sha256": hashlib.sha256(oracle_test_bytes).hexdigest(),
        },
    }
    (RUN_DIR / "final-adversarial-results.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
