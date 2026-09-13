# WS-004 Project Manifest

## Identity and status

- **Iteration:** WS-004
- **Project:** Corporate Carbon Disclosure Reconciliation Desk
- **Status:** APPROVED - pre-implementation source selection
- **Release:** None
- **Reviewed commit / PR / tag:** Not applicable; no candidate exists
- **Primary reviewer:** ESG assurance, sustainability reporting, or accounting reviewer

## Selection declaration

No client posting was supplied. Public-preliminary market evidence supports deterministic document extraction, normalization, provenance, review states, and structured exports, but does not prove demand for this exact service. Three concepts were compared; this one was approved because document-plus-numeric reconciliation is more distinct from WS-001 procurement monitoring, WS-002 entity matching, and WS-003 lifecycle/aggregation.

## Buyer decision and proposed proof

The proposed tool decides whether disclosed arithmetic is reproducible from explicit evidence, conflicts with it, or needs review. It will parse a minimized six-case fixture, normalize supported units, resolve only exact versioned factors, and emit reason-coded JSON/CSV. Planned oracle totals are 2 RECONCILED, 1 MISMATCH, and 3 REVIEW_REQUIRED; these are not observed results.

## Sources and boundaries

The source strategy is one official Companies House Free Accounts Data Product archive plus the official corrected 2026 UK government conversion-factor flat file. The [source contract](SOURCE_CONTRACT.md) prohibits committing or redistributing full filings and excludes personal names, signatures, contacts, addresses, and unrelated content. Results cannot certify compliance, audit assurance, truthfulness, environmental performance, production accuracy, or savings.

## Roles and approvals

| Role | Responsibility | Current result |
|---|---|---|
| Human approver | Candidate and four-turn ceiling | Approved bounded proof on 2026-09-12 |
| Root builder/orchestrator | Source contract, plan freeze, proof implementation and same-agent checks | Source contract drafted; implementation not started |
| Fresh non-builder validator | Execute frozen plan after a stable expanded candidate, if expansion is approved | Reserved, not dispatched |
| Repair recheck | One recheck after at most one repair pass | Reserved, not used |

## Evidence and release status

- Project-local frozen validation plan: pending source selection
- Runnable proof: not built
- Test results: none
- Visual PDF: not authorized or built
- Independent validation: not dispatched
- Manifest/release checklist: this Manifest is provisional; release checklist pending expansion
- Hosting/publication: not authorized

## Next gate

Confirm three usable permitted source documents and the exact factor file, freeze and commit `evidence/VALIDATION_PLAN.json`, then transition to PROVING. After the bounded proof passes same-agent checks, stop at `AWAITING_BUILD_APPROVAL` for human expansion approval.
