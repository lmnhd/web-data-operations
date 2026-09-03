# Codex Shipping Pipeline Migration

## Decision

The Claude workflow scripts under `.claude/workflows/` are paused as historical evidence. They produced valuable source and metric findings, but their multi-agent refutation architecture is too expensive and rejection-oriented for routine portfolio delivery.

The active implementation is the repository skill at `.agents/skills/web-data-shipping/` plus the deterministic `ACTIVE_ITERATION.json` state contract.

## Cost controls

- Compact active state replaces full-history injection into every task.
- Agents read only files listed for the current stage.
- Discovery permits two parallel researchers and one consolidated critic.
- No automatic runner-up promotion.
- Findings are severity-classified instead of counted as rejection votes.
- One repair pass is allowed before human review.
- Mechanical checks and state transitions run in deterministic scripts.
- A vertical proof precedes extensive design, documentation, and release work.
- Each stage has a delegated-turn budget; exceeding it requires human approval.

## Gate correction

Novelty is evaluated against released portfolio projects. Rejected candidates remain research evidence but do not occupy portfolio territory. Candidate-register suggestions are not mandatory requirements unless a human explicitly promotes them into the approved brief.

Only prohibited access, no usable source, no buyer outcome, an untestable central claim, or material duplication of a released project automatically blocks a vertical proof. Other findings become repair conditions or disclosed limitations.

## WS-001 migration outcome

WS-001 is reframed as Qualified Tender Change Intelligence. The bounded proof tests material field diffs plus deterministic opportunity qualification and provenance. It excludes production monitoring and PDF reconciliation. The latter remains available as a distinct future project.
