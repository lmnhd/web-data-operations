# WS-003 Concept Recommendation

> **2026-09-12 source-contract correction:** The original recommendation assumed the public dataset could support lifecycle target/closure timing. The verified 2026 Toronto ZIP contains creation date, current status, ward, request type, division, section, and coarse location fields, but no target or closure timestamps. The approved release is therefore an adapter-ready engine demonstrated with explicitly synthetic SLA records. It makes no official Toronto performance claim. This correction supersedes source/fixture claims below while preserving the original selection history.

## Decision boundary

- **Stage:** AWAITING_APPROVAL
- **Authorized work so far:** planning and source/demand verification only
- **Build authorization:** none
- **Publication authorization:** none; WS-001 and WS-002 approvals do not transfer
- **Delegation used:** 0 of 4 available turns

This recommendation follows the bounded Shipping Pipeline (`.agents/skills/web-data-shipping/SKILL.md`), `START_NEXT_ITERATION.md`, and the [reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md). The selected concept must end with its own runnable demonstration, project-specific visual PDF, reproducible evidence, Manifest, and artifact-linked release checklist. Those requirements are planned now, but do not authorize implementation or publication.

---

## Evidence quality

No client posting was supplied with this iteration request. Market demand evidence is derived from public freelance marketplace postings (PeoplePerHour, Freelancer.com), market reports (Apify, Proxyway, PromptCloud), and industry practitioner commentary recorded in `research/UPWORK_DEMAND_MATRIX.md`.

The strongest current signals relevant to WS-003 are:

- [Develop an agent/tool that checks websites daily, compares results run-over-run, flags new listings/changes, and surfaces changes via an operator dashboard](https://www.peopleperhour.com/freelance-data-scraping-jobs) - daily monitoring, run-over-run comparison/diffing, operator dashboard with filtering.
- [Power BI Dashboard from CSV Data](https://www.upwork.com/freelance-jobs/apply/Power-Dashboard-Specialist-Build-Clean-Interactive-Reports-from-CSV-Data_~022094968596444905810/) - data modeling, operational filtering, actionable exception queues.
- [E-commerce / Operations Data Cleanup and Standardization](https://www.upwork.com/freelance-jobs/apply/Product-Data-Cleanup-Standardization-CRM-Entry-200-SKUs_~022091051177676672807/) - status normalization, missing data/SLA rules, issues queue routing.
- Upwork's [web-scraper hiring guide](https://www.upwork.com/hire/web-scrapers/) highlights operational dashboards, status tracking, clean exports, and maintainable data pipelines as core buyer needs.

These signals support the capabilities below. They do not prove demand for the exact public datasets or public-demo framing.

---

## Three bounded concepts

| Candidate | Target Buyer and Operational Decision | Permitted Source Path | Net-new Proof versus WS-001 & WS-002 | Main Weakness |
|---|---|---|---|---|
| **A. Municipal SLA & Service Bottleneck Operations Explorer** | Municipal operations managers or public works contractors deciding which service categories/wards exceed SLA response limits and require staff reallocation | City of Toronto 311 Service Requests API (CKAN Action API under Open Government Licence – Toronto) | Spatial-temporal SLA breach detection, multi-status lifecycle tracking (open $\rightarrow$ in-progress $\rightarrow$ closed timestamp drift), and ward-level bottleneck aggregation | Public 311 dashboards exist in simple forms; buyer value lies in operational SLA analytics rather than raw data viewing |
| **B. Corporate Energy & Carbon Disclosure Audit Desk** | ESG compliance auditors or supply-chain sustainability teams verifying whether corporate carbon/energy disclosures match official conversion standards and benchmark ratios | UK Companies House API (Streamlined Energy and Carbon Reporting under OGL v3.0) & UK DEFRA conversion factors | Multi-source numerical unit-conversion reconciliation ($kWh \rightarrow tCO_2e$), conversion factor verification, and ratio audit logging | SECR filings vary in format across companies; PDF/iXBRL text extraction complexity may expand proof scope |
| **C. Financial Advisor License Drift & Sanction Monitor** | Financial firm compliance officers or vendor risk managers verifying that third-party advisors/firms retain active regulatory authorization without restriction flags | UK Financial Conduct Authority (FCA) Financial Services Register API (public API under OGL / FCA terms) | Multi-tier regulatory authorization state machine (firm-individual permissions, disciplinary flags, status transitions) | Requires a free FCA developer API key; regulatory registry updates occur on fixed schedules rather than real-time streams |

---

## Recommendation: A. Municipal SLA & Service Bottleneck Operations Explorer

### Target buyer and problem

Municipal operations leads and public works contractors manage thousands of service requests across city wards. Standard open-data downloads provide raw rows, but operators lack an actionable operational queue that highlights service categories breaching SLA response targets, tracks timestamp drift across request lifecycles, and flags emerging bottleneck wards before compliance failures escalate.

### Operational decision

Decide which service request categories and wards require immediate resource re-allocation or supervisor escalation based on explicit SLA target breaches and timestamp lifecycle drift. The tool does not perform emergency dispatch or replace internal 311 ticketing systems.

### Central testable claim

An operational SLA engine can ingest structured 311 municipal service records, calculate precise SLA breach intervals across request lifecycles, and reproduce an independently labeled benchmark queue of compliant, at-risk, and breached requests using explicit field timestamps.

### Source and compliance boundary

The [City of Toronto Open Data 311 Service Requests API](https://open.toronto.ca/dataset/311-service-requests-customer-service-feedback/) exposes structured municipal service records under the [Open Government Licence – Toronto](https://open.toronto.ca/open-data-licence/) (verified in `design/SOURCE_AND_COMPLIANCE_LEDGER.md` as cleared source #2). The licence permits worldwide commercial reuse with attribution.

- **Access Path:** Official CKAN Action API (`datastore_search` endpoint) and direct CSV/JSON resource downloads.
- **Privacy & Compliance:** Personal information is excluded by the source. Request records contain service category, status, ward, creation date, target response date, and completion date. No individual resident names or private addresses are collected or displayed.
- **Throttling:** Self-imposed conservative rate limiting (1 request/second) to ensure zero impact on municipal data infrastructure.

### Difference from released WS-001 and WS-002

- **WS-001 (Qualified Tender Change Intelligence):** Monitored UK procurement notices for OCDS release updates and evaluated bid qualification rules over categorical fields.
- **WS-002 (Product Recall Match Desk):** Matched e-commerce SKUs against openFDA enforcement records using cross-schema fuzzy matching and explainable ambiguity boundaries.
- **WS-003 (Municipal SLA Operations Explorer):** Implements spatial-temporal SLA breach analytics, lifecycle state transition tracking, ward-level bottleneck aggregation, and dynamic rule-threshold filtering. It introduces a new target buyer, operational problem, data domain, and analytical engine.

### Smallest vertical proof

1. Ingest a bounded, representative set of 311 service request records (100–200 rows across 3–5 service types and wards).
2. Normalize status timestamps (`created_date`, `target_date`, `closed_date`) and map operational states into a unified lifecycle (`OPEN`, `IN_PROGRESS`, `CLOSED_ON_TIME`, `CLOSED_OVERDUE`, `SLA_BREACHED`).
3. Compute exact response duration, SLA threshold margin, and ward-level SLA compliance percentages.
4. Emit an actionable operations queue categorized by compliance state, with explicit reason codes, source retrieval timestamps, and record fingerprints.
5. Benchmark output against a hand-labeled ground-truth fixture containing known compliant, at-risk, and breached service records.
6. Export the operational queue and summary metrics as CSV and JSON.

### Reviewer-operated scenario and edge case

- **Scenario:** The reviewer modifies the SLA threshold rule (e.g. adjusts target response window from 5 days to 3 days) and re-executes the engine. The operations queue immediately updates request statuses and ward compliance percentages with explicit audit trails.
- **Edge Case:** Records with missing `closed_date` or incomplete timestamp fields are safely routed to an `INCOMPLETE_DATA_REVIEW` queue rather than defaulting to false SLA compliance.

### Final evidence plan

- **Runnable Demo:** Interactive Web UI / Proof Lab allowing reviewers to adjust SLA thresholds, filter by ward/category, inspect record provenance, and export queues.
- **PDF Page 1:** Buyer problem, operational result, and screenshot of the working SLA queue.
- **PDF Page 2:** Creative problem-solving - handling timestamp drift and missing lifecycle markers across heterogeneous service types, with annotated code excerpt.
- **PDF Page 3:** Measured benchmark results against labeled ground truth, test summary, limitations, and try-it-yourself path with working demo link.
- **Traceability:** Sanitized input fixtures, labeled benchmark oracle, output artifacts, test records, Manifest, and `evidence/RELEASE_CHECKLIST.md`.

---

## Consolidated review

```json
{
  "decision": "proceed",
  "fatal": [],
  "repairable": [
    "Verify the active status of 311 API resources on open.toronto.ca before freezing the proof fixture.",
    "Ensure timestamp parsing explicitly handles timezone offsets and missing completion dates without silent failures.",
    "Formally record the independent validation plan in evidence/VALIDATION_PLAN.json prior to build."
  ],
  "limitations": [
    "No client posting was supplied; demand evidence is based on general operational dashboard and monitoring signals.",
    "The proof uses a bounded Toronto 311 dataset and does not establish live real-time integration with internal municipal ticketing systems.",
    "The SLA calculations serve operational review purposes and do not constitute legal or regulatory compliance certifications."
  ],
  "required_vertical_proof": [
    "Independent labeled SLA compliance benchmark fixture",
    "Explainable rule-change result (adjusted SLA threshold window)",
    "Safely routed incomplete timestamp edge cases",
    "Provenance tracking and structured CSV/JSON exports",
    "Zero personal data or private resident detail collection"
  ],
  "claims_to_avoid": [
    "real-time municipal dispatch integration",
    "legal SLA certification",
    "complete exhaustive multi-year city coverage",
    "automated municipal policy enforcement"
  ]
}
```

## Approval request

Awaiting human review and decision before proceeding to vertical proof implementation:
1. **Approval of Candidate A (Municipal SLA Operations Explorer)** for WS-003.
2. **Approval of bounded agent budget** (4 stage turns max).
3. **Approval to draft proof brief upon concept sign-off.**
