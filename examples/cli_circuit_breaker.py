"""
Circuit breaker for the free local-CLI tier.

Problem: the free tier (a flat-rate AI subscription invoked via a local CLI) can
hang or fail. If a digest processes 20 items and the CLI is broken, naively
retrying it on every item means 20 timeouts before each falls back.

Fix (design principle #3): the FIRST failure in a run trips a flag; every
subsequent call short-circuits straight to the paid API. One bad component can't
make the whole run crawl.

Sanitized excerpt.
"""
import os
import shutil
import subprocess
import time

# Per-process flag. A fresh run resets it, giving the CLI another chance.
_CLI_BROKEN = False


def run_local_cli(prompt: str, timeout_s: int = 600):
    """Invoke the free local CLI. Returns text, or None (and trips the breaker)
    if disabled, missing, errored, or timed out."""
    global _CLI_BROKEN

    # Only use the CLI where it's actually free (a flag set on that machine).
    if os.environ.get("USE_LOCAL_CLI") != "1":
        return None

    # Breaker already tripped this run — don't even try.
    if _CLI_BROKEN:
        return None

    if not shutil.which("the-cli"):
        _CLI_BROKEN = True
        return None

    t0 = time.time()
    try:
        proc = subprocess.run(["the-cli", "-p", prompt],
                              capture_output=True, text=True, timeout=timeout_s)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        _CLI_BROKEN = True          # trip: stop retrying for the rest of this run
        return None

    if proc.returncode != 0:
        _CLI_BROKEN = True
        return None

    return proc.stdout or ""
