import json
from pathlib import Path

import pytest
from dmforge.infrastructure.repository.json_spell_repository import JSONSpellRepository


def test_load_all_spells(tmp_path: Path):
    spell_data = [
        {
            "name": "Magic Missile",
            "level": 1,
            "school": "Evocation",
            "classes": ["Wizard"],
            "desc": "Shoots darts",
            "duration": "Instant",
        },
        {
            "name": "Shield",
            "level": 1,
            "school": "Abjuration",
            "classes": ["Wizard"],
            "desc": "Adds AC",
            "duration": "1 round",
        },
    ]
    file_path = tmp_path / "spells.json"
    file_path.write_text(json.dumps(spell_data), encoding="utf-8")

    repo = JSONSpellRepository(file_path)
    result = repo.load_all_spells()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Magic Missile"


def test_missing_file_raises(tmp_path: Path):
    file_path = tmp_path / "nonexistent.json"
    repo = JSONSpellRepository(file_path)
    with pytest.raises(FileNotFoundError):
        repo.load_all_spells()


def test_invalid_data_raises(tmp_path: Path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"not": "a list"}', encoding="utf-8")

    repo = JSONSpellRepository(file_path)
    with pytest.raises(ValueError):
        repo.load_all_spells()
