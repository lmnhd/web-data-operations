"""Deterministic normalization, diffing, and qualification for WS-001."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


MATERIAL_FIELDS = (
    "tender.status",
    "tender.tenderPeriod.endDate",
    "tender.value.amount",
    "tender.value.currency",
    "tender.classification.id",
    "tender.lots",
)


def _get(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _fingerprint(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def extract_releases(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("releases"), list):
        return payload["releases"]

    releases: list[dict[str, Any]] = []
    for record in payload.get("records", []):
        if isinstance(record, dict) and isinstance(record.get("releases"), list):
            releases.extend(record["releases"])
    return releases


def normalize_release(
    release: dict[str, Any], source_url: str, retrieved_at: str
) -> dict[str, Any]:
    """Return only approved procurement fields; contact and prose are never retained."""
    tender = release.get("tender") if isinstance(release.get("tender"), dict) else {}
    period = tender.get("tenderPeriod") if isinstance(tender.get("tenderPeriod"), dict) else {}
    value = tender.get("value") if isinstance(tender.get("value"), dict) else {}
    classification = tender.get("classification") if isinstance(tender.get("classification"), dict) else {}

    lots = []
    for lot in tender.get("lots", []):
        if isinstance(lot, dict):
            lots.append({"id": lot.get("id"), "status": lot.get("status")})
    lots.sort(key=lambda item: (str(item.get("id")), str(item.get("status"))))

    tags = release.get("tag") if isinstance(release.get("tag"), list) else []
    source_fingerprint = release.get("sourceFingerprint") or _fingerprint(release)
    return {
        "ocid": release.get("ocid"),
        "release_id": release.get("id"),
        "release_date": release.get("date"),
        "source_tags": sorted(str(tag) for tag in tags),
        "tender": {
            "status": tender.get("status"),
            "tenderPeriod": {"endDate": period.get("endDate")},
            "value": {"amount": value.get("amount"), "currency": value.get("currency")},
            "classification": {"id": classification.get("id")},
            "lots": lots,
        },
        "provenance": {
            "source_url": source_url,
            "retrieved_at": retrieved_at,
            "content_fingerprint": source_fingerprint,
            "release_id": release.get("id"),
            "ocid": release.get("ocid"),
            "process_id": release.get("ocid"),
        },
    }


def diff_releases(previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
    changes = []
    for path in MATERIAL_FIELDS:
        old_value = _get(previous, path)
        new_value = _get(current, path)
        if old_value != new_value:
            changes.append({"field": path, "old": old_value, "new": new_value})
    return changes


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def qualify(release: dict[str, Any], profile: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    review: list[str] = []
    classification = _get(release, "tender.classification.id")
    amount = _get(release, "tender.value.amount")
    deadline = _get(release, "tender.tenderPeriod.endDate")

    prefixes = [str(value) for value in profile.get("allowedClassificationPrefixes", [])]
    if prefixes:
        if not classification:
            review.append("MISSING_CLASSIFICATION")
        elif not any(str(classification).startswith(prefix) for prefix in prefixes):
            reasons.append("CLASSIFICATION_NOT_ALLOWED")

    if amount is None:
        review.append("MISSING_VALUE")
    else:
        minimum = profile.get("minimumValue")
        maximum = profile.get("maximumValue")
        if minimum is not None and amount < minimum:
            reasons.append("VALUE_BELOW_MINIMUM")
        if maximum is not None and amount > maximum:
            reasons.append("VALUE_ABOVE_MAXIMUM")

    threshold = _parse_datetime(profile.get("deadlineOnOrAfter"))
    parsed_deadline = _parse_datetime(deadline)
    if threshold:
        if parsed_deadline is None:
            review.append("MISSING_DEADLINE")
        elif parsed_deadline < threshold:
            reasons.append("DEADLINE_TOO_SOON")

    if reasons:
        return "rejected", reasons
    if review:
        return "review-needed", review
    return "accepted", ["QUALIFICATION_RULES_PASSED"]


def run_pipeline(
    payload: dict[str, Any], profile: dict[str, Any], source_url: str, retrieved_at: str
) -> dict[str, Any]:
    normalized = [normalize_release(item, source_url, retrieved_at) for item in extract_releases(payload)]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for release in normalized:
        if release["ocid"]:
            grouped[str(release["ocid"])].append(release)

    outputs = {"accepted": [], "rejected": [], "review-needed": []}
    comparisons = 0
    update_tagged = 0
    material = 0

    for ocid in sorted(grouped):
        timeline = sorted(grouped[ocid], key=lambda item: (str(item["release_date"]), str(item["release_id"])))
        for previous, current in zip(timeline, timeline[1:]):
            comparisons += 1
            if any("Update" in tag or "Amendment" in tag for tag in current["source_tags"]):
                update_tagged += 1
            changes = diff_releases(previous, current)
            if not changes:
                status, reasons = "rejected", ["NO_MATERIAL_CHANGE"]
            else:
                material += 1
                status, reasons = qualify(current, profile)

            outputs[status].append(
                {
                    "ocid": ocid,
                    "previous_release_id": previous["release_id"],
                    "current_release_id": current["release_id"],
                    "source_tags": current["source_tags"],
                    "changes": changes,
                    "decision": status,
                    "reason_codes": reasons,
                    "provenance": current["provenance"],
                }
            )

    return {
        "summary": {
            "input_releases": len(normalized),
            "processes": len(grouped),
            "comparisons": comparisons,
            "update_tagged_comparisons": update_tagged,
            "material_change_comparisons": material,
            "accepted": len(outputs["accepted"]),
            "rejected": len(outputs["rejected"]),
            "review_needed": len(outputs["review-needed"]),
        },
        "queues": outputs,
    }


def write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "run-report.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    fieldnames = ("process_id", "ocid", "previous_release_id", "current_release_id", "source_tags", "changed_fields", "decision", "reason_codes", "source_url", "retrieved_at", "content_fingerprint")
    for queue_name, rows in result["queues"].items():
        with (output_dir / f"{queue_name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        "process_id": row["provenance"]["process_id"],
                        "ocid": row["ocid"],
                        "previous_release_id": row["previous_release_id"],
                        "current_release_id": row["current_release_id"],
                        "source_tags": "|".join(row["source_tags"]),
                        "changed_fields": "|".join(change["field"] for change in row["changes"]),
                        "decision": row["decision"],
                        "reason_codes": "|".join(row["reason_codes"]),
                        "source_url": row["provenance"]["source_url"],
                        "retrieved_at": row["provenance"]["retrieved_at"],
                        "content_fingerprint": row["provenance"]["content_fingerprint"],
                    }
                )
