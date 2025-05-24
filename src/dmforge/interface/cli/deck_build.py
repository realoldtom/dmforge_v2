from pathlib import Path
from typing import Annotated, Optional

import typer
from dmforge.application.controllers.deck_controller import DeckController
from dmforge.application.services.deck_builder import BasicDeckBuilder
from dmforge.infrastructure.repository.json_spell_repository import JSONSpellRepository

app = typer.Typer()


@app.command()
def build(
    spell_data: Annotated[Path, typer.Option("--spell-data", help="Path to spell JSON")],
    output: Annotated[Path, typer.Option("--output", help="Path to save deck JSON")],
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
