#!/bin/bash
# skill_drift_audit.sh: captured-skill drift detector.
#
# Curated skills live once in a central library and are SYMLINKED into each
# lane's skills/ directory. A skill that exists as a real directory (not a
# symlink) is one an agent captured at runtime, bypassing the curation +
# lint discipline. This finds them so good ones get promoted and junk gets
# deleted. It's stateless, so it re-reports the same backlog until triaged.
#
# Paired with skill_lint.py (vetting) and skillify.sh (triage).
# See docs/09-the-ops-lane.md. (Sanitized: paths are placeholders.)
#
# Exit code:  0 = clean, 1 = drift detected.

set -eo pipefail
LIB=/opt/skill-library                 # the curated source-of-truth library
LANES="work mba family"
DRIFT_LIST=()

for lane in $LANES; do
  SKILLS_DIR="$HOME/.agent-$lane/skills"
  [[ -d $SKILLS_DIR ]] || continue
  while IFS= read -r skill_md; do
    skill_dir=$(dirname "$skill_md")
    if [[ ! -L $skill_dir ]]; then        # a real dir, not a symlink => drift
      echo "DRIFT: lane=$lane path=$skill_dir"
      DRIFT_LIST+=("$skill_dir")
    fi
  done < <(find "$SKILLS_DIR" -maxdepth 3 -type f -name SKILL.md 2>/dev/null)
done

if [[ ${#DRIFT_LIST[@]} -gt 0 ]]; then
  echo
  echo "Found ${#DRIFT_LIST[@]} captured-skill drift(s). Triage each with:"
  for p in "${DRIFT_LIST[@]}"; do
    echo "  ./skillify.sh \"$p\""
  done
  exit 1
fi

echo "Audit clean. No captured-skill drift across the lanes."
exit 0
