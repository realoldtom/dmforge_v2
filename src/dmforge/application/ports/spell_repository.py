from typing import Protocol


class SpellRepository(Protocol):
    def load_all_spells(self) -> list[dict]: ...
