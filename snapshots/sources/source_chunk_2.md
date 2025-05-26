# FILE: src/dmforge/application/services/deck_builder.py
```python
from typing import Protocol

from dmforge.application.ports.spell_repository import SpellRepository
from dmforge.domain.models import Deck, DeckOptions, SpellCard


class DeckBuilder(Protocol):
    def build(self, options: DeckOptions) -> Deck: ...


class BasicDeckBuilder:
    def __init__(self, repository: SpellRepository):
        self.repository = repository

    def build(self, options: DeckOptions) -> Deck:
        spells = self.repository.load_all_spells()
        filtered = self._apply_filters(spells, options)
        cards = [self._to_card(spell) for spell in filtered]
        return Deck(name=options.name, cards=cards)

    def _apply_filters(self, spells: list[dict], options: DeckOptions) -> list[dict]:
        return [
            spell
            for spell in spells
            if (
                not options.classes
                or any(cls in spell.get("classes", []) for cls in options.classes)
            )
            and (not options.levels or spell.get("level") in options.levels)
            and (not options.schools or spell.get("school") in options.schools)
        ]

    def _to_card(self, spell: dict) -> SpellCard:
        return SpellCard(
            name=spell.get("name", "Unknown"),
            level=spell.get("level", 0),
            school=spell.get("school", "Unknown"),
            classes=spell.get("classes", []),
            description=spell.get("desc", ""),
            duration=spell.get("duration", "Instantaneous"),
        )
```

# FILE: src/dmforge/application/services/weasy_renderer.py
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

# FILE: src/dmforge/application/services/weasy_renderer.py
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

# FILE: src/dmforge/domain/__init__.py
```python

```

# FILE: src/dmforge/domain/__init__.py
```python

```

# FILE: src/dmforge/domain/models.py
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

# FILE: src/dmforge/domain/models.py
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

# FILE: src/dmforge/infrastructure/__init__.py
```python

```

# FILE: src/dmforge/infrastructure/__init__.py
```python

```

# FILE: src/dmforge/infrastructure/repository/__init__.py
```python

```

# FILE: src/dmforge/infrastructure/repository/__init__.py
```python

```

# FILE: src/dmforge/infrastructure/repository/json_deck_storage.py
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

# FILE: src/dmforge/infrastructure/repository/json_deck_storage.py
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

# FILE: src/dmforge/infrastructure/repository/json_spell_repository.py
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

# FILE: src/dmforge/infrastructure/repository/json_spell_repository.py
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

# FILE: src/dmforge/interface/cli/deck_build.py
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

# FILE: src/dmforge/interface/cli/deck_build.py
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

# FILE: src/dmforge/interface/cli/deck_render.py
```python
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer
from dmforge.application.controllers.render_controller import RenderController
from dmforge.application.services.weasy_renderer import WeasyRenderer
from dmforge.infrastructure.repository.json_deck_storage import JSONDeckStorage

# Top-level app used by main.py as "render"
app = typer.Typer()


@app.command()
def render(
    input: Annotated[Path, typer.Option("--input", help="Path to deck JSON file")] = Path(
        "exports/dev/deck_latest.json"
    ),
    output: Annotated[
        Path, typer.Option("--output", help="Path to rendered output (PDF or HTML)")
    ] = None,
    format: Annotated[
        str, typer.Option("--format", "-f", help="Output format: pdf or html")
    ] = "pdf",
    template_dir: Annotated[
        Path, typer.Option("--template-dir", help="Path to templates directory")
    ] = Path("src/dmforge/resources/templates"),
    asset_dir: Annotated[Path, typer.Option("--asset-dir", help="Path to assets directory")] = Path(
        "src/dmforge/resources/assets"
    ),
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
):
    """
    Render a deck as a PDF or HTML using the given JSON input.
    """
    try:
        if not input.exists():
            typer.echo(f"❌ Input file not found: {input}", err=True)
            raise

        if not template_dir.exists():
            typer.echo(f"❌ Template directory not found: {template_dir}", err=True)
            raise

        format_lower = format.lower()
        if format_lower not in ["pdf", "html"]:
            typer.echo(f"❌ Unsupported format: {format}. Use 'pdf' or 'html'", err=True)
            raise

        if output is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = Path(f"exports/dev/render_{timestamp}.{format_lower}")

        output.parent.mkdir(parents=True, exist_ok=True)

        renderer = WeasyRenderer(template_dir=template_dir, asset_dir=asset_dir, verbose=verbose)
        storage = JSONDeckStorage()
        controller = RenderController(renderer, storage)

        if verbose:
            typer.echo(f"🔧 Input:        {input}")
            typer.echo(f"🔧 Output:       {output}")
            typer.echo(f"🔧 Format:       {format_lower}")
            typer.echo(f"🔧 Template dir: {template_dir}")
            typer.echo(f"🔧 Asset dir:    {asset_dir}")

        controller.render_from_file(input_path=input, fmt=format_lower, output_path=output)
        typer.echo(f"✅ Rendered {format.upper()} to: {output}")

    except Exception as e:
        typer.echo(f"❌ Error during rendering: {str(e)}", err=True)
        if verbose:
            import traceback

            typer.echo(traceback.format_exc(), err=True)
        raise


@app.command()
def validate(
    input: Annotated[Path, typer.Option("--input", help="Path to deck JSON file")] = Path(
        "exports/dev/deck_latest.json"
    ),
):
    """
    Validate a deck JSON file without rendering.
    """
    try:
        if not input.exists():
            typer.echo(f"❌ Input file not found: {input}", err=True)
            raise

        storage = JSONDeckStorage()
        deck = storage.load(input)
        typer.echo(f"✅ Valid deck with {len(deck.cards)} cards")

    except Exception as e:
        typer.echo(f"❌ Validation failed: {str(e)}", err=True)
        raise


if __name__ == "__main__":
    app()
```

# FILE: src/dmforge/interface/cli/deck_render.py
```python
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer
from dmforge.application.controllers.render_controller import RenderController
from dmforge.application.services.weasy_renderer import WeasyRenderer
from dmforge.infrastructure.repository.json_deck_storage import JSONDeckStorage

# Top-level app used by main.py as "render"
app = typer.Typer()


@app.command()
def render(
    input: Annotated[Path, typer.Option("--input", help="Path to deck JSON file")] = Path(
        "exports/dev/deck_latest.json"
    ),
    output: Annotated[
        Path, typer.Option("--output", help="Path to rendered output (PDF or HTML)")
    ] = None,
    format: Annotated[
        str, typer.Option("--format", "-f", help="Output format: pdf or html")
    ] = "pdf",
    template_dir: Annotated[
        Path, typer.Option("--template-dir", help="Path to templates directory")
    ] = Path("src/dmforge/resources/templates"),
    asset_dir: Annotated[Path, typer.Option("--asset-dir", help="Path to assets directory")] = Path(
        "src/dmforge/resources/assets"
    ),
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
):
    """
    Render a deck as a PDF or HTML using the given JSON input.
    """
    try:
        if not input.exists():
            typer.echo(f"❌ Input file not found: {input}", err=True)
            raise

        if not template_dir.exists():
            typer.echo(f"❌ Template directory not found: {template_dir}", err=True)
            raise

        format_lower = format.lower()
        if format_lower not in ["pdf", "html"]:
            typer.echo(f"❌ Unsupported format: {format}. Use 'pdf' or 'html'", err=True)
            raise

        if output is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = Path(f"exports/dev/render_{timestamp}.{format_lower}")

        output.parent.mkdir(parents=True, exist_ok=True)

        renderer = WeasyRenderer(template_dir=template_dir, asset_dir=asset_dir, verbose=verbose)
        storage = JSONDeckStorage()
        controller = RenderController(renderer, storage)

        if verbose:
            typer.echo(f"🔧 Input:        {input}")
            typer.echo(f"🔧 Output:       {output}")
            typer.echo(f"🔧 Format:       {format_lower}")
            typer.echo(f"🔧 Template dir: {template_dir}")
            typer.echo(f"🔧 Asset dir:    {asset_dir}")

        controller.render_from_file(input_path=input, fmt=format_lower, output_path=output)
        typer.echo(f"✅ Rendered {format.upper()} to: {output}")

    except Exception as e:
        typer.echo(f"❌ Error during rendering: {str(e)}", err=True)
        if verbose:
            import traceback

            typer.echo(traceback.format_exc(), err=True)
        raise


@app.command()
def validate(
    input: Annotated[Path, typer.Option("--input", help="Path to deck JSON file")] = Path(
        "exports/dev/deck_latest.json"
    ),
):
    """
    Validate a deck JSON file without rendering.
    """
    try:
        if not input.exists():
            typer.echo(f"❌ Input file not found: {input}", err=True)
            raise

        storage = JSONDeckStorage()
        deck = storage.load(input)
        typer.echo(f"✅ Valid deck with {len(deck.cards)} cards")

    except Exception as e:
        typer.echo(f"❌ Validation failed: {str(e)}", err=True)
        raise


if __name__ == "__main__":
    app()
```

# FILE: tests/__init__.py
```python

```

# FILE: tests/__init__.py
```python

```

# FILE: tests/application/__init__.py
```python

```

# FILE: tests/application/__init__.py
```python

```

# FILE: tests/application/ports/__init__.py
```python

```

# FILE: tests/application/ports/__init__.py
```python

```

# FILE: tests/application/ports/test_spell_repository_contract.py
```python
import tempfile
from pathlib import Path

from dmforge.application.ports.spell_repository import SpellRepository
from dmforge.infrastructure.repository.json_spell_repository import JSONSpellRepository


def test_json_repository_implements_protocol():
    path = Path(tempfile.gettempdir()) / "fake.json"
    impl: SpellRepository = JSONSpellRepository(path)
    assert hasattr(impl, "load_all_spells")
    assert callable(impl.load_all_spells)
```

# FILE: tests/application/ports/test_spell_repository_contract.py
```python
import tempfile
from pathlib import Path

from dmforge.application.ports.spell_repository import SpellRepository
from dmforge.infrastructure.repository.json_spell_repository import JSONSpellRepository


def test_json_repository_implements_protocol():
    path = Path(tempfile.gettempdir()) / "fake.json"
    impl: SpellRepository = JSONSpellRepository(path)
    assert hasattr(impl, "load_all_spells")
    assert callable(impl.load_all_spells)
```

# FILE: tests/application/test_deck_builder.py
```python
from dmforge.application.services.deck_builder import BasicDeckBuilder
from dmforge.domain.models import DeckOptions


class FakeSpellRepository:
    def load_all_spells(self) -> list[dict]:
        return [
            {
                "name": "Fireball",
                "level": 3,
                "school": "Evocation",
                "classes": ["Wizard", "Sorcerer"],
                "desc": "Boom.",
                "duration": "Instant",
            },
            {
                "name": "Cure Wounds",
                "level": 1,
                "school": "Evocation",
                "classes": ["Cleric"],
                "desc": "Heals HP.",
                "duration": "Instant",
            },
            {
                "name": "Invisibility",
                "level": 2,
                "school": "Illusion",
                "classes": ["Wizard"],
                "desc": "Become unseen.",
                "duration": "1 hour",
            },
        ]


def test_deck_builder_filters_by_class():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(classes=["Cleric"])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Cure Wounds"


def test_deck_builder_filters_by_level():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(levels=[3])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Fireball"


def test_deck_builder_filters_by_school():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(schools=["Illusion"])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Invisibility"


def test_deck_builder_with_no_filters():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions()
    deck = builder.build(options)
    assert len(deck.cards) == 3
    names = [c.name for c in deck.cards]
    assert "Fireball" in names
    assert "Cure Wounds" in names
    assert "Invisibility" in names
```

# FILE: tests/application/test_deck_builder.py
```python
from dmforge.application.services.deck_builder import BasicDeckBuilder
from dmforge.domain.models import DeckOptions


class FakeSpellRepository:
    def load_all_spells(self) -> list[dict]:
        return [
            {
                "name": "Fireball",
                "level": 3,
                "school": "Evocation",
                "classes": ["Wizard", "Sorcerer"],
                "desc": "Boom.",
                "duration": "Instant",
            },
            {
                "name": "Cure Wounds",
                "level": 1,
                "school": "Evocation",
                "classes": ["Cleric"],
                "desc": "Heals HP.",
                "duration": "Instant",
            },
            {
                "name": "Invisibility",
                "level": 2,
                "school": "Illusion",
                "classes": ["Wizard"],
                "desc": "Become unseen.",
                "duration": "1 hour",
            },
        ]


def test_deck_builder_filters_by_class():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(classes=["Cleric"])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Cure Wounds"


def test_deck_builder_filters_by_level():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(levels=[3])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Fireball"


def test_deck_builder_filters_by_school():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(schools=["Illusion"])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Invisibility"


def test_deck_builder_with_no_filters():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions()
    deck = builder.build(options)
    assert len(deck.cards) == 3
    names = [c.name for c in deck.cards]
    assert "Fireball" in names
    assert "Cure Wounds" in names
    assert "Invisibility" in names
```

# FILE: tests/domain/__init__.py
```python

```

# FILE: tests/domain/__init__.py
```python

```

# FILE: tests/domain/test_models.py
```python
from dmforge.domain.models import Deck, DeckOptions, SpellCard


def test_spell_card_creation():
    card = SpellCard(
        name="Magic Missile",
        level=1,
        school="Evocation",
        classes=["Wizard"],
        description="A bolt of force darts toward the target.",
        duration="Instantaneous",
    )
    assert card.name == "Magic Missile"
    assert card.level == 1
    assert card.school == "Evocation"
    assert card.art_path is None


def test_deck_serialization():
    card = SpellCard(
        name="Magic Missile",
        level=1,
        school="Evocation",
        classes=["Wizard"],
        description="A bolt of force darts toward the target.",
        duration="Instantaneous",
    )
    deck = Deck(name="Test Deck", cards=[card])
    deck_dict = deck.to_dict()
    assert deck_dict["name"] == "Test Deck"
    assert deck_dict["version"] == "v1"
    assert isinstance(deck_dict["cards"], list)
    assert deck_dict["cards"][0]["name"] == "Magic Missile"

    deck_json = deck.to_json()
    assert '"name": "Magic Missile"' in deck_json


def test_deck_options_defaults():
    options = DeckOptions()
    assert options.classes == []
    assert options.levels == []
    assert options.schools == []
    assert options.name == "Untitled Deck"


def test_deck_options_custom_values():
    options = DeckOptions(classes=["Wizard", "Cleric"], levels=[1, 2], schools=["Evocation"])
    assert options.classes == ["Wizard", "Cleric"]
    assert options.levels == [1, 2]
    assert options.schools == ["Evocation"]
```

# FILE: tests/domain/test_models.py
```python
from dmforge.domain.models import Deck, DeckOptions, SpellCard


def test_spell_card_creation():
    card = SpellCard(
        name="Magic Missile",
        level=1,
        school="Evocation",
        classes=["Wizard"],
        description="A bolt of force darts toward the target.",
        duration="Instantaneous",
    )
    assert card.name == "Magic Missile"
    assert card.level == 1
    assert card.school == "Evocation"
    assert card.art_path is None


def test_deck_serialization():
    card = SpellCard(
        name="Magic Missile",
        level=1,
        school="Evocation",
        classes=["Wizard"],
        description="A bolt of force darts toward the target.",
        duration="Instantaneous",
    )
    deck = Deck(name="Test Deck", cards=[card])
    deck_dict = deck.to_dict()
    assert deck_dict["name"] == "Test Deck"
    assert deck_dict["version"] == "v1"
    assert isinstance(deck_dict["cards"], list)
    assert deck_dict["cards"][0]["name"] == "Magic Missile"

    deck_json = deck.to_json()
    assert '"name": "Magic Missile"' in deck_json


def test_deck_options_defaults():
    options = DeckOptions()
    assert options.classes == []
    assert options.levels == []
    assert options.schools == []
    assert options.name == "Untitled Deck"


def test_deck_options_custom_values():
    options = DeckOptions(classes=["Wizard", "Cleric"], levels=[1, 2], schools=["Evocation"])
    assert options.classes == ["Wizard", "Cleric"]
    assert options.levels == [1, 2]
    assert options.schools == ["Evocation"]
```