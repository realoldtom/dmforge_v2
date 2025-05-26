# FILE: tests/infrastructure/repository/test_json_spell_repository.py
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

# FILE: tests/infrastructure/repository/test_json_spell_repository.py
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

# FILE: tests/interface/cli/test_deck_build.py
```python
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
```

# FILE: tests/interface/cli/test_deck_build.py
```python
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
```

# FILE: tests/interface/cli/test_deck_render.py
```python
import json
import shutil
from pathlib import Path

import pytest
from dmforge.interface.cli.deck_render import app
from typer.testing import CliRunner

runner = CliRunner(mix_stderr=False)


def copy_template_to(tmp_template_dir: Path):
    real_template = Path("src/dmforge/resources/templates/deck.html.j2")
    assert real_template.exists(), "❌ Template missing: deck.html.j2"
    tmp_template_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(real_template, tmp_template_dir / "deck.html.j2")


def create_test_deck_file(path: Path, custom_data=None):
    """Create a test deck JSON file with optional custom data."""
    deck_data = custom_data or {
        "name": "Test Deck",
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
            },
            {
                "name": "Fireball",
                "level": 3,
                "school": "Evocation",
                "classes": ["Wizard", "Sorcerer"],
                "description": "A bright streak flashes from your pointing finger to a point you choose.",
                "duration": "Instantaneous",
                "art_path": "fireball.png",
            },
        ],
    }
    path.write_text(json.dumps(deck_data, indent=2), encoding="utf-8")


def create_test_template(template_dir: Path):
    """Create a minimal test template."""
    template_dir.mkdir(parents=True, exist_ok=True)
    template_file = template_dir / "deck.html.j2"

    template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ deck.name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ccc; margin: 20px 0; padding: 15px; border-radius: 5px; }
        .card-name { font-size: 1.2em; font-weight: bold; color: #2c5aa0; }
        .card-level { color: #666; font-style: italic; }
        .card-description { margin-top: 10px; line-height: 1.4; }
        .deck-header { border-bottom: 2px solid #2c5aa0; padding-bottom: 10px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="deck-header">
        <h1>{{ deck.name }}</h1>
        <p>Version: {{ deck.version }}</p>
        <p>Cards: {{ deck.cards|length }}</p>
    </div>
    
    <div class="cards">
        {% for card in deck.cards %}
        <div class="card">
            <div class="card-name">{{ card.name }}</div>
            <div class="card-level">Level {{ card.level }} {{ card.school }}</div>
            <div class="card-classes">Classes: {{ card.classes|join(', ') }}</div>
            <div class="card-description">{{ card.description }}</div>
            <div class="card-duration">Duration: {{ card.duration }}</div>
            {% if card.art_path %}
            <div class="card-art">Art: {{ card.art_path }}</div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>"""

    template_file.write_text(template_content, encoding="utf-8")
    return template_file


class TestCLI:

    def test_render_html_output(self, tmp_path):
        """Test HTML rendering with custom template."""
        # Arrange
        input_path = tmp_path / "deck.json"
        output_path = tmp_path / "output.html"
        template_dir = tmp_path / "templates"
        asset_dir = tmp_path / "assets"

        create_test_deck_file(input_path)
        create_test_template(template_dir)
        asset_dir.mkdir(exist_ok=True)

        # Act
        result = runner.invoke(
            app,
            [
                "render",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "html",
                "--template-dir",
                str(template_dir),
                "--asset-dir",
                str(asset_dir),
            ],
        )

        # Debug output
        if result.stdout:
            print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.exception:
            print("Exception:", result.exception)
            import traceback

            traceback.print_exception(
                type(result.exception), result.exception, result.exception.__traceback__
            )

        # Assert
        assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}"
        assert output_path.exists(), "Output file was not created"

        html_output = output_path.read_text(encoding="utf-8")
        assert "Magic Missile" in html_output
        assert "Fireball" in html_output
        assert "<html" in html_output.lower()
        assert "Test Deck" in html_output

    def test_render_pdf_output(self, tmp_path):
        """Test PDF rendering with custom template."""
        # Arrange
        input_path = tmp_path / "deck.json"
        output_path = tmp_path / "output.pdf"
        template_dir = tmp_path / "templates"
        asset_dir = tmp_path / "assets"

        create_test_deck_file(input_path)
        create_test_template(template_dir)
        asset_dir.mkdir(exist_ok=True)

        # Act
        result = runner.invoke(
            app,
            [
                "render",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "pdf",
                "--template-dir",
                str(template_dir),
                "--asset-dir",
                str(asset_dir),
                "--verbose",
            ],
        )

        # Debug output
        print("STDOUT:\n", result.stdout)
        if result.stderr:
            print("STDERR:\n", result.stderr)

        # Handle exceptions with specific checks
        if result.exit_code != 0:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            print("EXCEPTION:", result.exception)
            pytest.fail(f"PDF render command failed: {result.exception}")

        # Assert
        assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}"
        assert output_path.exists(), "PDF output file was not created"

        # Check file size (PDF should be reasonably sized)
        size = output_path.stat().st_size
        assert size > 1000, f"PDF file too small ({size} bytes), might be corrupted"
        assert size < 10_000_000, f"PDF file too large ({size} bytes), might indicate an issue"

    def test_validate_command(self, tmp_path):
        """Test the validate command."""
        # Arrange
        input_path = tmp_path / "deck.json"
        create_test_deck_file(input_path)

        # Act
        result = runner.invoke(app, ["validate", "--input", str(input_path)])

        # Debug output
        if result.stdout:
            print("STDOUT:", result.stdout)
        if result.exception:
            print("Exception:", result.exception)

        # Assert
        assert result.exit_code == 0
        assert "Valid deck with 2 cards" in result.stdout

    def test_invalid_input_file(self, tmp_path):
        """Test behavior with non-existent input file."""
        # Arrange
        input_path = tmp_path / "nonexistent.json"
        output_path = tmp_path / "output.html"

        # Act
        result = runner.invoke(
            app, ["render", "--input", str(input_path), "--output", str(output_path)]
        )

        # Debug output - check both stdout and stderr
        print("STDOUT:", repr(result.stdout))
        print("STDERR:", repr(result.stderr))
        print("OUTPUT:", repr(result.output))

        # Assert
        assert result.exit_code == 1
        # The error message might be in different places depending on how typer handles it
        error_text = result.stdout + result.stderr + (result.output or "")
        assert "Input file not found" in error_text or "not found" in error_text.lower()

    def test_invalid_format(self, tmp_path):
        """Test behavior with invalid format."""
        input_path = tmp_path / "deck.json"
        output_path = tmp_path / "output.xyz"
        template_dir = tmp_path / "templates"
        asset_dir = tmp_path / "assets"

        create_test_deck_file(input_path)
        create_test_template(template_dir)
        asset_dir.mkdir(exist_ok=True)

        result = runner.invoke(
            app,
            [
                "render",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "xyz",
                "--template-dir",
                str(template_dir),
                "--asset-dir",
                str(asset_dir),
            ],
        )

        print("STDOUT:", repr(result.stdout))
        print("STDERR:", repr(result.stderr))
        print("OUTPUT:", repr(result.output))

        assert result.exit_code == 1
        error_text = result.stdout + result.stderr + (result.output or "")
        assert "Unsupported format" in error_text or "format" in error_text.lower()

    def test_missing_template_directory(self, tmp_path):
        """Test behavior when template directory doesn't exist."""
        # Arrange
        input_path = tmp_path / "deck.json"
        output_path = tmp_path / "output.html"
        template_dir = tmp_path / "nonexistent_templates"

        create_test_deck_file(input_path)

        # Act
        result = runner.invoke(
            app,
            [
                "render",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--template-dir",
                str(template_dir),
            ],
        )

        # Debug output
        print("STDOUT:", repr(result.stdout))
        print("STDERR:", repr(result.stderr))
        print("OUTPUT:", repr(result.output))

        # Assert
        assert result.exit_code == 1
        error_text = result.stdout + result.stderr + (result.output or "")
        assert "Template directory not found" in error_text or "template" in error_text.lower()

    def test_verbose_output(self, tmp_path):
        """Test verbose mode output."""
        # Arrange
        input_path = tmp_path / "deck.json"
        output_path = tmp_path / "output.html"
        template_dir = tmp_path / "templates"
        asset_dir = tmp_path / "assets"

        create_test_deck_file(input_path)
        create_test_template(template_dir)
        asset_dir.mkdir(exist_ok=True)

        # Act
        result = runner.invoke(
            app,
            [
                "render",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "html",
                "--template-dir",
                str(template_dir),
                "--asset-dir",
                str(asset_dir),
                "--verbose",
            ],
        )

        # Assert
        assert result.exit_code == 0
        # Check that verbose output contains expected information
        assert "🔧 Input:" in result.stdout
        assert "🔧 Output:" in result.stdout
        assert "🔧 Format:" in result.stdout

    def test_large_deck(self, tmp_path):
        """Test rendering with a larger deck to ensure performance."""
        # Arrange
        input_path = tmp_path / "large_deck.json"
        output_path = tmp_path / "large_output.html"
        template_dir = tmp_path / "templates"
        asset_dir = tmp_path / "assets"

        # Create a deck with many cards
        large_deck_data = {"name": "Large Test Deck", "version": "v1", "cards": []}

        # Generate 50 cards
        for i in range(50):
            card = {
                "name": f"Test Spell {i+1}",
                "level": (i % 9) + 1,
                "school": ["Evocation", "Illusion", "Necromancy", "Abjuration"][i % 4],
                "classes": ["Wizard", "Sorcerer", "Cleric"][: (i % 3) + 1],
                "description": f"This is test spell number {i+1} with a longer description to test rendering performance.",
                "duration": "1 minute" if i % 2 else "Instantaneous",
                "art_path": f"spell_{i+1}.png" if i % 3 == 0 else None,
            }
            large_deck_data["cards"].append(card)

        create_test_deck_file(input_path, large_deck_data)
        create_test_template(template_dir)
        asset_dir.mkdir(exist_ok=True)

        # Act
        result = runner.invoke(
            app,
            [
                "render",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--format",
                "html",
                "--template-dir",
                str(template_dir),
                "--asset-dir",
                str(asset_dir),
                "--verbose",
            ],
        )

        # Assert
        assert result.exit_code == 0
        assert output_path.exists()

        html_output = output_path.read_text(encoding="utf-8")
        assert "Test Spell 1" in html_output
        assert "Test Spell 50" in html_output
        assert "Cards: 50" in html_output

    def test_malformed_json(self, tmp_path):
        """Test behavior with malformed JSON input."""
        # Arrange
        input_path = tmp_path / "malformed.json"

        # Create malformed JSON
        input_path.write_text('{"name": "Test", "cards": [', encoding="utf-8")

        # Act
        result = runner.invoke(app, ["validate", "--input", str(input_path)])

        # Debug output
        print("STDOUT:", repr(result.stdout))
        print("STDERR:", repr(result.stderr))
        print("OUTPUT:", repr(result.output))

        # Assert
        assert result.exit_code == 1
        error_text = result.stdout + result.stderr + (result.output or "")
        assert "Validation failed" in error_text or "failed" in error_text.lower()

    def test_pdf_dependency_check(self):
        """Test PDF dependency checking."""
        from dmforge.application.services.weasy_renderer import WeasyRenderer

        status = WeasyRenderer.check_pdf_dependencies()

        assert isinstance(status, dict)
        assert "weasyprint_installed" in status
        assert "pydyf_installed" in status
        assert "recommendations" in status

        print("PDF Dependencies:", status)


if __name__ == "__main__":
    # Allow running individual tests
    import sys

    if len(sys.argv) > 1:
        pytest.main([__file__ + "::" + sys.argv[1], "-v", "-s"])
    else:
        pytest.main([__file__, "-v", "-s"])
```