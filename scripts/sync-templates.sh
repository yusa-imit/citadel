#!/usr/bin/env bash
# Re-render template-owned skeleton files (build.zig, ci.yml, README, LICENSE, .gitignore) into the
# foundation repos — on a branch, never on a dirty tree, never directly on main.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
for n in sigil sirocco strata synod; do
  repo="$here/../$n"
  if ! git -C "$repo" diff --quiet || [ "$(git -C "$repo" symbolic-ref --short HEAD)" != main ]; then
    echo "$n: skipped (dirty tree or not on main)"; continue
  fi
  git -C "$repo" checkout -q -b "chore/sync-templates-$(date +%Y%m%d)"
  python3 "$here/scripts/scaffold.py" "$n" --force
  if git -C "$repo" diff --quiet; then git -C "$repo" checkout -q main; git -C "$repo" branch -q -D "chore/sync-templates-$(date +%Y%m%d)"; echo "$n: no changes"; continue; fi
  echo "$n: changes on branch chore/sync-templates-$(date +%Y%m%d) — review, commit, and open a PR"
  git -C "$repo" checkout -q main
done
