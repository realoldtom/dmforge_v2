# File: src/dmforge/application/services/weasy_renderer.py
```python
import logging
from pathlib import Path

import pydyf  # ✅ needed for version check
import weasyprint
from dmforge.domain.models import Deck
from jinja2 import Environment, FileSystemLoader, select_autoescape
from packaging.version import parse as vparse
from weasyprint import HTML

# Version checks (breaks in >= 61.0 and 0.11.0)
if vparse(weasyprint.__version__) >= vparse("61.0"):
    raise RuntimeError("❌ weasyprint >= 61.0 breaks PDF rendering. Pin to 60.1.")
if vparse(pydyf.__version__) >= vparse("0.11.0"):
    raise RuntimeError("❌ pydyf >= 0.11.0 breaks PDF constructor compatibility. Pin to 0.10.0.")


class WeasyRenderer:
    def __init__(self, template_dir: Path, asset_dir: Path, verbose: bool = False):
        self.template_dir = template_dir
        self.asset_dir = asset_dir
        self.verbose = verbose
        self.env = self._setup_jinja_env()

        if verbose:
            logging.getLogger("weasyprint").setLevel(logging.DEBUG)
        else:
            logging.getLogger("weasyprint").setLevel(logging.WARNING)

    def _setup_jinja_env(self) -> Environment:
        return Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render_html(self, deck: Deck, output_path: str) -> None:
        try:
            html_content = self._render_html_content(deck)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            if self.verbose:
                logging.info(f"✅ HTML rendered successfully: {output_path}")
        except Exception as e:
            logging.error(f"❌ HTML rendering failed: {str(e)}")
            raise RuntimeError(f"HTML rendering failed: {str(e)}") from e  # ✅ fix

    def render_pdf(self, deck: Deck, output_path: Path) -> None:
        try:
            html_string = self._render_html_content(deck)
            html = HTML(string=html_string, base_url=str(self.asset_dir))

            if self.verbose:
                logging.info(f"🔍 Rendering PDF to: {output_path}")
                logging.info(f"🔍 HTML content size: {len(html_string)} characters")

            html.write_pdf(target=str(output_path))

            if self.verbose:
                logging.info(f"✅ PDF rendered successfully: {output_path}")
        except Exception as e:
            logging.error(f"❌ PDF rendering failed: {str(e)}")
            raise RuntimeError(f"PDF rendering failed: {str(e)}") from e  # ✅ fix

    @staticmethod
    def check_pdf_dependencies() -> dict:
        try:
            import weasyprint

            return {
                "weasyprint_installed": True,
                "pydyf_installed": True,
                "available": True,
                "weasyprint_version": weasyprint.__version__,
                "recommendations": [],
                "error": None,
            }
        except ImportError as e:
            return {
                "weasyprint_installed": False,
                "pydyf_installed": False,
                "available": False,
                "weasyprint_version": None,
                "recommendations": [
                    "poetry add weasyprint",
                    "poetry add pydyf",
                ],
                "error": str(e),
            }

    def _render_html_content(self, deck: Deck) -> str:
        template = self.env.get_template("deck.html.j2")
        return template.render(deck=deck)
```
# File: src/dmforge/domain/__init__.py
```python
```
# File: src/dmforge/domain/models.py
```python
# domain/models.py
"""
Domain models for DMForge: SpellCard, Deck, DeckOptions
These are pure Python types with no dependencies or side effects.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class SpellCard:
    """A single spell card with optional art."""

    name: str
    level: int
    school: str
    classes: List[str]
    description: str
    duration: str
    art_path: Optional[str] = None  # Local image path or None


@dataclass(frozen=True)
class Deck:
    """A collection of spell cards with metadata."""

    name: str
    cards: List[SpellCard]
    version: str = "v1"

    def to_dict(self) -> dict:
        """Convert the deck to a dict for serialization."""
        return {
            "name": self.name,
            "version": self.version,
            "cards": [card.__dict__ for card in self.cards],
        }

    def to_json(self) -> str:
        """Convert the deck to a JSON string (requires manual import in adapter)."""
        import json

        return json.dumps(self.to_dict(), indent=2)


@dataclass(frozen=True)
class DeckOptions:
    """Filter criteria for building a deck."""

    classes: List[str] = field(default_factory=list)
    levels: List[int] = field(default_factory=list)
    schools: List[str] = field(default_factory=list)
    name: str = "Untitled Deck"
```
# File: src/dmforge/infrastructure/__init__.py
```python
```
# File: src/dmforge/infrastructure/repository/__init__.py
```python
```
# File: src/dmforge/infrastructure/repository/json_deck_storage.py
```python
import json
from pathlib import Path

from dmforge.application.ports.deck_storage import DeckStorage
from dmforge.domain.models import Deck, SpellCard


class JSONDeckStorage(DeckStorage):
    def save(self, deck: Deck, path: Path) -> None:
        path.write_text(deck.to_json(), encoding="utf-8")

    def load(self, path: Path) -> Deck:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Deck(
            name=data["name"],
            version=data["version"],
            cards=[SpellCard(**card) for card in data["cards"]],
        )
```
# File: src/dmforge/infrastructure/repository/json_spell_repository.py
```python
import json
from pathlib import Path


class JSONSpellRepository:
    def __init__(self, path: Path):
        self.path = path

    def load_all_spells(self) -> list[dict]:
        if not self.path.exists():
            raise FileNotFoundError(f"Spell data file not found: {self.path}")
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected a list of spells in the JSON file.")
        return data
```
# File: src/dmforge/interface/cli/deck_build.py
```python
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from dmforge.application.controllers.deck_controller import DeckController
from dmforge.application.services.deck_builder import BasicDeckBuilder
from dmforge.infrastructure.repository.json_spell_repository import JSONSpellRepository

app = typer.Typer()


@app.command()
def build(
    spell_data: Annotated[Path, typer.Option("--spell-data", help="Path to spell JSON")] = Path(
        "data/spells/spells.json"
    ),
    output: Annotated[Path, typer.Option("--output", help="Path to save deck JSON")] = None,
    name: Annotated[str, typer.Option("--name", help="Deck name")] = "Untitled Deck",
    classes: Annotated[
        Optional[list[str]], typer.Option("--class", "-c", help="Class filters")
    ] = None,
    levels: Annotated[
        Optional[list[int]], typer.Option("--level", "-l", help="Level filters")
    ] = None,
    schools: Annotated[
        Optional[list[str]], typer.Option("--school", "-s", help="School filters")
    ] = None,
):
    """
    Build a filtered deck of spells from input data.
    """
    # Validate spell_data file exists
    if not spell_data.exists():
        typer.echo(f"❌ Spell data not found at: {spell_data}", err=True)
        raise typer.Exit(1)

    # Default output file if not provided
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = Path(f"exports/dev/deck_{timestamp}.json")

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    classes = classes or []
    levels = levels or []
    schools = schools or []

    repo = JSONSpellRepository(spell_data)
    builder = BasicDeckBuilder(repo)
    controller = DeckController(builder)

    options_dict = {
        "name": name,
        "classes": classes,
        "levels": levels,
        "schools": schools,
    }

    deck = controller.build_from_cli(options_dict)
    output.write_text(deck.to_json(), encoding="utf-8")
    typer.echo(f"✅ Deck saved to: {output}")
```