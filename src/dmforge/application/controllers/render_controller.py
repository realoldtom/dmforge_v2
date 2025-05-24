from pathlib import Path

from dmforge.application.ports.deck_storage import DeckStorage
from dmforge.application.ports.render_service import RenderService


class RenderController:
    def __init__(self, renderer: RenderService, storage: DeckStorage):
        self.renderer = renderer
        self.storage = storage

    def render_from_file(self, input_path: Path, fmt: str, output_path: Path) -> None:
        deck = self.storage.load(input_path)
        if fmt == "pdf":
            self.renderer.render_pdf(deck, output_path)
        elif fmt == "html":
            self.renderer.render_html(deck, output_path)
        else:
            raise ValueError(f"Unsupported format: {fmt}")
