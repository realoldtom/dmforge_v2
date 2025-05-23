import json
from pathlib import Path


class JSONSpellRepository:
    def __init__(self, path: Path):
        self.path = path

    def load_all_spells(self) -> list[dict]:
        if not self.path.exists():
            raise FileNotFoundError(f"Spell data file not found: {self.path}")
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected a list of spells in the JSON file.")
        return data
