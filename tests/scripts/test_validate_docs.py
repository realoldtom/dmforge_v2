import subprocess


def test_version_docs_creates_version_header(tmp_path):
    # Prepare a markdown file without version header
    test_doc = tmp_path / "test_doc.md"
    test_doc.write_text("# Sample Title\n\nContent paragraph.")

    result = subprocess.run(
        ["python", "scripts/version_docs.py", str(test_doc), "1.0"],
        capture_output=True,
        text=True,
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

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

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    assert result.returncode != 0, "Expected failure due to existing header"
    assert "already contains a version header" in result.stdout or result.stderr
