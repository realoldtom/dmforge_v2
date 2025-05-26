# scripts/generate_cli_guide.py

"""
Generate CLI help output from dmforge and save to docs/05_usage.md.
Recursively includes all subcommands for full CLI coverage.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

OUTPUT_PATH = Path("docs/05_usage.md")


def generate_cli_help():
    subcommands = [
        (["main.py", "--help"], "Main CLI"),
        (["main.py", "deck", "build", "--help"], "Deck: Build"),
        (["main.py", "render", "render", "--help"], "Render: Render"),
        (["main.py", "render", "validate", "--help"], "Render: Validate"),
    ]

    content_blocks = ["# DMForge CLI Usage Guide\n"]

    for cmd, label in subcommands:
        try:
            result = subprocess.run(
                ["python"] + cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            block = f"## {label}\n```bash\n{result.stdout.strip()}\n```\n"
            content_blocks.append(block)
        except subprocess.CalledProcessError as e:
            print(f"[ERR] Failed to generate help for: {' '.join(cmd)}")
            print(e.stderr)
            sys.exit(1)

    version_header = f"## Version: 1.1 ({date.today().isoformat()})\n\n"
    OUTPUT_PATH.write_text(version_header + "\n".join(content_blocks), encoding="utf-8")
    print(f"[OK] CLI guide written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_cli_help()
