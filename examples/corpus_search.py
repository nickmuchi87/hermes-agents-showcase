"""
Free, no-AI keyword search over agent memory.

When you ask the work bot "/podcast_q oil Iran Hormuz", there is NO AI call. The
podcast corpus already lives in the memory service (written by the digest), so a
question is answered by deterministic keyword scoring over stored blocks.

Pattern (design principle #2): don't spend on the LLM for something a 40-line
script does instantly and for free.

Sanitized excerpt.
"""
import os
import re
import sys
import json
import urllib.request

MEMORY_URL = os.environ.get("MEMORY_URL", "http://localhost:3111").rstrip("/")
MAX_HITS = 8
STOP = {"the", "a", "an", "of", "in", "on", "to", "and", "or", "for", "what",
        "did", "any", "about", "with", "how", "does"}


def fetch_corpus() -> list[dict]:
    """Pull memories tagged 'podcast' (and only the latest version of each)."""
    url = f"{MEMORY_URL}/memories?limit=200"
    with urllib.request.urlopen(url, timeout=10) as r:
        mems = json.load(r).get("memories", [])
    return [m for m in mems
            if "podcast" in (m.get("concepts") or []) and m.get("isLatest", True)]


def blocks(mem: dict):
    """Split a memory's markdown into (heading, body) sections, skipping the
    YAML frontmatter preamble."""
    content = mem.get("content", "") or ""
    tag = next((c for c in (mem.get("concepts") or []) if c != "podcast"), "podcast")
    for part in re.split(r"\n(?=#{2,3} )", content):
        part = part.strip()
        if not part.startswith("##") or len(part) < 30:
            continue
        head = part.splitlines()[0].lstrip("# ").strip()
        yield f"[{tag}] {head}"[:120], part


def search(query: str):
    terms = [t for t in re.findall(r"[a-z0-9]+", query.lower())
             if t not in STOP and len(t) > 2]
    scored = []
    for mem in fetch_corpus():
        for head, body in blocks(mem):
            low = body.lower()
            score = sum(low.count(t) for t in terms)   # simple keyword overlap
            if score:
                scored.append((score, head, body))
    scored.sort(key=lambda x: -x[0])
    return scored[:MAX_HITS]


if __name__ == "__main__":
    q = " ".join(sys.argv[1:])
    for score, head, body in search(q):
        snippet = re.sub(r"\s+", " ", body)[:320]
        print(f"[score {score}] {head}\n  {snippet}\n")
