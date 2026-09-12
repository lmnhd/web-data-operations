"""Independent edge probes for WS-003 repair recheck candidate 2addbb6f."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PROJECT / "src"))

from app import app  # noqa: E402
from sla_engine import DEFAULT_CATEGORY_SLA_DAYS, evaluate_record  # noqa: E402


REFERENCE = datetime(2026, 8, 8, 12, tzinfo=timezone.utc)
BASE = {
    "service_request_id": "RECHECK",
    "service_name": "Pothole Repair",
    "ward": "Synthetic Ward",
    "created_date": "2026-08-01T12:00:00Z",
    "target_date": "2026-08-06T12:00:00Z",
    "closed_date": None,
    "status": "OPEN",
}


def record_case(name: str, changes: dict, expected_reason: str, rules=None) -> None:
    record = dict(BASE)
    record.update(changes)
    result = evaluate_record(record, rules=rules, reference_now=REFERENCE)
    observed = {
        "sla_status": result["sla_status"],
        "lifecycle_state": result["lifecycle_state"],
        "reason_code": result["reason_code"],
        "duration_days": result["duration_days"],
        "sla_target_days": result["sla_target_days"],
    }
    print(name, json.dumps(observed, sort_keys=True))
    assert result["sla_status"] == "INCOMPLETE_DATA_REVIEW"
    assert result["lifecycle_state"] == "DATA_ERROR"
    assert result["reason_code"] == expected_reason


record_case("invalid_created", {"created_date": "INVALID"}, "INVALID_CREATED_TIMESTAMP")
record_case(
    "invalid_closed",
    {"status": "CLOSED", "closed_date": "INVALID"},
    "INVALID_CLOSED_TIMESTAMP",
)
record_case("missing_closed", {"status": "CLOSED"}, "MISSING_CLOSED_TIMESTAMP")
record_case(
    "closed_before_created",
    {"status": "CLOSED", "closed_date": "2026-07-31T12:00:00Z"},
    "CLOSED_BEFORE_CREATED",
)
record_case("invalid_target", {"target_date": "INVALID"}, "INVALID_TARGET_TIMESTAMP")
record_case(
    "target_before_created",
    {"target_date": "2026-07-31T12:00:00Z"},
    "TARGET_BEFORE_CREATED",
)
record_case(
    "created_after_reference",
    {"created_date": "2026-08-09T12:00:00Z", "target_date": None},
    "CREATED_AFTER_REFERENCE_TIME",
)
record_case(
    "unknown_service_category",
    {"service_name": "Unmapped Service", "target_date": None},
    "UNKNOWN_SERVICE_CATEGORY",
)

invalid_rules = dict(DEFAULT_CATEGORY_SLA_DAYS)
invalid_rules["Pothole Repair"] = 1.5
record_case("invalid_direct_rule", {}, "INVALID_SLA_RULE", rules=invalid_rules)

client = app.test_client()
api_cases = [
    ("fractional_rule", {"rules": {"Pothole Repair": 1.5}}, 400),
    ("boolean_rule", {"rules": {"Pothole Repair": True}}, 400),
    ("unknown_rule", {"rules": {"Unmapped Service": 5}}, 400),
    ("zero_rule", {"rules": {"Pothole Repair": 0}}, 400),
    ("minimum_rule", {"rules": {"Pothole Repair": 1}}, 200),
    ("maximum_rule", {"rules": {"Pothole Repair": 30}}, 200),
    ("rules_empty_array", {"rules": []}, 400),
    ("rules_empty_string", {"rules": ""}, 400),
    ("rules_false", {"rules": False}, 400),
    ("rules_zero", {"rules": 0}, 400),
    ("rules_truthy_array", {"rules": [1]}, 400),
]

mismatches = []
for name, payload, expected_status in api_cases:
    response = client.post("/api/run", json=payload, headers={"Origin": "http://localhost"})
    body = response.get_json()
    print(name, "http", response.status_code, json.dumps(body, sort_keys=True)[:300])
    if response.status_code != expected_status:
        mismatches.append(
            {"case": name, "expected_http": expected_status, "observed_http": response.status_code}
        )

if mismatches:
    print("UNRESOLVED_API_VALIDATION_MISMATCHES", json.dumps(mismatches, sort_keys=True))
    raise SystemExit(1)

print("ALL_RECHECK_EDGE_PROBES_PASS")
