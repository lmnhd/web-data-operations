from __future__ import annotations

import copy
import csv
import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENGINE_PATH = PROJECT_ROOT / "src" / "reconcile.py"
CASES_PATH = PROJECT_ROOT / "evidence" / "fixtures" / "disclosure_cases.json"
FACTORS_PATH = PROJECT_ROOT / "evidence" / "factors" / "ghg_factors_2025.json"

spec = importlib.util.spec_from_file_location("ws004_recheck_reconcile", ENGINE_PATH)
assert spec and spec.loader
reconcile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reconcile)

cases = reconcile.load_json(CASES_PATH)
factors = reconcile.load_json(FACTORS_PATH)
factor_bytes = FACTORS_PATH.read_bytes()
engine_bytes = ENGINE_PATH.read_bytes()


def one_case(case: dict) -> dict:
    document = copy.deepcopy(cases)
    document["cases"] = [case]
    return reconcile.run_benchmark(
        document,
        factors,
        factor_file_bytes=factor_bytes,
        engine_file_bytes=engine_bytes,
    )["results"][0]


category_case = copy.deepcopy(cases["cases"][0])
category_case["calculation"]["activityCategory"] = "diesel"
category_result = one_case(category_case)

malformed_case = copy.deepcopy(cases["cases"][0])
malformed_case["source"]["sourceSha256"] = "not-a-sha256"
try:
    one_case(malformed_case)
except reconcile.EvidenceBoundaryError as error:
    malformed_engine = {"rejected": True, "error": str(error)}
else:
    malformed_engine = {"rejected": False, "error": None}

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from app import app
import demo_server

client = app.test_client()

category_document = copy.deepcopy(demo_server.load_cases())
category_document["cases"][0]["calculation"]["activityCategory"] = "diesel"
category_document["cases"] = [category_document["cases"][0]]
with patch("demo_server.load_cases", return_value=category_document):
    category_response = client.post(
        "/api/run",
        json={"caseId": category_document["cases"][0]["caseId"], "activityUnit": None},
        headers={"Origin": "http://localhost"},
    )

malformed_document = copy.deepcopy(demo_server.load_cases())
malformed_document["cases"][0]["source"]["sourceSha256"] = "not-a-sha256"
malformed_document["cases"] = [malformed_document["cases"][0]]
with patch("demo_server.load_cases", return_value=malformed_document):
    malformed_response = client.post(
        "/api/run",
        json={"caseId": malformed_document["cases"][0]["caseId"], "activityUnit": None},
        headers={"Origin": "http://localhost"},
    )

default_response = client.post(
    "/api/run",
    json={"caseId": None, "activityUnit": None},
    headers={"Origin": "http://localhost"},
)
default_payload = default_response.get_json()
web_csv = list(csv.DictReader(io.StringIO(default_payload["csv"])))

report = {
    "engineActivityCategoryConflict": {
        "decision": category_result["decision"],
        "reasonCode": category_result["reasonCode"],
        "computedEmissionsTco2e": category_result["computedEmissionsTco2e"],
    },
    "apiActivityCategoryConflict": {
        "status": category_response.status_code,
        "decision": category_response.get_json()["results"][0]["decision"],
        "reasonCode": category_response.get_json()["results"][0]["reasonCode"],
        "computedEmissionsTco2e": category_response.get_json()["results"][0]["computedEmissionsTco2e"],
    },
    "engineMalformedSourceSha256": malformed_engine,
    "apiMalformedSourceSha256": {
        "status": malformed_response.status_code,
        "error": malformed_response.get_json()["error"],
    },
    "webCsvRunIdentity": {
        "status": default_response.status_code,
        "jsonRunId": default_payload["runId"],
        "csvRunIds": sorted({row["runId"] for row in web_csv}),
        "rowCount": len(web_csv),
    },
}

print(json.dumps(report, indent=2))
