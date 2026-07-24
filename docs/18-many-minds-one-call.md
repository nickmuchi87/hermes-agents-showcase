# 18 · Many minds, one call: getting several AIs to vote

The [AI PM](14-the-ai-pm.md) uses **one** flagship model to deliberate over the day's signals. A newer experiment asks a different question: what if **several** different models each form a view, and then we fuse those views into a single decision? In the literature this is called a *mixture-of-agents*; here it's a third "engine" the PM can run.

> **Several models propose; one synthesis decides, and if the panel gets confused, it quietly falls back to the trusted single model.** A decision always ships.

## The shape

```mermaid
flowchart TB
    sig["📡 the day's EM signals"] --> panel
    subgraph panel["a panel of different models, each forms a view"]
        direction LR
        m1["model A"]
        m2["model B"]
        m3["model C"]
        m4["model D"]
    end
    panel --> syn["🧪 synthesis<br/>fuse the views into one decision"]
    syn --> ok{parsed<br/>cleanly?}
    ok -->|yes| memo["📱 the memo"]
    ok -->|"no"| fb["↩️ fall back to the<br/>proven single-model decision"]
    fb --> memo

    classDef ai fill:#ede7f6,stroke:#5e35b1;
    class panel,syn ai;
```

## Why bother at all

- Different models have different blind spots and habits. A panel can be **steadier** than any single one having an off day.
- But it isn't free: more models means more cost, and more ways to fail (one model returns garbage, or wraps its answer in formatting that breaks the parser).

## How it's kept safe and cheap

Same discipline as the rest of the fleet ([design principles](05-design-principles.md)):

- **It's gated.** It only fires on verified signals, at most once a day.
- **It's an A/B canary**, running *alongside* the proven single-model engine, not replacing it.
- **It auto-falls-back.** If the fused output can't be parsed cleanly, the PM uses the single-model decision instead, so a confused panel never means a missed memo.
- **It's cheap per run**, a couple of cents.

## The honest state

- **This is a trial, not a verdict.** It is *not* yet proven to beat one good model.
- **Early on it fell back a lot.** The panel kept wrapping its answers in formatting (code fences, preambles) that the parser choked on; the fix was a more forgiving parser plus a wider panel. Every one of those fall-back days still shipped a valid decision, which is exactly why the fallback exists.
- **The open question** is the whole point: does a panel of models actually produce better calls than a single strong one, cheaply enough to justify the extra moving parts? That's what the A/B is for.

## Where the council pattern spread

The panel idea graduated from experiment to workhorse in one place: the MBA lane's **weekly course notes**, where several budget models each read the week's materials and a judge fuses their drafts behind a citation gate (the full story is in [20 · The study companion](20-the-study-companion.md)). Scheduled, bounded, once a week: exactly the kind of heavy task where spending a dollar on several models beats spending a cent on one.

## The other direction: escalating one question, on demand

The council is *many cheap minds on a scheduled task*. There's a mirror-image trick for heavy thinking: *one strong mind on a single question*, and only when I ask for it.

Any lane's bot understands a message prefix, `deep:`. Prefix a question with it and the flow changes:

```mermaid
flowchart LR
    q["📱 me: 'deep: should I<br/>restructure X or Y?'"] --> gather["🤖 the lane's normal (cheap) model<br/>gathers: email, files, memory, data"]
    gather --> dossier["🗂️ a clean dossier:<br/>question + everything gathered"]
    dossier --> big["🧠 a frontier reasoning model<br/>(flat-rate subscription, via its CLI)"]
    big --> ans["📱 the deep answer"]
    big -."unavailable / out of quota".-> fb["↩️ lane's normal model answers,<br/>and TELLS me it's the fallback"]
    fb --> ans

    classDef ai fill:#ede7f6,stroke:#5e35b1;
    class gather,big ai;
```

Four design choices doing the work:

1. **Two stages, split by what each tier is good at.** The cheap model does the legwork (searching mail, reading files, pulling memory) because tool-use is cheap; the expensive model receives a finished dossier and spends every token on *reasoning*. It's the [watchers-feed-the-brief pattern](06-the-schedule.md) compressed into one conversation.
2. **A human is the trigger.** Escalation never happens automatically; typing the prefix *is* the opt-in. No cron or scanner is allowed to route itself to the expensive tier, so quota can't quietly leak into plumbing.
3. **Subscription, not metered.** The heavy model runs on a flat-rate consumer subscription through its own CLI, so the marginal cost of a deep question is zero. And because a misconfigured tool could silently fall through to a *metered* API, the call path strips the API credentials from the environment entirely, twice, in two independent layers. Belt and suspenders, for billing.
4. **Fallback is loud, not silent.** If the big model is unavailable (quota gone, login expired), the lane's normal model answers instead **and says so**. A degraded answer pretending to be a deep one would be worse than no feature at all.

Council for the scheduled heavy lifts, `deep:` for the occasional hard question, and the everyday cheap tier for everything else: three price points, each earning its slot.

---
**Back to:** [README](../README.md) · [The AI PM](14-the-ai-pm.md) · [The study companion](20-the-study-companion.md) · [Design principles](05-design-principles.md) · [Architecture](02-architecture.md)
