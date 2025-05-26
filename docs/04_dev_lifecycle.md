## Version: 1.0 (2025-05-26)

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