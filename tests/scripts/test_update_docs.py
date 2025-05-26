import importlib.util
from pathlib import Path


def load_update_docs_module():
    path = Path("scripts/update_docs.py")
    spec = importlib.util.spec_from_file_location("update_docs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_injects_version_header(tmp_path):
    mod = load_update_docs_module()
    doc = tmp_path / "target.md"
    doc.write_text("# My Title\n\nSome content.")

    mod._inject(doc, "2.0")

    output = doc.read_text()
    assert output.startswith("## Version: 2.0 ("), "Header not injected"
    assert "# My Title" in output


def test_skips_already_versioned_file(tmp_path):
    mod = load_update_docs_module()
    doc = tmp_path / "already_versioned.md"
    doc.write_text("## Version: 1.0 (2025-01-01)\n\n# My Doc")

    try:
        mod._inject(doc, "1.1")
    except ValueError as e:
        assert "already versioned" in str(e)
    else:
        raise AssertionError("Expected ValueError on already versioned file")


def test_fails_on_missing_file():
    mod = load_update_docs_module()
    fake = Path("nonexistent.md")

    try:
        mod._inject(fake, "9.9")
    except FileNotFoundError as e:
        assert "nonexistent.md" in str(e)
    else:
        raise AssertionError("Expected FileNotFoundError")
