from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
PROJECT = ROOT / "projects" / "WS-003-municipal-sla-operations-explorer"
RUN_DIR = Path(__file__).resolve().parent
PLAN_PATH = PROJECT / "evidence/VALIDATION_PLAN.json"
TEXT_SUFFIXES = {".cfg", ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".gitignore", ".vercelignore"}


def digest(path: Path) -> str:
    content = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
        content = content.replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def local(name: str) -> Path:
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError(f"Missing or out-of-repository artifact: {name}")
    return path


def main() -> None:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    files = {local(name) for name in plan["artifactPaths"]}
    excluded = {"INDEPENDENT_VALIDATION.json", "RELEASE_CHECKLIST.md"}
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".vercel"}
    for path in PROJECT.rglob("*"):
        rel = path.relative_to(PROJECT)
        if any(part in ignored for part in rel.parts):
            continue
        if path.name == ".env.local" or (path.name.startswith(".env.") and path.name.endswith(".local")):
            continue
        if rel.as_posix() in {"evidence/" + name for name in excluded} or rel.parts[:2] == ("evidence", "validation-runs"):
            continue
        if path.is_file():
            files.add(local(path.relative_to(ROOT).as_posix()))

    artifacts = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(files)}
    evidence_files = [
        "final-check-automated-tests.txt",
        "final-check-benchmark.txt",
        "final-check-edge-cases.txt",
        "final-check-exports.txt",
        "final-check-pdf-visual.txt",
        "final-check-ward-claims.txt",
        "final-check-privacy-boundary.txt",
        "final-adversarial-findings.txt",
        "final-adversarial-results.json",
        "final-production-results.json",
        "final-source-results.json",
        "final-export.json",
        "final-export.csv",
    ]
    evidence = {name: digest(RUN_DIR / name) for name in evidence_files}
    output = {
        "planSha256": digest(PLAN_PATH),
        "artifactCount": len(artifacts),
        "artifactSha256": artifacts,
        "evidenceSha256": evidence,
    }
    (RUN_DIR / "final-hash-map.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
