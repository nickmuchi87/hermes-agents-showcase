# 13 · Glossary

Plain-English definitions for the terms used across this repo. No prior knowledge assumed.

| Term | What it means here |
|------|--------------------|
| **Agent** | A long-running program that wakes on a schedule, gathers information, runs it through an AI with a specific job and memory, and messages me only when something matters. Not a chatbot you open; it comes to you. ([more](01-what-is-an-agent.md)) |
| **Lane** | One agent dedicated to one part of my life (work, MBA, family) plus a supervisory **ops** lane. Same machinery, different job description, memory, and data sources. ([more](02-architecture.md)) |
| **LLM** (large language model) | The kind of AI behind ChatGPT / Claude: it reads messy text and produces useful text. It does the *judging*; everything around it is plumbing. |
| **Model** | A specific AI you can call (e.g. Claude, DeepSeek, Gemini, Grok). Different models trade off cost, speed, and quality, so different jobs use different ones. |
| **Scheduled job / cron** | A task set to run at a fixed time ("every day at 11:15", "every 30 minutes"). "Cron" is the decades-old unix name for a scheduler. The fleet runs ~35 of these a day. ([the schedule](06-the-schedule.md)) |
| **Agent job vs no-agent job** | An **agent** job calls the AI (costs a little money). A **no-agent** job is a pure script with no AI (free). Most jobs are no-agent; the AI is reserved for genuine judgment. |
| **Gateway** | The always-on process for one lane: it holds the lane's schedule, runs its jobs, and sends its messages. If a gateway is down, that lane goes quiet. |
| **SOUL (SOUL.md)** | A plain-text "constitution" telling a lane's AI who it is and how to behave: tone, hard rules, what to never do. This is where the lanes differ most. ([example](../examples/SOUL.example.md)) |
| **Prompt** | The instructions handed to the AI for a given task. A good prompt is the difference between a useful answer and a useless one. |
| **Token** | The unit AI providers bill and measure by, roughly a word-piece. "A smaller context window" means a model can hold fewer tokens at once. |
| **Context window** | How much text a model can consider in one go. Overflow it and the job fails, which is exactly [one of the real bugs](11-when-it-goes-wrong.md). |
| **Fallback chain** | "Try the cheap or free option first; if it fails, fall through to a premium one." How the fleet survives a provider outage without me noticing. ([router](02-architecture.md)) |
| **OpenRouter** | A single API that sits in front of many AI providers, so I can pick the best model per job by changing a string instead of juggling five separate accounts. ([more](02-architecture.md)) |
| **MCP** (Model Context Protocol) | A standard way to expose real tools (Gmail, Calendar, Drive) to an AI. When you see `mcp_...` in the code, that's a real tool call, as opposed to a [tool the AI hallucinated](11-when-it-goes-wrong.md). |
| **Memory** | A small service the agents read and write so they remember things across days. It's how today's brief can open with "here's what changed since yesterday" and how two lanes collaborate. ([more](04-memory.md)) |
| **Watchdog / self-heal** | A job that runs hourly, spots failed jobs, and fixes a short whitelist of safe, reversible breakages on its own; everything else it escalates to me. ([ops lane](09-the-ops-lane.md)) |
| **Drift** | When an agent creates a skill at runtime that bypasses curation. A nightly audit flags it so good ones get promoted and junk gets removed. ([ops lane](09-the-ops-lane.md)) |
| **Telegram** | The messaging app the bots reach me through, one bot per lane, so work / school / family / ops stay separate threads on my phone. |

---
**Back to:** [README](../README.md) · [What is an agent](01-what-is-an-agent.md) · [Architecture](02-architecture.md)
