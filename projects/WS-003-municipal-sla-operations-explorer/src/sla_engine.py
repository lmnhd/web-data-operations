"""Municipal 311 SLA Operations Calculation Engine (WS-003).

Processes adapter-ready municipal service request records, computes exact SLA response
durations and margins, maps lifecycle states, and aggregates ward-level scenario analytics.

The bundled proof data is synthetic because Toronto's public 311 export does not expose
target or closure timestamps. This module does not calculate official municipal SLAs.
"""

from __future__ import annotations

import argparse
import csv
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_CATEGORY_SLA_DAYS: dict[str, int] = {
    "Pothole Repair": 5,
    "Streetlight Maintenance": 3,
    "Tree Trimming": 10,
    "Garbage Collection": 2,
}

AT_RISK_THRESHOLD_DAYS = 1.0  # Open/In-progress items with <= 1 day remaining are AT_RISK
FIXTURE_KIND = "synthetic_sla_scenario"
VALID_STATUSES = {"OPEN", "IN_PROGRESS", "CLOSED"}


def parse_iso_timestamp(ts_str: str | None) -> datetime | None:
    if not ts_str or not isinstance(ts_str, str) or ts_str.strip() == "":
        return None
    try:
        # Handle ISO strings ending in Z or offsets
        cleaned = ts_str.strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def calculate_record_fingerprint(record: dict[str, Any]) -> str:
    raw = json.dumps(record, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def evaluate_record(
    record: dict[str, Any],
    rules: dict[str, int] | None = None,
    reference_now: datetime | None = None,
) -> dict[str, Any]:
    if rules is None:
        rules = DEFAULT_CATEGORY_SLA_DAYS
    if reference_now is None:
        reference_now = datetime.now(timezone.utc)
    elif reference_now.tzinfo is None:
        reference_now = reference_now.replace(tzinfo=timezone.utc)

    s_id = str(record.get("service_request_id", "UNKNOWN"))
    s_name = str(record.get("service_name", "Uncategorized"))
    ward = str(record.get("ward", "Unknown Ward"))
    raw_created = record.get("created_date")
    raw_target = record.get("target_date")
    raw_closed = record.get("closed_date")
    raw_status = str(record.get("status", "OPEN")).upper()

    fingerprint = calculate_record_fingerprint(record)

    def review(reason_code: str, sla_target_days: int | None = None) -> dict[str, Any]:
        return {
            "fixture_kind": FIXTURE_KIND,
            "service_request_id": s_id,
            "service_name": s_name,
            "ward": ward,
            "created_date": raw_created,
            "target_date": raw_target,
            "closed_date": raw_closed,
            "status": raw_status,
            "duration_days": None,
            "sla_target_days": sla_target_days,
            "margin_days": None,
            "lifecycle_state": "DATA_ERROR",
            "sla_status": "INCOMPLETE_DATA_REVIEW",
            "reason_code": reason_code,
            "fingerprint": fingerprint,
        }

    if s_name not in rules:
        return review("UNKNOWN_SERVICE_CATEGORY")

    sla_target_days = rules[s_name]
    if isinstance(sla_target_days, bool) or not isinstance(sla_target_days, int) or not 1 <= sla_target_days <= 30:
        return review("INVALID_SLA_RULE")

    created_dt = parse_iso_timestamp(raw_created)
    if created_dt is None:
        return review("INVALID_CREATED_TIMESTAMP", sla_target_days)

    parsed_raw_target = parse_iso_timestamp(raw_target)

    if raw_target not in (None, "") and parsed_raw_target is None:
        return review("INVALID_TARGET_TIMESTAMP", sla_target_days)

    if parsed_raw_target is not None and rules == DEFAULT_CATEGORY_SLA_DAYS:
        target_dt = parsed_raw_target
        target_derived = False
    else:
        target_dt = datetime.fromtimestamp(created_dt.timestamp() + (sla_target_days * 86400), tz=timezone.utc)
        target_derived = (parsed_raw_target is None)

    if target_dt < created_dt:
        return review("TARGET_BEFORE_CREATED", sla_target_days)

    closed_dt = parse_iso_timestamp(raw_closed)

    if raw_closed not in (None, "") and closed_dt is None:
        return review("INVALID_CLOSED_TIMESTAMP", sla_target_days)
    if raw_status not in VALID_STATUSES:
        return review("UNKNOWN_STATUS", sla_target_days)
    if raw_status == "CLOSED" and closed_dt is None:
        return review("MISSING_CLOSED_TIMESTAMP", sla_target_days)
    if raw_status != "CLOSED" and closed_dt is not None:
        return review("STATUS_CLOSED_DATE_CONFLICT", sla_target_days)
    if closed_dt is not None and closed_dt < created_dt:
        return review("CLOSED_BEFORE_CREATED", sla_target_days)
    if closed_dt is not None and closed_dt > reference_now:
        return review("CLOSED_AFTER_REFERENCE_TIME", sla_target_days)
    if closed_dt is None and reference_now < created_dt:
        return review("CREATED_AFTER_REFERENCE_TIME", sla_target_days)

    if closed_dt is not None:
        duration_sec = (closed_dt - created_dt).total_seconds()
        duration_days = round(duration_sec / 86400.0, 2)
        margin_sec = (target_dt - closed_dt).total_seconds()
        margin_days = round(margin_sec / 86400.0, 2)

        if margin_days >= 0:
            lifecycle_state = "CLOSED_ON_TIME"
            sla_status = "COMPLIANT"
            reason_code = "CLOSED_BEFORE_SLA_TARGET"
        else:
            lifecycle_state = "CLOSED_OVERDUE"
            sla_status = "SLA_BREACHED"
            reason_code = "CLOSED_AFTER_SLA_TARGET"
    else:
        duration_sec = (reference_now - created_dt).total_seconds()
        duration_days = round(duration_sec / 86400.0, 2)
        margin_sec = (target_dt - reference_now).total_seconds()
        margin_days = round(margin_sec / 86400.0, 2)

        if margin_days < 0:
            lifecycle_state = "OPEN_OVERDUE"
            sla_status = "SLA_BREACHED"
            reason_code = "OPEN_PAST_SLA_TARGET"
        elif margin_days <= AT_RISK_THRESHOLD_DAYS:
            lifecycle_state = "IN_PROGRESS" if raw_status == "IN_PROGRESS" else "OPEN"
            sla_status = "AT_RISK"
            reason_code = "IN_PROGRESS_SLA_MARGIN_EXPIRING"
        else:
            lifecycle_state = "IN_PROGRESS" if raw_status == "IN_PROGRESS" else "OPEN"
            sla_status = "COMPLIANT"
            reason_code = "OPEN_TARGET_DERIVED_WITHIN_SLA" if target_derived else "IN_PROGRESS_WITHIN_SLA"

    return {
        "fixture_kind": FIXTURE_KIND,
        "service_request_id": s_id,
        "service_name": s_name,
        "ward": ward,
        "created_date": created_dt.isoformat(),
        "target_date": target_dt.isoformat(),
        "closed_date": closed_dt.isoformat() if closed_dt else None,
        "status": raw_status,
        "duration_days": duration_days,
        "sla_target_days": sla_target_days,
        "margin_days": margin_days,
        "lifecycle_state": lifecycle_state,
        "sla_status": sla_status,
        "reason_code": reason_code,
        "fingerprint": fingerprint,
    }


def evaluate_dataset(
    records: list[dict[str, Any]],
    rules: dict[str, int] | None = None,
    reference_now: datetime | None = None,
) -> dict[str, Any]:
    if rules is None:
        rules = DEFAULT_CATEGORY_SLA_DAYS
    if reference_now is None:
        reference_now = datetime.now(timezone.utc)

    evaluated_items = [evaluate_record(rec, rules=rules, reference_now=reference_now) for rec in records]

    # Summary counts
    status_counts: dict[str, int] = {
        "COMPLIANT": 0,
        "AT_RISK": 0,
        "SLA_BREACHED": 0,
        "INCOMPLETE_DATA_REVIEW": 0,
    }
    ward_analytics: dict[str, dict[str, Any]] = {}

    for item in evaluated_items:
        st = item["sla_status"]
        status_counts[st] = status_counts.get(st, 0) + 1

        ward = item["ward"]
        if ward not in ward_analytics:
            ward_analytics[ward] = {
                "total_requests": 0,
                "compliant": 0,
                "at_risk": 0,
                "breached": 0,
                "data_error": 0,
            }

        ward_analytics[ward]["total_requests"] += 1
        if st == "COMPLIANT":
            ward_analytics[ward]["compliant"] += 1
        elif st == "AT_RISK":
            ward_analytics[ward]["at_risk"] += 1
        elif st == "SLA_BREACHED":
            ward_analytics[ward]["breached"] += 1
        else:
            ward_analytics[ward]["data_error"] += 1

    # Compute ward compliance percentage
    for ward, stats in ward_analytics.items():
        evaluable = stats["total_requests"] - stats["data_error"]
        stats["compliance_rate_pct"] = round((stats["compliant"] / evaluable * 100.0), 1) if evaluable > 0 else 0.0

    return {
        "fixture_kind": FIXTURE_KIND,
        "reference_now": reference_now.isoformat(),
        "rules_applied": rules,
        "total_records": len(records),
        "status_summary": status_counts,
        "ward_analytics": ward_analytics,
        "evaluated_records": evaluated_items,
    }


def export_evaluated_records_csv(evaluated_items: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = [
        "fixture_kind",
        "service_request_id",
        "service_name",
        "ward",
        "created_date",
        "target_date",
        "closed_date",
        "status",
        "duration_days",
        "sla_target_days",
        "margin_days",
        "lifecycle_state",
        "sla_status",
        "reason_code",
        "fingerprint",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in evaluated_items:
            writer.writerow(item)


def main() -> None:
    parser = argparse.ArgumentParser(description="Municipal 311 SLA Operations Engine")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("projects/WS-003-municipal-sla-operations-explorer/evidence/fixtures/toronto_311_sample.json"),
        help="Path to input 311 JSON fixture",
    )
    parser.add_argument("--output-json", type=Path, help="Path for evaluated output JSON")
    parser.add_argument("--output-csv", type=Path, help="Path for evaluated output CSV")
    parser.add_argument("--ref-now", type=str, default="2026-08-08T12:00:00Z", help="Reference ISO timestamp for evaluation")
    args = parser.parse_args()

    ref_dt = parse_iso_timestamp(args.ref_now)
    with args.input.open("r", encoding="utf-8") as f:
        data = json.load(f)

    result = evaluate_dataset(data, reference_now=ref_dt)

    print("=== MUNICIPAL 311 SLA EVALUATION RUN REPORT ===")
    print(f"Reference Now: {result['reference_now']}")
    print(f"Total Records: {result['total_records']}")
    print("Status Summary:", json.dumps(result["status_summary"], indent=2))
    print("Ward Analytics:", json.dumps(result["ward_analytics"], indent=2))

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        with args.output_json.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Wrote JSON output to {args.output_json}")

    if args.output_csv:
        export_evaluated_records_csv(result["evaluated_records"], args.output_csv)
        print(f"Wrote CSV output to {args.output_csv}")


if __name__ == "__main__":
    main()
