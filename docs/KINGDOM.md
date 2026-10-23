# The Zig Kingdom — Map

> 아홉 개의 레포, 네 개의 층. 아래층은 위층을 모른다.

```
┌──────────────────────────────────────────────────────────────────────┐
│  SERVICES         silica (RDBMS, PG wire)     zoltraak (Redis-compat) │
├──────────────────────────────────────────────────────────────────────┤
│  TOOLING          zr (task runner · toolchains · monorepo · MCP/LSP)  │
├──────────────────────────────────────────────────────────────────────┤
│  LIBRARIES        sailor (TUI/CLI)            zuda (DS/algos/scicomp) │
├──────────────────────────────────────────────────────────────────────┤
│  FOUNDATION       sigil      sirocco      strata      synod           │
│                   (formats)  (net/async) (storage)   (consensus)      │
└──────────────────────────────────────────────────────────────────────┘
                   ▲ Zig std only — no kingdom dependencies ▲
```

## Components

| Repo | Layer | One line | Status |
|---|---|---|---|
| [sigil](https://github.com/yusa-imit/sigil) | Foundation | Value IR + comptime reflection; JSON/TOML/YAML/MessagePack/CBOR/Protobuf/CSV; layered config | v0.4.0 (2026-10-18, PR #65; v0.3.0 first tag 2026-10-13, PR #53) — plans 001-005 complete (`core`, `reflect`, `json` scanner/DOM/writer, `parseFile`/`stringifyFile`, `path` Pointer/Merge Patch/Patch/JSONPath, bench harness); plan 006 (Phase 3A TOML 1.0) approved (PR #66 merged 2026-10-18); no sibling pins sigil yet |
| [sirocco](https://github.com/yusa-imit/sirocco) | Foundation | Production `std.Io.VTable` implementation (kqueue/epoll/io_uring), powering std net/http/tls | v0.4.0 (2026-10-11, PR #43) — plans 001-003 complete (0.16 migration + Tiger Style; fiber scheduler + futex core; carrier-never-blocks: timing-wheel `sleep`, offload pool for blocking dir/file/net slots, eager `async` start, PRD gate 6 passes at 1000 in flight); everything else forwards to `Io.Threaded`; internal milestone, no consumer pins it; milestone sirocco#33 closed; plan 004 (evented net) approved (PR #44 merged 2026-10-12) |
| [strata](https://github.com/yusa-imit/strata) | Foundation | File I/O abstraction, pages + buffer pool, segmented WAL + recovery, B+Tree, LSM, KV engine, snapshots | v0.5.0 (2026-10-19, PR #61; v0.4.0 2026-10-12, PR #45) — plans 001-004 complete (`codec/`, `file/`, crash-test `testing/`, ADR-0002 `page/` layer, CLOCK `BufferPool`, segmented WAL with group commit, recovery replay, full-page-image redo, checkpoint and segment reclaim, seeded crash-recovery property test); milestone strata#48 closed; no consumer pins strata |
| [synod](https://github.com/yusa-imit/synod) | Foundation | Pure-state-machine Raft, joint consensus, SWIM, φ-accrual, HLC, deterministic simulator | v0.4.0 (2026-10-13, PR #54) — plan 003 complete (pure Raft core: election, replication, driver executing effects in persist, sync, send, apply order; 495 tests); milestone synod#39 closed; plan 004 (Phase 3 deterministic simulation harness) approved (PR #56 merged 2026-10-14; ADR-008 landed, PR #58); no consumer pins synod |
| [zuda](https://github.com/yusa-imit/zuda) | Library | ~60 containers, 24 algorithm families, 209 distributions, NDArray/linalg/stats/FFT/optimize, ML (461k LOC) | v2.3.0 (+130 unreleased commits; Zig 0.16 toolchain flip merged 2026-10-04, PR #60, zon at 0.16.0, v3.0.0 pending; ILU double-free PR #58 and GMRES breakdown PR #59 merged 2026-10-02) |
| [sailor](https://github.com/yusa-imit/sailor) | Library | TUI framework, 140 widgets, CLI toolkit (150k LOC) | v3.1.0 (2026-10-18, PR #63; plan 002 post-v3 cleanup; v3.0.0 2026-10-05, Zig 0.16 migration PR #40; consumer migration issues zr#178, silica#163, zoltraak#141 still open, all pin v2.99.0; main CI green) |
| [zr](https://github.com/yusa-imit/zr) | Tooling | Task runner + toolchain manager + monorepo + MCP/LSP server (112k LOC) | v1.114.0 |
| [silica](https://github.com/yusa-imit/silica) | Service | Embedded/server RDBMS, SQL:2016, MVCC, PG wire, replication (184k LOC) | v1.0.1 |
| [zoltraak](https://github.com/yusa-imit/zoltraak) | Service | Redis-compatible store, 500+ commands, RESP2/3, cluster, Lua (141k LOC) | 0.2.0 in zon (v0.2.14 latest tag) |

## Dependency graph

```mermaid
graph BT
  sigil[sigil]
  sirocco[sirocco]
  strata[strata]
  synod[synod]
  zuda[zuda]
  sailor[sailor]
  zr[zr]
  silica[silica]
  zoltraak[zoltraak]

  synod -.->|adapter| sirocco
  synod -.->|adapter| strata
  sailor -.-> sirocco
  zr --> sailor
  zr --> zuda
  zr -.-> sigil
  zr -.-> sirocco
  silica --> sailor
  silica --> zuda
  silica -.-> sigil
  silica -.-> sirocco
  silica -.-> strata
  silica -.-> synod
  zoltraak --> sailor
  zoltraak --> zuda
  zoltraak -.-> sigil
  zoltraak -.-> sirocco
  zoltraak -.-> strata
  zoltraak -.-> synod
```

Solid = dependency that exists today in `build.zig.zon`. Dotted = planned (see `ROADMAP.md`).

## Rules of the realm

1. **Foundation repos depend on Zig std only.** Kingdom integrations live in `src/adapters/` and are opt-in.
2. **Dependencies point down.** A library never imports a service; a foundation never imports a library.
3. **One version of each dependency across the kingdom.** `zr-repos.toml` `[deps]` is the reference; pin the same tag in every `build.zig.zon` (today zr pins zuda via a forbidden `git+…?ref=main` ref resolving to an untagged commit past v2.0.4 (pre-v2.1.0), zoltraak pins tag v2.0.4, silica pins tag v2.3.0 — tracked as the Phase 1 blocker in ROADMAP.md, converges once zr/zoltraak land zuda v3.0.0).
4. **Every repo has the same shape.** Code, `docs/` (`PRD.md`, `plans/`, `adr/`, `guides/`), `.github/`. No `CLAUDE.md`, no `.claude/` — the brain is `citadel/core/KINGDOM.md`, loaded through `/Users/fn/codespace/CLAUDE.md`. Policy: `protocol/DOCS.md`.
5. **Every repo is driven the same way.** A cron job (`workflows/jobs.toml`) runs `claude -p "/cycle <repo>"` in the repo with citadel attached (`--add-dir`). Plans are approved by merging PRs; see `protocol/GITHUB.md`.
6. **Zig 0.16.0 everywhere.** Realms still on 0.15.2 migrate under plan `001` (`docs/ROADMAP.md`); consumers wait for zuda v3.0.0 (sailor v3.1.0 is released).

## Names

| Name | Why |
|---|---|
| sigil | 의미를 새긴 기호 — 바이트에 의미를 새기는 직렬화 |
| sirocco | 함대를 밀어주는 바람 — sailor의 배를 움직이는 네트워크 |
| strata | 지층 — silica(광물) 아래 켜켜이 쌓인 저장 계층 |
| synod | 회의 — 노드들이 모여 합의에 이르는 곳 |
| citadel | 성채 — 왕국의 지휘소 |
