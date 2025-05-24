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
