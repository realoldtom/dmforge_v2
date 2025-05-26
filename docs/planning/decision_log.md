## Version: 1.0 (2025-05-26)

# File: docs/planning/decision_log.md

# 📘 DMForge Decision Log

This log captures all major architecture, tooling, and process decisions for DMForge v2.  
Each entry includes context, alternatives, rationale, and enforcement — ensuring traceable evolution.

---

### 📅 2025-05-24  
**Area:** Developer Lifecycle  
**Decision:** Create `start_dev.py` to enforce session context, GPT reload reminder, and snapshot validation at session start  
**Alternatives:** Start sessions manually; rely on dev memory; trust workflow discipline  
**Rationale:** Solo developer is neurodivergent and needs bootstrapping structure to reliably begin work  
**Enforcement:** `start_dev.py` (pending), lifecycle doc rules, GPT sync prompt

---

### 📅 2025-05-24  
**Area:** Planning Discipline  
**Decision:** All features must have dedicated `.md` planning docs before implementation  
**Alternatives:** Ad-hoc notes, inline TODOs, or code comments  
**Rationale:** Prevents scope creep, aligns to personas, ensures full traceability  
**Enforcement:** Commit blocks without traceability + planning doc in `docs/planning/`

---

### 📅 2025-05-24  
**Area:** Architecture Enforcement  
**Decision:** Implement `check_architecture.py` to block CLI-domain and app-infra violations  
**Alternatives:** Manual code review; lint-only enforcement  
**Rationale:** Violations of Clean Architecture are subtle and catastrophic over time  
**Enforcement:** Script blocks on import graph violations; required in `end_dev.py`

---

### 📅 2025-05-24  
**Area:** Documentation Parity  
**Decision:** Auto-generate `05_usage.md` from Typer CLI `--help` output  
**Alternatives:** Manual update of usage docs per feature  
**Rationale:** Manual parity drifts silently, introduces UX/test failures  
**Enforcement:** `update_docs.py`, snapshot test of CLI help, doc regeneration in `end_dev.py`

---

### 📅 2025-05-24  
**Area:** Rendering Compatibility  
**Decision:** Enforce `weasyprint < 61.0`, `pydyf < 0.11.0` to avoid render breakage  
**Alternatives:** Allow latest versions and patch if broken  
**Rationale:** Rendering is critical user path — stability trumps upgrades  
**Enforcement:** `validate_env.py` checks and blocks on version drift

---

### 📅 2025-05-24  
**Area:** Snapshot System Design  
**Decision:** Replace 300-line dump splitting with grouped context-aware snapshots for GPT ingestion  
**Alternatives:** Arbitrary chunk splitting; random file order  
**Rationale:** GPT misinterprets ungrouped input, causing hallucination and architectural errors  
**Enforcement:** `snapshot_split.py` with `group_config.yaml`, group tokens limit, enforced snapshot naming

---

###
