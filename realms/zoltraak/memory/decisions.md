# zoltraak — decisions

_(migrated and condensed from the repo's former CLAUDE.md and `.claude/memory/`)_

- **zuda-first, no local workarounds.** New data structures/algorithms must check zuda
  before a local implementation is written; zuda bugs get an upstream issue
  (`bug,from:zoltraak`) and a wait, never a local patch-around. This is now the kingdom-wide
  rule in `citadel/core/rules/00-kingdom.md` — no zoltraak-specific deviation exists other
  than the two permanently-BLOCKED exceptions below, which are accepted departures, not
  violations.
- **Geohash stays local, permanently.** Decided at the zuda-migration review: zuda's
  geometry API is string/base32-shaped, Redis sorted-set storage needs a 52-bit binary
  integer. Not a temporary blocker — do not re-open without a zuda API change.
- **Sorted Set migration is READY but deliberately deferred**, sequenced behind Geohash/
  HyperLogLog resolution so the migration order goes simplest-first (Glob, Haversine already
  landed).
- **Blocking semantics stay polling-based for now, on purpose.** The real event-driven
  infra (`src/storage/blocking.zig`) was built but deliberately not wired in, because wiring
  it needs a general event-loop refactor first (see `architecture.md`) rather than a
  point fix — the project chose to ship polling-based blocking behavior and defer the
  correct architecture rather than block on it.
- **WAITAOF ships as a stub deliberately** — full AOF fsync tracking was judged not worth
  building until real usage demanded it; documented as a known stub, not an oversight.
- **Version must be strictly monotonic and never skipped**, and a release requires
  `zig build test` green with zero open `bug`-labeled issues — this repo's own version of
  what `citadel/protocol/VERSIONING.md` now states kingdom-wide. The repo's own bespoke
  numeric thresholds (MINOR needs ≥20 new commands, MAJOR needs 500+ commands + human
  approval) were project-specific refinements on top of that; treat `VERSIONING.md` as the
  source of truth going forward, not these historical numbers.
- **`git add -A` is forbidden**, and every commit uses explicit paths — this predates and
  matches the kingdom-wide rule in `citadel/core/rules/git-github.md`.
- **Background processes must be killed and port 6379 freed before ending any session** —
  this was a hard rule in the repo's own autonomous-session protocol, kept as a realm-
  specific run note in REALM.md since nothing else in citadel covers it.
- **The 9-agent bespoke pipeline (spec-analyzer → test-writer/implementor → quality/code
  reviewer → integration-orchestrator → compat/perf validators → commit-push) was a
  deliberate choice** to enforce TDD and a hard quality gate per command-family iteration.
  This decision is now superseded: citadel's own `implement`/`stabilize`/`review` skills
  play that role kingdom-wide, so the bespoke `.claude/agents/` definitions were not carried
  forward as files — only the technical pattern they enforced (test-first, one iteration =
  one feature, no scope creep) is worth remembering, and is captured in `patterns.md`.
