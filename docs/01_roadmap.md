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
