"""
Sanitize, don't reject.

The weekly synthesis asks the AI for structured data — expert views, themes,
contradicting views — each requiring a citation. One run returned 30 perfect
items and 1 missing its citation; the validator rejected the ENTIRE synthesis
over that single item, losing a whole week's analysis.

Fix (design principle #4): drop the malformed item, keep the rest. Be strict
about quality, degrade gracefully. Run the sanitizer BEFORE the validator.

Sanitized excerpt.
"""
import logging

logger = logging.getLogger(__name__)


def sanitize_synthesis(data: dict) -> dict:
    """Drop items missing required fields, keep everything valid. Returns the
    same dict with bad items removed (rather than failing the whole payload)."""
    if not isinstance(data, dict):
        return data
    dropped = 0

    # Expert views need a name, at least one appearance citation, and a thesis.
    ev = data.get("expert_views") or []
    keep = [e for e in ev if isinstance(e, dict)
            and e.get("name") and e.get("podcast_appearances") and e.get("thesis")]
    dropped += len(ev) - len(keep)
    data["expert_views"] = keep

    # Themes need their source citations.
    tc = data.get("theme_convergence") or []
    keep = [t for t in tc if isinstance(t, dict) and t.get("episode_citations")]
    dropped += len(tc) - len(keep)
    data["theme_convergence"] = keep

    # Contradicting-views need a source, the view text, and a country.
    vc = data.get("views_contradicting_my_positions") or []
    keep = [v for v in vc if isinstance(v, dict)
            and v.get("source") and v.get("contradicting_view") and v.get("country")]
    dropped += len(vc) - len(keep)
    data["views_contradicting_my_positions"] = keep

    if dropped:
        logger.info("sanitize: dropped %d malformed item(s), kept the rest", dropped)
    return data


# Usage in the cascade:
#   result = sanitize_synthesis(result)   # <-- drop bad items first
#   errors = validate_synthesis(result)   # <-- now validation passes on the good 95%
#   if errors:
#       continue  # genuinely broken -> try the next model tier
