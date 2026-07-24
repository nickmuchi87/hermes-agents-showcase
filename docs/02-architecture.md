# 2 · The architecture

Everything runs on **one small cloud server** (a $5/month VPS). On it live three independent agent "lanes," a shared memory service, and a scheduler. Each lane talks to me through its own Telegram bot.

## The big picture

```mermaid
flowchart TB
    subgraph sources["📡 DATA SOURCES"]
        gmail[📨 Gmail<br/>3 accounts]
        gcal[📅 Google Calendar]
        gdrive[📑 Google Drive<br/>coursework]
        news[📰 News / RSS<br/>Bloomberg, IMF, ratings]
        pods[🎙️ Podcast feeds]
        mkts[📊 Prediction markets]
    end

    subgraph server["🖥️ ONE SMALL CLOUD SERVER"]
        direction TB
        sched[⏰ Scheduler<br/>~70 jobs/day]

        subgraph lanes["THREE CONTENT LANES (+ ops)"]
            em[💼 WORK lane<br/>23 scheduled jobs]
            wemba[🎓 MBA lane<br/>23 scheduled jobs]
            fam[👨‍👩‍👧 FAMILY lane<br/>11 scheduled jobs]
        end

        mem[(🧠 Shared memory<br/>service)]
        router{🔀 Model router<br/>cost vs quality}
    end

    subgraph ai["☁️ AI MODELS (commercial APIs)"]
        claude[Claude]
        deepseek[DeepSeek]
        gemini[Gemini]
    end

    tg[📱 Telegram<br/>3 separate bots]

    sources --> lanes
    sched --> lanes
    lanes <--> mem
    lanes --> router
    router --> ai
    lanes --> tg
    tg --> me([👤 Me])
```

> **A quiet fourth lane.** Above these three content lanes sits a supervisory **ops lane**: it produces no work of its own; it watches the other three, auto-fixes safe failures, and pings a separate ops bot when it needs me. It's covered in its own chapter: [09 · The ops lane](09-the-ops-lane.md).

## What each lane is made of

Every lane is the same machinery with different settings:

```mermaid
flowchart LR
    subgraph lane["ONE LANE (e.g. Work)"]
        soul[📜 SOUL.md<br/>the job description:<br/>'You are an EM credit<br/>chief-of-staff...']
        jobs[⏰ jobs.json<br/>the schedule:<br/>morning brief 6am,<br/>EOD nudge 8:45pm...]
        scripts[🔧 helper scripts<br/>fetch news, search<br/>corpus, archive]
        botcfg[🤖 bot config<br/>which Telegram bot,<br/>which models]
    end
    soul --> out([Behaviour])
    jobs --> out
    scripts --> out
    botcfg --> out
```

- **SOUL.md**: a plain-text "constitution" telling the AI who it is and how to behave (tone, hard rules, what never to do). This is where the three lanes diverge most.
- **jobs.json**: the cron schedule: which task fires when.
- **helper scripts**: small deterministic programs (no AI) that gather or post data, so the AI only does the *judgment*, not the plumbing.
- **bot + model config**: which Telegram bot it speaks through, and which AI models it's allowed to use.

## Two kinds of scheduled job

A subtle but important distinction that keeps costs down:

```mermaid
flowchart TB
    subgraph agentic["🧠 'Agent' jobs (use the LLM)"]
        a1[Morning brief: read everything,<br/>judge it, write a human summary]
    end
    subgraph noagent["⚙️ 'No-agent' jobs (pure script, no LLM)"]
        n1[Archive yesterday's brief]
        n2[Search the podcast corpus]
        n3[Health audit of all lanes]
    end
    agentic -->|costs API $| wallet[💰]
    noagent -->|costs nothing| free[🆓]
```

If a task can be done by deterministic code, it runs as a **no-agent** job, zero AI cost. The LLM is reserved for the genuinely hard part: *reading messy input and deciding what matters.* (This wasn't the original design, see the [cautionary tale in design principles](05-design-principles.md) about a job that was needlessly burning the AI ~48 times a day.)

## The model router

No single AI model is best for everything, so each lane routes work by **cost vs. quality**:

```mermaid
flowchart LR
    task[A task arrives] --> q{How hard?}
    q -->|"heavy reasoning<br/>(weekly synthesis)"| big[Flagship model<br/>~best quality]
    q -->|"bulk summarising<br/>(per-episode)"| cheap[Fast cheap model<br/>1/10th the cost]
    q -->|"free tier available<br/>(on my laptop)"| free[Local subscription<br/>$0 incremental]
    big & cheap & free --> fallback[If one fails,<br/>fall through to the next]
```

This "try the cheap/free option first, fall back to the premium one only if needed" pattern is everywhere in the system. It's the difference between a fun side-project and a $300/month habit.

### One gateway, many models: OpenRouter

A practical problem: I want to use the *best model for each job*, Claude for some things, DeepSeek for others, Gemini for the cheap utility work, but I don't want five separate API accounts, five billing relationships, and five different bits of code.

The fix is [**OpenRouter**](https://openrouter.ai): a single API that sits in front of dozens of providers. I send every request to one endpoint with a model name like `anthropic/claude-...` or `deepseek/deepseek-...`, and OpenRouter routes it, bills it centrally, and lets me **swap models by changing a string**: no code change.

```mermaid
flowchart LR
    lanes[💼🎓👨‍👩‍👧 all lanes<br/>+ digest pipeline] --> or{🔀 OpenRouter<br/>one API, one bill}
    or --> c[Claude<br/>headline reasoning]
    or --> d[DeepSeek<br/>bulk + synthesis]
    or --> q[Qwen / others<br/>swappable]
    direct[Gemini direct<br/>cheap utility tier] -.also used.-> g[noise audit ·<br/>compression ·<br/>embeddings]
```

Two things this unlocks:
- **Model choice is configuration, not code.** Each task has an env-overridable model name. When DeepSeek's flagship flaked one night and returned empty responses, switching that stage to its faster sibling was a one-line change, and I'd already wired it as an automatic fallback, so it self-healed.
- **Per-task routing.** Heavy reasoning → a flagship; bulk per-item work → a fast cheap model; throwaway utility judgments → the cheapest thing available.

### Who does what (the actual roster)

| Job | Model tier | Why |
|-----|-----------|-----|
| Morning/EOD briefs, weekly synthesis | **Flagship** (Claude / DeepSeek-pro), via OpenRouter | Hard reasoning, worth the cost |
| Per-episode podcast summaries | **Fast cheap** (DeepSeek-flash), via OpenRouter | High volume, doesn't need a flagship |
| **Noise classification** (nightly lane audits) | **Fast cheap** (DeepSeek-flash), via OpenRouter | Thousands of tiny "signal or noise?" calls, cheap, and one fewer provider to manage |
| Free tier (on my laptop) | **Local subscription CLI** | $0 incremental, tried *first* where available |
| **On-demand hard questions** (a `deep:` message prefix) | **Frontier reasoning model**, flat-rate subscription via its CLI | Human-triggered escalation, one question at a time, zero marginal cost ([ch. 18](18-many-minds-one-call.md)) |
| **Context compression** | **Gemini Flash-Lite** (direct) | Squashing long histories cheaply |
| **Embeddings** (podcast clustering) | **Gemini embeddings** (direct) | Cheap vector maths, not text generation |

> **A note on consolidation:** these things *can* run on any cheap model, and I've moved them around. The nightly noise-audit cron originally used Gemini Flash-Lite; I later pointed it at DeepSeek-flash (via OpenRouter) to keep the whole text-generation side on **one provider and one key**: simpler to reason about and bill. Gemini still earns its place for **embeddings** (vector maths, not text, a different job) and conversation **compression**. The lesson isn't "Gemini vs DeepSeek"; it's that *because* model choice is just a config string ([OpenRouter](#one-gateway-many-models-openrouter)), consolidating or swapping the cheap-utility tier is a one-line change, not a rewrite.

### Why a different model for X/Twitter

The work lane's morning brief leads with **what credible people are saying on X right now**: central-bank surprises, rating actions, analyst takes on specific markets. No general model can do that: it needs *live* access to X.

The answer is **Grok** (xAI's model), which has a native `x_search` tool: it can actually query X and read recent posts. So this one job routes to Grok instead of the usual models. Two design touches make it useful rather than noisy:

```mermaid
flowchart LR
    cron[⏰ pre-brief scan<br/>20:55 UTC] --> grok[🔍 Grok + x_search]
    prior[📋 prompt discipline:<br/>lead institutional and named-firm<br/>sources, tag the rest] --> grok
    grok --> tier{tier by source quality}
    tier --> a[institutional / named-firm<br/>→ lead]
    tier --> b[retail / anonymous<br/>→ tag unverified, keep]
    a & b --> brief[🗃️ snapshot file →<br/>feeds the morning brief]
```

1. **Two searches, merged.** One sweep for major political/market *events* (which often break on non-finance accounts first) and one for specialist *markets* chatter, so a big story is never missed just because only retail accounts carried it.
2. **Tiered surfacing, not filtering.** Posts from institutional or named-firm sources lead; anonymous hot-takes are tagged `[unverified]` and demoted, never silently dropped.

And one hard-won guardrail: the prompt ends with *"if NOTHING qualifies, output exactly NO_MATERIAL, no prose."* Without a forced sentinel like that, a model on a quiet day will invent filler rather than admit there's nothing to say (a failure mode that shows up in the [failure gallery](11-when-it-goes-wrong.md)).

---
**Next:** [03 · A worked example: the podcast digest →](03-the-digest-pipeline.md)
