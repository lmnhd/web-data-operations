"""Command-line runner for the WS-001 vertical proof."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tender_pipeline import run_pipeline, write_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--source-url")
    parser.add_argument("--retrieved-at")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    capture = payload.get("capture", {}) if isinstance(payload.get("capture"), dict) else {}
    source_url = args.source_url or capture.get("sourceUrl") or "fixture://ws-001/release-package"
    retrieved_at = args.retrieved_at or capture.get("retrievedAt") or "not-recorded"
    result = run_pipeline(payload, profile, source_url, retrieved_at)
    write_outputs(result, args.output_dir)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
