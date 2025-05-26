# scripts/snapshot_split.py

"""
Generate GPT-ingestable snapshot chunks from src/, scripts/, tests/
Outputs to: snapshots/sources/source_chunk_X.md
Each chunk is context-tagged with FILE: header and Python code blocks
"""

from pathlib import Path

MAX_CHARS_PER_CHUNK = 35000  # ~10k tokens
OUTPUT_DIR = Path("snapshots/sources")
INCLUDE_DIRS = ["src", "scripts", "tests", "."]
EXCLUDE_PATTERNS = ["__pycache__", ".pytest_cache", ".venv", ".md", ".pyc"]


def should_include(path: Path) -> bool:
    return path.suffix == ".py" and not any(p in path.parts for p in EXCLUDE_PATTERNS)


def collect_files() -> list[Path]:
    all_files = []
    for base in INCLUDE_DIRS:
        root = Path(base)
        if not root.exists():
            continue
        all_files += [p for p in root.rglob("*.py") if should_include(p)]
    return sorted(all_files)


def chunk_files(files: list[Path]) -> list[str]:
    chunks = []
    current_chunk = ""
    for file in files:
        rel_path = file.as_posix()
        content = file.read_text(encoding="utf-8").strip()
        block = f"# FILE: {rel_path}\n```python\n{content}\n```\n\n"

        if len(current_chunk) + len(block) > MAX_CHARS_PER_CHUNK:
            chunks.append(current_chunk.strip())
            current_chunk = block
        else:
            current_chunk += block

    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks


def write_chunks(chunks: list[str]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for i, chunk in enumerate(chunks, 1):
        out_file = OUTPUT_DIR / f"source_chunk_{i}.md"
        out_file.write_text(chunk, encoding="utf-8")
        print(f"[OK] Wrote: {out_file}")


def write_manifest(files: list[Path]):
    manifest_path = OUTPUT_DIR.parent / "source_manifest.md"
    content = "# Source Snapshot Manifest\n\n"
    for path in files:
        rel = path.as_posix()
        content += f"- `{rel}`\n"
    manifest_path.write_text(content.strip(), encoding="utf-8")
    print(f"[OK] Wrote manifest: {manifest_path}")


def main():
    print("[RUN] Snapshot generation started")
    files = collect_files()
    chunks = chunk_files(files)
    write_chunks(chunks)
    write_manifest(files)
    print(f"[DONE] {len(chunks)} chunks written")


if __name__ == "__main__":
    main()
