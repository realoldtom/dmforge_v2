# 🛠 DMForge v2 CLI Usage

This file documents how to use the DMForge CLI to build and render spell decks as JSON, HTML, or PDF files.

---

## 🎯 Basic Workflow

### 1. **Build a Deck**

```bash
python main.py deck build --spell-data data/spells/spells.json --class Wizard --level 1 --output exports/dev/deck.json
Loads spells from JSON file

Filters by class and level

Saves result to deck.json

You can also filter by --school and name the deck via --name.

2. Render to PDF
bash
Copy
Edit
python main.py render render --input exports/dev/deck.json --output exports/dev/deck.pdf --format pdf
Renders deck using HTML template + WeasyPrint

Output format: pdf or html

Templates expected in src/dmforge/resources/templates/

3. Validate a Deck
bash
Copy
Edit
python main.py render validate --input exports/dev/deck.json
Verifies JSON schema and card structure

Ensures input is renderable before committing

🧪 Development Checks
Use this before every commit:

bash
Copy
Edit
python scripts/end_dev.py "feat: add cleric support"
This will:

✅ Run environment + dependency checks

✅ Run tests with coverage

✅ Format code (black)

✅ Lint code (ruff)

✅ Commit + push if successful

💡 CLI Help
bash
Copy
Edit
python main.py --help
python main.py deck --help
python main.py deck build --help
python main.py render --help
🧱 File Locations
Folder	Purpose
data/spells/	Input spell JSON
exports/dev/	Output decks
src/dmforge/resources/templates/	Jinja2 templates
src/dmforge/resources/assets/	Fonts, images

🔥 Example: Full Flow
python main.py deck build --spell-data data/spells/spells.json --class Wizard --level 1 --output deck.json
python main.py render render --input deck.json --output deck.pdf --format pdf
🚫 Common Errors
Message	Fix
No such command	You forgot to wire main.py correctly
Template directory not found	Use --template-dir if you're in a test
Unsupported format	Use only pdf or html
Fontconfig error	Ignorable on Windows if rendering still succeeds