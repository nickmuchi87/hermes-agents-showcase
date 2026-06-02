#!/bin/bash
# skillify.sh <drift_path>: triage one captured-skill drift directory.
#
#   1. Lints SKILL.md against fictional-tool patterns (skill_lint.py)
#   2. lint FAIL  -> recommends rm -rf (a junk hallucination)
#   3. lint PASS  -> shows preview + the exact promote commands
#
# It prints commands; it does NOT auto-execute. A human decides.
# See docs/09-the-ops-lane.md. (Sanitized: paths are placeholders.)

set -eo pipefail
LIB=/opt/skill-library
DRIFT_PATH="$1"
[[ -n $DRIFT_PATH ]] || { echo "usage: $0 <drift_path>" >&2; exit 2; }
[[ -d $DRIFT_PATH ]] || { echo "ERROR: $DRIFT_PATH is not a directory"; exit 1; }
[[ -L $DRIFT_PATH ]] && { echo "NOTE: already a symlink, not drift. Nothing to do."; exit 0; }

NAME=$(basename "$DRIFT_PATH")
MD="$DRIFT_PATH/SKILL.md"
[[ -f $MD ]] || { echo "ERROR: no SKILL.md at $MD"; exit 1; }
LANE=$(echo "$DRIFT_PATH" | sed -nE 's|.*\.agent-([a-z]+)/.*|\1|p')

echo "=== Drift candidate: $NAME (lane $LANE) ==="
echo

echo "=== Lint check ==="
if python3 ./skill_lint.py "$MD"; then
  echo "Lint: PASS, safe to promote"
  echo
  echo "=== SKILL.md preview ==="; head -30 "$MD"; echo
  echo "=== Recommended: PROMOTE ==="
  echo "  mv \"$DRIFT_PATH\" \"$LIB/$NAME\""
  echo "  ln -sfn \"$LIB/$NAME\" \"$DRIFT_PATH\""
else
  echo
  echo "Lint: FAIL, captured-hallucination pattern detected."
  echo
  echo "=== SKILL.md preview ==="; head -30 "$MD"; echo
  echo "=== Recommended: DELETE ==="
  echo "  rm -rf \"$DRIFT_PATH\""
fi
