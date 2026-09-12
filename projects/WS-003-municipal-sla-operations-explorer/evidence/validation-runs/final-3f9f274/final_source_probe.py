from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path


PACKAGE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=311-service-requests-customer-initiated"
RESOURCE_ID = "99b7f283-7345-4f5a-a126-d078ed4f3419"
EXPECTED_HEADER = [
    "Creation Date",
    "Status",
    "First 3 Chars of Postal Code",
    "Intersection Street 1",
    "Intersection Street 2",
    "Ward",
    "Service Request Type",
    "Division",
    "Section",
]
RUN_DIR = Path(__file__).resolve().parent


def main() -> None:
    with urllib.request.urlopen(PACKAGE_URL, timeout=30) as response:
        package_payload = response.read()
    package = json.loads(package_payload)["result"]
    resource = next(item for item in package["resources"] if item["id"] == RESOURCE_ID)

    with urllib.request.urlopen(resource["url"], timeout=90) as response:
        zip_payload = response.read()
    with zipfile.ZipFile(io.BytesIO(zip_payload)) as archive:
        csv_name = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
        with archive.open(csv_name) as raw:
            reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
            header = next(reader)

    target_fields = [name for name in header if "target" in name.casefold()]
    closure_fields = [name for name in header if "clos" in name.casefold() or "complet" in name.casefold()]
    identifier_fields = [name for name in header if "request id" in name.casefold() or "request number" in name.casefold()]
    result = {
        "package_url": PACKAGE_URL,
        "package_id": package.get("id"),
        "package_name": package.get("name"),
        "package_title": package.get("title"),
        "package_metadata_modified": package.get("metadata_modified"),
        "license_id": package.get("license_id"),
        "license_title": package.get("license_title"),
        "resource_id": resource["id"],
        "resource_name": resource.get("name"),
        "resource_last_modified": resource.get("last_modified"),
        "resource_datastore_active": resource.get("datastore_active"),
        "resource_url": resource["url"],
        "zip_bytes": len(zip_payload),
        "zip_sha256": hashlib.sha256(zip_payload).hexdigest(),
        "csv_name": csv_name,
        "header": header,
        "header_matches_contract": header == EXPECTED_HEADER,
        "target_fields": target_fields,
        "closure_fields": closure_fields,
        "stable_request_identifier_fields": identifier_fields,
        "target_timestamp_absent": target_fields == [],
        "closure_timestamp_absent": closure_fields == [],
        "stable_request_identifier_absent": identifier_fields == [],
    }
    (RUN_DIR / "final-source-results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    assert result["header_matches_contract"]
    assert result["target_timestamp_absent"]
    assert result["closure_timestamp_absent"]
    assert result["stable_request_identifier_absent"]


if __name__ == "__main__":
    main()
