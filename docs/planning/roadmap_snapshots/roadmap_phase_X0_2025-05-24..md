## Version: 1.0 (2025-05-26)

# 🧭 DMForge v2 Roadmap (Enforced Architecture)

## 🔥 Core Principles

- **SRP (Single Responsibility)**: One reason to change per module  
- **SoC (Separation of Concerns)**: CLI, app, domain, infra fully isolated  
- **DI (Dependency Injection)**: All services and repos passed via Protocols  
- **Golden Testing**: All outputs (deck JSON, HTML/PDF, art) are snapshot tested  
- **CLI = Adapter**: CLI only parses input; no logic  
- **Strict Contracts**: All services and repos declare Protocols in `application.ports`  
- **Automated Enforcement**: Architecture validated before every commit  

---

## 🎯 MVP Target: Spell Deck Builder CLI

```sh
dmforge deck build --class Wizard --level 1 --output deck.json
dmforge deck render deck.json --format pdf --layout 6up
dmforge deck art deck.json
📚 Clean Architecture Layers
Layer	Purpose
domain/	Pure models: SpellCard, Deck
application/	Orchestration via interfaces
infrastructure/	File I/O, rendering, API clients
interface/cli/	Typer adapter only

📋 Phase Breakdown
Phase	Goal	Outcome
0	Project scaffold, CI, pre-commit	scripts/end_dev.py, .pre-commit-config.yaml
1	Deck builder MVP	deck build with filtering and JSON output
1.4	Environment-aware paths	data/, exports/, .venv/ auto-detected
2	PDF/HTML Renderer	WeasyPrint support with golden testing
2.1	PDF Compatibility Guard	Enforce weasyprint < 61.0, pydyf < 0.11.0
2.5	6-Up Printable Layout (Grid + Breaks)	Card sheet layout for print
3	Art Prompt + DALL·E Integration	Prompts, metadata, stable paths
4	Interactive CLI Menu	deck build --interactive with filters
X.0	Enforcement system	Full automation of snapshot, contracts, docs
X.1	Documentation generator suite	Auto-generate CLI guide, data flow, troubleshooting

🧪 Test Strategy
✅ Golden tests for rendered output and JSON

✅ Contract compliance tests (e.g., repo implements Protocol)

✅ CLI E2E tests for all commands

✅ Architecture boundary tests: layer violations raise

🚫 Out of Scope (Until Post-MVP)
Trait/feature/monster cards

Scene generators

Plugin framework

Web UI / API server

Live OpenAI calls

Anything not golden tested

🧱 Refactor Triggers
Violation	Action
❌ Logic in CLI	Extract to Controller
❌ Reused transform/filter	Move to utils
❌ Service uses file paths	Inject via DeckStorage protocol
❌ Protocol not enforced	Write interface, test compliance

🛠️ Developer Enforcement System
scripts/end_dev.py (runs before commit)
Step	Check
✅ validate_env.py	PDF render version compatibility
✅ snapshot_split.py	Save source snapshot to /snapshots/
✅ update_docs.py	Update CLI help + roadmap phase
✅ validate_contracts.py	Interface/protocol compliance check
✅ check_architecture.py	Detect CLI-domain or app-infra violations
✅ pytest with coverage	All tests must pass
✅ black, ruff	Style and format guard
✅ git add and commit	Atomic + scoped commit

📦 Pre-Commit Hook
.pre-commit-config.yaml runs end_dev.py for all staged commits. Enforced locally and in CI.

🧠 Final Law
If a feature is not tested, documented, golden-verified, and enforced by commit hooks — it does not exist.