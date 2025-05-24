# main.py
import typer
from dmforge.interface.cli import deck_build, deck_render

app = typer.Typer()

# Mount subcommands
app.add_typer(deck_build.app, name="deck")
app.add_typer(deck_render.app, name="render")

if __name__ == "__main__":
    app()
