# 12 · FAQ

The questions people actually ask when they see this, answered plainly.

### "Is it reading *all* my email?"

It reads the inboxes I explicitly connect, and only to triage them. A few things keep that sane:
- It runs on **my own small server**, not a third-party app I handed my whole mailbox to.
- Each lane only sees the accounts relevant to its job (the work agent never touches the family inbox).
- It surfaces a short summary of what matters; it isn't storing or forwarding raw email anywhere.

That said, be honest with yourself about this: triaging email with an LLM means the **text of those emails is sent to a commercial AI provider** to be read. That's a real trade-off (see the data question below). I made it deliberately for inboxes I control; you should decide that for yourself.

### "What happens when it gets something wrong?"

It's designed on the assumption that it **will**. The AI's job is to **triage and draft**, not to decide. By the time something reaches me, the noise is gone and what's left is framed for a fast *human* decision, which I make. And there's a whole layer of guardrails that catch its mistakes; see [when it goes wrong](11-when-it-goes-wrong.md) for real examples.

### "Why three (now four) agents instead of one big assistant?"

Because **context is everything**, and mixing it makes the AI worse at all three jobs. A work agent that also knows about the school newsletter starts surfacing the wrong things. Same underlying model, three different job descriptions + memories + data sources. That separation is the whole trick. ([Why three lanes](../README.md).)

### "Why not just use ChatGPT / Claude in a browser?"

A chat window is **reactive**: it waits for you to ask. This is **proactive**: it wakes itself up on a schedule, reads the firehose while I'm asleep, and messages me only when something needs me. The intelligence is similar; the difference is that nobody has to remember to open it. ([What is an agent](01-what-is-an-agent.md).)

### "Can it *do* things, or just message me?"

Mostly it reads and messages. The one lane with "hands" (the [ops lane](09-the-ops-lane.md), which can repair the system) is deliberately fenced: it may only do a short list of **safe, reversible** things on its own, and it **proposes** anything riskier and waits for my one-word yes. An agent that can change things needs a fence.

### "What does it cost?"

The **fleet** is cheap: a small server plus a modest API bill, because most jobs are free deterministic scripts and the AI is used sparingly. My total AI + infrastructure spend is higher (~$300/month), but that's my whole habit across many projects, not this fleet. Full breakdown: [what it actually costs](10-what-it-costs.md).

### "Is my data training someone's AI model?"

The agents call **commercial AI APIs**, so your text passes through those providers under *their* terms. Policies differ by provider and change over time, so the honest answer is: **check each provider's current data-use and retention policy** and choose accordingly. Don't assume a setup like this is private just because it runs on your own server, the *server* is yours, but the *model* isn't.

### "What if a model or provider goes down?"

Each job has a **fallback chain**: try the cheap or free option first, fall through to a premium one if it fails. One night a provider returned empty responses and the system self-healed by falling through to the next model, no intervention needed. ([The model router](02-architecture.md).)

### "Could I build one myself?"

Probably, and you don't need to be an engineer (I'm not a professional one). This repo is an **explainer, not a clone-and-run template**, but the [build story](07-how-i-built-this.md) is honest about the stack and what took the time, and there's a step-by-step Hermes tutorial linked there to get you started.

### "Is this a product I can buy?"

No. It's a personal setup shared to explain *a way of working*, not something packaged. Secrets and personal data have been removed; the architecture is real and in daily use.

---
**Next:** [13 · Glossary →](13-glossary.md)

**Back to:** [README](../README.md) · [What is an agent](01-what-is-an-agent.md) · [When it goes wrong](11-when-it-goes-wrong.md)
