#!/usr/bin/env python

import os
from pathlib import Path

# Set project root (assumes script is in dmforge_v2/scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Folders to exclude from snapshot
EXCLUDED_DIRS = {
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".git",
    "dist",
    "build",
    ".idea",
    ".vscode",
    ".ruff_cache",
}
EXCLUDED_FILES = {".DS_Store"}

# File extensions to include
INCLUDE_EXTENSIONS = {".py", ".toml", ".yaml", ".yml", ".md"}

# Output file (or print to console)
OUTPUT_FILE = PROJECT_ROOT / "snapshot.txt"


def should_include(path: Path) -> bool:
    if path.name in EXCLUDED_FILES:
        return False
    if path.suffix not in INCLUDE_EXTENSIONS:
        return False
    parts = set(path.parts)
    return not parts.intersection(EXCLUDED_DIRS)


def main():
    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for root, _, files in os.walk(PROJECT_ROOT):
            root_path = Path(root)
            # Skip excluded dirs
            if any(part in EXCLUDED_DIRS for part in root_path.parts):
                continue

            included_files = [f for f in files if should_include(root_path / f)]
            if included_files:
                rel_root = root_path.relative_to(PROJECT_ROOT)
                out.write(f"# {rel_root}/\n")
                for file in sorted(included_files):
                    out.write(f"- {file}\n")
                out.write("\n")
    print(f"📄 Snapshot written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
