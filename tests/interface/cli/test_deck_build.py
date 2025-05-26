import json

from dmforge.interface.cli.deck_build import app
from typer.testing import CliRunner

runner = CliRunner(mix_stderr=False)


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
