# scripts/version_docs.py

import sys
from datetime import date
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


def _insert_version_header(doc_path: Path, version: str):
    if not doc_path.exists():
        raise FileNotFoundError(f"File not found: {doc_path}")

    content = doc_path.read_text(encoding="utf-8")
    if content.strip().startswith("## Version:"):
        raise ValueError("Document already contains a version header.")

    header = f"## Version: {version} ({date.today().isoformat()})\n"
    new_content = header + "\n" + content
    doc_path.write_text(new_content, encoding="utf-8")


@app.command()
def version(
    path: Annotated[Path, typer.Argument(help="Path to markdown file")],
    version: Annotated[str, typer.Argument(help="Version string")],
):
    try:
        _insert_version_header(path, version)
        print(f"[OK] Versioned: {path}")
    except Exception as e:
        print(f"[ERR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
