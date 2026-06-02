# 7 · How I built this

The honest version, for anyone thinking *"could I do something like this?"* Short answer: yes, and you don't need to be an engineer, but you do need to be willing to iterate.

## It started as one annoyed afternoon

I was drowning. Three inboxes, a relocation, an MBA, and a day job where missing an IMF headline costs real money. I didn't set out to build a "fleet." I built **one** thing, a script that read my work inbox and texted me a morning summary, because I was tired of doom-scrolling Bloomberg at 6am.

It was useful enough that I built a second one for family. Then the pattern became obvious: *same machinery, different job description.* The fleet grew from there.

## The stack (and why)

| Layer | What I used | Why |
|-------|-------------|-----|
| **Agent runtime** | [Hermes Agent](https://hermes-agent.nousresearch.com) | Open-source, handles scheduling + tools + messaging so I didn't build that plumbing |
| **Where it runs** | One $5/month cloud server | Always-on; my laptop sleeps |
| **How it reaches me** | Telegram bots | Free, instant, works everywhere, easy to reply to |
| **The "thinking"** | Claude, DeepSeek, Gemini, via [OpenRouter](https://openrouter.ai) | One API in front of all of them; route by cost/quality, swap models by changing a string ([details](02-architecture.md#one-gateway-many-models-openrouter)) |
| **Memory** | A small local memory service | So agents remember across days + collaborate |
| **Data** | Gmail, Google Calendar/Drive, RSS feeds, podcast feeds | Where my actual life already lives |

## What actually took the time

Not the AI. The AI part, "read this, tell me what matters", worked almost immediately. The 90% was everything *around* it:

- **Stopping the spam.** The first versions messaged me constantly. Teaching each agent to *stay quiet unless it mattered* took more iteration than anything else.
- **Cost control.** An early job quietly cost ~$15/month doing nothing useful (it called the AI every 30 min to almost always report "nothing"). Finding and fixing those is ongoing. ([Design principle #2](05-design-principles.md).)
- **Failure handling.** APIs flake. Models return junk. A weekly report died because *one* item in it was malformed. Every one of those became a rule. ([Design principles #3-4](05-design-principles.md).)
- **Keeping the three brains separate.** The whole value is that my family agent doesn't think like my work agent. Enforcing that cleanly took discipline.

## I built it *with* an AI, too

This is worth saying plainly: I'm a portfolio manager, not a software engineer. I built and maintain this **collaboratively with Claude** (Anthropic's AI, running in a coding assistant). I describe what I want in plain English, "the synthesis failed because one podcast quote had no citation, fix it so one bad item doesn't sink the whole thing", and iterate from there.

That's the actual unlock for non-engineers: you don't have to know *how* to write the fallback logic or the cron syntax. You have to know **what good looks like**, be specific about failures, and insist on the right behaviour. The AI handles the syntax; you handle the judgment. (Even this repo was written that way.)

## What I'd tell someone starting

1. **Build one agent, for your most annoying recurring task.** Not a fleet. One.
2. **Make it text you only when it matters** before you make it smarter. Noise kills adoption faster than dumbness.
3. **Watch the cost from day one.** Log what each job actually does. "It felt cheap" is how you end up at $300/month.
4. **Assume it'll be wrong sometimes** and design so that's safe, it drafts, you decide.
5. **Use an AI to build it.** Seriously. Describe the behaviour you want; iterate on the failures.

The leverage isn't in any single clever prompt. It's in a boring, reliable loop that runs every day whether you're paying attention or not, and earns enough trust that you *can* stop paying attention.

## Want to actually try it?

This fleet runs on **Hermes**, an open agent runtime. If you want a hands-on, from-zero walkthrough of setting one up, this is a good starting point:

- 📺 **[Hermes Agent Tutorial for Beginners, Step by Step](https://www.youtube.com/watch?v=LvWobwr0Neg)**, a step-by-step video guide to getting a Hermes agent running. (It's the kind of guide that gets you from "what is this?" to a working agent.)

Pair it with the [design principles](05-design-principles.md) here so you build in the cost control and "only ping me when it matters" discipline from day one, rather than learning them the expensive way.

---
**Back to:** [README](../README.md) · [The schedule](06-the-schedule.md) · [Design principles](05-design-principles.md)
