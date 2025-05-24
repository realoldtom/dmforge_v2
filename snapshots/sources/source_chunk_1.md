# File: docs/00_context.md
```
# 🧠 DMForge v2 Development Context

## 🖥 Environment
- OS: Windows 10+
- IDE: Visual Studio Code
- Terminal: PowerShell
- Python: 3.11+
- Dependency Manager: [Poetry](https://python-poetry.org/)
- Virtual Environment: `.venv/` in-project

## 📁 Project Structure

dmforge_v2/
├── domain/ # Core models (SpellCard, Deck, DeckOptions)
├── application/ # Business logic (DeckBuilder, RenderService)
├── infrastructure/ # IO, SRD loading, API calls
├── interface/cli/ # Typer CLI commands and adapters
├── tests/ # Unit + integration tests
├── scripts/ # Lifecycle and utility scripts
├── docs/ # Roadmap, architecture, contracts

markdown
Copy
Edit

## 📜 Development Discipline

- ✅ Strict adherence to Clean Architecture
- ✅ Frozen dataclasses in domain
- ✅ CLI layer never contains business logic
- ✅ All dependencies injected via interfaces
- ✅ One concern per commit (`feat:`, `test:`, `fix:`, etc.)
- ✅ All code tested before commit
- ✅ All commits run through `scripts/end_dev.py`
- ✅ `pre-commit` checks enforced locally

## 🧪 Testing Rules

- Test-first development
- No monkeypatching — use dependency injection
- Golden output tests for JSON, render, and summaries
- Contract tests for service/repo interfaces
- Domain tests isolated in `tests/domain/`

## 🔐 Commit Rules

- Must include test
- Must run formatting (`black`)
- Must pass lint (`ruff`)
- Must pass tests (`pytest --cov`)
- Must be atomic and logically scoped

## 🧑‍💻 Persona

**Solo developer** learning:
- Clean architecture
- Python packaging and modularity
- Test-driven development
- Distributed system design (future phases)

---
```
# File: docs/01_roadmap.md
```
# 🧭 DMForge v2 Roadmap

## 🔥 Core Principles

- **Single Responsibility Principle (SRP)**: One reason to change per module  
- **Separation of Concerns (SoC)**: CLI, app, domain, and infra are isolated  
- **Dependency Injection (DI)**: All services and repos passed explicitly  
- **Golden Tests**: All outputs (deck JSON, rendered HTML, etc.) are golden snapshot tested  
- **CLI = Adapter**: No domain logic in the CLI layer  
- **Strict Contracts**: Repositories, services, and transformers are interfaces  

---

## 🎯 MVP Target: Spell Deck Builder CLI

```sh
dmforge deck build --class Wizard --level 1 --output deck.json
dmforge deck render deck.json --format pdf
dmforge deck art deck.json
```

---

## 📚 Clean Architecture Layers

- `domain/`: Core models (`SpellCard`, `Deck`, `DeckOptions`, etc.)
- `application/`: Services like `DeckBuilder`, `RenderService`, etc.
- `infrastructure/`: JSON repo, OpenAI API, WeasyPrint
- `interface/cli/`: Typer CLI as adapter layer

---

## 📋 Phase Breakdown

| Phase | Goal                               | Outcome                                           |
|-------|------------------------------------|---------------------------------------------------|
| **0** | Project scaffold, CI, pre-commit   | `scripts/end_dev.py`, `.pre-commit-config.yaml`  |
| **1** | Deck builder MVP                   | `deck build` CLI with filters and JSON output    |
| 1.4 | Environment-aware CLI paths        | `data/` for spell JSON, `exports/` for decks |
| **2** | Deck renderer                      | `deck render` with golden test for HTML/PDF      |
| **3** | Art prompt + generation            | `deck art` with saved prompt/image paths         |
| **4** | Interactive CLI menu               | `deck build --interactive` with confirm loop     |

---

## 🚫 Out of Scope (Until Post-MVP)

- Trait/feature cards  
- Scene generation  
- Plugin support  
- API or web interface  
- OpenAI live calls without mocks  
- Any rendering without snapshot test  

---

## 🔧 Git Discipline

- **Branch strategy**: `main`, `dev`, `feat/*`, `fix/*`, `refactor/*`
- **Conventional commits**: `feat:`, `fix:`, `test:`, `refactor:`
- **Commit policy**: One concern per commit, include test + doc
- **Test gate**: All pushes go through `scripts/end_dev.py`

---

## 🧪 Test Strategy

- No monkeypatching — use DI only  
- Golden output tests for deck JSON, art metadata, rendered HTML  
- Contract tests for all input/output interfaces  

---

## 🧱 Refactor Triggers

- ❌ Logic appears in CLI → extract controller  
- ❌ Filters or transforms reused → move to shared utility  
- ❌ New feature breaks interface → rewrite contract before coding  

---

**You start here. This file is your contract with yourself. Violate it, and you're building another disaster.**
```
# File: docs/02_contracts.md
```
# 📜 DMForge v2 Contracts

This document defines the **explicit interfaces** (contracts) between architecture layers in DMForge v2.  
Every layer depends on **abstractions, not implementations**. These contracts are the glue — and the firewalls.

---

## 🧩 Contract Categories

- **Domain Types**: `SpellCard`, `Deck`, `DeckOptions`
- **Service Interfaces**: `DeckBuilder`, `RenderService`, `ArtService`
- **Repository Interfaces**: `SpellRepository`, `DeckStorage`
- **DTOs & Adapters**: CLI-facing objects like `DeckDTO`, `SummaryText`, etc.

---

## 🧱 Domain Contracts

### `SpellCard`
```python
@dataclass(frozen=True)
class SpellCard:
    name: str
    level: int
    school: School
    classes: list[str]
    description: str
    duration: str
    art_path: str | None = None
Deck

@dataclass(frozen=True)
class Deck:
    cards: list[SpellCard]
    name: str
    version: str

    def to_json(self) -> str
    def to_dict(self) -> dict
DeckOptions

@dataclass(frozen=True)
class DeckOptions:
    classes: list[str] = field(default_factory=list)
    levels: list[int] = field(default_factory=list)
    schools: list[str] = field(default_factory=list)
    name: str = "Untitled"
🧰 Service Contracts
DeckBuilder
python
Copy
Edit
class DeckBuilder(Protocol):
    def build(self, options: DeckOptions) -> Deck:
        ...
RenderService

class RenderService(Protocol):
    def render_pdf(self, deck: Deck, output_path: Path) -> None:
        ...
    def render_html(self, deck: Deck, output_path: Path) -> None:
        ...
ArtService


class ArtService(Protocol):
    def generate_prompt(self, card: SpellCard) -> str:
        ...
    def assign_art(self, card: SpellCard, prompt: str) -> SpellCard:
        ...
💾 Repository Contracts
SpellRepository
p
class SpellRepository(Protocol):
    def load_all_spells(self) -> list[dict]:
        ...
DeckStorage

class DeckStorage(Protocol):
    def save(self, deck: Deck, path: Path) -> None:
        ...
    def load(self, path: Path) -> Deck:
        ...
🎯 Adapter Contract (CLI ↔ App Layer)
DeckController

class DeckController:
    def __init__(self, builder: DeckBuilder)
    def build_from_cli(self, options_dict: dict) -> Deck
Used by CLI only — accepts CLI-native types (dicts, strings), returns typed results.

🚫 Anti-Patterns to Avoid
Mistake	Fix
CLI accesses SpellCard directly	Use DeckController only
App layer uses Path or file system	Go through DeckStorage or injected path
No Protocol on services	Write one, then inject
Domain returns JSON blobs	Domain returns pure Python; only adapter serializes

🔒 Rules
All app/infrastructure dependencies must be injected via interface

No service uses another without a testable interface

No domain object should ever import from infrastructure or application
```