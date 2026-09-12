"""Compute the exact artifact map required by scripts/validation_gate.py."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PROJECT = ROOT / "projects/WS-003-municipal-sla-operations-explorer"
PLAN = PROJECT / "evidence/VALIDATION_PLAN.json"
OUTPUT = Path(__file__).with_name("artifact-hash-map.json")
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


def local(name: str) -> Path:
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError(f"Missing or out-of-repository artifact: {name}")
    return path


plan = json.loads(PLAN.read_text(encoding="utf-8"))
files = {local(name) for name in plan["artifactPaths"]}
ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".vercel"}
excluded = {"INDEPENDENT_VALIDATION.json", "RELEASE_CHECKLIST.md"}

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
        files.add(local(path.relative_to(ROOT).as_posix()))

artifact_map = {
    path.relative_to(ROOT).as_posix(): digest(path)
    for path in sorted(files)
}
OUTPUT.write_text(json.dumps(artifact_map, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "planSha256": digest(PLAN),
    "artifactCount": len(artifact_map),
    "artifactSha256": artifact_map,
}, indent=2))
