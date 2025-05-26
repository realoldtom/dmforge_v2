## Version: 1.1 (2025-05-26)

# File: docs/planning/decision_log.md

# 📘 DMForge Decision Log

This document captures all major architectural, tooling, and process decisions.  
Each entry includes the context, alternatives considered, and rationale — because future-you will forget.

---

## 🧠 Format

| Field           | Meaning |
|----------------|---------|
| **Date**       | When the decision was made |
| **Area**       | Architecture, CLI, Testing, Docs, Workflow, etc. |
| **Decision**   | Summary of choice made |
| **Alternatives** | What other paths were considered |
| **Rationale**  | Why the current decision was selected |
| **Enforcement** | How this decision is now codified in code/tests/docs |

---

## 🔐 Decisions

---

### 📅 2025-05-24  
**Area:** Developer Lifecycle  
**Decision:** Create `start_dev.py` to enforce context, GPT reload reminder, and snapshot validation at session start  
**Alternatives:** Start sessions manually; rely on memory; trust dev to run checks  
**Rationale:** Dev has ADHD/autism and needs structural scaffolding to initiate work reliably  
**Enforcement:** Script runs snapshot/doc diff checks, echoes prior task, blocks on drift

---

### 📅 2025-05-24  
**Area:** Feature Planning Discipline  
**Decision:** Every feature must have a `.md` planning doc before implementation  
**Alternatives:** Use ad-hoc Notion, Obsidian notes, or inline TODOs  
**Rationale:** Ensures test + doc coverage, scope control, persona alignment  
**Enforcement:** Required by commit via roadmap reference, traceability matrix, and lifecycle policy

---

### 📅 2025-05-24  
**Area:** Architecture Validation  
**Decision:** Implement `check_architecture.py` to block CLI-domain and app-infra violations  
**Alternatives:** Lint-only rules; manual PR checks  
**Rationale:** Clean Architecture is project’s foundation; violations = failure  
**Enforcement:** Script checks import graph, runs on commit (`end_dev.py`)

---

### 📅 2025-05-24  
**Area:** Documentation Parity  
**Decision:** Auto-generate `05_usage.md` from Typer CLI `--help`  
**Alternatives:** Manually update usage docs with each feature  
**Rationale:** Manual sync fails silently; leads to user confusion and test rot  
**Enforcement:** `update_docs.py` runs as part of commit; snapshot compared

---

### 📅 2025-05-24  
**Area:** Rendering Compatibility  
**Decision:** Enforce `weasyprint < 61.0`, `pydyf < 0.11.0` due to known rendering issues  
**Alternatives:** Accept breakage, rely on patching upstream  
**Rationale:** PDF/HTML rendering is core output path; stability trumps freshness  
**Enforcement:** `validate_env.py` blocks incompatible versions on session start or commit
