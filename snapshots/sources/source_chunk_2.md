# File: docs/03_architecture.md
```
# 🧱 DMForge v2 Architecture

## 📚 Layer Overview

DMForge v2 follows strict Clean Architecture principles. Each layer has a specific role, and cross-layer contamination is explicitly forbidden.

dmforge_v2/
├── domain/ # Core data structures, no logic or dependencies
├── application/ # Business rules and orchestration
├── infrastructure/ # File I/O, network calls, external libraries
├── interface/
│ └── cli/ # Typer CLI adapter only

---

## 🔒 Allowed Dependencies

| From → To           | ✅ Allowed? | 📌 Notes |
|---------------------|------------|----------|
| `interface/*` → `application` | ✅ | CLI calls services only |
| `application` → `domain`     | ✅ | Services use core types |
| `application` → `infrastructure` | ❌ | Use interfaces/ports |
| `domain` → any other layer   | ❌ | Core is pure |
| `infrastructure` → `application` | ❌ | No upward dependencies |

---

## 🔁 Dependency Rules

- CLI depends on services, **never directly on infrastructure or domain**
- Application layer only depends on **interfaces** to infrastructure
- Infrastructure implements those interfaces, but is plug-and-play
- Domain is **pure Python** — no third-party packages, no I/O

---

## 🧪 Test Rules

- `tests/domain/`: Model behavior (e.g., `SpellCard.add_art_version`)
- `tests/application/`: Service behavior, injected mocks
- `tests/infrastructure/`: Golden tests or integration-only
- `tests/interface/cli/`: CLI args → service → output, no logic tests

---

## 📂 Example Use Case: Deck Generation

| Layer | Responsibility |
|-------|----------------|
| `interface/cli/deck_build.py` | Accepts CLI args, constructs `DeckOptions`, passes to service |
| `application/deck_builder.py` | Filters spell data and builds a `Deck` |
| `infrastructure/spell_repository.py` | Loads JSON from SRD and returns spell dicts |
| `domain/models.py` | `SpellCard`, `Deck`, `DeckOptions` – with no knowledge of source or CLI |

---

## ❌ Common Violations to Guard Against

| Violation | Fix |
|----------|-----|
| CLI imports `SpellCard` directly | Define a `DeckDTO` or use services only |
| Service reads from disk | Use a `SpellRepository` interface and inject implementation |
| Domain model returns raw JSON | Use `to_dict()` or `to_json()` explicitly, no auto-serialization |
| CLI generates summaries | Extract to `DeckSummaryService` or util module |

---

## 🔧 Refactor Rule

> If logic spans layers or causes unclear ownership: **Stop. Refactor the boundary before writing more code.**
```
# File: docs/04_dev_lifecycle.md
```
# 🧪 DMForge v2 Developer Lifecycle

This file defines your **daily developer ritual** — including Git, testing, scripting, and CI guardrails.  
It is not optional. This process protects your architecture and future self.

---

## 🧬 Git Flow

### 🔀 Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Clean, protected, production-grade |
| `dev` | Integration of all features |
| `feat/*` | Feature branches (`feat/deck-builder`) |
| `fix/*` | Bugfix branches |
| `refactor/*` | Non-breaking architecture rewrites |

### 🧾 Commit Format: Conventional Commits

| Prefix | Use for |
|--------|---------|
| `feat:` | New features |
| `fix:` | Bugfixes |
| `refactor:` | Internal change, no behavior shift |
| `test:` | Adding or fixing tests |
| `docs:` | Docs only |
| `chore:` | Build scripts, tooling, config |
| `ci:` | GitHub Actions, test runners, etc. |

✅ Example:
```bash
git commit -m "feat(cli): add --interactive flag to deck build"
🛠 Scripts
scripts/end_dev.py
Your required dev exit process. Blocks low-quality commits.

bash
Copy
Edit
#!/usr/bin/env python
# End-of-session enforcement: test, format, lint, commit, push

pytest --cov --exitfirst || exit 1
black . --check || exit 1
ruff check . || exit 1

git add .
git commit -m "$1"
git push origin HEAD
scripts/test_all.py
Runs golden tests, clears temp files, ensures contract stability.

📂 Pre-Commit Hooks
Configured in .pre-commit-config.yaml:

yaml
Copy
Edit
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks: [id: black]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks: [id: ruff]

  - repo: https://github.com/pytest-dev/pytest
    rev: stable
    hooks: [id: pytest]
Run:

bash
Copy
Edit
pre-commit install
✅ Daily Dev Flow
git checkout -b feat/cli-filters

Write test first

Write clean implementation (SRP only)

Run scripts/end_dev.py "feat(cli): add class filter"

Push to dev, merge only after pass

🚨 Red Flags
Violation	Outcome
Commit with no tests	🔥 Architecture rot begins
Multiple features in one commit	❌ Revert risk, unclear ownership
Tests failing in main	🔻 Revert and rollback
Format/lint skipped	❌ CI and peer devs will break

🧠 Final Law
If a feature is not tested, documented, and gated by a commit discipline, it does not exist.
```
# File: scripts/check_templates.py
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
# File: scripts/dumb_source_split.py
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