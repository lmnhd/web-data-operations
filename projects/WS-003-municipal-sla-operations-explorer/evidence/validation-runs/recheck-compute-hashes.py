"""Print canonical validation-gate hashes for WS-003 independent recheck."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "projects/WS-003-municipal-sla-operations-explorer"
PLAN = PROJECT / "evidence/VALIDATION_PLAN.json"
TEXT_SUFFIXES = {
    ".cfg", ".css", ".csv", ".html", ".ini", ".js", ".json", ".md",
    ".py", ".toml", ".txt", ".yaml", ".yml",
}
TEXT_NAMES = {".gitignore", ".vercelignore"}


def digest(path: Path) -> str:
    content = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
        content = content.replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


plan = json.loads(PLAN.read_text(encoding="utf-8"))
files = {(ROOT / name).resolve() for name in plan["artifactPaths"]}
excluded = {"INDEPENDENT_VALIDATION.json", "RELEASE_CHECKLIST.md"}
ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".vercel"}
for path in PROJECT.rglob("*"):
    rel = path.relative_to(PROJECT)
    if any(part in ignored for part in rel.parts):
        continue
    if path.name == ".env.local" or (path.name.startswith(".env.") and path.name.endswith(".local")):
        continue
    if rel.as_posix() in {"evidence/" + name for name in excluded}:
        continue
    if rel.parts[:2] == ("evidence", "validation-runs"):
        continue
    if path.is_file():
        files.add(path.resolve())

artifacts = {
    path.relative_to(ROOT).as_posix(): digest(path)
    for path in sorted(files)
}
evidence = {
    path.relative_to(ROOT).as_posix(): digest(path)
    for path in sorted((PROJECT / "evidence/validation-runs").glob("recheck-*.txt"))
}
print(json.dumps({"planSha256": digest(PLAN), "artifactSha256": artifacts, "evidenceSha256": evidence}, indent=2))
