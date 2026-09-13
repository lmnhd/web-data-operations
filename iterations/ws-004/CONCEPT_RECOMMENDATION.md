# WS-004 Concept Recommendation

## Decision boundary

- **Stage:** AWAITING_APPROVAL
- **Authorized work:** portfolio/source review and concept planning only
- **Recommendation:** Candidate A, Corporate Carbon Disclosure Reconciliation Desk
- **Build authorization:** none
- **Publication authorization:** none; prior approvals do not transfer
- **Delegation:** 0 of 4 turns used; one fresh-context non-builder validator and one repair recheck are reserved before any research/build agent

This brief follows the bounded Shipping Pipeline, [Reviewer Evidence Standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md), and [Independent Validation Protocol](../../docs/shipping-pipeline/INDEPENDENT_VALIDATION.md). It carries those files into the active state's `requiredFiles`. The separate validator must independently PASS the frozen candidate and the executable hash gate before release readiness; builder self-review cannot substitute.

## Demand and evidence quality

No client posting was supplied with this request. The demand signal is therefore **PUBLIC-PRELIMINARY**, not client-validated. The recorded matrix contains indirect evidence for deterministic PDF/data extraction, structured normalization, provenance, review states, interactive filtering, and CSV/Excel delivery. It does not establish demand for this exact carbon-disclosure service.

The portfolio and decision record were checked before selection:

- WS-001's procurement-monitoring concepts were repeatedly rejected or left unapproved because of duplication, source-use, and provability failures.
- WS-002 already proves cross-schema product matching with ambiguity handling.
- WS-003 already proves lifecycle rules, scenario aggregation, and an adapter-ready operations dashboard.
- WS-003 previously retained the carbon-disclosure direction as a fallback only. WS-004 may reuse its three-page presentation structure and provenance components, but none of WS-003's data, results, metrics, claims, or approval.

## Three commercially relevant concepts

| Candidate | Buyer decision | Distinct capability | Source path and feasibility | Main weakness / duplication risk |
|---|---|---|---|---|
| **A. Corporate Carbon Disclosure Reconciliation Desk** | ESG assurance or accounting reviewer decides which disclosed energy/emissions calculations are reproducible and which require evidence follow-up | Document extraction plus unit normalization, factor-year selection, numerical reconciliation, page/cell provenance, and evidence-sufficiency routing | Companies House filing history + Document API; 2026 UK government conversion-factor flat file and methodology | Filing layouts vary; Document API needs a key; exact reuse terms and presence of usable SECR content are binding pre-proof conditions |
| **B. Open Data Contract Sentinel** | Data engineering team decides whether an upstream dataset change is backward-compatible or will break a scheduled delivery | Metadata snapshots, schema/type diffs, compatibility classification, and fixture replay | NYC Open Data dataset metadata and SODA responses | Historical schema changes may not be available, so the proof may depend on controlled mutations rather than a recorded production break; some overlap with WS-001 monitoring |
| **C. Contract Award Concentration Review Desk** | Public-sector vendor or procurement analyst decides whether award exposure is concentrated by agency/vendor/category | Deterministic vendor-name normalization, concentration metrics, and drill-down reconciliation | NYC Open Data Recent Contract Awards, current official SODA/CSV export | Procurement repeats WS-001's vertical, vendor normalization approaches WS-002's matching mechanic, and the current-state dataset does not prove renewal forecasting |

These candidates demonstrate different mechanics: document/numeric reconciliation, data-contract change classification, and concentration analysis. Candidate A is the strongest portfolio addition because it changes the buyer, source class, proof method, and reviewer decision without reusing a released project's result.

## Recommendation: A. Corporate Carbon Disclosure Reconciliation Desk

### Buyer problem and operational decision

Corporate energy and emissions figures may appear in narrative filings with differing units, reporting periods, factor vintages, and calculation detail. A reviewer needs to decide whether each figure is directly reproducible from explicit evidence, internally contradictory, or impossible to verify without more detail.

The tool will not grade environmental performance. It will answer a narrower question: **does the disclosed calculation have enough explicit evidence to reproduce, and does the arithmetic agree within a declared tolerance?**

### Central testable claim

For a declared six-case benchmark built from a small permitted set of public filing facts and the official factor vintage cited by those filings, the proof can preserve source/table provenance, normalize supported units, produce **2 RECONCILED, 1 MISMATCH, and 3 REVIEW_REQUIRED** outcomes, and fail closed when units, activity breakdown, factor year, or supported document text are missing. Source verification selected the 2025 Version 1 / Final flat file rather than the newer 2026 file so the calculation basis matches the disclosures.

Those are planned oracle outcomes, not observed performance. They become publishable only if the built proof and independent validator reproduce them.

### Preliminary official-source findings

- Companies House documents public filing history through its read-only Public Data API and provides a Document API for metadata and content. Both require an API key.
- Official Document API metadata can advertise PDF, JSON, XML, XHTML, ZIP, or CSV content; availability varies per document.
- Companies House documents a limit of 600 requests per five minutes per application. The proof will use a much smaller recorded sample and no rate probing.
- The UK Department for Energy Security and Net Zero published a 2026 full set, automation-oriented flat file, methodology, and major-changes report. The flat file was corrected on 31 July 2026, so every factor input must carry its file hash and update date.
- Exact filing-document reuse/licensing and the availability of sufficiently structured SECR content remain **unverified**. No document acquisition or implementation may begin until those gates are recorded in a source contract.

Primary references:

- [Companies House Public Data API](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference)
- [Companies House Document API](https://developer-specs.company-information.service.gov.uk/document-api/reference)
- [Companies House rate limits](https://developer-specs.company-information.service.gov.uk/guides/rateLimiting)
- [UK government 2025 conversion factors](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2025)

### Smallest vertical proof after approval

1. Freeze a source contract before acquisition: exact permitted use, access method, rate ceiling, attribution, retained-artifact rules, excluded personal fields, and fallback.
2. Select three bounded filings with supported text-bearing PDF or XHTML and explicit company-level SECR metrics; record URL, company number, filing transaction, content type, retrieval time, and SHA-256.
3. Build a separate six-case oracle covering valid calculation, tolerance, mismatch, missing unit, insufficient activity breakdown, and unsupported image-only content.
4. Extract only the declared energy/emissions values, units, reporting period, factor references, and page locations. Do not retain or display names, signatures, contacts, or unrelated filing text.
5. Normalize supported units and recompute only when activity, unit, factor category, and factor year are explicit. Otherwise return `REVIEW_REQUIRED` with a reason code.
6. Provide reviewer-editable value/unit/factor inputs, visible before/after decisions, and JSON/CSV exports.

### Reviewer-operated scenario

The reviewer changes one declared activity unit from `MWh` to `kWh` while preserving the numeric value. The normalized activity and recomputed emissions must change by exactly 1,000x, the source input hash must change, and the decision must move to `MISMATCH` unless the disclosed result changes consistently.

Meaningful safe failure: a filing supplies only a total emissions number without activity breakdown or factor reference. The proof must return `REVIEW_REQUIRED: INSUFFICIENT_CALCULATION_EVIDENCE`, not infer an activity mix or declare compliance.

## Validation plan defined before implementation

The exact seven-category draft is in [PREBUILD_VALIDATION_PLAN.json](PREBUILD_VALIDATION_PLAN.json). After concept approval and before any code or fixture implementation, it must be copied to the project as `evidence/VALIDATION_PLAN.json`, updated with the final builder identity and exact artifact paths, reviewed, and committed. Scope changes require a recorded rationale before work continues.

Release readiness will require:

- one consolidated builder review and at most one repair pass;
- a stable candidate commit;
- a fresh-context non-builder validator that did not implement code or evidence;
- an independent PASS report covering tests, demo, edge case, exports, every PDF page, claims, and boundaries;
- the executable SHA-256 validation gate; and
- separate human approvals for expansion and publication.

## Required final evidence if expansion is later approved

- **Runnable demonstration:** real reconciliation logic, editable scenario, visible provenance/reason codes, safe failure, local instructions, and approved signed-out hosting or an explicitly approved runnable alternative.
- **Plain-English visual PDF:** three standalone client-facing pages: buyer/result screenshot; genuine extraction/reconciliation obstacle with implemented correction; reproducible results, limitations, and try-it path.
- **Problem-solving evidence and Manifest:** sanitized inputs, declared oracle, actual output, tests, run logs, source/factor hashes, implementation roles, limitations, and artifact-linked release checklist.

## Consolidated review

**Recommendation: PROCEED TO HUMAN CONCEPT APPROVAL ONLY.** Candidate A is meaningfully different and has an executable proof design. It is not cleared for implementation yet. The binding pre-proof conditions are filing reuse terms, three usable source documents, and a frozen project-local validation plan. No client-specific demand evidence exists, and no regulatory, audit, environmental-performance, production-accuracy, or savings claim is permitted.

## Approval request

Approve Candidate A and the four-turn delegated-agent ceiling if you want me to perform the bounded source-contract check and vertical proof. Expansion, hosting, and publication will each stop for separate approval.
