from pathlib import Path
from typing import Protocol
from dmforge.domain.models import Deck

class RenderService(Protocol):
    def render_pdf(self, deck: Deck, output_path: Path) -> None: ...
    def render_html(self, deck: Deck, output_path: Path) -> None: ...
