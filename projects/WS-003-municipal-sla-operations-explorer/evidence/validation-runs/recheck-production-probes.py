"""Signed-out production probes for WS-003 recheck candidate 2addbb6f."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


BASE = "https://municipal-311-sla-operations-desk.vercel.app"
EXPECTED_DEFAULT = {
    "COMPLIANT": 8,
    "AT_RISK": 1,
    "SLA_BREACHED": 5,
    "INCOMPLETE_DATA_REVIEW": 1,
}
EXPECTED_STRICT = {
    "COMPLIANT": 0,
    "AT_RISK": 1,
    "SLA_BREACHED": 13,
    "INCOMPLETE_DATA_REVIEW": 1,
}


def request(path: str, payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "WS003-independent-validator"},
        method="GET" if payload is None else "POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return response.status, raw
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


status, html = request("/")
html_lower = html.lower()
print("page", status, "bytes", len(html))
print("page_synthetic", "synthetic sla scenario" in html_lower)
print("page_missing_fields", "does not include target or closure timestamps" in html_lower)
print("page_old_recorded_claim_absent", "recorded toronto 311 records" not in html_lower)
assert status == 200
assert "synthetic sla scenario" in html_lower
assert "does not include target or closure timestamps" in html_lower
assert "recorded toronto 311 records" not in html_lower

status, raw = request("/api/config")
config = json.loads(raw)
print("config", status, json.dumps(config, sort_keys=True))
assert status == 200
assert "synthetic" in config["boundary"].lower()
assert "does not provide target or closure timestamps" in config["boundary"].lower()
assert config["default_rules"] == {
    "Garbage Collection": 2,
    "Pothole Repair": 5,
    "Streetlight Maintenance": 3,
    "Tree Trimming": 10,
}

for name, rules, expected in (
    ("default", {}, EXPECTED_DEFAULT),
    ("strict", {"Pothole Repair": 3, "Streetlight Maintenance": 2, "Tree Trimming": 5, "Garbage Collection": 1}, EXPECTED_STRICT),
):
    status, raw = request("/api/run", {"rules": rules})
    result = json.loads(raw)
    fixture_values = sorted({row["fixture_kind"] for row in result["evaluated_records"]})
    print(name, status, "counts", json.dumps(result["status_summary"], sort_keys=True), "fixture_top", result["fixture_kind"], "fixture_rows", fixture_values)
    assert status == 200
    assert result["status_summary"] == expected
    assert result["fixture_kind"] == "synthetic_sla_scenario"
    assert fixture_values == ["synthetic_sla_scenario"]
    assert len(result["evaluated_records"]) == 15

for name, rules in (
    ("fractional", {"Pothole Repair": 1.5}),
    ("unknown", {"Unmapped Service": 5}),
):
    status, raw = request("/api/run", {"rules": rules})
    print(name, status, raw)
    assert status == 400

mismatches = []
for name, rules in (
    ("empty_array", []),
    ("empty_string", ""),
    ("false", False),
    ("zero", 0),
):
    status, raw = request("/api/run", {"rules": rules})
    print(name, status, raw[:120])
    if status != 400:
        mismatches.append({"case": name, "expected_http": 400, "observed_http": status})

if mismatches:
    print("UNRESOLVED_PRODUCTION_API_VALIDATION_MISMATCHES", json.dumps(mismatches, sort_keys=True))
    raise SystemExit(1)

print("ALL_RECHECK_PRODUCTION_PROBES_PASS")
