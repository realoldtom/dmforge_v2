# scripts/update_docs.py

import sys
from datetime import date
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


def _has_header(path: Path) -> bool:
    return path.read_text(encoding="utf-8").strip().startswith("## Version:")


def _inject(path: Path, version: str):
    if not path.exists():
        raise FileNotFoundError(path)

    if _has_header(path):
        raise ValueError(f"{path} already versioned.")

    header = f"## Version: {version} ({date.today().isoformat()})\n"
    contents = path.read_text(encoding="utf-8")
    path.write_text(header + "\n" + contents, encoding="utf-8")


@app.command()
def main(
    version: Annotated[str, typer.Argument(help="Version string (e.g. 1.1)")],
):
    docs_root = Path("docs")
    paths = [p for p in docs_root.rglob("*.md") if "snapshots" not in p.parts]

    failed = []
    for path in paths:
        try:
            _inject(path, version)
            print(f"[OK] {path}")
        except ValueError:
            print(f"[SKIP] {path} already versioned.")
        except Exception as e:
            print(f"[ERR] {path}: {e}")
            failed.append(path)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    app()
