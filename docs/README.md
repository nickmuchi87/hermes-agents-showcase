# The full field guide: every chapter

This is the complete index. The [front page](../README.md) features the highlights; everything lives here.

## The foundations (start here if you're new)

| Chapter | What it shows |
|---------|---------------|
| [01 · What is an agent?](01-what-is-an-agent.md) | Plain-English: what an "agent" actually is, vs. a chatbot |
| [02 · Architecture](02-architecture.md) | The full system, with diagrams |
| [03 · The digest pipeline](03-the-digest-pipeline.md) | A worked example: how the podcast digest turns 20 hours of audio into a 2-minute read |
| [04 · Memory](04-memory.md) | How the agents *remember* things across days, and exactly what is (and isn't) shared between lanes |
| [05 · Design principles](05-design-principles.md) | The hard-won rules (cost control, "only ping me when it matters", failure handling) |

## The fleet, mapped

| Chapter | What it shows |
|---------|---------------|
| [06 · The schedule](06-the-schedule.md) | Every scheduled job (all ~70), how they connect, and how Telegram delivery works |
| [07 · How I built this](07-how-i-built-this.md) | The honest build story, stack, what took the time, and advice if you want to try |
| [08 · The fleet map](08-the-fleet-map.md) | The whole system at a glance, then each lane up close, every connection, and which ones ping Telegram |
| [09 · The ops lane](09-the-ops-lane.md) | The fleet that watches the fleet: a command-centre readiness board, an hourly self-healing watchdog, and an "on-call SRE" ops bot |

## The honest reality

| Chapter | What it shows |
|---------|---------------|
| [10 · What it costs](10-what-it-costs.md) | The honest money page: why the fleet is cheap, and what my ~$300/mo total actually covers |
| [11 · When it goes wrong](11-when-it-goes-wrong.md) | A gallery of real failures and how each was caught: the most honest page here |
| [12 · FAQ](12-faq.md) | The questions people actually ask (privacy, cost, "why not just ChatGPT", could I build one) |
| [13 · Glossary](13-glossary.md) | Plain-English definitions of every term, no prior knowledge assumed |
| [23 · The fleet by the numbers](23-the-fleet-by-the-numbers.md) | A date-stamped 30-day operating snapshot from the fleet's own ledgers: runs, health, incidents, cost, and what isn't tracked yet |
| [24 · What the agents can and cannot see](24-data-boundaries.md) | The data boundaries: what enters each lane, what never enters the system, where data lives, and what leaves the server |

## The deeper experiments

| Chapter | What it shows |
|---------|---------------|
| [14 · The AI PM](14-the-ai-pm.md) | An agent that makes a real (paper) decision daily: gather → deliberate → commit → memo, under guardrails |
| [15 · Cross-episode synthesis](15-cross-episode-synthesis.md) | How per-episode summaries become a cross-episode synthesis (themes, expert voices, challenges to my positions) that also feeds coursework and notes |
| [16 · The chief-of-staff](16-the-chief-of-staff.md) | The layer that tracks follow-through, not just deadlines, and checks for *evidence* a task got done |
| [17 · The fleet that fixes itself](17-the-fleet-that-fixes-itself.md) | A self-healing watchdog and a shadow-mode remediation agent that proposes safe fixes and escalates the rest |
| [18 · Many minds, one call](18-many-minds-one-call.md) | A mixture-of-agents experiment where several models vote on one AI-PM decision, with automatic fallback to the trusted single model |
| [19 · The family lane learns to see](19-the-family-lane-learns-to-see.md) | A vision model that judged house-listing *photos* to filter and rank our rental search (it worked, we found the house) |
| [20 · The study companion](20-the-study-companion.md) | A model panel writes citation-checked weekly course notes, notices when a course ends, writes its capstone, and keeps the calendar true |
| [21 · Evals as tripwires](21-evals-as-tripwires.md) | The day all four bots went quietly wrong, and the labeled regression suite that now guards the fleet |
| [22 · The queue that learns my taste](22-the-queue-that-learns-my-taste.md) | A shared podcast listen-queue I rate in plain words, so the fleet stops guessing what I want and learns it from my own verdicts |

## The code and visuals

| Where | What |
|-------|------|
| [`examples/`](../examples/) | Sanitized excerpts of the real code, several run as-is (see the [examples README](../examples/README.md)) |
| [`images/`](../images/) | Rendered workflow visuals and real bot screenshots |

---
**Back to:** [the front page](../README.md)
