"""Fetch exactly one Find a Tender record and persist only allowlisted fields."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tender_pipeline import extract_releases, normalize_release


OCID_PATTERN = re.compile(r"^ocds-h6vhtk-[0-9a-f]{6}$")
API_ROOT = "https://www.find-tender.service.gov.uk/api/1.0/ocdsRecordPackages"
USER_AGENT = "lmnhd-web-data-operations/WS-001 (+https://github.com/lmnhd/web-data-operations)"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sanitize_release(release: dict[str, Any], source_url: str, retrieved_at: str) -> dict[str, Any]:
    normalized = normalize_release(release, source_url, retrieved_at)
    return {
        "ocid": normalized["ocid"],
        "id": normalized["release_id"],
        "date": normalized["release_date"],
        "tag": normalized["source_tags"],
        "tender": normalized["tender"],
        "sourceFingerprint": normalized["provenance"]["content_fingerprint"],
    }


def fetch_once(ocid: str, timeout_seconds: int = 20) -> tuple[dict[str, Any], str, str]:
    if not OCID_PATTERN.fullmatch(ocid):
        raise ValueError("OCID must match ocds-h6vhtk followed by six lowercase hexadecimal characters")

    source_url = f"{API_ROOT}/{quote(ocid, safe='')}"
    retrieved_at = _utc_now()
    request = Request(source_url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})

    # Intentionally one request with no retry, pagination, rate probing, or fallback crawl.
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = json.load(response)

    return payload, source_url, retrieved_at


def sanitize_package(payload: dict[str, Any], source_url: str, retrieved_at: str) -> dict[str, Any]:
    releases = extract_releases(payload)
    sanitized = [_sanitize_release(release, source_url, retrieved_at) for release in releases]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for release in sanitized:
        if release["ocid"]:
            grouped.setdefault(str(release["ocid"]), []).append(release)

    return {
        "capture": {
            "sourceUrl": source_url,
            "retrievedAt": retrieved_at,
            "requestCount": 1,
            "rawPayloadPersisted": False,
            "excludedFieldClasses": ["contactPoint", "description", "unstructured free text"],
            "sourceLicense": payload.get("license"),
            "attribution": "Contains public sector information licensed under the Open Government Licence v3.0.",
        },
        "records": [
            {"ocid": ocid, "releases": sorted(items, key=lambda item: (str(item["date"]), str(item["id"])))}
            for ocid, items in sorted(grouped.items())
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ocid", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        payload, source_url, retrieved_at = fetch_once(args.ocid)
        sanitized = sanitize_package(payload, source_url, retrieved_at)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(sanitized, indent=2) + "\n", encoding="utf-8")
        release_count = sum(len(record["releases"]) for record in sanitized["records"])
        print(json.dumps({"requests": 1, "records": len(sanitized["records"]), "releases": release_count, "output": str(args.output)}, indent=2))
        return 0
    except HTTPError as error:
        retry_after = error.headers.get("Retry-After")
        print(f"Fetch stopped after HTTP {error.code}; Retry-After={retry_after!r}. No retry attempted.")
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as error:
        print(f"Fetch stopped: {error}. No retry attempted.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
