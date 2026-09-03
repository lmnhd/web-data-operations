"""Verify the public WS-001 evidence package before release review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import fitz


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "WS-001-qualified-tender-change-intelligence"
LIVE = PROJECT / "evidence" / "live"
PDF = ROOT / "output" / "pdf" / "WS-001-qualified-tender-change-intelligence.pdf"
EXCLUDED_RECORD_KEYS = {"contactPoint", "description", "unstructuredChanges"}


def walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(walk_keys(child))
    return keys


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Missing required evidence: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    captures = [
        LIVE / "sanitized-record.json",
        LIVE / "sanitized-record-06bb7d.json",
    ]
    for path in captures:
        package = load_json(path)
        if package.get("capture", {}).get("rawPayloadPersisted") is not False:
            raise ValueError(f"Raw-payload boundary missing in {path.name}")
        overlap = walk_keys(package.get("records", [])) & EXCLUDED_RECORD_KEYS
        if overlap:
            raise ValueError(f"Excluded record keys in {path.name}: {sorted(overlap)}")

    noise = load_json(LIVE / "run-06d396" / "run-report.json")["summary"]
    change = load_json(LIVE / "run-06bb7d" / "run-report.json")["summary"]
    if (noise["comparisons"], noise["material_change_comparisons"]) != (6, 0):
        raise ValueError("Live noise-case metrics changed")
    if (change["comparisons"], change["material_change_comparisons"], change["review_needed"]) != (1, 1, 1):
        raise ValueError("Live change-case metrics changed")

    if not PDF.is_file():
        raise ValueError("Reviewer PDF is missing")
    with fitz.open(PDF) as document:
        if document.page_count != 3:
            raise ValueError(f"Reviewer PDF must have 3 pages, found {document.page_count}")
        if any(len(page.get_text().strip()) < 500 for page in document):
            raise ValueError("Reviewer PDF contains an unexpectedly sparse page")

    print("WS-001 release evidence is valid: 2 sanitized captures, expected live metrics, 3-page PDF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
