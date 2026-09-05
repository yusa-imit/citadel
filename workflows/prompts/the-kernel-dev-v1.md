The Kernel 자율 개발 사이클을 1회 수행하라.

1. **동기화**: `git pull --rebase origin main`. 충돌·미커밋 잔여물이 있으면 먼저 수습하라 (직전 실행의 미완성 흔적이면 완성하거나 되돌리고, 판단 불가면 STATUS.md Blocked에 기록 후 종료).
2. **현황 파악**: CLAUDE.md → STATUS.md → docs/status/BACKLOG.md 순으로 읽어라. Now에 미완 항목이 있으면 그것을 잇고, 없으면 Next 최상단 항목 하나를 Now로 옮겨 착수한다 (동시 3개 이하 유지).
3. **작업 크기 조절**: 이번 실행(최대 60분) 안에 테스트까지 완결 가능한 단위로 잘라라. 크면 BACKLOG에서 하위 태스크로 분해하고 첫 조각만 수행한다.
4. **구현**: CLAUDE.md 규약 전부 준수 — 제1법칙(코드는 같은 작업 단위 안의 테스트와 함께), 아키텍처 불변 조건(domain 순수성, 시맨틱 이벤트 원칙, 렌더링 문자열 금지, 룰셋 파라미터화), 프로덕션 unwrap/expect 금지. 서브에이전트를 쓸 경우 개발은 sonnet, 감사는 opus(1회 200k 컨텍스트 규율).
5. **게이트**: `cargo fmt --all` → `cargo clippy --workspace --all-targets -- -D warnings` → `cargo test --workspace` 전부 통과를 확인하라. 실패 상태로는 절대 커밋하지 않는다.
6. **기록**: STATUS.md(Now/Next/Recently Done/진행률)와 BACKLOG 체크 상태를 실상과 일치시켜라. PRD·infra.md에 없는 결정은 DECISIONS.md에 번호를 붙여 기록. Recently Done이 10개를 넘으면 /status-sync 수행.
7. **커밋·푸시**: `<크레이트|영역>: <변경 요약>` 형식, AI 흔적 문구 금지. `git push origin main`.
8. **감사**: 수직 슬라이스(기능 단위)가 이번 실행으로 완성됐다고 판단되면 /audit 스킬로 감사를 수행하고, P0 발견 시 다음 실행 최우선으로 STATUS.md Now에 등재하라.
9. **차단 시**: 무리한 우회 금지. STATUS.md Blocked에 원인·시도 내용·다음 시도 방향을 남기고 종료하라. 미완성 코드는 커밋하지 마라.
