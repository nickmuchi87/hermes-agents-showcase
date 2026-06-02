# Sanitized code examples

These are **redacted excerpts** of the real, in-use code, trimmed to illustrate
a pattern, with all tokens, keys, file paths, and personal data removed or
genericised. They are here to make the [docs](../docs/) concrete, not to run as-is.

| File | Pattern it illustrates |
|------|------------------------|
| [`model_fallback.py`](model_fallback.py) | Cheap-first model routing with a fallback chain (design principle #2 & #3) |
| [`cli_circuit_breaker.py`](cli_circuit_breaker.py) | The "one failure trips the breaker, stop retrying" safeguard (#3) |
| [`sanitize_dont_reject.py`](sanitize_dont_reject.py) | Drop the one bad item, keep the rest (#4) |
| [`corpus_search.py`](corpus_search.py) | A no-AI, free keyword search over agent memory (#2) |
| [`agent_to_memory.py`](agent_to_memory.py) | How an agent writes a structured memory other agents can read (memory doc) |
| [`SOUL.example.md`](SOUL.example.md) | A lane's "job description" / constitution (architecture doc) |

> Every file here is illustrative. The production versions have more error
> handling, logging, and edge-case logic; the noise has been stripped so the
> *idea* is visible.
