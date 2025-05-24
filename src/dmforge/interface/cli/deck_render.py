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