# File: docs/planning/feature_DEV_SUPPORT_AUTOMATION.md

# 🧭 Feature Planning: Developer Session Automation

## 🎯 Feature Name: Developer Session Automation

### 📦 Scope
Automate session start/end to enforce architecture, prevent drift, and support neurodivergent solo devs.

---

## 🧑‍💼 Product Owner

| ID   | Acceptance Criteria                                                |
|------|---------------------------------------------------------------------|
| PO-1 | Session status summary printed on start                            |
| PO-2 | Commit blocked if snapshot/docs/contracts out-of-date              |
| PO-3 | CLI/docs/code always in sync                                       |
| PO-4 | GPT reminded to reload files                                       |
| PO-5 | Optional ADHD-mode UX behavior                                     |

---

## 👨‍💻 Senior Developer

| Required Tool         | Status       |
|-----------------------|--------------|
| `start_dev.py`        | ❌ To build  |
| `end_dev.py`          | ✅ Built     |
| `snapshot_split.py`   | ✅ Built     |
| `update_docs.py`      | ❌ To build  |
| `validate_contracts.py`| ❌ To build |
| `check_architecture.py`| ❌ To build |

---

## 🧠 Architecture Guardian

| Violation                       | Fix                                |
|----------------------------------|-------------------------------------|
| Domain → CLI                    | `check_architecture.py` fails     |
| No Protocol on service/repo     | `validate_contracts.py` aborts    |
| CLI drift                       | `update_docs.py` regenerates      |
| Snapshot missing                | `snapshot_split.py` writes        |

---

## 🧪 QA Engineer

Golden and contract tests required for all dev tooling. Files:

- `tests/scripts/test_start_dev.py`
- `tests/scripts/test_end_dev.py`
- `tests/scripts/test_validate_contracts.py`
- `tests/scripts/test_check_architecture.py`

---

## 📄 Deliverables

| File                     | Purpose                                | Status |
|--------------------------|----------------------------------------|--------|
| `start_dev.py`           | Session opener                         | ❌     |
| `end_dev.py`             | Commit enforcer                        | ✅     |
| `update_docs.py`         | Regenerate CLI + roadmap               | ❌     |
| `validate_contracts.py`  | Enforce Protocols                      | ❌     |
| `check_architecture.py`  | Block import violations                | ❌     |
| `tests/scripts/`         | Test all above                         | ❌     |

---

## 🔒 Warnings

> All sessions must run `start_dev.py`.  
> All commits must run `end_dev.py`.  
> No doc/test/snapshot = No feature.

---

## 🧠 GPT Enforcement Note

Custom GPTs must be prompted at session start:

❗ Have you reloaded the project snapshot and .md docs?

Optional: add `gpt_sync_check.py` to scan for out-of-date files.