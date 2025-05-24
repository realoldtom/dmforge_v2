# File: docs/planning/requirements_traceability_matrix.md

# 📊 Requirements Traceability Matrix

Every feature, interface, and enforcement point must map to its:
- Roadmap phase
- Responsible test file
- Protocol or contract
- Commit discipline
- Snapshot enforcement (if applicable)

---

## ✅ Legend

| ✅ | Requirement is satisfied via enforcement, tests, and docs |
| ❌ | Missing or unverified — commit is invalid until addressed |

---

## 📋 Feature → Enforcement Map

| Feature                          | Roadmap Phase | Commit Example                          | Test File                                 | Protocol / Contract                 | Snapshot Required | ✅ |
|----------------------------------|---------------|------------------------------------------|--------------------------------------------|-------------------------------------|-------------------|----|
| Deck Builder (CLI)              | 1             | `feat(cli): add deck builder filters`    | `test_deck_builder.py`                     | `DeckBuilder`                        | Yes               | ✅ |
| Deck Renderer (PDF/HTML)        | 2             | `feat(cli): add deck render command`     | `test_deck_render.py`                      | `RenderService`, `DeckStorage`      | Yes               | ✅ |
| PDF Compatibility Guard         | 2.1           | `test: render fails with bad version`    | `test_validate_env.py`                     | `check_pdf_dependencies()`          | No                | ✅ |
| Dev Session Automation          | X.0           | `chore: add start_dev and enforcement`   | `test_start_dev.py`, `test_end_dev.py`     | N/A                                  | Yes               | ❌ |
| Interface Compliance Checker    | X.0           | `test: validate all declared protocols`  | `test_validate_contracts.py`               | `SpellRepository`, etc.             | No                | ❌ |
| Architecture Boundary Checker   | X.0           | `test: fail on domain ↔ CLI import`      | `test_check_architecture.py`               | Clean Arch Layer Rules:contentReference[oaicite:0]{index=0} | No                | ❌ |
| CLI Docs Generator              | X.1           | `docs: update usage and CLI output`      | `test_update_docs.py` (planned)            | CLI help string parity               | Yes               | ❌ |

---

## 🧪 Test Enforcement Map

| Contract Name          | Interface File                         | Implementation File                          | Test File                                      | ✅ |
|------------------------|----------------------------------------|-----------------------------------------------|------------------------------------------------|----|
| `DeckBuilder`          | `application/ports/deck_builder.py`   | `application/services/deck_builder.py`        | `test_deck_builder.py`                         | ✅ |
| `RenderService`        | `application/ports/render_service.py` | `application/services/weasy_renderer.py`      | `test_deck_render.py`                          | ✅ |
| `SpellRepository`      | `application/ports/spell_repository.py`| `infrastructure/repository/json_spell_repository.py` | `test_json_spell_repository.py`         | ✅ |
| `DeckStorage`          | `application/ports/deck_storage.py`   | `infrastructure/repository/json_deck_storage.py` | (missing test)                            | ❌ |

---

## 🚨 Incomplete or Missing

- `DeckStorage` lacks golden test coverage
- CLI doc generation test (`test_update_docs.py`) not implemented
- Interface validation tests (`test_validate_contracts.py`) not yet written
- Architecture boundary checks untested

---

**No feature is complete until its entire row is ✅.**
