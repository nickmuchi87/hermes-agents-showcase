#!/usr/bin/env python3
"""pm_decision_loop.py: the AI PM's daily decision, in sketch form.

Shows the shape described in docs/14-the-ai-pm.md: cheap deterministic signal
gathering, then a budget-capped deliberation where a flagship model reasons over
everything and commits a full set of weights via a single tool call, then a
human-readable memo. Paper trading only; a real version has far more signal
detail, retries, and an audit trail.

This is illustrative pseudo-code (the model/tool calls are stubbed) and is not
the production engine. See docs/14 for the why.
"""
from __future__ import annotations

UNIVERSE = ["BRA", "MEX", "COL", "TUR", "ZAF", "EGY", "NGA", "GHA", "IDN", "PAK"]
BENCHMARK = {c: 0.10 for c in UNIVERSE}      # equal-weight benchmark
DECISION_BUDGET_USD = 0.50                    # hard ceiling per daily decision


class Budget:
    """A per-decision spend cap. The deliberation stops when it's exhausted, and
    the decision is flagged 'degraded' rather than silently overspending."""
    def __init__(self, limit_usd: float):
        self.limit = limit_usd
        self.spent = 0.0

    def charge(self, usd: float) -> None:
        self.spent += usd

    def remaining(self) -> float:
        return max(0.0, self.limit - self.spent)


def gather_signals() -> dict:
    """Cheap + deterministic: no flagship model here. Compute the regime from
    macro z-scores, pull relative-value and credit signals, and tag news with a
    fast cheap model. The expensive reasoning is saved for deliberation."""
    return {
        "regime": compute_regime(),              # 'calm' | 'transition' | 'stress'
        "rv": load_relative_value_signals(),     # rich/cheap, curve, dispersion
        "credit": load_credit_signals(),         # spreads, fundamentals, events
        "news": categorize_news_cheaply(),       # fast cheap model tags each item
    }


def run_daily_decision() -> dict:
    budget = Budget(DECISION_BUDGET_USD)
    signals = gather_signals()

    # The deliberation: a flagship model reasons across several turns and may
    # call tools to look closer. It MUST finish by calling submit_decision.
    weights, rationale, caveats, confidence = None, "", [], "low"
    degraded = False
    for turn in range(1, 9):
        if budget.remaining() < 0.05:            # cheap-first guard: wrap up early
            degraded = True
            break
        step = flagship_reason(signals, prior_turns=turn)   # stubbed model call
        budget.charge(step["cost_usd"])
        if step["tool"] == "look_closer":
            signals = enrich(signals, step["args"])          # e.g. one country
            continue
        if step["tool"] == "submit_decision":
            weights = normalize(step["args"]["weights"])     # must sum to ~1.0
            rationale = step["args"].get("rationale", "")
            caveats = step["args"].get("caveats", [])
            confidence = step["args"].get("confidence", "low")
            break

    if weights is None:                          # never committed -> hold
        return {"no_trade": True, "regime": signals["regime"], "degraded": True}

    active = {c: round(weights.get(c, 0.0) - BENCHMARK[c], 4) for c in UNIVERSE}
    return {
        "regime": signals["regime"],
        "final_weights": weights,
        "active_weights": active,                # >0 overweight, <0 underweight
        "benchmark_weights": BENCHMARK,
        "rationale": rationale,
        "caveats": caveats,
        "confidence": confidence,
        "degraded": degraded,
        "cost_usd": round(budget.spent, 4),
    }


def format_memo(d: dict) -> str:
    """Build the Telegram memo from the structured decision."""
    if d.get("no_trade"):
        return f"AI PM: NO TRADE (regime {d['regime']}), holding."
    ow = [c for c, a in d["active_weights"].items() if a > 0.005]
    uw = [c for c, a in d["active_weights"].items() if a < -0.005]
    lines = [
        f"AI PM decision (regime {d['regime']}, confidence {d['confidence']})",
        f"Overweight: {', '.join(ow) or 'none'}",
        f"Underweight: {', '.join(uw) or 'none'}",
        d["rationale"][:600],
    ]
    if d["caveats"]:
        lines.append("Caveats: " + "; ".join(d["caveats"][:3]))
    if d.get("degraded"):
        lines.append("(degraded: deliberation hit its budget and wrapped up early)")
    return "\n".join(lines)


# --- stubs (a real version wires these to data sources + the model SDK) ---
def compute_regime(): return "transition"
def load_relative_value_signals(): return {}
def load_credit_signals(): return {}
def categorize_news_cheaply(): return []
def enrich(signals, args): return signals
def normalize(weights): return weights
def flagship_reason(signals, prior_turns):
    return {"tool": "submit_decision", "cost_usd": 0.02,
            "args": {"weights": {c: 0.10 for c in UNIVERSE},
                     "rationale": "Benign vol; stay close to benchmark.",
                     "caveats": ["Oil reversal would hurt oil exporters"],
                     "confidence": "medium"}}


if __name__ == "__main__":
    decision = run_daily_decision()
    print(format_memo(decision))
