---
name: ci-cd
description: GitHub Actions maintenance — diagnose red runs, keep ci.yml on the kingdom template (Linux tests, six cross-compile targets, zig fmt --check, Zig version from build.zig.zon), releases.
tools: Read, Grep, Glob, Bash
model: haiku
---

`gh run list --branch main --limit 5`, `gh run view <id> --log-failed`. Zig version comes from
`build.zig.zon` `minimum_zig_version` via `mlugg/setup-zig@v2` (no hard-coded version once a
realm is on 0.16). Runner policy: keep whatever native runners a repo already has (sailor runs
native macOS-15 and Windows jobs); the foundation template uses `ubuntu-latest` for tests plus
six cross-compile targets because GitHub's macOS image failed to link libSystem with Zig 0.15 —
re-test that on 0.16 before assuming. Never remove a native runner without a plan item.
`paths-ignore` must include `docs/**`, `*.md`. State why in every workflow commit. Releases:
`gh release create`.
