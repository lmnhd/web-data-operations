# WS-004 Project Manifest

## Identity and status

- **Iteration:** WS-004
- **Project:** Corporate Carbon Disclosure Reconciliation Desk
- **Status:** EXPANSION APPROVED - build not yet started
- **Release:** None
- **Reviewed commit / PR / tag:** Not applicable; no candidate exists
- **Primary reviewer:** ESG assurance, sustainability reporting, or accounting reviewer

## Selection declaration

No client posting was supplied. Public-preliminary market evidence supports deterministic document extraction, normalization, provenance, review states, and structured exports, but does not prove demand for this exact service. Three concepts were compared; this one was approved because document-plus-numeric reconciliation is more distinct from WS-001 procurement monitoring, WS-002 entity matching, and WS-003 lifecycle/aggregation.

## Buyer decision and proposed proof

The tool decides whether disclosed arithmetic is reproducible from explicit evidence, conflicts with it, or needs review. It parses a minimized six-case fixture, normalizes supported units, resolves only exact versioned factors, and emits reason-coded JSON/CSV. The executed run matches the declared oracle: 2 RECONCILED, 1 MISMATCH, and 3 REVIEW_REQUIRED.

## Sources and boundaries

The source strategy used one official Companies House Free Accounts Data Product archive plus the official 2025 UK government conversion-factor flat file matching the filings' declared factor vintage. The [source contract](SOURCE_CONTRACT.md) prohibits committing or redistributing full filings and excludes company names, personal names, signatures, contacts, addresses, and unrelated content. Results cannot certify compliance, audit assurance, truthfulness, environmental performance, production accuracy, or savings.

## Roles and approvals

| Role | Responsibility | Current result |
|---|---|---|
| Human approver | Candidate and four-turn ceiling | Approved bounded proof on 2026-09-12 |
| Human approver | Expansion UI, evidence package, PDF, and independent validation | Approved on 2026-09-13; hosting/publication excluded |
| Root builder/orchestrator | Source contract, plan freeze, proof implementation and same-agent checks | Proof implemented; 13 tests and consolidated review pass after one formatting-only repair |
| Fresh non-builder validator | Execute frozen plan after a stable expanded candidate, if expansion is approved | Reserved, not dispatched |
| Repair recheck | One recheck after at most one repair pass | Reserved, not used |

## Evidence and release status

- Project-local frozen validation plan: recorded at `evidence/VALIDATION_PLAN.json` before implementation
- Selected-source and factor records: frozen; archive, workbook, and full filings remain uncommitted
- Runnable proof: `src/reconcile.py` with default and changed-input JSON/CSV evidence
- Test results: 13 passed, 0 failed on 2026-09-13; same-agent result only
- Consolidated builder review: PASS; one formatting-only repair removed two trailing-space lines; no product or execution evidence changed
- Visual PDF: not authorized or built
- Independent validation: not dispatched
- Manifest/release checklist: this Manifest is provisional; release checklist pending expansion
- Hosting/publication: not authorized

## Next gate

Build the approved reviewer UI, project-specific three-page visual PDF, tests, evidence, Manifest, and release checklist without hosting. Then freeze a stable candidate and dispatch the reserved non-builder validator. Publication approval remains a later human gate.
