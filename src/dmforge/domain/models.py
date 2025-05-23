# domain/models.py
"""
Domain models for DMForge: SpellCard, Deck, DeckOptions
These are pure Python types with no dependencies or side effects.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class SpellCard:
    """A single spell card with optional art."""

    name: str
    level: int
    school: str
    classes: List[str]
    description: str
    duration: str
    art_path: Optional[str] = None  # Local image path or None


@dataclass(frozen=True)
class Deck:
    """A collection of spell cards with metadata."""

    name: str
    cards: List[SpellCard]
    version: str = "v1"

    def to_dict(self) -> dict:
        """Convert the deck to a dict for serialization."""
        return {
            "name": self.name,
            "version": self.version,
            "cards": [card.__dict__ for card in self.cards],
        }

    def to_json(self) -> str:
        """Convert the deck to a JSON string (requires manual import in adapter)."""
        import json

        return json.dumps(self.to_dict(), indent=2)


@dataclass(frozen=True)
class DeckOptions:
    """Filter criteria for building a deck."""

    classes: List[str] = field(default_factory=list)
    levels: List[int] = field(default_factory=list)
    schools: List[str] = field(default_factory=list)
    name: str = "Untitled Deck"
