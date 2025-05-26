#!/usr/bin/env python

import os
from pathlib import Path

# Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "snapshots" / "sources"
INCLUDED_DIRS = {"src", "tests", "scripts", "docs"}
INCLUDED_FILES = {".py", ".toml", ".yaml", ".yml", ".md"}
EXCLUDED_NAMES = {"__pycache__", ".venv", ".git", ".mypy_cache", ".pytest_cache"}

LINES_PER_FILE = 300  # split output to keep it pasteable


def should_include(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix not in INCLUDED_FILES:
        return False
    if any(part in EXCLUDED_NAMES for part in path.parts):
        return False
    if path.parts[0] not in INCLUDED_DIRS and path.parent != PROJECT_ROOT:
        return False
    return True


def gather_files():
    files = []
    for root, _, filenames in os.walk(PROJECT_ROOT):
        for fname in filenames:
            fpath = Path(root) / fname
            if should_include(fpath.relative_to(PROJECT_ROOT)):
                files.append(fpath.relative_to(PROJECT_ROOT))
    return sorted(files)


def dump_chunks(files):
    chunks = []
    current_chunk = []
    line_count = 0

    for file in files:
        full_path = PROJECT_ROOT / file
        rel_path_str = f"# File: {file.as_posix()}"
        try:
            content_lines = full_path.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            content_lines = [f"# ERROR reading file {file}: {e}"]
        block = (
            [rel_path_str]
            + ["```python" if file.suffix == ".py" else "```"]
            + content_lines
            + ["```"]
        )

        if line_count + len(block) > LINES_PER_FILE and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            line_count = 0

        current_chunk.extend(block)
        line_count += len(block)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def write_chunks(chunks):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for i, chunk in enumerate(chunks):
        path = OUTPUT_DIR / f"source_chunk_{i+1}.md"
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(chunk))
        print(f"✅ Wrote: {path.relative_to(PROJECT_ROOT)}")


def main():
    files = gather_files()
    chunks = dump_chunks(files)
    write_chunks(chunks)


if __name__ == "__main__":
    main()
