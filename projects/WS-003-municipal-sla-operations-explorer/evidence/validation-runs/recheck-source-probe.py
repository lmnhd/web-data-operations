"""Verify the live official Toronto 2026 schema boundary for WS-003."""

from __future__ import annotations

import csv
import io
import json
import urllib.request
import zipfile


PACKAGE = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=311-service-requests-customer-initiated"
RESOURCE_ID = "99b7f283-7345-4f5a-a126-d078ed4f3419"
EXPECTED = [
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


with urllib.request.urlopen(PACKAGE, timeout=30) as response:
    package = json.load(response)["result"]
resource = next(item for item in package["resources"] if item["id"] == RESOURCE_ID)
with urllib.request.urlopen(resource["url"], timeout=60) as response:
    payload = response.read()
with zipfile.ZipFile(io.BytesIO(payload)) as archive:
    csv_name = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
    with archive.open(csv_name) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        header = next(csv.reader(text))

print("resource_id", resource["id"])
print("resource_last_modified", resource.get("last_modified"))
print("download_bytes", len(payload))
print("csv_name", csv_name)
print("header", json.dumps(header))
print("target_timestamp_absent", not any("target" in name.lower() for name in header))
print("closure_timestamp_absent", not any("clos" in name.lower() for name in header))
assert header == EXPECTED
assert not any("target" in name.lower() for name in header)
assert not any("clos" in name.lower() for name in header)
print("OFFICIAL_SOURCE_BOUNDARY_PASS")
