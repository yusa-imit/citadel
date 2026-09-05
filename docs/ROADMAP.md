# Kingdom Roadmap — foundation extraction & integration

각 foundation 레포의 내부 마일스톤은 해당 레포의 `docs/milestones.md`가 관리한다.
이 문서는 **레포 경계를 넘는** 작업만 다룬다.

## Phase 0 — Housekeeping (즉시)

- [ ] zr의 zuda 의존을 git ref 2.0.4 → 태그 v2.3.0으로 통일
- [ ] zoltraak `storage/{bloom,cuckoo,cms,topk,tdigest,heavykeeper}.zig` → zuda 사용으로 교체; topk/tdigest/heavykeeper는 zuda `containers/probabilistic/`로 상향
- [ ] 4개 foundation 레포 GitHub CI 첫 실행 녹색 확인
- [ ] cron 잡 4개 등록 (`zr jobs-apply`)

## Phase 1 — Foundation v0.1 (각 레포 Phase 1–2 완료 시점)

목표: 소비자가 실험적으로 붙여볼 수 있는 최소 API.

| Repo | v0.1 scope | First consumer PoC |
|---|---|---|
| sigil | core + reflect + JSON | zoltraak `JSON.GET` 경로에서 `sigil.path.jsonpath` |
| sirocco | Loop(kqueue/epoll) + net.tcp + timer | zr `toolchain/downloader.zig` HTTP client (Phase 4 이후) |
| strata | codec + file + page + cache + WAL | synod `LogStore` 어댑터 |
| synod | types + log + raft election/replication + sim | zoltraak `sentinel.zig` 선출 로직 대체 |

## Phase 2 — First migrations

- [ ] **zr → sigil**: TOML/YAML 파서 교체. zr 전체 테스트를 sigil 백엔드로 통과 (`zr/src/config/`)
- [ ] **zoltraak → sigil**: `json_value.zig`, `jsonpath.zig` 제거
- [ ] **synod ↔ strata**: `adapters/strata_logstore.zig`; 크래시 주입 + 시뮬레이션 동시 실행
- [ ] **synod ↔ sirocco**: `adapters/sirocco_transport.zig`; 3노드 실네트워크 통합 테스트 CI

## Phase 3 — Service migrations

- [ ] **zoltraak → strata**: AOF를 strata WAL로, RDB를 strata snapshot으로
- [ ] **zoltraak → synod**: cluster/sentinel/replication을 synod Raft + SWIM으로
- [ ] **zoltraak → sirocco**: `server.zig`, `network/tls.zig`를 sirocco로
- [ ] **silica → strata**: `src/storage/{page,buffer_pool,wal}` → strata (silica는 B+Tree 위 SQL/MVCC만 유지, 또는 strata btree 채택)
- [ ] **silica → synod**: replication failover/promotion을 synod 선출로
- [ ] **silica → sirocco**: `src/server/{server,connection}.zig`, TLS → sirocco
- [ ] **sailor → sirocco**: `tui/widgets/{httpclient,websocket}.zig` 위임

## Phase 4 — Next components (after foundation stabilizes)

후보 (순서 미정): 관측성(구조화 로깅·메트릭·트레이싱), 인증/암호 유틸(SCRAM/JWT/ACL 모델), 플러그인 VM(WASM), 클라이언트 SDK(silica/zoltraak 드라이버), 메시지 스트림(Kafka 포지션), S3 호환 오브젝트 스토리지, 웹 프레임워크.

## Version policy

- foundation: `0.x` 동안 마이너마다 API 변경 가능. 소비자 PoC가 두 개 이상 붙으면 `1.0` 검토
- 소비자 레포는 foundation을 **태그로만** 의존 (git ref 금지)
