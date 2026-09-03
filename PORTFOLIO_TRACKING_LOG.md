# Portfolio Tracking Log

## Purpose

This file is the durable coordination record for the Web Scraping and Data Operations portfolio and its multi-agent Shipping Pipeline. Every participating agent must read it before beginning an iteration or accepting a major task, and must update the relevant entry at handoff.

Do not erase rejected concepts or superseded decisions. Their history prevents repeated work and explains why the portfolio changed direction.

## Agent preflight record

Before starting work, add or update the active iteration entry with:

- agent or role name;
- UTC start time;
- iteration ID and claimed task;
- files expected to change;
- dependencies or blockers found;
- confirmation that prior and active concepts were reviewed;
- intended new portfolio capability.

If two agents claim overlapping outputs, the later claim pauses until the orchestrator resolves ownership.

## Portfolio catalog

| Iteration | Concept | Target buyer | Distinct proof | Status | Evidence/release | Notes |
|---|---|---|---|---|---|---|
| WS-000 | Multi-agent Shipping Pipeline foundation | Teams evaluating agentic development and repeatable delivery | Tracking, role handoffs, gates, measured iteration history | BUILDING | This README and tracking log | Foundation only; not yet a released portfolio case study |
| WS-001 | First web-data operation | TBD after candidate and demand review | Must add the first end-to-end collection and verification evidence | RESEARCHING | `PHASE_01_DISCOVERY_AND_EVIDENCE_PLAN.md` | Candidate selection remains evidence-gated |

## Active work claims

| Iteration | Role/agent | Claimed task | Expected outputs | Started UTC | Status/blocker |
|---|---|---|---|---|---|
| WS-001 | Portfolio orchestrator | Coordinate Phase 1 candidate selection and approval gate | Candidate scorecard, source feasibility comparison, recommendation | TBD | Current Upwork demand evidence still needs to be supplied or collected |

## Candidate and duplication register

| Concept | State | Similarity/duplication risk | What would make it distinct | Decision/evidence needed |
|---|---|---|---|---|
| Public opportunity intelligence | UNDER_REVIEW | May overlap with Local Contract Scouter if framed only as lead discovery | Solicitation documents, amendments, provenance, deadline change tracking, structured qualification | Current demand evidence and lawful source feasibility |
| Business-location monitoring | UNDER_REVIEW | Could become a generic directory scraper | Cross-source entity resolution, operating-detail changes, conflict review, scheduled monitoring | Current demand evidence and permitted source mix |
| Product and price intelligence | UNDER_REVIEW | Highly common portfolio category | Variant resolution, availability history, change alerts, resilient incremental collection | Current demand evidence and a differentiated buyer decision |

## Rejected or archived concepts

| Concept | State | Reason | May be reconsidered when |
|---|---|---|---|
| None recorded | - | - | - |

## Shared Shipping Pipeline capability ledger

Use `PLANNED`, `IN_PROGRESS`, `VERIFIED`, or `SUPERSEDED`. A capability is `VERIFIED` only when a recorded test or run supports it.

| Capability | State | Introduced by | Verification evidence | Reused by |
|---|---|---|---|---|
| Global iteration tracking and collision prevention | IN_PROGRESS | WS-000 | Pending first completed multi-agent handoff | TBD |
| Relevance and uniqueness gate | IN_PROGRESS | WS-000 | Pending first approved concept | TBD |
| Source/compliance ledger | PLANNED | WS-001 | TBD | TBD |
| Immutable raw capture and provenance | PLANNED | WS-001 | TBD | TBD |
| Normalization and validation stages | PLANNED | WS-001 | TBD | TBD |
| Reason-coded review outputs | PLANNED | WS-001 | TBD | TBD |
| Checkpoint, retry, and resume behavior | PLANNED | WS-001 | TBD | TBD |
| Reproducible exports and run report | PLANNED | WS-001 | TBD | TBD |
| Benchmark and claim verification | PLANNED | WS-001 | TBD | TBD |
| Reviewer-facing Project Manifest | PLANNED | WS-001 | Completed Manifest reconciled with approval and verification records | TBD |
| Common GitHub archive and release history | IN_PROGRESS | WS-000 | Public remote verified; protected integration flow, passing checks, and first tagged release remain pending | TBD |

## Iteration decision and handoff log

Append entries in chronological order. Use UTC timestamps and preserve earlier entries.

### 2026-09-02 - WS-000 workflow foundation

- **Decision:** Convert the portfolio process into a reusable multi-agent Shipping Pipeline.
- **Reason:** The portfolio should demonstrate continuous delivery and agentic coordination while producing multiple relevant web-data case studies.
- **Guardrail:** Agents must check this log and pass relevance and uniqueness gates before beginning a new iteration.
- **Current outcome:** Workflow contract and initial tracking structures created; no delivery-efficiency claim is verified yet.
- **Source-control decision:** Use the dedicated `lmnhd/web-data-operations` public monorepo as the implementation archive; keep `halimede-web` as the presentation layer.
- **Repository event:** Public remote `https://github.com/lmnhd/web-data-operations` created and verified on 2026-09-02. Initial archive checks are included; branch protection and the first project release remain pending.
- **Next decision:** Complete the WS-001 demand and candidate evaluation before approving the first vertical build.

## Per-iteration entry template

Copy this section for each new iteration.

```markdown
## <ITERATION-ID> - <Concept name>

- Status:
- Target buyer:
- Operational decision enabled:
- Demand evidence:
- Portfolio gap addressed:
- Novelty versus completed and active projects:
- Net-new technical capability:
- Shared capabilities reused:
- Approved scope:
- Explicit non-goals:
- Assigned roles and work claims:
- Dependencies and blockers:
- Verification evidence:
- Project Manifest:
- Reviewed commit and pull request:
- Release tag:
- Release artifacts:
- Measured Shipping Pipeline results:
- Handoff summary:
- Retrospective and next-iteration guidance:
```
