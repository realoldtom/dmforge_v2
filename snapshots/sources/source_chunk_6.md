# File: tests/infrastructure/repository/test_json_spell_repository.py
```python
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
```
# File: tests/interface/cli/test_deck_build.py
```python
import json

from dmforge.interface.cli.deck_build import app
from typer.testing import CliRunner

runner = CliRunner()


def test_build_basic_deck(tmp_path):
    # Arrange: input spell data
    spell_data = tmp_path / "spells.json"
    spell_data.write_text(
        json.dumps(
            [
                {
                    "name": "Magic Missile",
                    "level": 1,
                    "school": "Evocation",
                    "classes": ["Wizard"],
                    "desc": "Shoots darts of magical force.",
                    "duration": "Instantaneous",
                },
                {
                    "name": "Cure Wounds",
                    "level": 1,
                    "school": "Evocation",
                    "classes": ["Cleric"],
                    "desc": "Heals a creature you touch.",
                    "duration": "Instantaneous",
                },
            ]
        ),
        encoding="utf-8",
    )

    output_path = tmp_path / "deck.json"

    # Act: call the CLI
    result = runner.invoke(
        app, ["--spell-data", str(spell_data), "--output", str(output_path), "--class", "Wizard"]
    )
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    # Assert: CLI succeeded and output file matches snapshot
    assert result.exit_code == 0
    assert output_path.exists()

    generated = json.loads(output_path.read_text(encoding="utf-8"))

    expected = {
        "name": "Untitled Deck",
        "version": "v1",
        "cards": [
            {
                "name": "Magic Missile",
                "level": 1,
                "school": "Evocation",
                "classes": ["Wizard"],
                "description": "Shoots darts of magical force.",
                "duration": "Instantaneous",
                "art_path": None,
            }
        ],
    }

    assert generated == expected
```