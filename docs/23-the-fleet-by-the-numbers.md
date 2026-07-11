# 23 · The fleet by the numbers: a 30-day operating snapshot

Every claim in this repo ("~60 jobs", "mostly silent", "tens of dollars") is easy to write and hard to trust. So this page is the fleet's own ledgers, read out loud: a **date-stamped snapshot** of the 30 days ending **2026-07-12**, computed from the scheduler's job files, the ops lane's cost tracker, and its escalation log.

Two honesty rules up front:

1. **This is a snapshot, not a benchmark.** It's one month of one person's fleet, measured by its own instruments.
2. **Where the fleet doesn't measure something, I say "not tracked" instead of guessing.** The gaps are listed at the bottom, they're part of the picture.

---

## The shape of the fleet

| Metric | Value | Source |
|--------|-------|--------|
| Active scheduled jobs | **62** (work 21 · MBA 19 · family 10 · ops 12) | scheduler job files |
| Jobs that call an LLM ("agent" jobs) | **10** (16%) | scheduler job files |
| Pure-script jobs (no AI, ~free) | **52** (84%) | scheduler job files |
| Scheduled fires per day | **~266** (≈ 8,000 runs over the 30 days) | computed from each job's cron expression |

That 266/day number surprises people. Almost all of it is cheap polling: the every-30-minutes watchers (Drive, calendar events, remediation triage) account for most fires, and none of them call an AI or send a message unless something changed.

## Who is allowed to interrupt me

| Delivery class | Jobs | What it means |
|----------------|------|---------------|
| 📱 May ping my phone | **31** | Delivers to a Telegram bot, but most only fire a message when they found something |
| 🔄 Surfaces only with news | **10** | Delivers to the lane's channel *if* the run produced output; a quiet run says nothing |
| 🗃️ Can never reach me | **21** | Writes files/memory for other jobs; structurally silent |

So a third of the fleet is structurally incapable of interrupting me, and of the rest, the design principle ([05](05-design-principles.md)) is that a run with nothing to say sends nothing.

## Health, right now

| Metric | Value |
|--------|-------|
| Jobs whose last run succeeded | **61 of 62** |
| The one exception | A newly added weekly job still waiting for its first scheduled fire |
| Jobs currently in a failed state | **0** (the failure watch is empty) |

## Incidents over the 30 days

The ops lane logs an **escalation** whenever a job fails repeatedly, a feed goes stale past its freshness deadline, or a companion machine misses a check-in ([09 · the ops lane](09-the-ops-lane.md)).

| Metric | Value |
|--------|-------|
| Escalations opened in the window | **60** (~2/day) |
| Closed | **56**, the large majority auto-closed as "recovered" when the next run succeeded |
| Still open at snapshot time | **4**: two stale-feed flags pointing at feeds that were retired (the watch list needs pruning), one script-timeout that has since been fixed, and one missed check-in from a laptop job that is deliberately paused |

The honest read: about two flags a day, almost all self-resolving, and the ones that stay open are as likely to be *stale monitoring config* as real breakage. Watching the watchers is also maintenance.

## What it cost

| Metric | Value |
|--------|-------|
| API spend, 30 days (2026-06-11 → 2026-07-10) | **~$85** (~$2.80/day) |
| Caveat | This is the whole API account the fleet bills to, and the same account also serves a few non-fleet experiments, so treat it as an **upper bound** on the fleet's true spend |

That's consistent with the ["tens of dollars" claim in the cost chapter](10-what-it-costs.md): 84% of jobs never touch a model, and the ones that do are routed cheap-first.

## Quality gates

| Metric | Value |
|--------|-------|
| Labeled eval suite (deadline/completion matching) | **27 cases**, run weekly as a tripwire ([21 · evals as tripwires](21-evals-as-tripwires.md)) |
| Last eval run at snapshot time | green |

## What is *not* tracked (yet)

Real gaps, listed so the numbers above don't over-claim:

- **Messages actually sent per day.** The delivery classes above are structural; the fleet doesn't yet count sent messages centrally.
- **False-positive rate.** How often a ping was dismissed as noise is exactly the metric a recommender needs, and today it only exists for the podcast queue ([22](22-the-queue-that-learns-my-taste.md)), not for alerts.
- **Cost per lane.** Spend is tracked at the account level, not attributed per lane or per job.
- **Model fallback rate.** Fallbacks are logged in job output but not aggregated.

If those get instrumented, this page gets a second snapshot to compare against.

---

## How this was computed

All numbers come from files the fleet already maintains: the scheduler's per-lane job registry (job counts, cron expressions, delivery targets, last-run status), the ops lane's daily cost ledger (cumulative API usage, so the 30-day figure is a simple difference), and its escalation log. No new instrumentation was added to make the fleet look good for this page; the "not tracked" list is what honesty costs.

---
**Next:** [24 · What the agents can and cannot see →](24-data-boundaries.md)

**Back to:** [README](../README.md) · [The schedule](06-the-schedule.md) · [What it costs](10-what-it-costs.md) · [The ops lane](09-the-ops-lane.md)
