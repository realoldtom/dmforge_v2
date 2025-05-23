from dmforge.domain.models import Deck, DeckOptions, SpellCard


def test_spell_card_creation():
    card = SpellCard(
        name="Magic Missile",
        level=1,
        school="Evocation",
        classes=["Wizard"],
        description="A bolt of force darts toward the target.",
        duration="Instantaneous",
    )
    assert card.name == "Magic Missile"
    assert card.level == 1
    assert card.school == "Evocation"
    assert card.art_path is None


def test_deck_serialization():
    card = SpellCard(
        name="Magic Missile",
        level=1,
        school="Evocation",
        classes=["Wizard"],
        description="A bolt of force darts toward the target.",
        duration="Instantaneous",
    )
    deck = Deck(name="Test Deck", cards=[card])
    deck_dict = deck.to_dict()
    assert deck_dict["name"] == "Test Deck"
    assert deck_dict["version"] == "v1"
    assert isinstance(deck_dict["cards"], list)
    assert deck_dict["cards"][0]["name"] == "Magic Missile"

    deck_json = deck.to_json()
    assert '"name": "Magic Missile"' in deck_json


def test_deck_options_defaults():
    options = DeckOptions()
    assert options.classes == []
    assert options.levels == []
    assert options.schools == []
    assert options.name == "Untitled Deck"


def test_deck_options_custom_values():
    options = DeckOptions(classes=["Wizard", "Cleric"], levels=[1, 2], schools=["Evocation"])
    assert options.classes == ["Wizard", "Cleric"]
    assert options.levels == [1, 2]
    assert options.schools == ["Evocation"]
