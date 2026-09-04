"""Validate and transition the compact active state for the Shipping Pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
STATE_PATH = ROOT / "ACTIVE_ITERATION.json"

TRANSITIONS = {
    "PROPOSED": {"RESEARCHING", "REJECTED"},
    "RESEARCHING": {"AWAITING_APPROVAL", "REJECTED"},
    "AWAITING_APPROVAL": {"APPROVED", "RESEARCHING", "REJECTED"},
    "APPROVED": {"PROVING", "REJECTED"},
    "PROVING": {"AWAITING_BUILD_APPROVAL", "REPAIRING", "REJECTED"},
    "REPAIRING": {"PROVING", "AWAITING_APPROVAL", "REJECTED"},
    "AWAITING_BUILD_APPROVAL": {"BUILDING", "REPAIRING", "REJECTED"},
    "BUILDING": {"VERIFYING", "REPAIRING"},
    "VERIFYING": {"RELEASE_READY", "REPAIRING"},
    "RELEASE_READY": {"RELEASED", "REPAIRING"},
    "RELEASED": {"ARCHIVED"},
    "REJECTED": {"RESEARCHING", "ARCHIVED"},
    "ARCHIVED": set(),
}

REQUIRED_KEYS = {
    "schemaVersion",
    "iterationId",
    "stage",
    "concept",
    "authorizedScope",
    "nextAction",
    "humanApproval",
    "fatalBlockers",
    "repairableConditions",
    "limitations",
    "requiredFiles",
    "agentBudget",
}


def load_state() -> dict[str, Any]:
    if not STATE_PATH.is_file():
        raise ValueError(f"Missing {STATE_PATH.relative_to(ROOT)}")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def validate(state: dict[str, Any]) -> list[str]:
    errors = [f"Missing required key: {key}" for key in sorted(REQUIRED_KEYS - state.keys())]
    stage = state.get("stage")
    if stage not in TRANSITIONS:
        errors.append(f"Unknown stage: {stage}")

    required_files = state.get("requiredFiles", [])
    if not isinstance(required_files, list):
        errors.append("requiredFiles must be an array")
    else:
        for name in required_files:
            if not (ROOT / name).is_file():
                errors.append(f"Required file does not exist: {name}")

    budget = state.get("agentBudget", {})
    for key in ("stageLimit", "used"):
        if not isinstance(budget.get(key), int) or budget.get(key) < 0:
            errors.append(f"agentBudget.{key} must be a non-negative integer")
    if isinstance(budget.get("stageLimit"), int) and isinstance(budget.get("used"), int):
        if budget["used"] > budget["stageLimit"]:
            errors.append("Delegated-turn budget exceeded")

    approval = state.get("humanApproval", {})
    approved_stages = {"APPROVED", "PROVING", "AWAITING_BUILD_APPROVAL", "BUILDING", "VERIFYING", "RELEASE_READY", "RELEASED"}
    if stage in approved_stages and approval.get("status") != "approved":
        errors.append(f"Stage {stage} requires recorded human approval")

    if stage not in {"REJECTED", "ARCHIVED"} and state.get("fatalBlockers"):
        errors.append("An active iteration cannot proceed with fatalBlockers")

    return errors


def write_state(state: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def show(state: dict[str, Any]) -> None:
    keys = (
        "iterationId",
        "stage",
        "concept",
        "authorizedScope",
        "nextAction",
        "agentBudget",
        "fatalBlockers",
        "repairableConditions",
        "limitations",
        "requiredFiles",
    )
    print(json.dumps({key: state[key] for key in keys}, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("show")
    subparsers.add_parser("validate")
    transition = subparsers.add_parser("transition")
    transition.add_argument("--to", required=True, choices=sorted(TRANSITIONS))
    transition.add_argument("--next-action", required=True)
    args = parser.parse_args()

    try:
        state = load_state()
        errors = validate(state)
        if errors:
            raise ValueError("\n".join(errors))

        if args.command == "show":
            show(state)
        elif args.command == "validate":
            print("Active iteration state is valid.")
        else:
            current = state["stage"]
            if args.to not in TRANSITIONS[current]:
                raise ValueError(f"Illegal transition: {current} -> {args.to}")
            state["stage"] = args.to
            state["nextAction"] = args.next_action
            state["agentBudget"]["used"] = 0
            new_errors = validate(state)
            if new_errors:
                raise ValueError("\n".join(new_errors))
            write_state(state)
            print(f"Transitioned {state['iterationId']}: {current} -> {args.to}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"State validation failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
