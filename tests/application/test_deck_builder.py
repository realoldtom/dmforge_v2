from dmforge.application.services.deck_builder import BasicDeckBuilder
from dmforge.domain.models import DeckOptions


class FakeSpellRepository:
    def load_all_spells(self) -> list[dict]:
        return [
            {
                "name": "Fireball",
                "level": 3,
                "school": "Evocation",
                "classes": ["Wizard", "Sorcerer"],
                "desc": "Boom.",
                "duration": "Instant",
            },
            {
                "name": "Cure Wounds",
                "level": 1,
                "school": "Evocation",
                "classes": ["Cleric"],
                "desc": "Heals HP.",
                "duration": "Instant",
            },
            {
                "name": "Invisibility",
                "level": 2,
                "school": "Illusion",
                "classes": ["Wizard"],
                "desc": "Become unseen.",
                "duration": "1 hour",
            },
        ]


def test_deck_builder_filters_by_class():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(classes=["Cleric"])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Cure Wounds"


def test_deck_builder_filters_by_level():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(levels=[3])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Fireball"


def test_deck_builder_filters_by_school():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions(schools=["Illusion"])
    deck = builder.build(options)
    assert len(deck.cards) == 1
    assert deck.cards[0].name == "Invisibility"


def test_deck_builder_with_no_filters():
    builder = BasicDeckBuilder(FakeSpellRepository())
    options = DeckOptions()
    deck = builder.build(options)
    assert len(deck.cards) == 3
    names = [c.name for c in deck.cards]
    assert "Fireball" in names
    assert "Cure Wounds" in names
    assert "Invisibility" in names
