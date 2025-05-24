# File: docs/planning/test_strategy.md

# 🧪 DMForge Test Strategy

This file defines the **non-optional test categories** required to validate and protect the architecture of DMForge v2.

If a feature is not tested per this strategy — it does not exist.

---

## 🧱 Golden Tests

Golden tests compare output files against known-good snapshots.  
Used to prevent regressions and enforce render/output discipline.

| Target           | Test File                        | Snapshot Location     |
|------------------|----------------------------------|------------------------|
| Rendered HTML    | `test_deck_render.py`            | `snapshots/*.html`    |
| Rendered PDF     | `test_deck_render.py` (size check only) | (binary: size & hash) |
| Deck JSON        | `test_deck_build.py`             | `snapshots/*.json`    |

✅ Must be updated intentionally via `scripts/end_dev.py`

---

## 📑 Contract Tests

These ensure that all services and repositories implement declared `Protocol`s in `application.ports`.

| Protocol             | Implementation File                          | Test File                                      |
|----------------------|----------------------------------------------|------------------------------------------------|
| `SpellRepository`    | `json_spell_repository.py`                   | `test_json_spell_repository.py`               |
| `DeckBuilder`        | `deck_builder.py`                            | `test_deck_builder.py`                        |
| `RenderService`      | `weasy_renderer.py`                          | `test_deck_render.py`                         |
| `DeckStorage`        | `json_deck_storage.py`                       | ❌ Missing test                                |

🛑 Any missing test is a hard blocker for commit.

---

## 🧪 CLI Integration Tests

Each CLI command must:
- Accept all valid options
- Return exit code 0 on success
- Fail cleanly with informative error messages

| Command          | Test File                  |
|------------------|----------------------------|
| `deck build`     | `test_deck_build.py`       |
| `render`         | `test_deck_render.py`      |
| `validate`       | `test_deck_render.py`      |

📌 All CLI args must be snapshot tested where possible.

---

## 🔐 Architecture Boundary Tests

No layer may import or reference a disallowed layer.

| Rule                              | Enforced By                  |
|-----------------------------------|-------------------------------|
| Domain must not import anything   | `check_architecture.py`       |
| CLI must not touch domain directly| `check_architecture.py`       |
| App must not use raw file I/O     | `validate_contracts.py`       |

These rules must fail builds if violated.

---

## 🚫 Testing Anti-Patterns

| Pattern              | Why It’s Rejected                |
|----------------------|----------------------------------|
| Monkeypatching       | Breaks DI. Use mock via interface |
| Test without snapshot| Regression risk                  |
| Tests that hit disk  | Must be wrapped in `tmp_path`    |
| Untyped mocks        | Must implement Protocol if injected |

---

## 🧠 Final Law

If there is no test, and no golden snapshot, your code is fiction.
