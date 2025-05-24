# File: src/dmforge/interface/cli/deck_render.py
```python
# cli.py
from pathlib import Path
from typing import Annotated
import typer
import sys

from dmforge.application.controllers.render_controller import RenderController
from dmforge.infrastructure.repository.json_deck_storage import JSONDeckStorage
from dmforge.application.services.weasy_renderer import WeasyRenderer

app = typer.Typer()

@app.command()
def render(
    input: Annotated[Path, typer.Option("--input", help="Path to deck JSON file")],
    output: Annotated[Path, typer.Option("--output", help="Path to rendered output (PDF or HTML)")],
    format: Annotated[str, typer.Option("--format", "-f", help="Output format: pdf or html")] = "pdf",
    template_dir: Annotated[Path, typer.Option("--template-dir", help="Path to templates directory")] = Path("templates"),
    asset_dir: Annotated[Path, typer.Option("--asset-dir", help="Path to assets directory")] = Path("assets"),
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
):
    """
    Render a deck as a PDF or HTML using the given JSON input.
    """
    try:
        # Validate inputs
        if not input.exists():
            typer.echo(f"❌ Input file not found: {input}", err=True)
            raise typer.Exit(1)
        
        if not template_dir.exists():
            typer.echo(f"❌ Template directory not found: {template_dir}", err=True)
            raise typer.Exit(1)
        
        # Validate format
        format_lower = format.lower()
        if format_lower not in ["pdf", "html"]:
            typer.echo(f"❌ Unsupported format: {format}. Use 'pdf' or 'html'", err=True)
            raise typer.Exit(1)
        
        # Create output directory if it doesn't exist
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        renderer = WeasyRenderer(
            template_dir=template_dir, 
            asset_dir=asset_dir,
            verbose=verbose
        )
        storage = JSONDeckStorage()
        controller = RenderController(renderer, storage)

        if verbose:
            typer.echo(f"🔧 Input: {input}")
            typer.echo(f"🔧 Output: {output}")
            typer.echo(f"🔧 Format: {format_lower}")
            typer.echo(f"🔧 Template dir: {template_dir}")
            typer.echo(f"🔧 Asset dir: {asset_dir}")

        # Render
        controller.render_from_file(input_path=input, fmt=format_lower, output_path=output)
        typer.echo(f"✅ Rendered {format.upper()} to: {output}")
        
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(traceback.format_exc(), err=True)
        raise typer.Exit(1)


@app.command()
def validate(
    input: Annotated[Path, typer.Option("--input", help="Path to deck JSON file")],
):
    """
    Validate a deck JSON file without rendering.
    """
    try:
        if not input.exists():
            typer.echo(f"❌ Input file not found: {input}", err=True)
            raise typer.Exit(1)
        
        storage = JSONDeckStorage()
        deck = storage.load(input)
        typer.echo(f"✅ Valid deck with {len(deck.cards)} cards")
        
    except Exception as e:
        typer.echo(f"❌ Validation failed: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
```
# File: tests/__init__.py
```python
```
# File: tests/application/__init__.py
```python
```
# File: tests/application/ports/__init__.py
```python
```
# File: tests/application/ports/test_spell_repository_contract.py
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
# File: tests/application/test_deck_builder.py
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
# File: tests/domain/__init__.py
```python
```
# File: tests/domain/test_models.py
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