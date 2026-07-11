# Three AI Agents That Run My Life, and One That Keeps Them Alive

![Three AI agents: Work, MBA, Family](images/hero.png)

> How one person uses a small fleet of always-on AI agents to handle **work**, an **MBA**, and **family logistics**: explained for people who have never touched an "agent" before.

I'm an emerging-markets fixed-income portfolio manager, a part-time Wharton EMBA student, and a dad relocating a family across the world. Three different lives, three different streams of email/calendars/documents/news, and not enough hours.

So I built the fleet: **three user-facing agents run my work, school, and family workflows. A fourth, supervisory agent watches the fleet itself**, fixing the safe stuff on its own and asking me about the rest. Together they run about 60 scheduled jobs a day, but stay silent unless something actually needs me.

This is not a product or a clone-and-run template. It is a **field guide** to what worked, what failed, what it costs, and the guardrails that make always-on agents tolerable in real life. It is deliberately written for a **non-technical reader**. If you've heard "AI agents" and thought *"...okay but what does that actually mean in practice?"*, this is for you.

---

## The one-paragraph version

Each agent ("lane") is a long-running program that wakes up on a schedule, gathers information from my email/calendar/documents/news feeds, runs it through a large language model (the same kind of AI behind ChatGPT/Claude) with a **specific job description and memory**, and then sends me a short, human Telegram message, only when something's worth my attention. The fleet does this on its own, ~60 scheduled jobs a day, across three separate content "lanes" so my work brain, school brain, and family brain never bleed into each other, while the fourth lane watches the other three.

```
   📨 emails        📅 calendars       📰 news/RSS        📑 documents
        \                |                  |                /
         \               |                  |               /
          ▼              ▼                  ▼              ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                  THREE AI AGENT "LANES"                       │
   │                                                               │
   │   💼 WORK (em)        🎓 MBA (wemba)        👨‍👩‍👧 FAMILY        │
   │   markets, credit,    course prep,          school, relocation,│
   │   IMF, ratings        deliverables          calendar           │
   └─────────────────────────────────────────────────────────────┘
              ▲                   │
              │ safe auto-fixes   ▼
   ┌──────────┴──────────┐   📱 short Telegram messages,
   │ 🛟 OPS lane watches  │      only when it matters
   │ the other three     │
   └─────────────────────┘
```

---

## Why separate agents instead of one?

Because **context is everything**, and mixing it makes the AI worse at all three jobs.

- My **work** agent knows it's a sovereign-credit PM. It cares about Egypt's IMF program and Brazilian rates. It should *never* surface my daughter's school newsletter.
- My **MBA** agent knows my Wharton courses and deliverables. It links a podcast on startup unit-economics to my entrepreneurship class.
- My **family** agent knows we're relocating, knows the kids' schools, and counts down to move-day. It should never page me about bond spreads.
- And the **ops** agent knows nothing about any of that: its whole world is "did every job run, is every feed fresh, what needs fixing."

Same underlying AI, four different **"job descriptions" + memories + data sources**. That separation is the whole trick.

| Lane | Role | Watches | Example output |
|------|------|---------|----------------|
| 💼 **Work** (`em`) | EM sovereign-credit chief-of-staff | Financial press, IMF, rating agencies, EM podcasts, research | "Morning brief: Nigeria OW under pressure, Brent <$90; S&P upgraded SA outlook." |
| 🎓 **MBA** (`wemba`) | EMBA study partner | Google Drive coursework, Wharton email, class calendar, Canvas | "Pre-class brief: OIDD 6360 case due Thu; a podcast this week maps to your scaling-ops paper." |
| 👨‍👩‍👧 **Family** (`family`) | Household logistics assistant | School emails, relocation tasks, family calendar | "T-14 to the move. Patricia (school) sent enrolment forms, due Friday." |
| 🛟 **Ops** (`ops`) | On-call SRE for the fleet | The other three lanes' jobs, feeds, and services | "Repaired a torn login token at 22:00; everything else green." |

Everything reaches me the same way: **separate Telegram bots**, one per lane, and only when something's worth my attention.

![Telegram bots messaging only when it matters](images/telegram-bots.png)

### See it in action

> 📸 *Real screenshots of the bots in daily use live in [`images/screenshots/`](images/screenshots/).*

**MBA bot, the daily WEMBA brief:** deadlines, what's new in Drive, and what's worth noting, pushed each morning.

![WEMBA daily brief: pending deadlines, new Drive files, and worth-noting items](images/screenshots/mba-preclass.png)

<!-- Work-bot + family-bot shots to add next: images/screenshots/work-brief.png, images/screenshots/family-nudge.png
| Work bot, morning brief | MBA bot, brief | Family bot, relocation nudge |
|---|---|---|
| ![](images/screenshots/work-brief.png) | ![](images/screenshots/mba-preclass.png) | ![](images/screenshots/family-nudge.png) |
-->


---

## Where to start

The full field guide is **22 chapters**: the [complete index is in `docs/`](docs/README.md). The highlights:

| Featured chapter | Why read it |
|------------------|-------------|
| [01 · What is an agent?](docs/01-what-is-an-agent.md) | Plain-English: what an "agent" actually is, vs. a chatbot |
| [05 · Design principles](docs/05-design-principles.md) | The hard-won rules: cost control, "only ping me when it matters", failure handling |
| [08 · The fleet map](docs/08-the-fleet-map.md) | The whole system on one page: every job, every connection, and which ones ping my phone |
| [10 · What it costs](docs/10-what-it-costs.md) | The honest money page |
| [11 · When it goes wrong](docs/11-when-it-goes-wrong.md) | A gallery of real failures and how each was caught: the most honest page here |
| [21 · Evals as tripwires](docs/21-evals-as-tripwires.md) | The day all four bots went quietly wrong, and the regression suite that now guards the fleet |
| [22 · The queue that learns my taste](docs/22-the-queue-that-learns-my-taste.md) | The fleet stops guessing what I want and learns it from my own plain-word verdicts |

### A reading path, by who you are

- **Total beginner:** [01 What is an agent](docs/01-what-is-an-agent.md) → [03 A worked example](docs/03-the-digest-pipeline.md) → [04 Memory](docs/04-memory.md) → [12 FAQ](docs/12-faq.md). Keep [13 Glossary](docs/13-glossary.md) open in a tab.
- **Want the architecture:** [02 Architecture](docs/02-architecture.md) → [08 The fleet map](docs/08-the-fleet-map.md) → [09 The ops lane](docs/09-the-ops-lane.md) → [05 Design principles](docs/05-design-principles.md).
- **Thinking of building one:** [07 How I built this](docs/07-how-i-built-this.md) (incl. a step-by-step Hermes tutorial) → [05 Design principles](docs/05-design-principles.md) → [10 What it costs](docs/10-what-it-costs.md) → [`examples/`](examples/).

---

## The honest disclaimers

- **This is a personal setup, not a product.** It's shared to *explain a way of working*, not as something to clone-and-run. Secrets, tokens, and personal data have been removed.
- **It costs real (small) money.** The agents call commercial AI APIs. The fleet itself stays cheap by design; the full, honest breakdown (and what my larger ~$300/mo AI habit actually covers) is in [what it costs](docs/10-what-it-costs.md).
- **The AI is a junior assistant, not an oracle.** It triages and drafts; I decide. Every design choice assumes it will sometimes be wrong.
- **Context stays put.** Lanes don't share personas, credentials, or raw data; only tagged, derived insights cross lanes, deliberately. The exact boundary is a table in [04 · Memory](docs/04-memory.md), and the privacy trade-offs are in the [FAQ](docs/12-faq.md).

---

## The tech, named (for the curious)

Built on [Hermes Agent](https://hermes-agent.nousresearch.com) (an open agent runtime), reachable over Telegram, with a local memory service, scheduled jobs ("crons"), and a mix of language models routed by cost/quality (Claude, DeepSeek, Gemini). Everything runs on one small cloud server. You do **not** need to know any of that to read the docs above, they start from zero.

**Want a hands-on intro to Hermes itself?** This step-by-step video is a good place to start: [Hermes Agent Tutorial for Beginners, Step by Step](https://www.youtube.com/watch?v=LvWobwr0Neg).

---

## Where to go next

- 📖 **Read the field guide:** the [full 22-chapter index](docs/README.md).
- 🧪 **Run the examples:** several of the sanitized scripts in [`examples/`](examples/) run as-is, no keys or setup needed; see the [examples README](examples/README.md).
- 🛠️ **Build your own:** start with [07 · How I built this](docs/07-how-i-built-this.md).

*Questions? This was built and documented collaboratively with Claude (Anthropic). The architecture is real and in daily use.*
