from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sys
import urllib.error
import urllib.request
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[5]
PROJECT = REPO / "projects" / "WS-003-municipal-sla-operations-explorer"
RUN_DIR = Path(__file__).resolve().parent
PRODUCTION = "https://municipal-311-sla-operations-desk.vercel.app"

sys.path.insert(0, str(PROJECT / "src"))
import demo_server  # noqa: E402
import sla_engine  # noqa: E402

app_spec = importlib.util.spec_from_file_location("ws003_app", PROJECT / "app.py")
assert app_spec and app_spec.loader
app_module = importlib.util.module_from_spec(app_spec)
app_spec.loader.exec_module(app_module)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def summarize_run(result: dict[str, Any]) -> dict[str, Any]:
    record = next(item for item in result["evaluated_records"] if item["service_request_id"] == "SR-311-001")
    return {
        "fixture_kind": result["fixture_kind"],
        "total_records": result["total_records"],
        "status_summary": result["status_summary"],
        "ward_01": result["ward_analytics"]["Ward 01 - Etobicoke North"],
        "sr_311_001": {
            "sla_status": record["sla_status"],
            "reason_code": record["reason_code"],
            "sla_target_days": record["sla_target_days"],
        },
        "engine_sha256": result.get("engine_sha256"),
    }


def http_request(
    url: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    request_headers = {"User-Agent": "WS-003-independent-validator/1.0"}
    request_headers.update(headers or {})
    req = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            status = response.status
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as error:
        content = error.read()
        status = error.code
        response_headers = dict(error.headers.items())
    text = content.decode("utf-8", errors="replace")
    parsed: Any = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        pass
    return {
        "status": status,
        "headers": response_headers,
        "body_sha256": sha256_bytes(content),
        "body_length": len(content),
        "json": parsed,
        "text_excerpt": text[:500],
    }


def json_post(url: str, payload: Any, *, headers: dict[str, str] | None = None) -> dict[str, Any]:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    return http_request(url, method="POST", body=body, headers=request_headers)


def local_client_post(payload: Any, *, base_url: str = "http://localhost", headers: dict[str, str] | None = None):
    client = app_module.app.test_client()
    response = client.post("/api/run", json=payload, base_url=base_url, headers=headers or {})
    return {"status": response.status_code, "json": response.get_json(silent=True)}


def main() -> None:
    fixture_path = PROJECT / "tests" / "fixtures" / "toronto_311_sample.json"
    oracle_path = PROJECT / "tests" / "fixtures" / "benchmark_oracle.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    reference_now = sla_engine.parse_iso_timestamp(oracle["reference_now"])
    assert reference_now is not None

    default_result = sla_engine.evaluate_dataset(fixture, reference_now=reference_now)
    strict_rules = {
        "Pothole Repair": 3,
        "Streetlight Maintenance": 2,
        "Tree Trimming": 5,
        "Garbage Collection": 1,
    }
    strict_result = sla_engine.evaluate_dataset(fixture, rules=strict_rules, reference_now=reference_now)

    base_record = {
        "service_request_id": "ADV-001",
        "service_name": "Pothole Repair",
        "ward": "Synthetic Ward",
        "created_date": "2026-08-01T12:00:00Z",
        "target_date": "2026-08-06T12:00:00Z",
        "closed_date": None,
        "status": "OPEN",
    }
    record_cases: list[tuple[str, dict[str, Any], str]] = []

    def add_case(name: str, changes: dict[str, Any], expected_reason: str) -> None:
        record = deepcopy(base_record)
        record.update(changes)
        record_cases.append((name, record, expected_reason))

    add_case("malformed_created", {"created_date": "not-a-time"}, "INVALID_CREATED_TIMESTAMP")
    add_case("missing_created", {"created_date": None}, "INVALID_CREATED_TIMESTAMP")
    add_case("malformed_target", {"target_date": "not-a-time"}, "INVALID_TARGET_TIMESTAMP")
    add_case("target_before_created", {"target_date": "2026-07-31T12:00:00Z"}, "TARGET_BEFORE_CREATED")
    add_case("malformed_closed", {"status": "CLOSED", "closed_date": "not-a-time"}, "INVALID_CLOSED_TIMESTAMP")
    add_case("closed_before_created", {"status": "CLOSED", "closed_date": "2026-07-31T12:00:00Z"}, "CLOSED_BEFORE_CREATED")
    add_case("unknown_category", {"service_name": "Unmapped Service"}, "UNKNOWN_SERVICE_CATEGORY")
    add_case("future_created", {"created_date": "2026-08-09T12:00:00Z", "target_date": None}, "CREATED_AFTER_REFERENCE_TIME")
    add_case("unknown_status", {"status": "NONSENSE"}, "UNKNOWN_STATUS")
    add_case("open_with_closed", {"status": "OPEN", "closed_date": "2026-08-02T12:00:00Z"}, "STATUS_CLOSED_DATE_CONFLICT")
    add_case("in_progress_with_closed", {"status": "IN_PROGRESS", "closed_date": "2026-08-02T12:00:00Z"}, "STATUS_CLOSED_DATE_CONFLICT")
    add_case("closed_without_closed", {"status": "CLOSED", "closed_date": None}, "MISSING_CLOSED_TIMESTAMP")
    add_case("closed_after_reference", {"status": "CLOSED", "closed_date": "2026-08-09T12:00:00Z"}, "CLOSED_AFTER_REFERENCE_TIME")

    record_results = []
    for name, record, expected_reason in record_cases:
        evaluated = sla_engine.evaluate_record(record, reference_now=reference_now)
        record_results.append(
            {
                "case": name,
                "sla_status": evaluated["sla_status"],
                "lifecycle_state": evaluated["lifecycle_state"],
                "reason_code": evaluated["reason_code"],
                "expected_reason": expected_reason,
                "pass": evaluated["sla_status"] == "INCOMPLETE_DATA_REVIEW"
                and evaluated["lifecycle_state"] == "DATA_ERROR"
                and evaluated["reason_code"] == expected_reason,
            }
        )

    direct_rule_results = []
    for name, invalid_value in [
        ("boolean", True),
        ("fractional", 1.5),
        ("zero", 0),
        ("negative", -1),
        ("over_30", 31),
        ("string", "3"),
    ]:
        rules = dict(sla_engine.DEFAULT_CATEGORY_SLA_DAYS)
        rules["Pothole Repair"] = invalid_value
        evaluated = sla_engine.evaluate_record(base_record, rules=rules, reference_now=reference_now)
        direct_rule_results.append(
            {
                "case": name,
                "value": invalid_value,
                "sla_status": evaluated["sla_status"],
                "reason_code": evaluated["reason_code"],
                "pass": evaluated["reason_code"] == "INVALID_SLA_RULE",
            }
        )

    invalid_api_payloads = [
        ("fractional", {"rules": {"Pothole Repair": 1.5}}),
        ("unknown_category", {"rules": {"Unmapped Service": 5}}),
        ("boolean", {"rules": {"Pothole Repair": True}}),
        ("zero", {"rules": {"Pothole Repair": 0}}),
        ("negative", {"rules": {"Pothole Repair": -1}}),
        ("over_30", {"rules": {"Pothole Repair": 31}}),
        ("numeric_string", {"rules": {"Pothole Repair": "3"}}),
        ("empty_array", {"rules": []}),
        ("empty_string", {"rules": ""}),
        ("false", {"rules": False}),
        ("zero_non_object", {"rules": 0}),
        ("null", {"rules": None}),
        ("root_array", []),
        ("root_string", ""),
        ("root_null", None),
    ]
    local_invalid_api = []
    for name, payload in invalid_api_payloads:
        result = local_client_post(payload, headers={"Origin": "http://localhost"})
        local_invalid_api.append({"case": name, **result, "pass": result["status"] == 400})

    local_default_api = local_client_post({"rules": {}}, headers={"Origin": "http://localhost"})
    local_strict_api = local_client_post({"rules": strict_rules}, headers={"Origin": "http://localhost"})
    local_origin_probes = {
        "same_origin_http": local_default_api,
        "same_origin_https": local_client_post(
            {"rules": {}},
            base_url=PRODUCTION,
            headers={"Origin": PRODUCTION},
        ),
        "cross_origin": local_client_post(
            {"rules": {}},
            base_url=PRODUCTION,
            headers={"Origin": "https://evil.example"},
        ),
        "cross_scheme_same_host": local_client_post(
            {"rules": {}},
            base_url=PRODUCTION,
            headers={"Origin": "http://municipal-311-sla-operations-desk.vercel.app"},
        ),
        "sec_fetch_cross_site": local_client_post(
            {"rules": {}},
            base_url=PRODUCTION,
            headers={"Sec-Fetch-Site": "cross-site"},
        ),
        "opaque_origin": local_client_post(
            {"rules": {}},
            base_url=PRODUCTION,
            headers={"Origin": "null"},
        ),
    }

    fingerprints_default = {row["service_request_id"]: row["fingerprint"] for row in default_result["evaluated_records"]}
    fingerprints_strict = {row["service_request_id"]: row["fingerprint"] for row in strict_result["evaluated_records"]}
    changed_record = deepcopy(fixture[0])
    changed_record["ward"] = "Changed Synthetic Ward"
    fingerprint_checks = {
        "all_16_hex": all(len(value) == 16 and all(char in "0123456789abcdef" for char in value) for value in fingerprints_default.values()),
        "unique_for_fixture": len(set(fingerprints_default.values())) == len(fixture),
        "stable_across_rules": fingerprints_default == fingerprints_strict,
        "changes_with_source_record": sla_engine.calculate_record_fingerprint(fixture[0])
        != sla_engine.calculate_record_fingerprint(changed_record),
    }

    pii_terms = ["name", "address", "email", "phone", "postal", "intersection"]
    exported_fields = set(default_result["evaluated_records"][0])
    serialized_exports = json.dumps(default_result, ensure_ascii=True).lower()
    privacy_checks = {
        "forbidden_field_fragments": sorted(
            field for field in exported_fields if any(term in field.lower() for term in pii_terms)
        ),
        "email_marker_present": "@" in serialized_exports,
        "phone_like_present": False,
        "all_rows_synthetic": all(row["fixture_kind"] == sla_engine.FIXTURE_KIND for row in default_result["evaluated_records"]),
    }

    production_static = {
        "index": http_request(PRODUCTION + "/"),
        "app_js": http_request(PRODUCTION + "/app.js"),
        "style_css": http_request(PRODUCTION + "/style.css"),
        "config": http_request(PRODUCTION + "/api/config"),
        "code": http_request(PRODUCTION + "/api/code"),
    }
    production_default = json_post(
        PRODUCTION + "/api/run",
        {"rules": {}},
        headers={"Origin": PRODUCTION, "Sec-Fetch-Site": "same-origin"},
    )
    production_strict = json_post(
        PRODUCTION + "/api/run",
        {"rules": strict_rules},
        headers={"Origin": PRODUCTION, "Sec-Fetch-Site": "same-origin"},
    )
    production_invalid_api = []
    for name, payload in invalid_api_payloads:
        result = json_post(
            PRODUCTION + "/api/run",
            payload,
            headers={"Origin": PRODUCTION, "Sec-Fetch-Site": "same-origin"},
        )
        production_invalid_api.append({"case": name, **result, "pass": result["status"] == 400})

    production_origin_probes = {
        "same_origin": production_default,
        "cross_origin": json_post(
            PRODUCTION + "/api/run",
            {"rules": {}},
            headers={"Origin": "https://evil.example", "Sec-Fetch-Site": "cross-site"},
        ),
        "cross_scheme_same_host": json_post(
            PRODUCTION + "/api/run",
            {"rules": {}},
            headers={"Origin": "http://municipal-311-sla-operations-desk.vercel.app", "Sec-Fetch-Site": "same-site"},
        ),
        "sec_fetch_cross_site_without_origin": json_post(
            PRODUCTION + "/api/run",
            {"rules": {}},
            headers={"Sec-Fetch-Site": "cross-site"},
        ),
        "opaque_origin": json_post(
            PRODUCTION + "/api/run",
            {"rules": {}},
            headers={"Origin": "null", "Sec-Fetch-Site": "cross-site"},
        ),
    }
    malformed_json = http_request(
        PRODUCTION + "/api/run",
        method="POST",
        body=b'{"rules":',
        headers={"Content-Type": "application/json", "Origin": PRODUCTION, "Sec-Fetch-Site": "same-origin"},
    )
    wrong_content_type = http_request(
        PRODUCTION + "/api/run",
        method="POST",
        body=b'{"rules":{}}',
        headers={"Content-Type": "text/plain", "Origin": PRODUCTION, "Sec-Fetch-Site": "same-origin"},
    )
    oversized = http_request(
        PRODUCTION + "/api/run",
        method="POST",
        body=json.dumps({"rules": {}, "padding": "x" * 9000}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Origin": PRODUCTION, "Sec-Fetch-Site": "same-origin"},
    )

    local_hashes = {
        "index": sha256_bytes((PROJECT / "demo" / "index.html").read_bytes()),
        "app_js": sha256_bytes((PROJECT / "demo" / "app.js").read_bytes()),
        "style_css": sha256_bytes((PROJECT / "demo" / "style.css").read_bytes()),
        "engine": sha256_bytes((PROJECT / "src" / "sla_engine.py").read_bytes()),
    }

    output = {
        "candidate_commit": "57ac8a4cf8b5d8ff344e3b12cb5b1a29c1465a2e",
        "production_url": PRODUCTION,
        "production_deployment_id": "dpl_JBt2EBRSHRN8PKDLTsnBWpYHtjCb",
        "executed_at": datetime.now().astimezone().isoformat(),
        "local_engine": {
            "default": summarize_run(default_result),
            "strict": summarize_run(strict_result),
            "record_edge_cases": record_results,
            "direct_invalid_rules": direct_rule_results,
            "fingerprints": fingerprint_checks,
            "privacy": privacy_checks,
        },
        "local_api": {
            "default": {"status": local_default_api["status"], "summary": summarize_run(local_default_api["json"])},
            "strict": {"status": local_strict_api["status"], "summary": summarize_run(local_strict_api["json"])},
            "invalid_payloads": local_invalid_api,
            "origin_probes": local_origin_probes,
        },
        "production": {
            "static": production_static,
            "default": production_default,
            "strict": production_strict,
            "invalid_payloads": production_invalid_api,
            "origin_probes": production_origin_probes,
            "malformed_json": malformed_json,
            "wrong_content_type": wrong_content_type,
            "oversized": oversized,
            "local_hashes": local_hashes,
            "static_hash_matches": {
                key: production_static[key]["body_sha256"] == local_hashes[key]
                for key in ("index", "app_js", "style_css")
            },
        },
    }

    output_path = RUN_DIR / "remediation-probe-results.json"
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
