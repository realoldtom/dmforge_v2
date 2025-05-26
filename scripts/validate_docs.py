# scripts/validate_docs.py

"""
Validate that all .md files in docs/ begin with a version header:
'## Version: X.Y (YYYY-MM-DD)'

Fails with nonzero exit code if any file is missing or malformed.
"""

import re
import sys
from pathlib import Path

VERSION_HEADER_REGEX = re.compile(r"^## Version:\s+\d+\.\d+( \(\d{4}-\d{2}-\d{2}\))?$")


def validate_version_header(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"[ERR] File not found: {file_path}")
        return False

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # skip empty lines
                return bool(VERSION_HEADER_REGEX.match(line.strip()))
    return False


def scan_docs_directory():
    docs_root = Path("docs")
    failures = []

    for file in docs_root.rglob("*.md"):
        if file.name.startswith("README") or "snapshots" in file.parts:
            continue  # skip README/snapshots

        if not validate_version_header(file):
            failures.append(file)

    return failures


if __name__ == "__main__":
    failed = scan_docs_directory()

    if failed:
        print("❌ Missing or invalid version headers:")
        for f in failed:
            print(f" - {f}")
        sys.exit(1)

    print("✅ All documentation files are versioned.")
