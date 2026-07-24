# 8 · The fleet map: everything, on one page

This is the **whole system in one picture**: every scheduled job across the fleet's four lanes, what each one does, how they connect, and exactly which ones reach my phone over Telegram.

If you only look at one diagram in this repo, make it this one. (The [schedule](06-the-schedule.md) has the same jobs as tables with times; this is the *visual* of how they wire together.)

## How to read it

| Symbol | Meaning |
|--------|---------|
| 🧠 | **Agent job**: calls the AI to read, judge, and write. Costs a little money. |
| ⚙️ | **No-agent job**: a script (deterministic, or one cheap model call). Most jobs are these. |
| 📱 | **Pings my phone**: surfaces to that lane's Telegram bot. |
| 🗃️ → memory | Writes data other jobs read later. I'm *not* pinged. |
| dashed arrow | "Tomorrow reads yesterday", a memory loop across days. |

> All times are **UTC**. My local morning is ~20:30 UTC.

---

## The whole fleet, on one page

The fleet is ~70 jobs, so one all-in-one graph renders too small to read on GitHub. So here it is in **two zooms**: first the *shape* of the whole thing, then **each content lane up close** with every job. Same colour key throughout, **green = pings my phone**, purple = AI/agent, grey = free plumbing, amber = shared memory, blue = Telegram bots.

### Zoom 1, the shape of the whole fleet

```mermaid
flowchart LR
    SRC["📡 SOURCES<br/>Gmail×3 · Calendar · Drive ·<br/>markets / IMF / ratings / press ·<br/>research · podcasts · Canvas"]:::src
    WORK["💼 WORK · 23 jobs<br/>markets · credit · research"]:::work
    MBA["🎓 MBA · 23 jobs<br/>coursework · deadlines · evals"]:::mba
    FAM["👨‍👩‍👧 FAMILY · 11 jobs + school helpers<br/>school · settling in"]:::fam
    OPS["🛟 OPS · 15 jobs<br/>watches the other three"]:::ping
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

### Zoom 2a, 💼 WORK lane (23 jobs)

The pattern to notice: a stack of cheap **watchers** gather data first, then **one** AI brief reads all of it. Green nodes are the ones that surface to me.

```mermaid
flowchart TB
    subgraph WS["⚙️ watchers, gather first (cheap / free)"]
        direction LR
        w_cmp["20:25 · competitor_watch<br/>peer-manager commentary"]:::plumb
        w_idx["20:28 · index_event_monitor<br/>bond-index inclusion event"]:::plumb
        w_pol["20:30 · policy_commentary<br/>think-tank / policy RSS"]:::plumb
        w_arx["20:30 · arxiv_research<br/>new research papers"]:::plumb
        w_prs["20:40 · press_scan_am<br/>morning financial press"]:::plumb
        w_rat["20:50 · rating_watcher<br/>rating-agency actions"]:::plumb
        w_x["20:55 · x_brief_am<br/>X/Twitter regional market scan"]:::plumb
        w_pub["20:55 · em_digest_publish<br/>assemble the digest"]:::plumb
    end
    eml["🧠📱 20:45 · em_email_digest<br/>triage work inbox"]:::ping
    brief["🧠📱 21:15 · em_morning_brief<br/>reads ALL watchers + memory → the brief"]:::ping
    kan["⚙️📱 21:00 · kanban_digest<br/>task-board state"]:::ping
    arch["⚙️ 21:30 · em_brief_archive<br/>save brief → memory"]:::plumb
    vault["⚙️ 21:45 · vault_daily_snapshot<br/>snapshot the data vault"]:::plumb
    ingest["⚙️ 21:50 · agentmemory_ingest<br/>ingest the day → memory"]:::plumb
    prspm["⚙️ 10:10 · press_scan_pm<br/>evening financial press"]:::plumb
    eod["🧠📱 10:45 · em_eod_nudge<br/>EOD wrap: what moved, what needs me"]:::ping
    eoda["⚙️ 01:15 · em_eod_archive<br/>save EOD → memory"]:::plumb
    pod["⚙️📱 Sun/Wed · podcast_weekly_synthesis<br/>cross-episode 2-min read"]:::ping
    pq["⚙️📱 08:00 · podcast_queue_sync<br/>listen-queue + ratings"]:::ping
    nwr["🧠📱 Sat · news_weekly_review<br/>the week's coverage"]:::ping
    dash["⚙️📱 Sun · dashboard_monitor<br/>is the dashboard up?"]:::ping
    aud["⚙️ 03:55 · em_lane_audit<br/>self-check: did it all run?"]:::plumb
    drift["⚙️📱 04:30 · skills_drift_audit<br/>flag a stale skill"]:::ping
    mem[("🧠 memory")]:::mem
    bot(["🤖 Work bot"]):::bot

    WS --> brief
    mem -. "yesterday's diff" .-> brief
    brief --> bot
    eml --> bot
    kan --> bot
    brief --> arch --> mem
    vault --> mem
    ingest --> mem
    prspm -. "context" .-> eod
    eod --> bot
    eod --> eoda --> mem
    pod --> bot
    pq --> bot
    nwr --> bot
    dash --> bot
    drift --> bot
    aud -. "self-check" .-> mem

    classDef agent fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef plumb fill:#f5f5f5,stroke:#9e9e9e,color:#424242;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1,stroke-width:2px;
```

### Zoom 2b, 🎓 MBA lane (23 jobs)

Two clusters: the **study help** (brief, chief-of-staff, pre-class packs, weekly notes) and the **guardrails** (evals, ledger invariants, Canvas reconciliation) that keep the coursework data honest. Its smartest weekly output is the cross-lane link between a podcast and a course.

```mermaid
flowchart TB
    drive["⚙️ every 30m · drive_watch<br/>watch Drive for new coursework"]:::plumb
    pre["⚙️ every 30m · preclass_brief<br/>prep a brief if class is imminent"]:::plumb
    hb["⚙️ every 6h · canvas_heartbeat<br/>is the Canvas data fresh?"]:::plumb
    catchup["⚙️📱 every 15m · canvas_catchup<br/>tick off fresh submissions fast"]:::ping
    chealth["⚙️📱 hourly · canvas_health<br/>is the Canvas pipeline itself ok?"]:::ping
    eclose["⚙️📱 every 3h · email_close<br/>close items email proves done"]:::ping
    commit["⚙️ 20:30 · commitments<br/>mine sent mail for promises made"]:::plumb
    brief["🧠📱 20:30 · daily_wemba_brief<br/>study brief: deadlines, materials, email"]:::ping
    cos["🧠 21:00 · chief_of_staff<br/>deadlines + follow-through"]:::agent
    coseod["🧠 09:00 · chief_of_staff_eod<br/>evening pass"]:::agent
    radar["🧠 21:15 · prof_email_radar<br/>what in course email needs action"]:::agent
    cal["⚙️ 21:00 · calendar_sync<br/>keep the class calendar true"]:::plumb
    recon["⚙️📱 21:00 · assignment_reconcile<br/>assignments vs evidence they're done"]:::ping
    ctruth["⚙️📱 every 3h · canvas_truth<br/>reconcile vs Canvas (source of truth)"]:::ping
    pack["🧠📱 Mon/Thu · preclass_pack<br/>deeper prep before class days"]:::ping
    eod["🧠 01:00 · wemba_eod_nudge<br/>tomorrow's prep"]:::agent
    meval["⚙️📱 Sun · matcher_eval<br/>labeled matching regression suite"]:::ping
    inv["⚙️📱 Sun · ledger_invariants<br/>completion-ledger invariants hold?"]:::ping
    synth["🧠 Sun 22:00 · weekly_synthesis<br/>model panel writes course notes"]:::agent
    load["🧠 Sun 22:00 · load_forecast<br/>next week's coursework load"]:::agent
    cad["⚙️📱 Sun · canvas_cadence_report<br/>weekly coverage report"]:::ping
    bridge["⚙️📱 Sun 23:30 · podcast_course_bridge<br/>links coursework ↔ podcast themes"]:::ping
    aud["⚙️ 03:55 · wemba_lane_audit<br/>self-check"]:::plumb
    work["💼 Work lane's podcast<br/>insights (tag: startup-ai)"]:::agent
    mem[("🧠 shared memory")]:::mem
    bot(["🤖 MBA bot"]):::bot

    drive --> brief
    pre --> brief
    hb -. "freshness" .-> ctruth
    catchup -. "quick closes" .-> ctruth
    eclose -. "email closes" .-> ctruth
    chealth -. "pipeline ok?" .-> ctruth
    commit -. "'you owe' items" .-> brief
    brief --> bot
    brief --> cos
    cos --> recon
    recon --> bot
    ctruth --> bot
    radar -. "actions" .-> mem
    pack --> bot
    meval --> bot
    inv --> bot
    cad --> bot
    synth --> mem
    load -. "forecast" .-> mem
    work --> mem
    mem -. "course themes + podcast insights" .-> bridge
    bridge --> bot

    classDef agent fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef plumb fill:#f5f5f5,stroke:#9e9e9e,color:#424242;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1,stroke-width:2px;
```

### Zoom 2c, 👨‍👩‍👧 FAMILY lane (11 jobs + school helpers)

The most time-sensitive lane. The move has happened, so the centre of gravity is now school life and settling in; it still polls often during waking hours, and a cluster of **school helpers** (system timers rather than lane cron jobs) feeds it.

```mermaid
flowchart TB
    subgraph POLL["⚙️📱 frequent pollers (waking hours)"]
        direction LR
        imm["family_imminent · :00/:30<br/>imminent calendar events"]:::ping
        reloc["relocation_emails · :15<br/>move / settling-in email"]:::ping
    end
    subgraph SCHOOL["🏫 school helpers (system timers)"]
        direction LR
        salert["school_email_alerter · every 30m<br/>school email → family chat"]:::ping
        sport["school_portal_check · each morning<br/>the day's school notices"]:::ping
        scal["school_calendar_watch · daily<br/>public calendar, enriched"]:::plumb
        snews["newsletter_engine · daily<br/>newsletters → tasks + archive"]:::plumb
        sweekly["week_ahead · Sun<br/>unified family week-ahead"]:::ping
        sevents["local_events · Thu<br/>community events, kid-filtered"]:::ping
    end
    cos["🧠 20:00 · chief_of_staff<br/>pull tasks + check follow-through"]:::agent
    brief["🧠📱 20:30 · daily_family_brief<br/>morning brief: today's events + actions"]:::ping
    arch["⚙️ 20:45 · family_brief_archive<br/>save brief → memory"]:::plumb
    adv["🧠📱 21:00 · family_advisor<br/>proactive guidance + flags"]:::ping
    notion["⚙️ 21:00 · notion_sync<br/>mirror the settling-in board"]:::plumb
    urgent["⚙️📱 02:00/08:00 · cos_urgent<br/>only if something is about to fall due"]:::ping
    ins["⚙️📱 Sun · family_insights_digest<br/>weekly, what the lane learned"]:::ping
    sweep["⚙️📱 Sun · relocation_sweep<br/>weekly settling-in checklist"]:::ping
    aud["⚙️ 03:55 · family_lane_audit<br/>self-check"]:::plumb
    mem[("🧠 memory")]:::mem
    bot(["🤖 Family bot"]):::bot

    cos -. "ledger" .-> brief
    snews -. "tasks + archive" .-> cos
    scal -. "flagged events" .-> brief
    brief --> arch --> mem
    brief --> bot
    adv --> bot
    notion -. "board" .-> mem
    urgent --> bot
    POLL --> bot
    salert --> bot
    sport --> bot
    sweekly --> bot
    sevents --> bot
    ins --> bot
    sweep --> bot
    aud -. "self-check" .-> mem

    classDef agent fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef plumb fill:#f5f5f5,stroke:#9e9e9e,color:#424242;
    classDef ping fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
    classDef mem fill:#fff8e1,stroke:#f9a825,color:#5f4300,stroke-width:2px;
    classDef bot fill:#e3f2fd,stroke:#1565c0,color:#0d47a1,stroke-width:2px;
```

> The **ops lane** (the 4th, supervisory one, 15 jobs) has its own close-up in [09 · The ops lane](09-the-ops-lane.md).

**Green nodes ping my phone.** Purple nodes think (AI). Grey nodes are free plumbing into the amber memory store. That's the whole fleet: ~70 jobs, and only the briefs, digests and alerts ever interrupt me, the watchers stay silent.

---

## Just the Telegram side: who is allowed to ping me, and when

The single most important design choice is **restraint**: most jobs never reach my phone. Here's only the part that *can* interrupt me, by lane:

```mermaid
flowchart LR
    subgraph work["💼 WORK bot"]
        direction TB
        a1["em_morning_brief · 21:15<br/>the daily market brief"]
        a2["em_email_digest · 20:45<br/>inbox triage"]
        a3["em_eod_nudge · 10:45<br/>end-of-day wrap"]
        a4["podcast synthesis / queue<br/>the 2-min read + listen-queue"]
        a5["news_weekly_review · Sat<br/>the week's coverage"]
        a6["skills_drift_audit · 04:30<br/>'a skill went stale'"]
    end
    subgraph mba["🎓 MBA bot"]
        b1["daily_wemba_brief · 20:30<br/>deadlines + new materials"]
        b2["preclass_pack · Mon/Thu<br/>prep before class"]
        b3["assignment_reconcile / canvas_truth<br/>'did you finish X?'"]
        b4["podcast_course_bridge · Sun<br/>'this episode maps to your paper'"]
    end
    subgraph fam["👨‍👩‍👧 FAMILY bot"]
        c1["family_imminent · :00/:30<br/>event starting soon"]
        c2["relocation_emails · :15<br/>settling-in mail landed"]
        c3["family_advisor · 21:00<br/>proactive guidance"]
        c4["cos_urgent · 02:00/08:00<br/>something is about to fall due"]
        c5["school helpers · daily<br/>notices, newsletters, week-ahead"]
    end
    subgraph ops["🛟 OPS bot"]
        d1["self_heal_watchdog · hourly<br/>only if it escalated something"]
        d2["fleet_health / morning_ops_digest<br/>readiness, before the briefs"]
        d3["/health · on demand<br/>I ask, it answers"]
    end

    work --> phone(["📱 my phone"])
    mba --> phone
    fam --> phone
    ops --> phone
    phone -. "I reply 'done: X', it sticks" .-> brain[("🧠 memory")]

    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
    class work,mba,fam,ops g;
```

Notice the asymmetry: the **family** bot is the chattiest (school life and settling into a new country are time-sensitive), the **work** bot fires on a predictable rhythm around the morning brief, the **MBA** bot surfaces a daily study brief plus its smartest weekly output (the cross-lane podcast↔course link), and the **ops** bot stays quiet unless the fleet itself needs help (or I ask it `/health`). Everything else those lanes do is quiet plumbing into memory. (The ops lane gets its own chapter: [09 · The ops lane →](09-the-ops-lane.md).)

And it's **two-way**: every bot is a conversation, not a broadcast. I reply `done: <thing>` and the agent marks it complete in memory; I can ask a corpus query and it searches on demand. (More in [memory](04-memory.md).)

---

## The three connection patterns worth noticing

Strip away the seventy boxes and there are really only **three wiring tricks** doing the work:

```mermaid
flowchart LR
    subgraph p1["1 · Watchers feed the brief"]
        direction TB
        w["cheap ⚙️ watchers<br/>gather data first"] --> b["1 🧠 brief reads<br/>all of it at once"]
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

1. **Watchers → brief.** Several free scripts do the gathering so the *one* paid AI call only does the judging. (Cost control, [design principles](05-design-principles.md).)
2. **Memory across days.** A brief is archived the moment it's sent, so tomorrow's can open with a diff, *"since yesterday: S&P upgraded the outlook."*
3. **Lanes collaborate.** The work lane's podcast insights and the MBA lane's course themes live in the same memory; a Sunday job reads both and spots the overlap. Two agents that never call each other still cooperate, through shared memory. (See [memory](04-memory.md).)

---
**Next:** [01 · What is an agent? →](01-what-is-an-agent.md) (back to the start)

**Back to:** [README](../README.md) · [Schedule](06-the-schedule.md) · [Architecture](02-architecture.md) · [Memory](04-memory.md)
