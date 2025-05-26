# tests/scripts/test_version_docs.py

import importlib.util
import subprocess
from pathlib import Path


def load_validate_docs():
    script_path = Path("scripts/validate_docs.py")
    spec = importlib.util.spec_from_file_location("validate_docs", script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Attach manually
    return {"validate_version_header": mod.__dict__.get("validate_version_header")}


def test_valid_version_header(tmp_path):
    funcs = load_validate_docs()
    good_file = tmp_path / "valid.md"
    good_file.write_text("## Version: 1.0 (2025-05-24)\n\n# Content")
    assert funcs["validate_version_header"](good_file) is True


def test_missing_version_header(tmp_path):
    funcs = load_validate_docs()
    bad_file = tmp_path / "invalid.md"
    bad_file.write_text("# Missing version\n\nContent")
    assert funcs["validate_version_header"](bad_file) is False


def test_version_docs_creates_version_header(tmp_path):
    # Prepare a markdown file without version header
    test_doc = tmp_path / "test_doc.md"
    test_doc.write_text("# Sample Title\n\nContent paragraph.")

    result = subprocess.run(
        ["python", "scripts/version_docs.py", str(test_doc), "1.0"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"stderr: {result.stderr}"
    content = test_doc.read_text(encoding="utf-8")
    assert content.startswith("## Version: 1.0 ("), "Missing version header"
    assert "# Sample Title" in content, "Original content missing"


def test_version_docs_fails_on_existing_version(tmp_path):
    # Prepare a markdown file with existing version header
    test_doc = tmp_path / "test_doc_existing.md"
    test_doc.write_text("## Version: 0.9 (2025-01-01)\n\n# Already versioned")

    result = subprocess.run(
        ["python", "scripts/version_docs.py", str(test_doc), "1.0"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, "Expected failure due to existing header"
    assert "already contains a version header" in result.stdout or result.stderr
