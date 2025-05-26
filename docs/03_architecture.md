## Version: 1.0 (2025-05-26)

# 🧱 DMForge v2 Architecture

## 📚 Layer Overview

DMForge v2 follows strict Clean Architecture principles. Each layer has a specific role, and cross-layer contamination is explicitly forbidden.

dmforge_v2/
├── domain/ # Core data structures, no logic or dependencies
├── application/ # Business rules and orchestration
├── infrastructure/ # File I/O, network calls, external libraries
├── interface/
│ └── cli/ # Typer CLI adapter only

---

## 🔒 Allowed Dependencies

| From → To           | ✅ Allowed? | 📌 Notes |
|---------------------|------------|----------|
| `interface/*` → `application` | ✅ | CLI calls services only |
| `application` → `domain`     | ✅ | Services use core types |
| `application` → `infrastructure` | ❌ | Use interfaces/ports |
| `domain` → any other layer   | ❌ | Core is pure |
| `infrastructure` → `application` | ❌ | No upward dependencies |

---

## 🔁 Dependency Rules

- CLI depends on services, **never directly on infrastructure or domain**
- Application layer only depends on **interfaces** to infrastructure
- Infrastructure implements those interfaces, but is plug-and-play
- Domain is **pure Python** — no third-party packages, no I/O

---

## 🧪 Test Rules

- `tests/domain/`: Model behavior (e.g., `SpellCard.add_art_version`)
- `tests/application/`: Service behavior, injected mocks
- `tests/infrastructure/`: Golden tests or integration-only
- `tests/interface/cli/`: CLI args → service → output, no logic tests

---

## 📂 Example Use Case: Deck Generation

| Layer | Responsibility |
|-------|----------------|
| `interface/cli/deck_build.py` | Accepts CLI args, constructs `DeckOptions`, passes to service |
| `application/deck_builder.py` | Filters spell data and builds a `Deck` |
| `infrastructure/spell_repository.py` | Loads JSON from SRD and returns spell dicts |
| `domain/models.py` | `SpellCard`, `Deck`, `DeckOptions` – with no knowledge of source or CLI |

---

## ❌ Common Violations to Guard Against

| Violation | Fix |
|----------|-----|
| CLI imports `SpellCard` directly | Define a `DeckDTO` or use services only |
| Service reads from disk | Use a `SpellRepository` interface and inject implementation |
| Domain model returns raw JSON | Use `to_dict()` or `to_json()` explicitly, no auto-serialization |
| CLI generates summaries | Extract to `DeckSummaryService` or util module |

---

## 🔧 Refactor Rule

> If logic spans layers or causes unclear ownership: **Stop. Refactor the boundary before writing more code.**
