#!/usr/bin/env bash
# Re-render template-owned files (CLAUDE.md, agents, commands, ci.yml, ...) into every
# foundation repo after editing citadel/templates/repo. Source files are never touched.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
for n in sigil sirocco strata synod; do
  python3 "$here/scripts/scaffold.py" "$n" --force
done
echo "review with: for n in sigil sirocco strata synod; do (cd ../\$n && git status --short); done"
