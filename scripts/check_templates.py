#!/usr/bin/env python
import sys
from pathlib import Path

required_templates = ["deck.html.j2"]
template_dir = Path("src/dmforge/resources/templates")

missing = [tpl for tpl in required_templates if not (template_dir / tpl).exists()]

if missing:
    print("❌ Missing templates:")
    for m in missing:
        print(f" - {m}")
    sys.exit(1)

print("✅ All templates present.")
