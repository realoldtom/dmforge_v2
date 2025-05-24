# File: docs/planning/project_lifecycle_policy.md

# 📜 DMForge Project Lifecycle Policy

This document defines the **mandatory behaviors** that must occur at each project lifecycle stage.  
No feature or phase is valid unless these rules are followed, enforced, and documented.

---

## 🔁 Daily Session Rules

| Step         | Required Script         | Behavior Enforced                                                                            |
|--------------|--------------------------|-----------------------------------------------------------------------------------------------|
| Start of Dev | `scripts/start_dev.py`   | ✅ Snapshot parity<br>✅ Doc parity<br>✅ GPT reload prompt<br>✅ Last commit and roadmap echo |
| End of Dev   | `scripts/end_dev.py`     | ✅ Coverage pass<br>✅ Format/lint<br>✅ Interface contract check<br>✅ Commit/test/doc sync   |

---

## 🔀 Git & Commit Policy

| Rule                     | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| One concern per commit   | Each commit must touch a single logical change only                   |
| Conventional format      | `feat:`, `test:`, `refactor:`, `docs:`, etc.                          |
| Pre-commit hook required | `.pre-commit-config.yaml` must run `end_dev.py` locally               |
| CI equivalent required   | CI must run full lifecycle script (`end_dev.py`) before merge to main |

---

## 🧪 Feature Definition Rules

| Requirement                        | Enforcement Tool             |
|-----------------------------------|-------------------------------|
| Golden snapshot exists            | `snapshot_split.py` + golden tests |
| Interface has declared Protocol   | `application.ports/*.py`             |
| CLI calls controller only         | `check_architecture.py`              |
| Doc and CLI help match            | `update_docs.py`                     |
| Commit includes test and doc      | `end_dev.py` + `requirements_traceability_matrix.md` |

---

## 📚 Roadmap & Planning Discipline

| Event           | Required Artifacts                                                                 |
|------------------|-----------------------------------------------------------------------------------|
| New feature      | `docs/planning/feature_{NAME}.md` + traceability entry                           |
| Phase transition | `roadmap_versions/roadmap_phase_{ID}_{date}.md` snapshot                         |
| Decision change  | `decision_log.md` entry                                                           |
| Detected risk    | `risk_log.md` entry                                                               |

---

## 🔒 Final Enforcement Rules

- 🔥 Any feature without tests, documentation, and traceability = does not exist
- 🚫 Commits that skip `end_dev.py` or drift from snapshot = invalid
- 🧠 Start sessions via `start_dev.py` or risk architectural misalignment
- 🧾 Planning files must be updated **before** feature implementation

---

## 🧠 Mental Health Mode (Optional)

- Enables focus task picker, Pomodoro integration, and session logging
- Default off, toggle via `.dmforge.conf` or CLI flag `--adhd-mode`
- Log sessions in `logs/daily_log_{date}.md` with start/stop markers