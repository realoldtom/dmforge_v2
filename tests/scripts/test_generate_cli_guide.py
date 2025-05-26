# tests/scripts/test_generate_cli_guide.py

import importlib.util
from pathlib import Path


def load_generate_cli_module():
    path = Path("scripts/generate_cli_guide.py")
    spec = importlib.util.spec_from_file_location("generate_cli_guide", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_cli_help_written(tmp_path, monkeypatch):
    mod = load_generate_cli_module()

    out_file = tmp_path / "cli_help.md"
    monkeypatch.setattr(mod, "OUTPUT_PATH", out_file)

    mod.generate_cli_help()

    content = out_file.read_text(encoding="utf-8")
    assert "Usage: main.py" in content
    assert "--help" in content
    assert content.startswith("## Version:"), "Missing version header"
    assert "# DMForge CLI Usage Guide" in content
