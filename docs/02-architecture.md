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
        sched[⏰ Scheduler<br/>~35 jobs/day]

        subgraph lanes["THREE AGENT LANES"]
            em[💼 WORK lane<br/>17 scheduled jobs]
            wemba[🎓 MBA lane<br/>9 scheduled jobs]
            fam[👨‍👩‍👧 FAMILY lane<br/>9 scheduled jobs]
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

- **SOUL.md** — a plain-text "constitution" telling the AI who it is and how to behave (tone, hard rules, what never to do). This is where the three lanes diverge most.
- **jobs.json** — the cron schedule: which task fires when.
- **helper scripts** — small deterministic programs (no AI) that gather or post data, so the AI only does the *judgment*, not the plumbing.
- **bot + model config** — which Telegram bot it speaks through, and which AI models it's allowed to use.

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

If a task can be done by deterministic code, it runs as a **no-agent** job — zero AI cost. The LLM is reserved for the genuinely hard part: *reading messy input and deciding what matters.* (This wasn't the original design — see the [cautionary tale in design principles](05-design-principles.md) about a job that was needlessly burning the AI ~48 times a day.)

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

---
**Next:** [03 · A worked example: the podcast digest →](03-the-digest-pipeline.md)
