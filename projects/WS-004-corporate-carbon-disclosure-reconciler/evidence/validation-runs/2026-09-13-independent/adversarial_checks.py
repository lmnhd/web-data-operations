from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENGINE_PATH = PROJECT_ROOT / "src" / "reconcile.py"
CASES_PATH = PROJECT_ROOT / "evidence" / "fixtures" / "disclosure_cases.json"
FACTORS_PATH = PROJECT_ROOT / "evidence" / "factors" / "ghg_factors_2025.json"

spec = importlib.util.spec_from_file_location("ws004_validator_reconcile", ENGINE_PATH)
assert spec and spec.loader
reconcile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reconcile)


def evaluate(case: dict, factors: dict) -> dict:
    cases = reconcile.load_json(CASES_PATH)
    cases["cases"] = [case]
    return reconcile.run_benchmark(
        cases,
        factors,
        factor_file_bytes=json.dumps(factors, sort_keys=True).encode("utf-8"),
        engine_file_bytes=ENGINE_PATH.read_bytes(),
    )["results"][0]


cases = reconcile.load_json(CASES_PATH)
factors = reconcile.load_json(FACTORS_PATH)
base = copy.deepcopy(cases["cases"][0])

category_conflict = copy.deepcopy(base)
category_conflict["calculation"]["activityCategory"] = "diesel"
category_result = evaluate(category_conflict, copy.deepcopy(factors))

bad_source_hash = copy.deepcopy(base)
bad_source_hash["source"]["sourceSha256"] = "not-a-sha256"
hash_result = evaluate(bad_source_hash, copy.deepcopy(factors))

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from app import app

client = app.test_client()
api_observations = {
    "cross_origin_status": client.post(
        "/api/run", json={}, headers={"Origin": "http://evil.example"}
    ).status_code,
    "unknown_file_field_status": client.post(
        "/api/run", json={"file": "../../SOURCE_CONTRACT.md"}
    ).status_code,
    "path_like_case_id_status": client.post(
        "/api/run", json={"caseId": "../../SOURCE_CONTRACT.md", "activityUnit": None}
    ).status_code,
    "get_run_status": client.get("/api/run").status_code,
}

report = {
    "activityCategoryConflict": {
        "inputActivityCategory": "diesel",
        "factorId": category_result["factorId"],
        "decision": category_result["decision"],
        "reasonCode": category_result["reasonCode"],
        "computedEmissionsTco2e": category_result["computedEmissionsTco2e"],
        "expectedBoundaryBehavior": "REVIEW_REQUIRED because the explicit activity category is incompatible with the electricity factor",
    },
    "malformedSuppliedSourceHash": {
        "inputSourceSha256": "not-a-sha256",
        "outputSourceSha256": hash_result["sourceSha256"],
        "decision": hash_result["decision"],
        "expectedBoundaryBehavior": "Reject or review a supplied source digest that is not 64 hexadecimal characters",
    },
    "apiBoundaryObservations": api_observations,
}

print(json.dumps(report, indent=2))
