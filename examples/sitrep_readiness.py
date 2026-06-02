#!/usr/bin/env python3
"""sitrep_readiness.py: the scoring core of the fleet "command centre".

The real SITREP (see docs/09-the-ops-lane.md) SSH-probes the host(s) and gathers
hosts, bots, services, crons, data feeds, and API keys, then renders a
colour-coded readiness board. This excerpt keeps the part worth studying: the
two checks that catch failures which DON'T announce themselves, and the roll-up
into one verdict.

  - feed freshness: a feed that merely went STALE (beyond its SLA) is RED even
    though nothing "errored". A stale feed is a job that quietly stopped.
  - feed quality: a live-market scan can run "successfully" and still return
    "no material" every time. We score the empty ratio over the last N runs,
    because green-on-"did it run" is not the same as green-on-"was it useful".

The host-probe plumbing (SSH heredocs, real hostnames) is omitted; probe() here
returns a sample so the scoring is self-contained and runnable.
(Sanitized excerpt; logic mirrors the live version.)
"""
from __future__ import annotations

# Freshness SLAs in hours. Beyond the SLA, a feed is RED even if it never errored.
FEED_SLA = {
    "x_trends": 16,            # refreshed morning + evening daily
    "imf_publications": 48,
    "policy_commentary": 36,
    "ratings": 48,
    "prediction_markets": 26,
}

G, Y, R, B = "\U0001f7e2", "\U0001f7e1", "\U0001f534", "⚪"  # green/yellow/red/white


def classify_feed(name: str, age_hours: float | None) -> tuple[str, str]:
    """Liveness is not enough: judge a feed by freshness against its SLA."""
    if age_hours is None:
        return R, "MISSING"
    sla = FEED_SLA.get(name)
    if sla is None:
        return B, "no SLA"
    return (G, "fresh") if age_hours <= sla else (R, f"STALE >{sla}h")


def classify_quality(no_material: int, window: int) -> tuple[str, str]:
    """A job can 'succeed' and still produce nothing. Score the empty ratio:
    >=60% of recent runs empty is RED, >=30% is AMBER."""
    if window == 0:
        return B, "no data"
    ratio = no_material / window
    icon = R if ratio >= 0.6 else (Y if ratio >= 0.3 else G)
    return icon, f"{no_material}/{window} runs produced nothing"


def assess(probe: dict) -> dict:
    """Roll everything up into one verdict: CRITICAL > DEGRADED > OPERATIONAL.
    Anything RED is immediate; anything AMBER is monitor-only."""
    reds, yellows = [], []

    for name, age in probe.get("feeds", {}).items():
        icon, note = classify_feed(name, age)
        if icon == R:
            reds.append(f"feed {name}: {note}")

    q = probe.get("x_quality")
    if q:
        icon, note = classify_quality(q["no_material"], q["window"])
        if icon == R:
            reds.append(f"x_search quality: {note}")
        elif icon == Y:
            yellows.append(f"x_search quality: {note}")

    for name, status in probe.get("services", {}).items():
        if status != "active":
            reds.append(f"service {name}: {status}")

    for lane, jobs in probe.get("crons", {}).items():
        for j in jobs:
            if j.get("last_status") == "error":
                reds.append(f"cron {lane}/{j['name']}: errored")
            elif j.get("paused"):
                yellows.append(f"cron {lane}/{j['name']}: paused")

    readiness = f"{R} CRITICAL" if reds else (f"{Y} DEGRADED" if yellows else f"{G} OPERATIONAL")
    return {"readiness": readiness, "red": reds, "amber": yellows}


def probe() -> dict:
    """STUB. The real version SSH-probes the host(s) for live status. Sample:"""
    return {
        "feeds": {"x_trends": 5.0, "ratings": 15.1, "imf_publications": 60.0},  # imf is STALE (SLA 48h)
        "x_quality": {"no_material": 7, "window": 10},                          # 70% empty -> RED
        "services": {"agent-work": "active", "agent-mba": "active"},
        "crons": {"work": [{"name": "morning-brief", "last_status": "ok"}]},
    }


if __name__ == "__main__":
    result = assess(probe())
    print(f"READINESS: {result['readiness']}   \U0001f534 {len(result['red'])}  \U0001f7e1 {len(result['amber'])}")
    for r in result["red"]:
        print(f"  {R} {r}")
    for y in result["amber"]:
        print(f"  {Y} {y}")
