## Version: 1.0 (2025-05-26)

# File: docs/planning/risk_log.md

# ⚠️ DMForge Risk Log (Role-Enforced)

This log captures all known risks to DMForge, now mapped to mitigation responsibility by role.  
If a risk is not actively mitigated by at least two roles, it must be reclassified as **Critical**.

---

## 🧠 Developer-Specific Risks

### DEV-1: Session Initiation Failure (ADHD paralysis)

| Description | The developer cannot initiate sessions without structure |
| Severity | High | Likelihood | High |
| Roles Mitigating |
- 👨‍💻 Senior Dev: `start_dev.py` enforces session context, previous commit echo, and roadmap phase.
- 🧠 Arch Guardian: Session structure is non-optional; session start = execution boundary.
- 📦 Doc Lead: Lifecycle policy mandates ritualized startup.

### DEV-2: Overbuilding Without Roadmap Justification

| Description | Developer begins features without scope control |
| Severity | Medium | Likelihood | High |
| Roles Mitigating |
- 🧑‍💼 Product Owner: All features must trace to roadmap and persona story.
- 📦 Doc Lead: Roadmap versions + traceability matrix required for commit acceptance.
- 👨‍💻 Senior Dev: Blocks commits that don’t include planning artifacts.

### DEV-3: GPT Uses Stale Files

| Description | AI assistant advises based on outdated local files |
| Severity | Medium | Likelihood | High |
| Roles Mitigating |
- 👨‍💻 Senior Dev: `start_dev.py` includes a GPT reload reminder.
- 🧠 Arch Guardian: Optional `gpt_sync_check.py` verifies file freshness.
- 📦 Doc Lead: Lifecycle doc mandates snapshot load confirmation before GPT interaction.

### DEV-4: Partial or Incomplete Commits

| Description | Developer commits only part of a feature/test |
| Severity | High | Likelihood | High |
| Roles Mitigating |
- 🧪 QA Engineer: `end_dev.py` fails if any test/doc/golden file is missing.
- 👨‍💻 Senior Dev: Only allows staged, scoped commits with enforced coverage.
- 🧑‍💼 Product Owner: Enforces commit discipline tied to single-scope deliverables.

---

## 🧱 Architectural Risks

### ARCH-1: CLI Touches Domain Directly

| Description | Violates Clean Architecture separation of concerns |
| Severity | Critical | Likelihood | Medium |
| Roles Mitigating |
- 🧠 Arch Guardian: `check_architecture.py` fails on cross-layer import.
- 🧪 QA Engineer: Integration tests verify all CLI routes call controllers.

### ARCH-2: Undeclared Interfaces (Missing Protocols)

| Description | Services or repositories bypass DI via implicit use |
| Severity | High | Likelihood | Medium |
| Roles Mitigating |
- 👨‍💻 Senior Dev: All services must start with a Protocol in `application.ports`.
- 🧠 Arch Guardian: `validate_contracts.py` checks implementation presence.
- 📦 Doc Lead: Contracts file (`02_contracts.md`) must reflect current interfaces.

### ARCH-3: Snapshot or Roadmap Drift

| Description | Source and documentation fall out of sync |
| Severity | Critical | Likelihood | High |
| Roles Mitigating |
- 👨‍💻 Senior Dev: `start_dev.py` and `end_dev.py` check snapshot and roadmap freshness.
- 📦 Doc Lead: Roadmap changes require saved version + planning artifact update.
- 🧠 Arch Guardian: Diff in `snapshot_split.py` halts further dev.

### ARCH-4: No Golden Output Test

| Description | Rendered output lacks regression guard |
| Severity | High | Likelihood | Medium |
| Roles Mitigating |
- 🧪 QA Engineer: All output formats must be covered by snapshot-based tests.
- 👨‍💻 Senior Dev: Commits blocked if golden tests missing or unapproved diff exists.
- 📦 Doc Lead: Test strategy explicitly ties snapshot file to CLI command.

---

## 🔧 Tooling/Process Risks

### TOOL-1: Format, Lint, and Test Steps Skipped

| Description | Dev bypasses quality tools |
| Severity | High | Likelihood | Medium |
| Roles Mitigating |
- 👨‍💻 Senior Dev: `end_dev.py` runs `black`, `ruff`, `pytest` before commit.
- 🧪 QA Engineer: Fail builds where lint or test coverage not present.
- 📦 Doc Lead: Lifecycle document lists formatting and linting as mandatory.

### TOOL-2: WeasyPrint or Pydyf Version Drift

| Description | Breaks rendering pipeline without warning |
| Severity | Medium | Likelihood | Medium |
| Roles Mitigating |
- 🧠 Arch Guardian: `validate_env.py` aborts if bad versions are found.
- 👨‍💻 Senior Dev: Versions locked in `pyproject.toml`.
- 📦 Doc Lead: Requirements explained in compatibility section of architecture doc.

### TOOL-3: CLI Usage Mismatch with Documentation

| Description | `05_usage.md` doesn't match `--help` output |
| Severity | Medium | Likelihood | Medium |
| Roles Mitigating |
- 📦 Doc Lead: `update_docs.py` regenerates usage from Typer CLI.
- 🧪 QA Engineer: Test output of `--help` against golden snapshot.
- 👨‍💻 Senior Dev: `end_dev.py` fails if CLI doc is stale.

---

> If a risk lacks at least two enforcers — you’ve built in your own failure.
