## Version: 1.0 (2025-05-26)

# Folder: docs/planning/roadmap_versions/

# 🧭 Roadmap Version Snapshots

This folder contains **timestamped snapshots** of the canonical `01_roadmap.md`.  
Each snapshot locks in the roadmap at a specific milestone or before a major architectural shift.

---

## 📂 Usage Rules

- Snapshots are **immutable**. Once created, do not edit.
- Snapshots are created:
  - Before starting a new roadmap phase
  - After finalizing a new architectural rule
  - Before merging a major feature branch
- Filenames must follow this convention:

roadmap_phase_{PHASE_ID}_{YYYY-MM-DD}.md

yaml
Copy
Edit

✅ Example:
roadmap_phase_X0_2025-05-24.md

yaml
Copy
Edit

---

## 📌 Enforcement

- `scripts/end_dev.py` must copy `01_roadmap.md` here automatically if `PHASE:` or `Outcome:` blocks have changed.
- `scripts/update_docs.py` should include this snapshot creation as part of its lifecycle.
- `start_dev.py` should warn if the current roadmap does not match the last locked version.

---

## 📋 Index Template (auto-generated)

When you have snapshots, regenerate this section:

| Filename                         | Phase | Date       | Notes                          |
|----------------------------------|-------|------------|--------------------------------|
| `roadmap_phase_X0_2025-05-24.md`| X.0   | 2025-05-24 | Enforcement system planning    |