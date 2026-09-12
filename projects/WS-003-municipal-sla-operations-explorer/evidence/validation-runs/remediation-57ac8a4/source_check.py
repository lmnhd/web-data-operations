from __future__ import annotations

import csv
import io
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
PACKAGE_API = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/"
    "package_show?id=311-service-requests-customer-initiated"
)
RESOURCE_ID = "99b7f283-7345-4f5a-a126-d078ed4f3419"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "WS-003-independent-validator/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    package = json.loads(fetch(PACKAGE_API))
    resources = package["result"]["resources"]
    resource = next(item for item in resources if item["id"] == RESOURCE_ID)
    payload = fetch(resource["url"])
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        csv_names = sorted(name for name in archive.namelist() if name.lower().endswith(".csv"))
        if not csv_names:
            raise RuntimeError("Official 2026 resource contains no CSV file")
        with archive.open(csv_names[0]) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            header = next(csv.reader(text))

    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "package_api": PACKAGE_API,
        "resource_id": RESOURCE_ID,
        "resource_name": resource.get("name"),
        "resource_url": resource.get("url"),
        "resource_last_modified": resource.get("last_modified"),
        "resource_bytes": len(payload),
        "archive_csv": csv_names[0],
        "header": header,
        "missing_required_for_sla_proof": {
            "stable_request_id": not any("request" in column.lower() and "id" in column.lower() for column in header),
            "target_timestamp": not any("target" in column.lower() for column in header),
            "closure_timestamp": not any(
                term in column.lower() for column in header for term in ("closed", "closure", "completion")
            ),
        },
    }
    (RUN_DIR / "source-check-results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
