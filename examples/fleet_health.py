#!/usr/bin/env python3
"""fleet_health.py: one-shot fleet status for the ops lane's /health command.

Deterministic, no LLM. Reads each lane's cron ledger (jobs.json) plus its
gateway status and prints a terse, phone-ready health summary. This is what
answers `/health` instantly (no AI call) in docs/09-the-ops-lane.md.

(Lightly sanitized from the live fleet; paths/lane names are placeholders.)
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LANES = ["work", "mba", "family", "ops"]
NOW = datetime.now(timezone.utc)


def _gateway(lane: str) -> str:
    """Is this lane's always-on gateway process up?"""
    try:
        r = subprocess.run(["systemctl", "is-active", f"agent-{lane}"],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _jobs(lane: str) -> list[dict]:
    p = Path.home() / f".agent-{lane}" / "cron" / "jobs.json"
    try:
        d = json.loads(p.read_text())
    except Exception:
        return []
    if isinstance(d, dict):
        j = d.get("jobs")
        return j if isinstance(j, list) else [v for v in d.values() if isinstance(v, dict)]
    return d if isinstance(d, list) else []


def main() -> int:
    lines = ["\U0001f6df <b>Fleet health</b> · " + NOW.strftime("%Y-%m-%d %H:%M UTC")]
    errored = []
    for lane in LANES:
        gw = _gateway(lane)
        jobs = _jobs(lane)
        errs = [j for j in jobs if j.get("last_status") == "error"]
        errored += [(lane, j) for j in errs]
        # green only if the gateway is up AND nothing errored
        icon = "\U0001f7e2" if gw == "active" and not errs else ("\U0001f7e1" if gw == "active" else "\U0001f534")
        detail = f"{len(jobs)} jobs" + (f", <b>{len(errs)} errored</b>" if errs else "")
        lines.append(f"{icon} <b>{lane}</b>: gateway {gw} · {detail}")

    if errored:
        lines.append("\n<b>Errored jobs:</b>")
        for lane, j in errored[:12]:
            err = (str(j.get("last_error") or "").strip().splitlines() or [""])[0][:90]
            when = str(j.get("last_run_at") or "")[:16]
            lines.append(f"• {lane}/{j.get('name','?')} ({when}): {err}")
    else:
        lines.append("\n✅ All jobs green.")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
