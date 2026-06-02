# 11 · When it goes wrong

Every other page here explains how the fleet *works*. This one is the opposite, and it's the most honest page in the repo: **a gallery of real ways it has failed**, and how each was caught.

The whole design assumes the AI will sometimes be wrong. So the interesting question was never "will it break?" but "**when it breaks, will I find out, and how bad is the blast radius?**" Here are four real ones.

---

## 1. The agent invented a tool that doesn't exist

**What happened.** Agents can write their own helper skills at runtime. A few of them confidently referenced a tool called `execute_code`, a plausible-sounding "run this Python" feature that **does not exist** in this system. A skill that calls a fictional tool doesn't error loudly; it just silently does the wrong thing when invoked.

**How it was caught.** A nightly audit lints every skill against a list of known-fictional tool names. It flagged the bad references, and they were rewritten to use the real mechanism.

**The lesson.** A confident LLM will invent capabilities that sound real. You need a **deterministic gate** (a linter, not another LLM) that knows the actual tool surface and refuses anything outside it. ([The ops lane](09-the-ops-lane.md) covers this auditor.)

---

## 2. The brief that cried "quiet session"

**What happened.** The evening market brief reads what credible people are posting on X. The evening window is thinner than the morning, so a strict model kept concluding *"no material chatter"* and reporting **nothing**, even on evenings when there were perfectly usable posts. A useful agent that says "nothing to report" is indistinguishable from a broken one.

**How it was caught.** A health check counts how many of the last 10 runs came back empty. When that ratio spiked, it flagged the feed as **degraded** (working, but producing nothing), which is a failure mode a simple "did it run?" check would have called green.

**The lesson.** "Ran successfully" is not the same as "produced something worth having." Monitor **output quality**, not just liveness, and give thin-window jobs explicit instructions to surface the best of what they find rather than declaring silence.

---

## 3. The end-of-day wrap that overflowed

**What happened.** One night the end-of-day summary job failed outright. The cause: a fallback model (used when the primary was unavailable) had a **smaller context window**, and the accumulated input overflowed it. The primary would have handled it fine; the cheaper stand-in couldn't.

**How it was caught.** The job's status flipped to `error`, and the on-call ops bot surfaced it with a plain-language explanation (*"context overflow; a fallback model hit a smaller window"*) rather than a stack trace.

**The lesson.** Fallbacks are not free swaps. The cheaper or backup option can have different limits, so a design that "self-heals" by falling through still needs to **report when it had to**, so you can see the seam.

---

## 4. The login token two jobs tore in half

**What happened.** Several jobs share one Google login file. Occasionally two of them wrote it at the **same instant** and tore it, leaving corrupted text. Every job that needed Google then failed with a parse error, a single shared resource taking out many jobs at once.

**How it was caught and fixed.** The hourly self-heal watchdog recognises this exact signature. It backs up the file, keeps the first valid record, drops the garbage, atomically replaces it, and re-runs the affected jobs, all on its own. By morning it was already fixed, with a one-line note that it had happened.

**The lesson.** **Shared resources are shared failure points.** The highest-leverage automation isn't a smarter brief; it's a boring watchdog that repairs the dumb, recurring, mechanical breakages before you wake up. ([Self-healing watchdog](09-the-ops-lane.md).)

---

## The pattern across all four

None of these were caught by the AI being smarter. They were caught by **deterministic guardrails around** the AI:

- a linter that knows the real tools,
- a quality counter, not just an uptime check,
- a status ledger plus a plain-language reporter,
- a watchdog with a short whitelist of safe repairs.

That's the whole philosophy: treat the AI as a **capable but fallible junior**, and spend your engineering effort on the rails that catch it. ([Design principles](05-design-principles.md).)

---
**Next:** [12 · FAQ →](12-faq.md)

**Back to:** [README](../README.md) · [Ops lane](09-the-ops-lane.md) · [Design principles](05-design-principles.md)
