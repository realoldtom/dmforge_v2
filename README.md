# 🧙 DMForge v2

Clean Architecture toolkit for generating printable D&D 5e spell and character cards.

---

## 📦 Project Structure

src/dmforge/
├── domain/ # Core models (SpellCard, Deck, etc.)
├── application/ # Business logic (DeckBuilder, RenderService)
├── infrastructure/ # File I/O, JSON loader, OpenAI
├── interface/cli/ # Typer CLI interface
tests/
scripts/
docs/
---

## 🚀 Usage

```bash
poetry install
poetry shell
python scripts/end_dev.py "feat: initial setup"

🧪 Testing
PYTHONPATH=src poetry run pytest --cov --exitfirst
🎯 Roadmap
See docs/01_roadmap.md

👤 Maintainer
Built by a solo dev learning architecture through test-first Python engineering.