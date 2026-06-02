#!/usr/bin/env python3
"""skill_lint.py: validate a SKILL.md doesn't reference fictional tools.

Real tools use prefixed MCP names (mcp_<server>_<tool>) or shell scripts.
Agents that write their own skills at runtime sometimes "capture" a plausible
but non-existent tool (a direct-API call notion, a code-interpreter idea) that
silently fails when invoked. This linter is a deterministic gate: it knows the
real tool surface and rejects anything outside it.

This is the gate behind the "agent invented a tool that doesn't exist" failure
in docs/11-when-it-goes-wrong.md, and the lint step in docs/09-the-ops-lane.md.

(Lightly sanitized from the live fleet; logic unchanged.)

Usage:    skill_lint.py <SKILL.md> [SKILL.md ...]
Exit:     0 = clean, 1 = violations found, 2 = usage error.
"""

import re
import sys
from pathlib import Path

# Each pattern is a known-fictional tool notion, with the correction to suggest.
FORBIDDEN = {
    r"\bdefault_api\b": "fictional direct-call notion; use prefixed mcp_<server>_<tool> names instead",
    r"\bexecute_code\b": "fictional code-interpreter notion; run bash/python via the terminal tool",
    r"from\s+hermes_tools\s+import": "no such module; tools are exposed via MCP, not python imports",
    r"`google_workspace`\s*(?:tool|MCP|server)": "bare server name is not a tool; use mcp_google_workspace_<tool>",
}


def lint(path: Path) -> int:
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1
    text = path.read_text()
    violations = []
    for pattern, hint in FORBIDDEN.items():
        for m in re.finditer(pattern, text):
            line_no = text[: m.start()].count("\n") + 1
            violations.append((line_no, m.group(), hint))
    if violations:
        print(f"FAIL: {path}")
        for line_no, match, hint in violations:
            print(f"  L{line_no}: {match!r}: {hint}")
        return 1
    return 0


if __name__ == "__main__":
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        print("usage: skill_lint.py <SKILL.md> [SKILL.md ...]", file=sys.stderr)
        sys.exit(2)
    sys.exit(max(lint(p) for p in paths))
