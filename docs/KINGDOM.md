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
| [sigil](https://github.com/yusa-imit/sigil) | Foundation | Value IR + comptime reflection; JSON/TOML/YAML/MessagePack/CBOR/Protobuf/CSV; layered config | 0.2.0 in zon (no tag yet) — plans 001 and 002 complete (core `Value`/`ValueTree`/`Diagnostics`/number parsing), plan 003 (Phase 1C/1D unicode + comptime reflection) approved (PR #26, 2026-09-29), items 1-7 of 10 merged (`core/unicode.zig`, `unicode_escape.zig`, ADR 0002, `reflect/options.zig`, `reflect/parse.zig` scalars, structs/sequences, unions/string maps/hook; PR #34) |
| [sirocco](https://github.com/yusa-imit/sirocco) | Foundation | Production `std.Io.VTable` implementation (kqueue/epoll/io_uring), powering std net/http/tls | v0.2.0 — plan 001 (0.16 migration + Tiger Style) complete, plan 002 (fiber scheduler + futex core) approved (PR #13, 2026-09-29), items 1-4 of 9 merged (macOS CI, `Runtime` forwarding all 109 slots, parity harness, fiber substrate `sched.zig`; PR #22), naked per-arch fiber switch fix merged (PR #24) |
| [strata](https://github.com/yusa-imit/strata) | Foundation | File I/O abstraction, pages + buffer pool, segmented WAL + recovery, B+Tree, LSM, KV engine, snapshots | v0.2.0 (PR #15) — plan 001 (0.16 migration + Tiger Style hygiene) complete; plan 002 (codec, file I/O, crash harness) items 1-6 of 10 merged (tidy self-hosting, `codec/` fixed·varint·CRC32C·xxhash64, `file/` core and durability; PR #23), crash sink PR #24 open |
| [synod](https://github.com/yusa-imit/synod) | Foundation | Pure-state-machine Raft, joint consensus, SWIM, φ-accrual, HLC, deterministic simulator | v0.3.0 (2026-09-30, PR #31) — plan 002 complete (`types.zig`, in-memory `log.zig`, `store.zig` LogStore); plan 003 (phase 2 pure Raft core) proposed (PR #33) |
| [zuda](https://github.com/yusa-imit/zuda) | Library | ~60 containers, 24 algorithm families, 209 distributions, NDArray/linalg/stats/FFT/optimize, ML (461k LOC) | v2.3.0 (+115 unreleased commits; ILU double-free PR #58 and GMRES breakdown PR #59 merged 2026-10-02) |
| [sailor](https://github.com/yusa-imit/sailor) | Library | TUI framework, 140 widgets, CLI toolkit (150k LOC) | v2.99.0 (Zig 0.16 migration merged to main, PR #40, unreleased; v3.0.0 pending — main CI green again since 2026-09-30) |
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
6. **Zig 0.16.0 everywhere.** Realms still on 0.15.2 migrate under plan `001` (`docs/ROADMAP.md`); consumers wait for zuda/sailor v3.0.0.

## Names

| Name | Why |
|---|---|
| sigil | 의미를 새긴 기호 — 바이트에 의미를 새기는 직렬화 |
| sirocco | 함대를 밀어주는 바람 — sailor의 배를 움직이는 네트워크 |
| strata | 지층 — silica(광물) 아래 켜켜이 쌓인 저장 계층 |
| synod | 회의 — 노드들이 모여 합의에 이르는 곳 |
| citadel | 성채 — 왕국의 지휘소 |
