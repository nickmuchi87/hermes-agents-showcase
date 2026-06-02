"""
Cheap-first model routing with a fallback chain.

Pattern (design principles #2 and #3): try the free/cheap option first, fall
through to a premium model only if needed, and never let one provider's flake
kill the whole job.

Sanitized excerpt, real version has retries, cost logging, and prompt caching.
"""
import os
import requests

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# Per-task model choice, overridable by env so models can be A/B'd without
# touching code. Cheap fast model for bulk work; flagship for hard reasoning.
SUMMARY_MODEL = os.environ.get("SUMMARY_MODEL", "<cheap-fast-model>")   # bulk per-item
SYNTH_MODEL = os.environ.get("SYNTH_MODEL", "<flagship-model>")        # weekly reasoning
SYNTH_FALLBACK_MODEL = os.environ.get("SYNTH_FALLBACK_MODEL", "<fast-model>")  # if flagship flakes


def call_model(prompt: str, model: str, *, json_mode=True, max_tokens=None, timeout_s=120):
    """Single completion call. Returns text, or None on any failure (caller decides
    whether to fall through to the next tier)."""
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return None
    body = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
    if max_tokens:
        body["max_tokens"] = max_tokens
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    try:
        r = requests.post(f"{OPENROUTER_BASE}/chat/completions",
                          headers={"Authorization": f"Bearer {api_key}"},
                          json=body, timeout=timeout_s)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"] or None
    except Exception:
        return None  # let the cascade handle it


def synthesize(prompt: str):
    """Weekly synthesis with a fallback chain:
        free local CLI  →  flagship API  →  fast API
    On a machine with a flat-rate subscription, the first tier costs nothing.
    On the server, the local tier is skipped and it goes straight to the API.
    """
    for label, fn in (
        ("local_cli", lambda p: run_local_cli(p)),                     # $0 where available
        ("flagship",  lambda p: call_model(p, SYNTH_MODEL, max_tokens=8000)),
        ("fallback",  lambda p: call_model(p, SYNTH_FALLBACK_MODEL, max_tokens=8000)),
    ):
        text = fn(prompt)
        if text:
            return {"text": text, "model_used": label}
    return None  # every tier failed, caller degrades gracefully


def run_local_cli(prompt: str):
    """Placeholder for the free local-subscription path (see cli_circuit_breaker.py)."""
    return None
