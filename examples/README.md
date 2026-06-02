# Sanitized code examples

These are **redacted excerpts** of the real, in-use code, trimmed to illustrate
a pattern, with all tokens, keys, file paths, and personal data removed or
genericised. They are here to make the [docs](../docs/) concrete, not to run as-is.

| File | Pattern it illustrates |
|------|------------------------|
| [`model_fallback.py`](model_fallback.py) | Cheap-first model routing with a fallback chain (design principle #2 & #3) |
| [`cli_circuit_breaker.py`](cli_circuit_breaker.py) | The "one failure trips the breaker, stop retrying" safeguard (#3) |
| [`sanitize_dont_reject.py`](sanitize_dont_reject.py) | Drop the one bad item, keep the rest (#4) |
| [`corpus_search.py`](corpus_search.py) | A no-AI, free keyword search over agent memory (#2) |
| [`agent_to_memory.py`](agent_to_memory.py) | How an agent writes a structured memory other agents can read (memory doc) |
| [`SOUL.example.md`](SOUL.example.md) | A lane's "job description" / constitution (architecture doc) |

### The ops / fleet-health tooling

The actual scripts behind [docs/09 (the ops lane)](../docs/09-the-ops-lane.md) and [docs/11 (when it goes wrong)](../docs/11-when-it-goes-wrong.md), lightly sanitized (real hosts, IPs, emails, and paths replaced with placeholders; logic unchanged):

| File | What it is |
|------|------------|
| [`fleet_health.py`](fleet_health.py) | The deterministic, no-LLM status check behind the ops bot's `/health` command |
| [`self_heal_watchdog.py`](self_heal_watchdog.py) | Hourly self-healing: a safe/reversible remediation whitelist that escalates everything else |
| [`sitrep_readiness.py`](sitrep_readiness.py) | The "command centre" scoring core: feed-freshness SLAs, output-quality scoring, and the readiness roll-up |
| [`skill_drift_audit.sh`](skill_drift_audit.sh) | Nightly captured-skill drift detector (real dir vs curated symlink) |
| [`skill_lint.py`](skill_lint.py) | The deterministic gate that rejects skills referencing fictional tools |
| [`skillify.sh`](skillify.sh) | Triages a drift: lint, then print the promote-or-delete commands for a human |

> Every file here is illustrative. The production versions have more error
> handling, logging, and edge-case logic; the noise has been stripped so the
> *idea* is visible. The Python ones run as-is; `sitrep_readiness.py` even
> ships a sample probe so you can run it and see the scoring.
