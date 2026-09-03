"""Validate the reviewer-facing portfolio archive without external packages."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT_FILES = (
    "README.md",
    "PORTFOLIO_TRACKING_LOG.md",
    "PROJECT_MANIFEST_TEMPLATE.md",
    "SOURCE_CONTROL_AND_PUBLIC_ARCHIVE.md",
)


def validate_root() -> list[str]:
    return [f"Missing required root file: {name}" for name in REQUIRED_ROOT_FILES if not (ROOT / name).is_file()]


def validate_projects() -> list[str]:
    errors: list[str] = []
    projects_dir = ROOT / "projects"
    if not projects_dir.is_dir():
        return ["Missing projects directory"]

    for project_dir in sorted(path for path in projects_dir.iterdir() if path.is_dir()):
        for required in ("README.md", "PROJECT_MANIFEST.md"):
            if not (project_dir / required).is_file():
                errors.append(f"{project_dir.relative_to(ROOT)} is missing {required}")

        manifest = project_dir / "PROJECT_MANIFEST.md"
        if manifest.is_file() and "Status: RELEASED" in manifest.read_text(encoding="utf-8"):
            if "TBD" in manifest.read_text(encoding="utf-8"):
                errors.append(f"Released manifest contains TBD fields: {manifest.relative_to(ROOT)}")

    return errors


def main() -> int:
    errors = validate_root() + validate_projects()
    if errors:
        print("Archive validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Archive structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
