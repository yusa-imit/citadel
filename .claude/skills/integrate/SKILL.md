---
name: integrate
description: Plan a cross-repo integration (consumer adopts a foundation library) as ROADMAP items and a consumer plan; execution happens in the consumer's own cycles.
argument-hint: <consumer> <foundation>
---

Call `kingdom-architect` (opus) with the pair. Required: what code in the consumer is replaced,
the foundation API it maps onto, parity tests, rollback. If the foundation API does not exist
yet, add the requirement to the foundation's next plan instead. Update
`citadel/docs/ROADMAP.md`; the consumer's next `/plan` picks it up. Never edit two repos in
one PR.
