from pathlib import Path
from dmforge.domain.models import Deck
from typing import Protocol

class DeckStorage(Protocol):
    def save(self, deck: Deck, path: Path) -> None: ...
    def load(self, path: Path) -> Deck: ...
