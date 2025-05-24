# File: docs/planning/project_lifecycle_policy.md

# 📜 DMForge Project Lifecycle Policy

This document defines the **mandatory behaviors** that must occur at each project lifecycle stage. No feature or phase is valid unless these rules are followed, enforced, and documented.

---

## 🔁 Daily Session Rules

| Step           | Required Script      | Behavior Enforced                            |
|----------------|----------------------|----------------------------------------------|
| Start of Dev   | `scripts/start_dev.py` | ✅ Snapshot parity<br>✅ Doc parity<br>✅ GPT reload warning<br>✅ Last commit echo |
| End of Dev     | `scripts/end_dev.py`   | ✅ Coverage pass<br>✅ Format/lint<br>✅ Interface contract check<br>✅ Snapshot and roadmap sync |

---

## 🔀 Git & Commit Policy

| Rule                     | Description                                              |
|--------------------------|----------------------------------------------------------|
| One concern per commit   | Each commit must touch a single logical change only      |
| Conventional format      | `feat:`, `test:`, `refactor:`, `docs:` etc.              |
| Pre-commit hook required | `.pre-commit-config.yaml` must run `end_dev.py` locally  |
| CI equivalent enforced   | Future CI must run same scripts before accepting merge   |

---

## 🧪 Feature Rules

| Requirement                        | Enforcement Tool             |
|-----------------------------------|-------------------------------|
| Golden snapshot exists            | `tests/` + `snapshot_split.py` |
| Interface has declared Protocol   | `application/ports/*.py`      |
| CLI calls controller only         | `check_architecture.py`       |
| Doc and CLI help match            | `update_docs.py`              |
| No cross-layer violations         | `check_architecture.py`       |
| Commit describes scope            | `end_dev.py` (requires `sys.argv[1]`) |

---

## 📚 Phase Transition Rules

| Transition | Must Include |
|------------|---------------|
| New roadmap phase | Updated `01_roadmap.md` + snapshot to `roadmap_versions/` |
| New feature       | `feature_*.md` + commit trace in `requirements_traceability_matrix.md` |
| Architectural shift | Entry in `decision_log.md` |

---

## 🔒 Non-Negotiable Laws

- Any script bypass is invalid.
- Any commit without test + doc = does not exist.
- Any stale snapshot or roadmap = automatic failure.
- Every architectural change must be logged.

---

## 🧠 Mental Health Mode

Optional, but recommended for neurodivergent devs:
- `start_dev.py` offers “focus mode” with a task picker
- Logging of session starts + completions in `daily_log/`
- No new tasks until previous commit passes lifecycle checks

## 🧠 GPT Interaction Policy

- All GPT usage must start with `docs/system/gpt_system_prompt.md`
- GPT sessions must only receive grouped snapshot files (max 19)
- If system prompt is updated, it must be versioned and logged in `decision_log.md`
- Developer must confirm system prompt match before GPT upload
