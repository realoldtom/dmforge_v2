from pathlib import Path
from typing import Protocol

from dmforge.domain.models import Deck


class DeckStorage(Protocol):
    def save(self, deck: Deck, path: Path) -> None: ...
    def load(self, path: Path) -> Deck: ...
