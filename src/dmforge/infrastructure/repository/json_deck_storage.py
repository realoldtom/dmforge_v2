import json
from pathlib import Path

from dmforge.application.ports.deck_storage import DeckStorage
from dmforge.domain.models import Deck, SpellCard


class JSONDeckStorage(DeckStorage):
    def save(self, deck: Deck, path: Path) -> None:
        path.write_text(deck.to_json(), encoding="utf-8")

    def load(self, path: Path) -> Deck:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Deck(
            name=data["name"],
            version=data["version"],
            cards=[SpellCard(**card) for card in data["cards"]],
        )
