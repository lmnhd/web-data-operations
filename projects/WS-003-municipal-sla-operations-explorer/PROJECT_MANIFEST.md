# Project Manifest: Municipal 311 SLA Operations Desk (WS-003)

## 1. Project identity

- **Iteration ID:** WS-003
- **Project name:** Municipal SLA and Service Bottleneck Operations Explorer
- **Public name:** Municipal 311 SLA Operations Desk
- **Version/release:** v1.0.0 release package
- **Status:** Approved release candidate; independent PASS and immutable tag required
- **Release date:** 2026-09-12
- **Repository/demo:** https://github.com/lmnhd/web-data-operations / https://municipal-311-sla-operations-desk.vercel.app
- **Reviewed commit:** Bound by the final independent artifact hash map; the GitHub release records the exact integrated commit
- **Pull request:** Recorded in the GitHub release and portfolio tracking log
- **Release tag:** `ws-003-v1.0.0`
- **Primary reviewer audience:** Operations and data teams evaluating an adapter-ready SLA review workflow

## 2. Executive declaration

Municipal service teams may receive public request summaries while keeping target and completion timestamps inside operational systems. Toronto's current public 311 export illustrates that gap: it exposes creation date, status, ward, request type, division, and section, but not target or closure timestamps.

WS-003 demonstrates the decision workflow without inventing municipal facts. A real Python engine processes 15 explicitly synthetic, 311-style records; applies configurable hypothetical targets; isolates malformed timestamps; aggregates scenario ward results; and exports labeled JSON/CSV evidence. Production use would require an authorized adapter to internal fields.

## 3. Why this project was chosen

### Demand evidence

- Public marketplace signals in `research/UPWORK_DEMAND_MATRIX.md` show recurring demand for operational dashboards, status cleanup, and CSV/JSON delivery.
- Evidence was gathered in August-September 2026.
- No client posting was supplied. Demand confidence is `PUBLIC-PRELIMINARY`, not proof of demand for this exact product.

### Portfolio gap

WS-001 demonstrates procurement change intelligence and WS-002 demonstrates cross-schema product matching. WS-003 adds configurable temporal rules, explicit failure routing, aggregate operational views, and an interactive browser workbench.

### Candidate decision

Three concepts were compared in `iterations/ws-003/CONCEPT_RECOMMENDATION.md`. The user approved the municipal scenario on 2026-09-08 and authorized finishing its release before WS-004 on 2026-09-12.

## 4. Alternatives considered

| Alternative | Potential value | Why deferred | Reconsider when |
|---|---|---|---|
| Corporate Energy Disclosure Audit Desk | Unit-conversion and filing reconciliation | Higher document-extraction scope | A sustainability request supplies demand evidence |
| Financial Advisor Licence Monitor | Regulatory status state machine | Requires FCA developer access and stronger compliance demand | A financial-compliance request is supplied |
| Treat public Toronto rows as SLA facts | Stronger apparent realism | Rejected because target and closure timestamps are absent | An authorized source provides those fields |

## 5. The buyer problem

- **Target user:** Operations managers and data teams reviewing time-bound service work.
- **Current workflow:** Join request summaries with internal targets and completion events, then identify exceptions manually.
- **Risk:** Missing or malformed timestamps can create false compliance or breach claims.
- **Decision enabled:** Which enriched records need review under a chosen rule set.
- **Useful outcome:** A reproducible queue with reasons, scenario aggregates, and exports.
- **Incorrect-data consequence:** A record must enter review; the system must not silently classify it.

## 6. Solution overview

```text
Authorized adapter-ready records
  -> timestamp normalization
  -> configurable hypothetical target rules
  -> lifecycle and margin calculation
  -> COMPLIANT / AT_RISK / SLA_BREACHED / INCOMPLETE_DATA_REVIEW
  -> synthetic ward scenario aggregation
  -> JSON/CSV with fixture label, reason code, and fingerprint
```

The bundled browser workbench runs the real engine, exposes rule changes, shows the failure state, and supports exports. Its source boundary is documented in `SOURCE_CONTRACT.md` and `evidence/FIXTURE_PROVENANCE.md`.

## 7. Development Manifest

| Role/agent | Bounded responsibility | Recorded outputs | Handoff/approval |
|---|---|---|---|
| Root builder/orchestrator | Engine integration, demo, evidence correction, PDF, release assembly | Project files and tracking entries | Human approvals on 2026-09-08 and 2026-09-12 |
| `/root/ws003_remediation_validator` | Fresh-context execution of the final frozen plan; no implementation | Validation logs and `INDEPENDENT_VALIDATION.json` | PASS required before release |
| Human owner | Concept, expansion, publication, and closeout authority | Approval record and existing Upwork publication | Consequential gates remain human-controlled |

### Iteration history

| Date | Planned outcome | Material result | Evidence |
|---|---|---|---|
| 2026-09-08 | Select and prove a municipal operations concept | Synthetic engine, workbench, tests, PDF, and Upwork publication prepared | Iteration brief and proof report |
| 2026-09-09 | Check public presentation | Upwork publication verified; PDF overlap and demo 404 recorded | Tracking history |
| 2026-09-12 | Finish before WS-004 | Source contract corrected, PDF repaired, candidate revalidated | This Manifest and validation evidence |

Shared Shipping Pipeline gates and WS-001 presentation structure were reused. The SLA engine, synthetic fixture, scenario workbench, and source-gap correction are project-specific. The major pivot was relabeling the fixture after the official 2026 source audit found no target or closure timestamps.

## 8. Technical trust and operating boundaries

- The demo is fixture-only and makes no live source request.
- Every result row is labeled `synthetic_sla_scenario`.
- Fingerprints cover input-record content; reason codes explain each classification.
- Invalid creation timestamps route to `INCOMPLETE_DATA_REVIEW`.
- No retry/checkpoint layer is claimed because the release has no live collector.
- No resident names, contact details, postal codes, intersections, or private addresses are included.
- Duplicate resolution, official SLA definitions, production scaling, and internal-system authorization are outside scope.

## 9. Proof and measured results

### Benchmark method

- Dataset: 15-row synthetic fixture at reference time `2026-08-08T12:00:00Z`.
- Oracle: predeclared expected classifications in `tests/fixtures/benchmark_oracle.json`.
- Reproduction: run the exact commands in `README.md`.
- Environment: Python 3 and Flask 3.1.2; no network required.

| Metric | Measured result | Evidence | Interpretation/limit |
|---|---:|---|---|
| Synthetic oracle agreement | 15/15 | `evidence/evaluated_run.json` | Deterministic fixture agreement, not production accuracy |
| Status counts | 8 / 1 / 5 / 1 | `evidence/evaluated_run.json` | Compliant / at-risk / breached / review in the scenario |
| Scenario ward rate | 40.0% | `evidence/evaluated_run.json` | Fictional Ward 01 scenario, not a City metric |
| Automated tests | 17/17 builder precheck | Independent validation test log pending | Engine and Flask adapter scope only |

The changed-rule scenario reclassifies synthetic `SR-311-001`; malformed timestamps, reversed chronology, future creation or closure dates, unknown statuses, status/closure contradictions, and unmapped categories route safely to review. Fractional, unknown, and falsey non-object rule overrides are rejected, and the HTTPS deployment rejects same-host HTTP origins. `evidence/VALIDATION_PLAN.json` freezes the seven required validation categories. `evidence/INDEPENDENT_VALIDATION.json` is valid only when its fresh non-builder verdict is PASS and the executable hash gate passes.

## 10. Limitations and non-goals

- Synthetic sample only; no production accuracy, completeness, scale, freshness, or impact claim.
- No official Toronto request IDs, target dates, closure dates, SLA definitions, or performance measures.
- No live municipal integration, dispatch, staffing action, legal certification, or emergency use.
- Public hosting is a reviewer convenience, not an operational service guarantee.
- A production adapter requires separate authorization, field mapping, privacy review, monitoring, and operational testing.

## 11. Reviewer walkthrough

1. Open the workbench and read the synthetic-data boundary.
2. Run the default 15-record scenario.
3. Apply the strict-rule preset and observe the changed queue.
4. Inspect the malformed timestamp review record.
5. Download JSON/CSV and confirm `fixture_kind`, reason codes, and fingerprints.
6. Review the source contract, three-page PDF, and independent validation report.

## 12. Contribution to the next iteration

WS-003 adds a reusable pattern for separating licensed public context from an authorized internal adapter contract. The key lesson is to verify source columns before naming performance metrics. WS-004 should add a materially different buyer outcome and must define its validation plan before implementation.

## 13. Declaration integrity checklist

- [x] Reviewer evidence standard and independent-validation protocol linked and enforced.
- [x] Demand gaps and synthetic inputs disclosed.
- [x] Agent roles and human approvals match the tracking record.
- [x] Metrics trace to recorded outputs and are not described as production accuracy.
- [x] Limitations, privacy boundaries, and source gaps are visible.
- [x] Project is materially distinct from WS-001 and WS-002.
- [ ] Final independent PASS, signed-out link check, reviewed integration, and immutable tag - required before release.

## 14. Release approval

- **Manifest prepared by:** Root orchestrator/builder
- **Evidence verified by:** `/root/ws003_remediation_validator` after the final candidate freeze
- **Release approved by:** Human owner; original publication approval 2026-09-08, closeout approval 2026-09-12
- **Tracking-log entry:** `PORTFOLIO_TRACKING_LOG.md`, WS-003 closeout section
