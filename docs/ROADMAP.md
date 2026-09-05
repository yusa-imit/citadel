# Kingdom Roadmap

Cross-repo order and the prescribed first plan of every realm. Realm-internal detail lives in
each repo's `docs/plans/`. Updated by citadel cycles and by `/integrate`.

## Phase 0 — Restructure (2026-09-05, done by citadel)

- [x] Per-repo `CLAUDE.md`/`.claude/` removed; core moved to `citadel/core`, loaded via
      `/Users/fn/codespace/CLAUDE.md` → `citadel/core/KINGDOM.md`.
- [x] Interrupted work preserved on `wip/*` branches (silica, sailor, zoltraak, zr, zuda).
- [x] Old cron jobs paused; new `<realm>-cycle` jobs defined in `workflows/`.
- [ ] Repo hygiene PRs merged (root artifacts, docs layout, `.gitignore`, CI paths-ignore).
- [ ] `001` plan PRs open in all nine realms, awaiting human merge.

## Phase 1 — Plan 001 everywhere: Zig 0.16 + Tiger Style baseline

Every realm's first plan has the same skeleton; the probe numbers set the size.

| Realm | 0.16 errors (probe) | Effort | Blocked by | Version impact |
|---|---|---|---|---|
| sigil | 1 | trivial | — | none (0.1 → 0.2) |
| strata | 1 | trivial | — | none |
| synod | 1 | trivial | — | none |
| sirocco | 2 | trivial + PRD rewrite to `std.Io.VTable` | — | none |
| zuda | 44 + `linkLibC` | medium | — | **MAJOR** → v3.0.0 |
| sailor | 368 + `linkLibC` | medium | — | **MAJOR** → v3.0.0 |
| zr | 79 + deps | large | zuda v3, sailor v3 | MINOR |
| silica | 275 + deps | medium | zuda v3, sailor v3 | MINOR |
| zoltraak | ~110 + luajit link + deps | large | zuda v3, sailor v3 | MINOR (zon 0.2.0 → 0.3.0; reconcile with claimed 0.2.13) |

Plan 001 skeleton (planner adapts):
1. Hygiene leftovers not covered by the restructure PR.
2. `tidy` test: a `zig build test` step that enforces line length 100, function length 70
   (ratchet: red zone 71–72 for existing code), ban list (`catch unreachable` without proof,
   `std.debug.print` in lib, `std.time.*` in lib, `usize` in formats), `//!` headers.
3. Zig 0.16 migration in checklist order (`citadel/core/rules/zig-0.16.md`), `io: Io`
   convention applied, `minimum_zig_version = "0.16.0"`, CI on 0.16.
4. Assertion baseline: every public function of the top-N hot modules gets pre/post assertions
   (N sized to the realm).
5. Finish or discard the `wip/*` branch (decision recorded).
6. README/CHANGELOG reconciled with reality; release per version impact.

Order of execution across realms (cron runs all realms; blocked items wait):
sigil (spike — sets the `io: Io` convention, records it in `zig-0.16.md`) → strata, synod,
sirocco → zuda, sailor (release v3.0.0) → zr → silica → zoltraak.

## Phase 2 — Foundation v0.1 and first consumers

| Repo | v0.1 scope | First consumer PoC |
|---|---|---|
| sigil | core + reflect + JSON (+path) | zoltraak `JSON.GET` on `sigil.path.jsonpath` |
| sirocco | `std.Io.VTable` implementation: kqueue + epoll, net + sleep/now, hybrid with `Io.Threaded` | swap `Io` at `main` in zoltraak |
| strata | codec + file + page + cache + WAL | synod `LogStore` adapter |
| synod | types + log + raft election/replication + simulator | zoltraak sentinel election |

## Phase 3 — Migrations

- zr → sigil (TOML/YAML), zoltraak → sigil (JSON), synod ↔ strata/sirocco adapters,
  zoltraak → strata (AOF/RDB), zoltraak/silica → synod (failover), silica → strata
  (page/cache/WAL), sailor → sirocco (network widgets).
- Structural debt flagged by the survey, one plan each: silica `engine.zig` 43k lines /
  `executor.zig` 35k; zoltraak `memory.zig` 15.6k; zr `parseToml` 5.1k-line function; zuda
  `distributions.zig` 128k lines; sailor 52 files > 800 lines.

## Phase 4 — Next components

Observability, auth/crypto utilities, plugin VM (WASM), client SDKs, message stream, S3-compatible
object store, web framework. Each starts with `/new-realm`.
