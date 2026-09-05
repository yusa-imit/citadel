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
  br="chore/sync-templates-$(date +%Y%m%d)"
  git -C "$repo" add build.zig .github/workflows/ci.yml README.md LICENSE .gitignore src/stdx.zig 2>/dev/null || true
  git -C "$repo" commit -q -m "chore: sync kingdom templates" && git -C "$repo" push -q -u origin "$br" \
    && gh pr create -R "yusa-imit/$n" --head "$br" --title "chore: sync kingdom templates" \
         --body "Rendered from citadel/templates. 🤖 Generated with [Claude Code](https://claude.com/claude-code)" >/dev/null
  echo "$n: PR opened from $br"
  git -C "$repo" checkout -q main
done
