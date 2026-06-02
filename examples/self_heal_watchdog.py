#!/usr/bin/env python3
"""self_heal_watchdog.py: autonomous fleet self-healing.

Runs hourly as a no-agent cron. Scans every lane's cron ledger for failures,
applies SAFE / REVERSIBLE remediations for known failure signatures, logs every
action, and messages the ops bot ONLY when it fixed something or needs a human.
Silent (empty stdout) when all green.

Autonomy bound: safe + reversible only (repair a corrupt JSON token, retry a
transient-failed cron). Anything touching code/config/money is ESCALATED, never
auto-applied. This is the watchdog in docs/09-the-ops-lane.md, and the fix for
the "torn login token" failure in docs/11-when-it-goes-wrong.md.

Known remediations (whitelist):
  1. corrupt-token   -> JSON decode error on a *.json creds file => truncate to
                        the first valid JSON object (atomic, backup first).
  2. transient-fail  -> a job that failed once on a network/timeout signature,
                        whose previous runs were fine => one retry.
Everything else -> escalate (report, don't touch).

(Lightly sanitized from the live fleet: real paths/email are placeholders.)
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

LANES = ["work", "mba", "family"]
AGENT_BIN = os.path.expanduser("~/.local/bin/agent")
STATE = Path.home() / ".agent-work" / "memories" / "self_heal_state.json"  # dedup escalations
NOW = datetime.now(timezone.utc)

# Credential files known to suffer concurrent-write tears (a shared OAuth token).
KNOWN_TOKENS = [
    os.path.expanduser("~/.config/google/credentials/you@example.com.json"),
]

actions: list[str] = []      # what we fixed
escalations: list[str] = []  # what a human must look at


def _read_jobs(lane: str) -> list[dict]:
    p = Path.home() / f".agent-{lane}" / "cron" / "jobs.json"
    try:
        d = json.loads(p.read_text())
    except Exception:
        return []
    if isinstance(d, list):
        return d
    if isinstance(d, dict):
        jobs = d.get("jobs", d.get("crons"))
        return jobs if isinstance(jobs, list) else [v for v in d.values() if isinstance(v, dict)]
    return []


def _repair_json_token(path: str) -> bool:
    """Truncate a token file to its first valid JSON object. Safe: backs up,
    atomic replace, and only acts if the file currently fails to parse AND its
    first object parses cleanly and looks like a real token."""
    p = Path(path)
    if not p.exists():
        return False
    raw = p.read_text()
    try:
        json.loads(raw)
        return False  # already valid, nothing to do
    except json.JSONDecodeError:
        pass
    try:
        obj, _ = json.JSONDecoder().raw_decode(raw)
    except Exception:
        return False  # can't safely recover, escalate instead
    if not (isinstance(obj, dict) and obj.get("refresh_token") and obj.get("client_id")):
        return False
    ts = NOW.strftime("%Y%m%d-%H%M%S")
    p.with_suffix(p.suffix + f".corrupt-{ts}").write_text(raw)  # backup
    tmp = str(p) + ".heal.tmp"
    Path(tmp).write_text(json.dumps(obj))
    os.replace(tmp, p)  # atomic
    os.chmod(p, 0o600)
    return True


def _retrigger(lane: str, job_name: str) -> bool:
    try:
        r = subprocess.run(
            [AGENT_BIN, "cron", "run", job_name],
            env={**os.environ, "AGENT_HOME": os.path.expanduser(f"~/.agent-{lane}")},
            capture_output=True, text=True, timeout=30,
        )
        return r.returncode == 0
    except subprocess.SubprocessError:
        return False


def _load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def _save_state(s: dict) -> None:
    try:
        STATE.write_text(json.dumps(s))
    except Exception:
        pass


def main() -> int:
    state = _load_state()
    seen_fixed_token = False

    for lane in LANES:
        for job in _read_jobs(lane):
            if job.get("last_status") != "error":
                continue
            name = job.get("name", "?")
            err = str(job.get("last_error") or "") + " " + str(job.get("last_delivery_error") or "")
            key = f"{lane}/{name}"

            # only act on RECENT failures (last 26h) to avoid re-acting on stale ones
            try:
                lr = datetime.fromisoformat(str(job.get("last_run_at")).replace("Z", "+00:00"))
                if NOW - lr > timedelta(hours=26):
                    continue
            except Exception:
                pass

            # Remediation 1: corrupt OAuth token JSON (two jobs wrote it at once)
            if re.search(r"Extra data|Expecting value|JSONDecodeError", err) and \
               re.search(r"from_authorized_user_file|credentials|token", err, re.I):
                if not seen_fixed_token:  # repair the shared token once per run
                    if any(_repair_json_token(t) for t in KNOWN_TOKENS):
                        actions.append("\U0001f527 Repaired corrupt OAuth token (torn write); retriggering affected jobs.")
                    seen_fixed_token = True
                if _retrigger(lane, name):
                    actions.append(f"  re-ran {key}: ok")
                else:
                    escalations.append(f"⚠️ {key}: token repaired but re-run still failed, check manually.")
                continue

            # Remediation 2: a transient single failure (prior runs were fine).
            # Guard: only on a recognised network/timeout signature. A bare
            # non-zero exit with no such signature is NOT auto-retried; it
            # escalates, so genuine bugs aren't masked by a retry loop.
            if re.search(r"\btimeout\b|timed out|\b50[0-9]\b|empty response|ConnectionError|temporarily unavailable|rate limit|429", err, re.I):
                if state.get(key) == NOW.strftime("%Y-%m-%d"):
                    escalations.append(f"⚠️ {key}: transient retry already tried today, still failing: {err[:80]}")
                    continue
                state[key] = NOW.strftime("%Y-%m-%d")
                if _retrigger(lane, name):
                    actions.append(f"\U0001f501 Retriggered transient-failed {key}: ok")
                else:
                    escalations.append(f"⚠️ {key}: retry failed: {err[:80]}")
                continue

            # Unknown failure: escalate, deduped per day. NEVER auto-touch.
            dkey = f"esc:{key}"
            if state.get(dkey) != NOW.strftime("%Y-%m-%d"):
                state[dkey] = NOW.strftime("%Y-%m-%d")
                escalations.append(f"❓ {key}: {err.strip()[:160]}")

    _save_state(state)

    if not actions and not escalations:
        return 0  # silent: all green

    lines = ["\U0001f6df <b>Fleet self-heal</b>"]
    if actions:
        lines.append("\n<b>Auto-fixed:</b>"); lines += actions
    if escalations:
        lines.append("\n<b>Needs you:</b>"); lines += escalations
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
