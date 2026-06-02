# 8 · The fleet map: everything, on one page

This is the **whole system in one picture**: every scheduled job across the three lanes, what each one does, how they connect, and exactly which ones reach my phone over Telegram.

If you only look at one diagram in this repo, make it this one. (The [schedule](06-the-schedule.md) has the same jobs as tables with times; this is the *visual* of how they wire together.)

## How to read it

| Symbol | Meaning |
|--------|---------|
| 🧠 | **Agent job**: calls the AI to read, judge, and write. Costs a little money. |
| ⚙️ | **No-agent job**: pure script, no AI, free. Most jobs are these. |
| 📱 | **Pings my phone**: delivers to that lane's Telegram bot. |
| 🗃️ → memory | Writes data other jobs read later. I'm *not* pinged. |
| dashed arrow | "Tomorrow reads yesterday", a memory loop across days. |

> All times are **UTC**. My morning is ~11:00 UTC (≈ 6-7am US Eastern).

---

## The whole fleet, on one page

Because the fleet is ~35 jobs, one all-in-one graph renders too small to read on GitHub. So here it is in **two zooms**: first the *shape* of the whole thing, then **each lane up close** with every job. Same colour key throughout, **green = pings my phone**, purple = AI/agent, grey = free plumbing, amber = shared memory, blue = Telegram bots.

### Zoom 1, the shape of the whole fleet

```mermaid
flowchart LR
    SRC["📡 SOURCES<br/>Gmail×3 · Calendar · Drive ·<br/>Bloomberg / IMF / ratings ·<br/>X · podcasts · markets"]:::src
    WORK["💼 WORK · 17 jobs<br/>markets · credit · IMF · ratings"]:::work
    MBA["🎓 MBA · 9 jobs<br/>coursework · deadlines"]:::mba
    FAM["👨‍👩‍👧 FAMILY · 9 jobs<br/>school · relocation"]:::fam
    OPS["🛟 OPS · watchdog + /health<br/>watches the other three"]:::ping
    MEM[("🧠 SHARED MEMORY")]:::mem
    BW(["🤖 Work bot"]):::bot
    BM(["🤖 MBA bot"]):::bot
    BF(["🤖 Family bot"]):::bot
    BO(["🤖 Ops bot"]):::bot
    ME(["👤 my phone<br/>4 threads"]):::me

    SRC --> WORK & MBA & FAM
    WORK & MBA & FAM --> MEM
    MEM -. "diffs · cross-lane links" .-> WORK & MBA
    WORK --> BW
    MBA --> BM
    FAM --> BF
    WORK & MBA & FAM -. "job status" .-> OPS
    OPS -. "safe auto-fix" .-> WORK
    OPS --> BO
    BW & BM & BF & BO --> ME
    ME -. "reply 'done: X'" .-> MEM

    classDef src fill:#eceff1,stroke:#607d8b,color:#263238;
    classDef work fill:#ede7f6,stroke:#5e35b1,color:#311b92,stroke-width:2px;
    classDef mba fill:#e8eaf6,stroke:#3949ab,color:#1a237e,stroke-width:2px;
    classDef fam fill:#fce4ec,stroke:#ad1457,color:#880e4f,stroke-width:2px;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef me fill:#fff,stroke:#000,color:#000,stroke-width:2px;
```

Four lanes write into one shared memory and speak through four separate bots; the ops lane sits above and watches the other three. Now the detail, one lane at a time.

### Zoom 2a, 💼 WORK lane (17 jobs)

The pattern to notice: five cheap **watchers** gather data first, then **one** AI brief reads all of it. Only four jobs ever ping me.

```mermaid
flowchart TB
    subgraph WS["⚙️ watchers, gather first (cheap / free)"]
        direction LR
        w_imf["10:10 Sun/Wed · imf-watcher<br/>IMF program news"]:::plumb
        w_pol["10:30 · policy-commentary<br/>think-tank / policy RSS"]:::plumb
        w_eml["🧠 10:45 · em_email_digest<br/>triage work inbox"]:::agent
        w_rat["10:50 · rating-watcher<br/>rating-agency actions"]:::plumb
        w_xam["10:55 · x-brief-am<br/>AM EM chatter (Grok)"]:::plumb
    end
    brief["🧠📱 11:15 · em-morning-brief<br/>reads ALL watchers + memory → the brief"]:::ping
    arch["⚙️ 11:30 · em_brief_archive<br/>save brief → memory"]:::plumb
    pos["⚙️ 11:32 · em_position_log<br/>snapshot positions"]:::plumb
    poly["⚙️ 11:00 / 21:00 · polymarket_snapshot<br/>prediction-market odds"]:::plumb
    news2["⚙️📱 every 2h Mon-Fri · em_news_triage<br/>Bloomberg, ping if market-moving"]:::ping
    intra["⚙️📱 16:00 / 20:00 · x-intraday-alerter<br/>intraday X, ping if notable"]:::ping
    xpm["⚙️ 21:00 · x-brief-pm<br/>PM EM chatter"]:::plumb
    aaa["⚙️ 22:00 · em_after_action_audit<br/>day's calls vs outcomes"]:::plumb
    eod["🧠📱 00:45 · em_eod_nudge<br/>EOD wrap: what moved, what needs me"]:::ping
    eoda["⚙️ 01:15 · em_eod_archive<br/>save EOD → memory"]:::plumb
    aud["⚙️ 03:55 · em_lane_audit<br/>self-check: did it all run?"]:::plumb
    drift["⚙️📱 04:30 · skills_drift_audit<br/>flag a stale skill"]:::ping
    mem[("🧠 memory")]:::mem
    bot(["🤖 Work bot"]):::bot

    WS --> brief
    mem -. "yesterday's diff" .-> brief
    poly -. "odds" .-> brief
    brief --> bot
    brief --> arch --> mem
    pos --> mem
    aaa --> mem
    xpm --> eod
    eod --> bot
    eod --> eoda --> mem
    news2 --> bot
    intra --> bot
    drift --> bot
    aud -. "self-check" .-> mem

    classDef agent fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef plumb fill:#f5f5f5,stroke:#9e9e9e,color:#424242;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1,stroke-width:2px;
```

### Zoom 2b, 🎓 MBA lane (9 jobs)

Mostly quiet plumbing into memory; it pings me **once a week** with its smartest output, the cross-lane link between a podcast and a course.

```mermaid
flowchart TB
    drive["⚙️ every 30m · wemba_drive_watch<br/>watch Drive for new coursework"]:::plumb
    pre["⚙️ every 30m · wemba_preclass_brief<br/>prep a brief if class is imminent"]:::plumb
    brief["🧠 11:00 · daily_wemba_brief<br/>study brief: deadlines, materials, email"]:::agent
    risk["🧠 12:00 · wemba_atrisk_radar<br/>flag deliverables at risk of slipping"]:::agent
    sweep["⚙️ 13:00 · wemba_completion_sweep<br/>Drive vs deliverables, 'did you finish X?'"]:::plumb
    eod["🧠 01:00 · wemba_eod_nudge<br/>end-of-day: tomorrow's prep"]:::agent
    aud["⚙️ 03:55 · wemba_lane_audit<br/>self-check"]:::plumb
    synth["⚙️ 22:00 Sun · wemba_weekly_synthesis<br/>week's coursework → memory"]:::plumb
    bridge["⚙️📱 23:30 Sun · podcast_course_bridge<br/>links coursework ↔ podcast themes"]:::ping
    work["💼 Work lane's podcast<br/>insights (tag: startup-ai)"]:::agent
    mem[("🧠 shared memory")]:::mem
    bot(["🤖 MBA bot"]):::bot

    drive --> brief
    pre --> brief
    brief --> risk
    brief --> sweep
    eod -. "prep" .-> mem
    synth --> mem
    work --> mem
    mem -. "course themes + podcast insights" .-> bridge
    bridge --> bot

    classDef agent fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef plumb fill:#f5f5f5,stroke:#9e9e9e,color:#424242;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1,stroke-width:2px;
```

### Zoom 2c, 👨‍👩‍👧 FAMILY lane (9 jobs)

The most time-sensitive lane (school + an international move), so it polls often during waking hours and the move-day countdown is allowed to get louder as we get closer.

```mermaid
flowchart TB
    subgraph POLL["⚙️📱 frequent pollers (waking hours)"]
        direction LR
        imm["family_imminent · :00/:30<br/>imminent calendar events"]:::ping
        reloc["relocation_emails · :15<br/>relocation email"]:::ping
        school["school_email_check · hourly 11-23<br/>school emails, tiered by sender"]:::ping
    end
    brief["🧠 11:00 · daily_family_brief<br/>morning brief: today's events + actions"]:::agent
    arch["⚙️ 11:15 · family_brief_archive<br/>save brief → memory"]:::plumb
    cd["⚙️ 12:00 · family_au_countdown<br/>move-day countdown (T-30/14/7/3/1)"]:::plumb
    sweep["⚙️📱 12:00 Sun · relocation_sweep<br/>weekly relocation checklist"]:::ping
    rent["⚙️📱 every 48h · au_rental_search<br/>scan rentals in destination city"]:::ping
    aud["⚙️ 03:55 · family_lane_audit<br/>self-check"]:::plumb
    mem[("🧠 memory")]:::mem
    bot(["🤖 Family bot"]):::bot

    cd -. "urgency" .-> brief
    brief --> arch --> mem
    POLL --> bot
    sweep --> bot
    rent --> bot
    aud -. "self-check" .-> mem

    classDef agent fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef plumb fill:#f5f5f5,stroke:#9e9e9e,color:#424242;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1,stroke-width:2px;
```

> The **ops lane** (the 4th, supervisory one) has its own close-up in [09 · The ops lane](09-the-ops-lane.md).

**Green nodes ping my phone.** Purple nodes think (AI). Grey nodes are free plumbing into the amber memory store. That's the whole fleet: ~35 jobs, and only a handful ever interrupt me.

---

## Just the Telegram side: who is allowed to ping me, and when

The single most important design choice is **restraint**: most jobs never reach my phone. Here's only the part that *can* interrupt me, by lane:

```mermaid
flowchart LR
    subgraph work["💼 WORK bot"]
        direction TB
        a1["em-morning-brief · 11:15<br/>the daily market brief"]
        a2["em_news_triage · every 2h<br/>only if market-moving"]
        a3["x-intraday-alerter · 16:00/20:00<br/>only if notable"]
        a4["em_eod_nudge · 00:45<br/>end-of-day wrap"]
        a5["skills_drift_audit · 04:30<br/>'a skill went stale'"]
        a6["podcast digest · 3×/wk<br/>the 2-min read"]
    end
    subgraph mba["🎓 MBA bot"]
        b1["podcast_course_bridge · Sun 23:30<br/>'this episode maps to your paper'"]
    end
    subgraph fam["👨‍👩‍👧 FAMILY bot"]
        c1["family_imminent · :00/:30<br/>event starting soon"]
        c2["relocation_emails · :15<br/>relocation mail landed"]
        c3["school_email_check · hourly<br/>tiered by sender importance"]
        c4["relocation_sweep · Sun 12:00<br/>weekly checklist"]
        c5["au_rental_search · every 48h<br/>new rentals found"]
    end
    subgraph ops["🛟 OPS bot"]
        d1["self-heal watchdog · hourly<br/>only if it escalated something"]
        d2["/health · on demand<br/>I ask, it answers"]
    end

    work --> phone(["📱 my phone"])
    mba --> phone
    fam --> phone
    ops --> phone
    phone -. "I reply 'done: X', it sticks" .-> brain[("🧠 memory")]

    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
    class work,mba,fam,ops g;
```

Notice the asymmetry: the **family** bot is the chattiest (school + an international move are time-sensitive), the **work** bot fires on a predictable rhythm with two "only-if-it-matters" interrupters, the **MBA** bot deliberately pings *once a week* with its smartest output, the cross-lane link between a podcast and a course, and the **ops** bot stays silent unless the fleet itself needs help (or I ask it `/health`). Everything else those lanes do is quiet plumbing into memory. (The ops lane gets its own chapter: [09 · The ops lane →](09-the-ops-lane.md).)

And it's **two-way**: every bot is a conversation, not a broadcast. I reply `done: <thing>` and the agent marks it complete in memory; I can ask `/podcast_q oil Iran` and it searches the corpus on demand. (More in [memory](04-memory.md).)

---

## The three connection patterns worth noticing

Strip away the 35 boxes and there are really only **three wiring tricks** doing the work:

```mermaid
flowchart LR
    subgraph p1["1 · Watchers feed the brief"]
        direction TB
        w["5 cheap ⚙️ watchers<br/>gather data first"] --> b["1 🧠 brief reads<br/>all of it at once"]
    end
    subgraph p2["2 · Memory loops across days"]
        direction TB
        t["today's brief"] --> mm[("🧠")]
        mm -. "tomorrow" .-> t2["opens with<br/>'what changed'"]
    end
    subgraph p3["3 · Lanes collaborate via memory"]
        direction TB
        cm["MBA: course themes"] --> mm2[("🧠")]
        pm["Work: podcast insights"] --> mm2
        mm2 --> br["Sunday bridge<br/>finds the overlap → 📱"]
    end
```

1. **Watchers → brief.** Five free scripts do the gathering so the *one* paid AI call only does the judging. (Cost control, [design principles](05-design-principles.md).)
2. **Memory across days.** A brief is archived the moment it's sent, so tomorrow's can open with a diff, *"since yesterday: S&P upgraded SA outlook."*
3. **Lanes collaborate.** The work lane's podcast insights and the MBA lane's course themes live in the same memory; a Sunday job reads both and spots the overlap. Two agents that never call each other still cooperate, through shared memory. (See [memory](04-memory.md).)

---
**Next:** [01 · What is an agent? →](01-what-is-an-agent.md) (back to the start)

**Back to:** [README](../README.md) · [Schedule](06-the-schedule.md) · [Architecture](02-architecture.md) · [Memory](04-memory.md)
