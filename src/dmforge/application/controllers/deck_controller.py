from dmforge.application.services.deck_builder import DeckBuilder
from dmforge.domain.models import Deck, DeckOptions


class DeckController:
    def __init__(self, builder: DeckBuilder):
        self.builder = builder

    def build_from_cli(self, options_dict: dict) -> Deck:
        """
        Accepts raw dict from CLI, converts to typed DeckOptions, returns Deck.
        """
        options = DeckOptions(
            name=options_dict.get("name", "Untitled Deck"),
            classes=options_dict.get("classes", []),
            levels=options_dict.get("levels", []),
            schools=options_dict.get("schools", []),
        )
        return self.builder.build(options)
