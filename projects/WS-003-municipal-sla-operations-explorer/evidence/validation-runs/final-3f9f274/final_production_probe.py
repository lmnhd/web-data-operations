from __future__ import annotations

import hashlib
import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path


BASE = "https://municipal-311-sla-operations-desk.vercel.app"
ROOT = Path(__file__).resolve().parents[5]
PROJECT = ROOT / "projects" / "WS-003-municipal-sla-operations-explorer"
RUN_DIR = Path(__file__).resolve().parent
SSL_CONTEXT = ssl.create_default_context()


def request(path: str, *, body=None, content_type="application/json", headers=None):
    data = None
    if body is not None:
        if isinstance(body, bytes):
            data = body
        else:
            data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    all_headers = dict(headers or {})
    if data is not None and content_type is not None:
        all_headers["Content-Type"] = content_type
    req = urllib.request.Request(BASE + path, data=data, headers=all_headers, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=30) as response:
            raw = response.read()
            return response.status, dict(response.headers), raw
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()


def decoded(raw: bytes):
    try:
        return json.loads(raw)
    except Exception:
        return raw.decode("utf-8", errors="replace")


def canonical_text_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def main() -> None:
    result = {"base": BASE, "gets": {}, "cases": []}
    for path in ["/", "/app.js", "/style.css", "/api/config", "/api/code"]:
        status, headers, raw = request(path)
        result["gets"][path] = {
            "status": status,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "cache_control": headers.get("Cache-Control"),
            "content_security_policy": headers.get("Content-Security-Policy"),
            "x_content_type_options": headers.get("X-Content-Type-Options"),
            "body": decoded(raw) if path.startswith("/api/") else None,
        }

    local_assets = {"/": PROJECT / "demo/index.html", "/app.js": PROJECT / "demo/app.js", "/style.css": PROJECT / "demo/style.css"}
    for path, local_path in local_assets.items():
        result["gets"][path]["local_sha256"] = hashlib.sha256(local_path.read_bytes()).hexdigest()
        result["gets"][path]["matches_local_bytes"] = result["gets"][path]["sha256"] == result["gets"][path]["local_sha256"]
        result["gets"][path]["local_canonical_lf_sha256"] = canonical_text_sha256(local_path.read_bytes())
        result["gets"][path]["production_canonical_lf_sha256"] = canonical_text_sha256(request(path)[2])
        result["gets"][path]["matches_local_canonical_lf"] = (
            result["gets"][path]["local_canonical_lf_sha256"]
            == result["gets"][path]["production_canonical_lf_sha256"]
        )

    origin = {"Origin": BASE}
    invalid_values = [
        ("rules_empty_array", []),
        ("rules_empty_string", ""),
        ("rules_false", False),
        ("rules_zero", 0),
        ("rules_null", None),
        ("rules_truthy_array", [1]),
        ("rules_truthy_string", "x"),
        ("rules_truthy_number", 1),
        ("rules_truthy_boolean", True),
        ("rule_fractional", {"Pothole Repair": 1.5}),
        ("rule_boolean_true", {"Pothole Repair": True}),
        ("rule_boolean_false", {"Pothole Repair": False}),
        ("rule_zero", {"Pothole Repair": 0}),
        ("rule_negative", {"Pothole Repair": -1}),
        ("rule_31", {"Pothole Repair": 31}),
        ("rule_string", {"Pothole Repair": "3"}),
        ("rule_value_null", {"Pothole Repair": None}),
        ("rule_unknown", {"Unmapped Service": 5}),
    ]
    for name, value in invalid_values:
        status, headers, raw = request("/api/run", body={"rules": value}, headers=origin)
        result["cases"].append({"name": name, "status": status, "body": decoded(raw)})

    raw_cases = [
        ("malformed_json", b'{"rules":', "application/json", origin),
        ("empty_json_body", b"", "application/json", origin),
        ("top_level_array", b"[]", "application/json", origin),
        ("top_level_string", b'"x"', "application/json", origin),
        ("top_level_false", b"false", "application/json", origin),
        ("non_json_content_type", b'{"rules":{}}', "text/plain", origin),
        ("oversized_json", json.dumps({"rules": {}, "padding": "x" * 9000}).encode("utf-8"), "application/json", origin),
        ("cross_origin", b'{"rules":{}}', "application/json", {"Origin": "https://evil.example"}),
        ("sec_fetch_cross_site", b'{"rules":{}}', "application/json", {"Origin": BASE, "Sec-Fetch-Site": "cross-site"}),
        ("same_origin", b'{"rules":{}}', "application/json", origin),
        ("origin_absent", b'{"rules":{}}', "application/json", {}),
        ("scheme_mismatch_same_host", b'{"rules":{}}', "application/json", {"Origin": BASE.replace("https://", "http://")}),
    ]
    for name, body, content_type, headers in raw_cases:
        status, response_headers, raw = request("/api/run", body=body, content_type=content_type, headers=headers)
        parsed = decoded(raw)
        item = {"name": name, "status": status, "body": parsed}
        if isinstance(parsed, dict) and "status_summary" in parsed:
            item["status_summary"] = parsed["status_summary"]
        result["cases"].append(item)

    rulesets = {
        "default": {"Pothole Repair": 5, "Streetlight Maintenance": 3, "Tree Trimming": 10, "Garbage Collection": 2},
        "strict": {"Pothole Repair": 3, "Streetlight Maintenance": 2, "Tree Trimming": 5, "Garbage Collection": 1},
    }
    result["scenarios"] = {}
    for name, rules in rulesets.items():
        status, headers, raw = request("/api/run", body={"rules": rules}, headers=origin)
        data = decoded(raw)
        sr_001 = next(item for item in data["evaluated_records"] if item["service_request_id"] == "SR-311-001")
        result["scenarios"][name] = {
            "status": status,
            "fixture_kind": data["fixture_kind"],
            "engine_sha256": data["engine_sha256"],
            "status_summary": data["status_summary"],
            "ward_01": data["ward_analytics"]["Ward 01 - Etobicoke North"],
            "sr_311_001": {
                "sla_status": sr_001["sla_status"],
                "reason_code": sr_001["reason_code"],
                "fingerprint": sr_001["fingerprint"],
            },
            "all_rows_synthetic": all(item["fixture_kind"] == "synthetic_sla_scenario" for item in data["evaluated_records"]),
            "all_reason_codes_present": all(bool(item["reason_code"]) for item in data["evaluated_records"]),
            "all_fingerprints_present": all(bool(item["fingerprint"]) for item in data["evaluated_records"]),
        }

    local_engine_sha = hashlib.sha256((PROJECT / "src/sla_engine.py").read_bytes()).hexdigest()
    result["local_engine_sha256"] = local_engine_sha
    result["production_engine_matches_local"] = all(
        scenario["engine_sha256"] == local_engine_sha for scenario in result["scenarios"].values()
    )
    result["expected_status_checks"] = {
        case["name"]: case["status"]
        for case in result["cases"]
    }
    (RUN_DIR / "final-production-results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
