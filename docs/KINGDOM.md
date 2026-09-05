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
| [sigil](https://github.com/yusa-imit/sigil) | Foundation | Value IR + comptime reflection; JSON/TOML/YAML/MessagePack/CBOR/Protobuf/CSV; layered config | Bootstrap |
| [sirocco](https://github.com/yusa-imit/sirocco) | Foundation | Completion-based event loop (kqueue/epoll/io_uring/IOCP), sockets, DNS, pool, TLS, HTTP/1.1+2, WebSocket | Bootstrap |
| [strata](https://github.com/yusa-imit/strata) | Foundation | File I/O abstraction, pages + buffer pool, segmented WAL + recovery, B+Tree, LSM, KV engine, snapshots | Bootstrap |
| [synod](https://github.com/yusa-imit/synod) | Foundation | Pure-state-machine Raft, joint consensus, SWIM, φ-accrual, HLC, deterministic simulator | Bootstrap |
| [zuda](https://github.com/yusa-imit/zuda) | Library | 100+ data structures, 80+ algorithms, NDArray/linalg/stats/FFT/optimize | v2.3 stable |
| [sailor](https://github.com/yusa-imit/sailor) | Library | TUI framework, 40+ widgets, CLI toolkit | v2.99 stable |
| [zr](https://github.com/yusa-imit/zr) | Tooling | Task runner + toolchain manager + monorepo + MCP/LSP server | v1.114 |
| [silica](https://github.com/yusa-imit/silica) | Service | Embedded/server RDBMS, SQL:2016, MVCC, PG wire, replication | v1.0.1 |
| [zoltraak](https://github.com/yusa-imit/zoltraak) | Service | Redis-compatible in-memory store, RESP, cluster, Lua | active |

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

  synod -.-> sigil
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
3. **One version of each dependency across the kingdom.** `zr-repos.toml` `[deps]` is the reference; pin the same tag in every `build.zig.zon` (today zr pins zuda 2.0.4 while silica pins 2.3.0 — fix in ROADMAP Phase 0).
4. **Every repo has the same shape.** `CLAUDE.md` orchestrator, `docs/PRD.md`, `docs/milestones.md`, `.claude/{agents,commands,memory}`, `ci.yml`. Foundation repos are rendered from `citadel/templates/repo`; re-render with `scripts/scaffold.py <name> --force`.
5. **Every repo is driven the same way.** A cron job (see `workflows/jobs.toml`) runs `claude -p` with the repo's prompt from `workflows/prompts/<repo>.md`. citadel is the source of truth for those prompts.
6. **Zig 0.15.2 everywhere.** Bump kingdom-wide, foundation first.

## Names

| Name | Why |
|---|---|
| sigil | 의미를 새긴 기호 — 바이트에 의미를 새기는 직렬화 |
| sirocco | 함대를 밀어주는 바람 — sailor의 배를 움직이는 네트워크 |
| strata | 지층 — silica(광물) 아래 켜켜이 쌓인 저장 계층 |
| synod | 회의 — 노드들이 모여 합의에 이르는 곳 |
| citadel | 성채 — 왕국의 지휘소 |
