---
name: release
description: Release a realm after a milestone completes — version bump, CHANGELOG, tag, GitHub release, consumer migration issues.
argument-hint: <realm> <major|minor|patch>
---

Follow `/Users/fn/codespace/citadel/protocol/VERSIONING.md`. Abort loudly on any failed gate.
Respect the cycle deadline: every CI wait is capped at `min(8 min, deadline − now)`; if a wait
expires, record `release vX.Y.Z awaiting CI` in realm memory and return to `/report`.
1. Gates: milestone checklist complete; `zig build test` green; CI green on main; zero open
   `bug` issues; `git tag -l 'v*' --sort=-v:refname | head -1` < new version; `build.zig.zon`
   version < new version.
2. PR `chore: release vX.Y.Z`: bump `build.zig.zon`, move `CHANGELOG.md` `[Unreleased]` into
   `## [X.Y.Z] - YYYY-MM-DD`. Merge when green (capped wait).
3. `git tag -a vX.Y.Z -m "Release vX.Y.Z"`, `git push origin vX.Y.Z`,
   `gh release create vX.Y.Z --title vX.Y.Z --notes-file <changelog section>`.
4. Consumers = repos whose `build.zig.zon` `.dependencies` actually names this realm (grep the
   nine sibling repos), intersected with `/Users/fn/codespace/citadel/zr-repos.toml [deps]`. For each, open ONE issue
   `migration: <realm> vX.Y.Z` (label `from:<realm>`, create the label if missing) unless an open
   one already exists for that consumer; list the API changes from CHANGELOG.
5. Close the `milestone` issue with the release link. Record the release in
   `/Users/fn/codespace/citadel/realms/<realm>/STATE.md`; the citadel cycle propagates it to
   `docs/KINGDOM.md`.
