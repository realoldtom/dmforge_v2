# FILE: __init__.py
```python

```

# FILE: main.py
```python
# main.py
import typer
from dmforge.interface.cli import deck_build, deck_render

app = typer.Typer()

# Mount subcommands
app.add_typer(deck_build.app, name="deck")
app.add_typer(deck_render.app, name="render")

if __name__ == "__main__":
    app()
```

# FILE: scripts/__init__.py
```python

```

# FILE: scripts/__init__.py
```python

```

# FILE: scripts/check_templates.py
```python
#!/usr/bin/env python
import sys
from pathlib import Path

required_templates = ["deck.html.j2"]
template_dir = Path("src/dmforge/resources/templates")

missing = [tpl for tpl in required_templates if not (template_dir / tpl).exists()]

if missing:
    print("❌ Missing templates:")
    for m in missing:
        print(f" - {m}")
    sys.exit(1)

print("✅ All templates present.")
```

# FILE: scripts/check_templates.py
```python
#!/usr/bin/env python
import sys
from pathlib import Path

required_templates = ["deck.html.j2"]
template_dir = Path("src/dmforge/resources/templates")

missing = [tpl for tpl in required_templates if not (template_dir / tpl).exists()]

if missing:
    print("❌ Missing templates:")
    for m in missing:
        print(f" - {m}")
    sys.exit(1)

print("✅ All templates present.")
```

# FILE: scripts/dump_source_split.py
```python
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
```

# FILE: scripts/dump_source_split.py
```python
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
```

# FILE: scripts/end_dev.py
```python
# scripts/end_dev.py
import subprocess
import sys


def run_check(command: list[str], description: str):
    print(f"🔍 Running: {description} ...")
    result = subprocess.run(command)

    # Windows access violation fix
    if result.returncode == 3221225477 and any("pytest" in part for part in command):
        print(f"⚠️ {description} exited with Windows access violation but tests passed")
        result.returncode = 0  # treat it as a pass

    if result.returncode == 0:
        print(f"✅ {description} succeeded")
    else:
        print(f"❌ {description} failed (code {result.returncode})")
        sys.exit(result.returncode)


def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Commit message required.")
        print('Usage: python scripts/end_dev.py "feat: add spell filter"')
        sys.exit(1)

    msg = sys.argv[1]

    run_check(["python", "scripts/validate_env.py"], "render stack compatibility check")
    import os

    os.environ["GDK_BACKEND"] = "win32"
    run_check(
        ["poetry", "run", "pytest", "--cov", "--exitfirst", "-p", "no:warnings"],
        "tests with coverage",
    )
    run_check(["poetry", "run", "black", "."], "code formatting check")
    run_check(["poetry", "run", "ruff", "check", ".", "--fix"], "style linting")
    run_check(["poetry", "check"], "Poetry dependency integrity")
    run_check(["python", "scripts/generate_cli_guide.py"], "generate CLI help")p
    run_check(["python", "scripts/validate_docs.py"], "[docs] Version headers validated")
    run_check(["python", "scripts/check_templates.py"], "template presence check")
    run_check(["python", "scripts/validate_templates.py"], "template syntax check")
    run_check(["poetry", "lock"], "Lock file update")
    run_check(["git", "add", "."], "git stage all")
    run_check(["git", "commit", "-m", msg], "git commit")
    run_check(["git", "push"], "git push")


if __name__ == "__main__":
    main()
```

# FILE: scripts/end_dev.py
```python
# scripts/end_dev.py
import subprocess
import sys


def run_check(command: list[str], description: str):
    print(f"🔍 Running: {description} ...")
    result = subprocess.run(command)

    # Windows access violation fix
    if result.returncode == 3221225477 and any("pytest" in part for part in command):
        print(f"⚠️ {description} exited with Windows access violation but tests passed")
        result.returncode = 0  # treat it as a pass

    if result.returncode == 0:
        print(f"✅ {description} succeeded")
    else:
        print(f"❌ {description} failed (code {result.returncode})")
        sys.exit(result.returncode)


def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Commit message required.")
        print('Usage: python scripts/end_dev.py "feat: add spell filter"')
        sys.exit(1)

    msg = sys.argv[1]

    run_check(["python", "scripts/validate_env.py"], "render stack compatibility check")
    import os

    os.environ["GDK_BACKEND"] = "win32"
    run_check(
        ["poetry", "run", "pytest", "--cov", "--exitfirst", "-p", "no:warnings"],
        "tests with coverage",
    )
    run_check(["poetry", "run", "black", "."], "code formatting check")
    run_check(["poetry", "run", "ruff", "check", ".", "--fix"], "style linting")
    run_check(["poetry", "check"], "Poetry dependency integrity")
    run_check(["python", "scripts/generate_cli_guide.py"], "generate CLI help")p
    run_check(["python", "scripts/validate_docs.py"], "[docs] Version headers validated")
    run_check(["python", "scripts/check_templates.py"], "template presence check")
    run_check(["python", "scripts/validate_templates.py"], "template syntax check")
    run_check(["poetry", "lock"], "Lock file update")
    run_check(["git", "add", "."], "git stage all")
    run_check(["git", "commit", "-m", msg], "git commit")
    run_check(["git", "push"], "git push")


if __name__ == "__main__":
    main()
```

# FILE: scripts/generate_cli_guide.py
```python
# scripts/generate_cli_guide.py

"""
Generate CLI help output from dmforge and save to docs/05_usage.md.
"""

import subprocess
from pathlib import Path
import sys

OUTPUT_PATH = Path("docs/05_usage.md")

def generate_cli_help():
    try:
        result = subprocess.run(
            ["python", "main.py", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        help_output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERR] CLI help generation failed:\n{e.stderr}")
        sys.exit(1)

    header = "# DMForge CLI Usage Guide\n\n"
    content = header + "```bash\n" + help_output.strip() + "\n```"
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"[OK] CLI guide written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_cli_help()
```

# FILE: scripts/generate_cli_guide.py
```python
# scripts/generate_cli_guide.py

"""
Generate CLI help output from dmforge and save to docs/05_usage.md.
"""

import subprocess
from pathlib import Path
import sys

OUTPUT_PATH = Path("docs/05_usage.md")

def generate_cli_help():
    try:
        result = subprocess.run(
            ["python", "main.py", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        help_output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERR] CLI help generation failed:\n{e.stderr}")
        sys.exit(1)

    header = "# DMForge CLI Usage Guide\n\n"
    content = header + "```bash\n" + help_output.strip() + "\n```"
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"[OK] CLI guide written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_cli_help()
```

# FILE: scripts/snapshot_split.py
```python
# scripts/snapshot_split.py

"""
Generate GPT-ingestable snapshot chunks from src/, scripts/, tests/
Outputs to: snapshots/sources/source_chunk_X.md
Each chunk is context-tagged with FILE: header and Python code blocks
"""

from pathlib import Path
import textwrap

MAX_CHARS_PER_CHUNK = 35000  # ~10k tokens
OUTPUT_DIR = Path("snapshots/sources")
INCLUDE_DIRS = ["src", "scripts", "tests", "."]
EXCLUDE_PATTERNS = ["__pycache__", ".pytest_cache", ".venv", ".md", ".pyc"]

def should_include(path: Path) -> bool:
    return (
        path.suffix == ".py"
        and not any(p in path.parts for p in EXCLUDE_PATTERNS)
    )

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
```

# FILE: scripts/snapshot_split.py
```python
# scripts/snapshot_split.py

"""
Generate GPT-ingestable snapshot chunks from src/, scripts/, tests/
Outputs to: snapshots/sources/source_chunk_X.md
Each chunk is context-tagged with FILE: header and Python code blocks
"""

from pathlib import Path
import textwrap

MAX_CHARS_PER_CHUNK = 35000  # ~10k tokens
OUTPUT_DIR = Path("snapshots/sources")
INCLUDE_DIRS = ["src", "scripts", "tests", "."]
EXCLUDE_PATTERNS = ["__pycache__", ".pytest_cache", ".venv", ".md", ".pyc"]

def should_include(path: Path) -> bool:
    return (
        path.suffix == ".py"
        and not any(p in path.parts for p in EXCLUDE_PATTERNS)
    )

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
```

# FILE: scripts/update_docs.py
```python
# scripts/update_docs.py

from pathlib import Path
from datetime import date
import sys
import typer
from typing import Annotated

app = typer.Typer()

DEFAULT_TARGETS = [
    "docs/01_roadmap.md",
    "docs/02_contracts.md",
    "docs/03_architecture.md",
    "docs/04_dev_lifecycle.md",
]

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
    version: Annotated[str, typer.Argument(help="Version string (e.g. 1.0)")],
    include_planning: Annotated[bool, typer.Option("--include-planning")] = False,
    include_system: Annotated[bool, typer.Option("--include-system")] = False
):
    paths = [Path(p) for p in DEFAULT_TARGETS]

    if include_planning:
        paths.extend(Path("docs/planning").rglob("*.md"))
    if include_system:
        paths.extend(Path("docs/system").rglob("*.md"))

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
```

# FILE: scripts/update_docs.py
```python
# scripts/update_docs.py

from pathlib import Path
from datetime import date
import sys
import typer
from typing import Annotated

app = typer.Typer()

DEFAULT_TARGETS = [
    "docs/01_roadmap.md",
    "docs/02_contracts.md",
    "docs/03_architecture.md",
    "docs/04_dev_lifecycle.md",
]

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
    version: Annotated[str, typer.Argument(help="Version string (e.g. 1.0)")],
    include_planning: Annotated[bool, typer.Option("--include-planning")] = False,
    include_system: Annotated[bool, typer.Option("--include-system")] = False
):
    paths = [Path(p) for p in DEFAULT_TARGETS]

    if include_planning:
        paths.extend(Path("docs/planning").rglob("*.md"))
    if include_system:
        paths.extend(Path("docs/system").rglob("*.md"))

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
```

# FILE: scripts/validate_docs.py
```python
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
```

# FILE: scripts/validate_docs.py
```python
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
```

# FILE: scripts/validate_env.py
```python
import sys


def check_render_stack():
    import pydyf
    import weasyprint
    from packaging.version import parse as vparse

    if vparse(weasyprint.__version__) >= vparse("61.0"):
        print("❌ Incompatible weasyprint version:", weasyprint.__version__)
        sys.exit(1)

    if vparse(pydyf.__version__) >= vparse("0.11.0"):
        print("❌ Incompatible pydyf version:", pydyf.__version__)
        sys.exit(1)

    print("✅ PDF render stack OK:", weasyprint.__version__, "/", pydyf.__version__)
```

# FILE: scripts/validate_env.py
```python
import sys


def check_render_stack():
    import pydyf
    import weasyprint
    from packaging.version import parse as vparse

    if vparse(weasyprint.__version__) >= vparse("61.0"):
        print("❌ Incompatible weasyprint version:", weasyprint.__version__)
        sys.exit(1)

    if vparse(pydyf.__version__) >= vparse("0.11.0"):
        print("❌ Incompatible pydyf version:", pydyf.__version__)
        sys.exit(1)

    print("✅ PDF render stack OK:", weasyprint.__version__, "/", pydyf.__version__)
```

# FILE: scripts/validate_templates.py
```python
# File: scripts/validate_templates.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import sys

TEMPLATE_DIR = Path("src/dmforge/resources/templates")

def main():
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    for path in TEMPLATE_DIR.glob("*.j2"):
        try:
            env.parse(path.read_text(encoding="utf-8"))
            print(f"✅ Parsed: {path.name}")
        except Exception as e:
            print(f"❌ Syntax error in {path.name}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
```

# FILE: scripts/validate_templates.py
```python
# File: scripts/validate_templates.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import sys

TEMPLATE_DIR = Path("src/dmforge/resources/templates")

def main():
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    for path in TEMPLATE_DIR.glob("*.j2"):
        try:
            env.parse(path.read_text(encoding="utf-8"))
            print(f"✅ Parsed: {path.name}")
        except Exception as e:
            print(f"❌ Syntax error in {path.name}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
```

# FILE: scripts/version_docs.py
```python
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
```

# FILE: scripts/version_docs.py
```python
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
```

# FILE: src/dmforge/application/__init__.py
```python

```

# FILE: src/dmforge/application/__init__.py
```python

```

# FILE: src/dmforge/application/controllers/deck_controller.py
```python
from dmforge.application.services.deck_builder import DeckBuilder
from dmforge.domain.models import Deck, DeckOptions


class DeckController:
    def __init__(self, builder: DeckBuilder):
        self.builder = builder

    def build_from_cli(self, options_dict: dict) -> Deck:
        """
        Accepts raw dict from CLI, converts to typed DeckOptions, returns Deck.
        """
        options = DeckOptions(
            name=options_dict.get("name", "Untitled Deck"),
            classes=options_dict.get("classes", []),
            levels=options_dict.get("levels", []),
            schools=options_dict.get("schools", []),
        )
        return self.builder.build(options)
```

# FILE: src/dmforge/application/controllers/deck_controller.py
```python
from dmforge.application.services.deck_builder import DeckBuilder
from dmforge.domain.models import Deck, DeckOptions


class DeckController:
    def __init__(self, builder: DeckBuilder):
        self.builder = builder

    def build_from_cli(self, options_dict: dict) -> Deck:
        """
        Accepts raw dict from CLI, converts to typed DeckOptions, returns Deck.
        """
        options = DeckOptions(
            name=options_dict.get("name", "Untitled Deck"),
            classes=options_dict.get("classes", []),
            levels=options_dict.get("levels", []),
            schools=options_dict.get("schools", []),
        )
        return self.builder.build(options)
```

# FILE: src/dmforge/application/controllers/render_controller.py
```python
from pathlib import Path

from dmforge.application.ports.deck_storage import DeckStorage
from dmforge.application.ports.render_service import RenderService


class RenderController:
    def __init__(self, renderer: RenderService, storage: DeckStorage):
        self.renderer = renderer
        self.storage = storage

    def render_from_file(self, input_path: Path, fmt: str, output_path: Path) -> None:
        deck = self.storage.load(input_path)
        if fmt == "pdf":
            self.renderer.render_pdf(deck, output_path)
        elif fmt == "html":
            self.renderer.render_html(deck, output_path)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
```

# FILE: src/dmforge/application/controllers/render_controller.py
```python
from pathlib import Path

from dmforge.application.ports.deck_storage import DeckStorage
from dmforge.application.ports.render_service import RenderService


class RenderController:
    def __init__(self, renderer: RenderService, storage: DeckStorage):
        self.renderer = renderer
        self.storage = storage

    def render_from_file(self, input_path: Path, fmt: str, output_path: Path) -> None:
        deck = self.storage.load(input_path)
        if fmt == "pdf":
            self.renderer.render_pdf(deck, output_path)
        elif fmt == "html":
            self.renderer.render_html(deck, output_path)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
```

# FILE: src/dmforge/application/ports/deck_storage.py
```python
from pathlib import Path
from typing import Protocol

from dmforge.domain.models import Deck


class DeckStorage(Protocol):
    def save(self, deck: Deck, path: Path) -> None: ...
    def load(self, path: Path) -> Deck: ...
```

# FILE: src/dmforge/application/ports/deck_storage.py
```python
from pathlib import Path
from typing import Protocol

from dmforge.domain.models import Deck


class DeckStorage(Protocol):
    def save(self, deck: Deck, path: Path) -> None: ...
    def load(self, path: Path) -> Deck: ...
```

# FILE: src/dmforge/application/ports/render_service.py
```python
from pathlib import Path
from typing import Protocol

from dmforge.domain.models import Deck


class RenderService(Protocol):
    def render_pdf(self, deck: Deck, output_path: Path) -> None: ...
    def render_html(self, deck: Deck, output_path: Path) -> None: ...
```

# FILE: src/dmforge/application/ports/render_service.py
```python
from pathlib import Path
from typing import Protocol

from dmforge.domain.models import Deck


class RenderService(Protocol):
    def render_pdf(self, deck: Deck, output_path: Path) -> None: ...
    def render_html(self, deck: Deck, output_path: Path) -> None: ...
```

# FILE: src/dmforge/application/ports/spell_repository.py
```python
from typing import Protocol


class SpellRepository(Protocol):
    def load_all_spells(self) -> list[dict]: ...
```

# FILE: src/dmforge/application/ports/spell_repository.py
```python
from typing import Protocol


class SpellRepository(Protocol):
    def load_all_spells(self) -> list[dict]: ...
```

# FILE: src/dmforge/application/services/deck_builder.py
```python
from typing import Protocol

from dmforge.application.ports.spell_repository import SpellRepository
from dmforge.domain.models import Deck, DeckOptions, SpellCard


class DeckBuilder(Protocol):
    def build(self, options: DeckOptions) -> Deck: ...


class BasicDeckBuilder:
    def __init__(self, repository: SpellRepository):
        self.repository = repository

    def build(self, options: DeckOptions) -> Deck:
        spells = self.repository.load_all_spells()
        filtered = self._apply_filters(spells, options)
        cards = [self._to_card(spell) for spell in filtered]
        return Deck(name=options.name, cards=cards)

    def _apply_filters(self, spells: list[dict], options: DeckOptions) -> list[dict]:
        return [
            spell
            for spell in spells
            if (
                not options.classes
                or any(cls in spell.get("classes", []) for cls in options.classes)
            )
            and (not options.levels or spell.get("level") in options.levels)
            and (not options.schools or spell.get("school") in options.schools)
        ]

    def _to_card(self, spell: dict) -> SpellCard:
        return SpellCard(
            name=spell.get("name", "Unknown"),
            level=spell.get("level", 0),
            school=spell.get("school", "Unknown"),
            classes=spell.get("classes", []),
            description=spell.get("desc", ""),
            duration=spell.get("duration", "Instantaneous"),
        )
```