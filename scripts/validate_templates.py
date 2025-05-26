# File: scripts/validate_templates.py
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path("src/dmforge/resources/templates")


def main():
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    for path in TEMPLATE_DIR.glob("*.j2"):
        try:
            env.parse(path.read_text(encoding="utf-8"))
            print(f"✅ Parsed: {path.name}")
        except Exception as e:
            print(f"❌ Syntax error in {path.name}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
