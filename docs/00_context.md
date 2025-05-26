## Version: 1.1 (2025-05-26)

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
