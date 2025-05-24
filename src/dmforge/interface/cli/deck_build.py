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
