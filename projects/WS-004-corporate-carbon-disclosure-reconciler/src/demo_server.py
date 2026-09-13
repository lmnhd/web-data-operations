"""Reviewer workbench adapter for the WS-004 reconciliation engine."""

from __future__ import annotations

import copy
import csv
import inspect
import io
import json
from pathlib import Path
from typing import Any

import reconcile


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evidence" / "fixtures" / "disclosure_cases.json"
FACTORS_PATH = ROOT / "evidence" / "factors" / "ghg_factors_2025.json"
ALLOWED_UNITS = {"kWh", "MWh"}


def load_cases() -> dict[str, Any]:
    return reconcile.load_json(CASES_PATH)


def load_factors() -> dict[str, Any]:
    return reconcile.load_json(FACTORS_PATH)


def available_cases() -> list[dict[str, str]]:
    return [
        {
            "caseId": case["caseId"],
            "fixtureKind": case["fixtureKind"],
            "label": case["caseId"].replace("CASE-", "Case ").replace("-", " ").title(),
        }
        for case in load_cases()["cases"]
    ]


def _selected_document(
    case_id: str | None, activity_unit: str | None
) -> dict[str, Any]:
    document = copy.deepcopy(load_cases())
    if not case_id:
        if activity_unit is not None:
            raise ValueError("An activity-unit change requires one selected case.")
        return document

    matches = [case for case in document["cases"] if case["caseId"] == case_id]
    if len(matches) != 1:
        raise ValueError("Select a known benchmark case.")
    document["cases"] = matches

    if activity_unit is not None:
        if activity_unit not in ALLOWED_UNITS:
            raise ValueError("Activity unit must be kWh or MWh.")
        if case_id != "CASE-02-CONTROLLED-MWH-RECONCILED":
            raise ValueError("The unit exercise is limited to the controlled Case 02 scenario.")
        matches[0]["calculation"]["activityUnit"] = activity_unit
    return document


def _csv_for_run(run: dict[str, Any]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output, fieldnames=reconcile.CSV_FIELDS, extrasaction="ignore"
    )
    writer.writeheader()
    writer.writerows(
        {"runId": run["runId"], **result} for result in run["results"]
    )
    return output.getvalue()


def run_demo(
    case_id: str | None = None, activity_unit: str | None = None
) -> dict[str, Any]:
    cases = _selected_document(case_id, activity_unit)
    factors = load_factors()
    run = reconcile.run_benchmark(
        cases,
        factors,
        factor_file_bytes=FACTORS_PATH.read_bytes(),
        engine_file_bytes=Path(reconcile.__file__).read_bytes(),
    )
    run["csv"] = _csv_for_run(run)
    run["selection"] = {
        "caseId": case_id,
        "activityUnitOverride": activity_unit,
    }
    return run


def code_excerpt() -> str:
    source_lines = inspect.getsource(reconcile.evaluate_case).splitlines()
    start = next(
        index
        for index, line in enumerate(source_lines)
        if "SUPPORTED_SOURCE_FORMATS" in line
    )
    return "\n".join(source_lines[start : start + 24])
