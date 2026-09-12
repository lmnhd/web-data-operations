"""Local reviewer workbench adapter for the Municipal 311 SLA Operations Desk (WS-003)."""

from __future__ import annotations

import copy
import csv
import hashlib
import inspect
import io
import json
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "src"))
import sla_engine

RUNS: dict[str, dict] = {}
RUN_LOCK = threading.Lock()
EDITABLE_CATEGORIES = ["Pothole Repair", "Streetlight Maintenance", "Tree Trimming", "Garbage Collection"]


def load_fixture() -> list[dict]:
    with (FIXTURES / "toronto_311_sample.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def default_rules() -> dict[str, int]:
    return dict(sla_engine.DEFAULT_CATEGORY_SLA_DAYS)


def default_reference_now() -> str:
    return "2026-08-08T12:00:00Z"


def validate_rules_override(rules: object) -> dict[str, int]:
    if not isinstance(rules, dict):
        raise ValueError("Rules must be an object.")
    unknown = sorted(set(rules) - set(EDITABLE_CATEGORIES))
    if unknown:
        raise ValueError(f"Unknown SLA rule categories: {', '.join(unknown)}.")
    clean_rules = dict(sla_engine.DEFAULT_CATEGORY_SLA_DAYS)
    for cat in EDITABLE_CATEGORIES:
        if cat in rules:
            val = rules[cat]
            if isinstance(val, bool) or not isinstance(val, int) or val < 1 or val > 30:
                raise ValueError(f"SLA target for {cat} must be an integer between 1 and 30 days.")
            clean_rules[cat] = val
    return clean_rules


def run_demo(rules_override: dict[str, int] | None = None, ref_now_str: str | None = None) -> dict:
    records = load_fixture()
    rules = validate_rules_override(rules_override or {})
    ref_dt = sla_engine.parse_iso_timestamp(ref_now_str or default_reference_now())

    started = time.perf_counter()
    result = sla_engine.evaluate_dataset(records, rules=rules, reference_now=ref_dt)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)

    output = io.StringIO(newline="")
    # Perform in-memory CSV generation
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
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for item in result["evaluated_records"]:
        writer.writerow(item)

    run_id = str(uuid.uuid4())
    payload = {
        "fixture_kind": result["fixture_kind"],
        "run_id": run_id,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_ms": elapsed_ms,
        "engine": "sla_engine.evaluate_dataset (Python)",
        "engine_sha256": hashlib.sha256(Path(sla_engine.__file__).read_bytes()).hexdigest(),
        "rules_applied": rules,
        "reference_now": result["reference_now"],
        "total_records": result["total_records"],
        "status_summary": result["status_summary"],
        "ward_analytics": result["ward_analytics"],
        "evaluated_records": result["evaluated_records"],
        "csv": output.getvalue(),
    }
    return payload
