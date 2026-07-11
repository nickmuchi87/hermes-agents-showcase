#!/usr/bin/env python3
"""Fail CI if any relative markdown link or image target doesn't exist.

Checks every .md file in the repo (docs/, examples/, root). External links
(http/https/mailto) and pure in-page anchors are skipped; anchors on relative
links are checked for file existence only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")

def targets(md: Path):
    text = md.read_text(encoding="utf-8")
    # strip fenced code blocks and HTML comments so mermaid samples and
    # commented-out placeholders aren't parsed for links
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in LINK_RE.finditer(text):
        yield m.group(1)

def main() -> int:
    broken = []
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        for raw in targets(md):
            if raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            rel = raw.split("#", 1)[0]
            if not rel:
                continue
            if not (md.parent / rel).resolve().exists():
                broken.append(f"{md.relative_to(ROOT)}: {raw}")
    if broken:
        print("Broken relative links:")
        print("\n".join(f"  {b}" for b in broken))
        return 1
    print("All relative links resolve.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
