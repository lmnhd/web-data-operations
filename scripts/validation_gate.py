"""Fail-closed evidence gate; checks attestations, not agent identity authentication."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"tests", "demo", "edge_case", "exports", "pdf_visual", "claims", "boundaries"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing or out-of-repository evidence: {name}")
    return path


def check(state, root=ROOT):
    if not isinstance(state, dict) or not isinstance(state.get("stage"), str):
        return ["Independent validation gate: invalid state object or stage"]
    if state.get("stage") not in {"RELEASE_READY", "RELEASED", "ARCHIVED"}:
        return []
    # Rejected experiments can be archived without pretending they were released.
    if state.get("stage") == "ARCHIVED" and state.get("archivedFrom") == "REJECTED":
        return []
    # Historical release predates this gate; never fabricate retrospective review.
    if state.get("iterationId") == "WS-001":
        return []
    try:
        iteration = state["iterationId"]
        if not re.fullmatch(r"WS-\d{3,}", iteration):
            raise ValueError("Invalid iteration ID")
        projects = list((root / "projects").glob(iteration + "-*"))
        if len(projects) != 1:
            raise ValueError("Expected exactly one iteration project")
        project = projects[0]
        plan_path = project / "evidence/VALIDATION_PLAN.json"
        report_path = project / "evidence/INDEPENDENT_VALIDATION.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if plan.get("iterationId") != iteration or report.get("iterationId") != iteration:
            raise ValueError("Validation iteration mismatch")
        builders = plan.get("builderAgentIds", [])
        reviewer = report.get("validatorAgentId")
        if not builders or not all(isinstance(x, str) and x.strip() for x in builders):
            raise ValueError("Builder agent IDs are required")
        if not isinstance(reviewer, str) or not reviewer.strip() or reviewer in builders:
            raise ValueError("Validator must be a different agent from every builder")
        if report.get("verdict") != "PASS" or report.get("unresolvedFindings") != []:
            raise ValueError("Independent validation has not passed without unresolved findings")
        if report.get("planSha256") != digest(plan_path):
            raise ValueError("Validation plan changed after review")
        paths = plan.get("artifactPaths", [])
        if not paths or len(set(paths)) != len(paths):
            raise ValueError("Declare unique reviewer artifacts in the validation plan")
        artifacts = [local(root, name) for name in paths]
        if not any(p.suffix.lower() == ".pdf" for p in artifacts):
            raise ValueError("Validation must cover the final PDF")
        # Hash every project file except generated caches and review-owned outputs.
        excluded = {"INDEPENDENT_VALIDATION.json", "RELEASE_CHECKLIST.md"}
        ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".vercel"}
        files = set(artifacts)
        for path in project.rglob("*"):
            rel = path.relative_to(project)
            if any(part in ignored for part in rel.parts):
                continue
            # Hosting CLIs can materialize ignored, machine-local credentials.
            # They are neither portable review artifacts nor safe report content.
            if path.name == ".env.local" or (path.name.startswith(".env.") and path.name.endswith(".local")):
                continue
            if rel.as_posix() in {"evidence/" + name for name in excluded} or rel.parts[:2] == ("evidence", "validation-runs"):
                continue
            if path.is_file():
                files.add(local(root, path.relative_to(root).as_posix()))
        current = {p.relative_to(root).as_posix(): digest(p) for p in sorted(files)}
        if report.get("artifactSha256") != current:
            raise ValueError("Reviewed files changed, were added/removed, or coverage is incomplete; revalidate")
        checks = plan.get("checks", [])
        if {c.get("category") for c in checks} != CATEGORIES:
            raise ValueError("Plan must cover tests, demo, edge_case, exports, pdf_visual, claims and boundaries")
        ids = [c["id"] for c in checks]
        if len(set(ids)) != len(ids) or not all(ids):
            raise ValueError("Validation check IDs must be unique and nonempty")
        if not all(isinstance(c.get(k), str) and c[k].strip() for c in checks for k in ("procedure", "expected", "id")):
            raise ValueError("Each check needs a predefined procedure and expected result")
        results = report.get("checks", [])
        if len(results) != len(ids) or {r.get("id") for r in results} != set(ids):
            raise ValueError("Every predefined check needs exactly one result")
        for result in results:
            if result.get("status") != "PASS" or not isinstance(result.get("observed"), str) or not result["observed"].strip():
                raise ValueError("All checks must pass with observed results")
            evidence = local(root, result["evidencePath"])
            if evidence.stat().st_size == 0 or result.get("evidenceSha256") != digest(evidence):
                raise ValueError("Missing, empty or changed validation evidence")
        return []
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        return [f"Independent validation gate: {error}"]


if __name__ == "__main__":
    state = json.loads((ROOT / "ACTIVE_ITERATION.json").read_text(encoding="utf-8"))
    errors = check(state)
    print("\n".join(errors) if errors else "Independent validation gate passed (or not yet at release stage).")
    raise SystemExit(bool(errors))
