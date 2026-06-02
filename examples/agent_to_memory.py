"""
How an agent writes a structured memory that OTHER agents can later read.

This is the glue behind cross-agent collaboration (see docs/04-memory.md): the
work agent's podcast digest writes tagged memories; the MBA agent reads them
later to connect coursework to podcast themes. The two never talk directly ,
they collaborate through shared, tagged memory.

Sanitized excerpt.
"""
import os
import sys
import json
import hashlib
import urllib.request

MEMORY_URL = os.environ.get("MEMORY_URL", "http://localhost:3111").rstrip("/")


def _post(path: str, payload: dict, timeout=15):
    req = urllib.request.Request(MEMORY_URL + path,
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def remember(title: str, content: str, concepts: list[str], mem_type="note"):
    """Save one memory. A stable session id (derived from the title) means
    re-running supersedes the previous version instead of piling up duplicates ,
    so 'this week's expert views' updates in place each week."""
    sid = "podcast_" + hashlib.sha1(title.encode()).hexdigest()[:12]

    # Make sure the session exists, then write the memory.
    _post("/session/start", {"sessionId": sid, "project": "/lanes/work"})
    resp = _post("/remember", {
        "sessionId": sid,
        "project": "/lanes/work",
        "title": title,
        "content": content[:8000],
        "type": mem_type,
        "concepts": concepts,        # <-- the tags other agents filter on
    })
    return (resp.get("memory") or {}).get("id")


# Example: the work agent tags an AI/startup podcast insight with the MBA course
# it maps to. The MBA agent later filters memories on concept "MGMT 8010".
if __name__ == "__main__":
    remember(
        title="Podcast AI/Startup Insights (rolling 4w)",
        content="## Costco unit economics, durable-moat flywheel pricing ...",
        concepts=["podcast", "startup-ai", "MGMT 8010"],
        mem_type="podcast",
    )
