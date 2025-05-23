from typing import Protocol

from dmforge.application.ports.spell_repository import SpellRepository
from dmforge.domain.models import Deck, DeckOptions, SpellCard


class DeckBuilder(Protocol):
    def build(self, options: DeckOptions) -> Deck: ...


class BasicDeckBuilder:
    def __init__(self, repository: SpellRepository):
        self.repository = repository

    def build(self, options: DeckOptions) -> Deck:
        spells = self.repository.load_all_spells()
        filtered = self._apply_filters(spells, options)
        cards = [self._to_card(spell) for spell in filtered]
        return Deck(name=options.name, cards=cards)

    def _apply_filters(self, spells: list[dict], options: DeckOptions) -> list[dict]:
        return [
            s
            for s in spells
            if (not options.classes or any(cls in s.get("classes", []) for cls in options.classes))
            and (not options.levels or s.get("level") in options.levels)
            and (not options.schools or s.get("school") in options.schools)
        ]

    def _to_card(self, spell: dict) -> SpellCard:
        return SpellCard(
            name=spell.get("name", "Unknown"),
            level=spell.get("level", 0),
            school=spell.get("school", "Unknown"),
            classes=spell.get("classes", []),
            description=spell.get("desc", ""),
            duration=spell.get("duration", "Instantaneous"),
        )
