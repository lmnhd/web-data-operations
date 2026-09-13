# WS-004 Project Manifest

## Identity and status

- **Iteration:** WS-004
- **Project:** Corporate Carbon Disclosure Reconciliation Desk
- **Status:** BUILDING - expanded local candidate; independent validation pending
- **Release:** None
- **Reviewed commit / PR / tag:** Not applicable; no candidate exists
- **Primary reviewer:** ESG assurance, sustainability reporting, or accounting reviewer

## Selection declaration

No client posting was supplied. Public-preliminary market evidence supports deterministic document extraction, normalization, provenance, review states, and structured exports, but does not prove demand for this exact service. Three concepts were compared; this one was approved because document-plus-numeric reconciliation is more distinct from WS-001 procurement monitoring, WS-002 entity matching, and WS-003 lifecycle/aggregation.

## Buyer decision and implemented workflow

The tool decides whether disclosed arithmetic is reproducible from explicit evidence, conflicts with it, or needs review. The Python engine parses a minimized six-case fixture, normalizes supported units, resolves only exact versioned factors, and emits reason-coded JSON/CSV. A Flask adapter and responsive reviewer UI expose the real engine, the unit-change exercise, reason codes, source locators, hashes, and downloads. The executed run matches the declared oracle: 2 RECONCILED, 1 MISMATCH, and 3 REVIEW_REQUIRED.

## Sources and boundaries

The source strategy used one official Companies House Free Accounts Data Product archive plus the official 2025 UK government conversion-factor flat file matching the filings' declared factor vintage. The [source contract](SOURCE_CONTRACT.md) prohibits committing or redistributing full filings and excludes company names, personal names, signatures, contacts, addresses, and unrelated content. Results cannot certify compliance, audit assurance, truthfulness, environmental performance, production accuracy, or savings.

## Roles and approvals

| Role | Responsibility | Current result |
|---|---|---|
| Human approver | Candidate and four-turn ceiling | Approved bounded proof on 2026-09-12 |
| Human approver | Expansion UI, evidence package, PDF, and independent validation | Approved on 2026-09-13; hosting/publication excluded |
| Root builder/orchestrator | Source contract, plan freeze, engine, UI, tests, screenshots, PDF, evidence, and same-agent checks | Expanded candidate built; 23 tests pass; visual inspection complete |
| `/root/ws004_independent_validator` | Fresh non-builder execution of the frozen seven-category plan after candidate freeze | Reserved target identity; not yet dispatched |
| Repair recheck | One recheck after at most one repair pass | Reserved, not used |

## Evidence and release status

- Project-local frozen validation plan: recorded at `evidence/VALIDATION_PLAN.json` before implementation
- Selected-source and factor records: frozen; archive, workbook, and full filings remain uncommitted
- Runnable proof: `app.py` / `src/demo_server.py` / `demo/` plus the CLI engine and default/changed-input JSON/CSV evidence
- Test results: 23 passed, 0 failed on 2026-09-13; same-agent result only
- Browser evidence: actual default and changed-input screenshots captured at 1440 x 900 with asserted page state
- Consolidated builder review: the iteration's one review passed at the bounded-proof gate; the expanded candidate receives deterministic builder verification and separate independent validation, not a second consolidated review
- Visual PDF: three-page Letter case study built from actual project evidence and rendered at 150 DPI with no builder-observed clipping or overlap
- Independent validation: not dispatched
- Manifest/release checklist: assembled; validator and publication items remain BLOCKED
- Hosting/publication: deployment-ready configuration exists, but no deployment or publication is authorized

## Creative decision and implementation boundary

Preliminary feasibility selected the newer 2026 factor workbook. The filings themselves cite 2025 factors, so the source contract and frozen plan were corrected before implementation to the official 2025 Version 1 / Final workbook. The engine also refuses to select gross or net natural-gas factors when the filing does not state the calorific basis, even when one row happens to reproduce the disclosed number.

The web adapter accepts only a known case ID and the `kWh`/`MWh` exercise for controlled Case 02. It caps JSON requests at 4 KB, rejects unknown fields and types, enforces same-origin POSTs, exposes no arbitrary file/URL access, performs no writes, and serves only minimized evidence.

## Next gate

Finish deterministic checks, freeze a stable candidate, and dispatch the reserved non-builder validator with no inherited conversation. Same-agent evidence cannot satisfy release readiness. Publication approval remains a later human gate.
