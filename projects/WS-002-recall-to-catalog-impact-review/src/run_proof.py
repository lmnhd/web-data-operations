"""Run the WS-002 fixture proof and export reviewer-readable artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from catalog_matcher import evaluate, match_catalog


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def export_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "catalog_id", "classification", "matched_recall_number",
        "candidate_recall_numbers", "reasons", "top_score", "source_url",
        "retrieved_at", "content_fingerprint", "candidate_provenance",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            flattened = {key: row.get(key) for key in fields}
            flattened["candidate_recall_numbers"] = "|".join(row["candidate_recall_numbers"])
            flattened["reasons"] = "|".join(row["reasons"])
            flattened["candidate_provenance"] = json.dumps(
                row["candidate_provenance"], sort_keys=True, separators=(",", ":")
            )
            writer.writerow(flattened)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--recalls", type=Path, required=True)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    catalog = load_json(args.catalog)
    recall_fixture = load_json(args.recalls)
    results = match_catalog(catalog, recall_fixture["records"], recall_fixture["provenance"])
    evaluation = evaluate(results, load_json(args.expected)) if args.expected else None
    counts = Counter(row["classification"] for row in results)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "results.json", results)
    for classification, filename in (
        ("match", "matches.csv"),
        ("no_match", "no-matches.csv"),
        ("review_needed", "review-needed.csv"),
    ):
        export_csv(args.output_dir / filename, [row for row in results if row["classification"] == classification])

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalog_rows": len(catalog),
        "recall_records": len(recall_fixture["records"]),
        "classification_counts": dict(sorted(counts.items())),
        "evaluation": evaluation,
        "source_request_count": recall_fixture["provenance"]["request_count"],
        "limitations": [
            "Fixture proof only; no production coverage or scale claim.",
            "Not medical advice, a public alert, or a current recall-status determination.",
            "Synthetic catalog rows do not prove integration with private retailer data.",
        ],
    }
    write_json(args.output_dir / "run-report.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not evaluation or evaluation["labels_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
