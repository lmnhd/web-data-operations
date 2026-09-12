# WS-003 Codex vertical-proof brief

> **2026-09-12 proof amendment:** The 15-row input is an explicitly synthetic SLA scenario, not a recorded Toronto extract. The official 2026 public ZIP does not provide target or closure timestamps. The proof validates adapter-ready calculation behavior only; it does not validate official municipal rules or performance. `SOURCE_CONTRACT.md`, `FIXTURE_PROVENANCE.md`, and the amended `VALIDATION_PLAN.json` control the release interpretation.

## Controlling decision

- **Iteration:** WS-003
- **Concept:** Municipal SLA & Service Bottleneck Operations Explorer
- **Public working name:** Municipal 311 SLA Operations Desk
- **Status:** APPROVED for the bounded vertical proof below
- **Human approval:** "Approved, you may proceed."
- **Date:** 2026-09-08

This approval covers the smallest fixture-based vertical proof only. It does not authorize expansion, paid services, production operational use, municipal dispatch integration, or public publication.

## Buyer problem and decision

Municipal operations managers, public works team leads, and service contractors receive raw 311 municipal service request data from open data portals. They need an actionable operational queue that highlights requests breaching or at risk of breaching SLA response targets, tracks timestamp drift across request lifecycles, and identifies ward-level bottlenecks so resources can be reallocated before compliance failures escalate.

## Central claim

An operational SLA engine can process structured 311 municipal service records, calculate SLA breach intervals across request lifecycles, and reproduce an independently labeled benchmark queue of compliant, at-risk, and breached requests using explicit field timestamps.

The claim fails if the proof depends on fabricated timestamps, hidden manual overrides, unsafe default compliance assumptions for incomplete records, or labels derived from the engine's own unverified output.

## Authorized scope

- Create project directory `projects/WS-003-municipal-sla-operations-explorer/`.
- Record a explicit source contract in `SOURCE_CONTRACT.md` covering the Toronto 311 Service Requests dataset under Open Government Licence – Toronto.
- Collect/record a bounded, representative source fixture of 15–30 311 service request records covering multiple service categories (e.g., Pothole Repair, Streetlight Maintenance, Tree Trimming, Garbage Collection) across multiple wards.
- Normalize timestamp fields (`created_date`, `target_date`, `closed_date`) and map operational lifecycle states (`OPEN`, `IN_PROGRESS`, `CLOSED_ON_TIME`, `CLOSED_OVERDUE`, `SLA_BREACHED`).
- Define explicit service category SLA rules (e.g., Pothole = 5 calendar days, Streetlight = 3 calendar days, Tree = 10 calendar days).
- Compute exact response duration, SLA margin (days remaining/overdue), and ward-level compliance rates.
- Emit structured JSON and CSV review queues plus a machine-readable run report with record fingerprints and retrieval timestamps.
- Build automated tests covering SLA calculations, lifecycle mapping, threshold adjustments, incomplete timestamp edge cases, and exports.

## Source boundary

- Dataset: City of Toronto 311 Service Requests under Open Government Licence – Toronto.
- Personal data: Excluded by source portal. No resident names, private phone numbers, or personal emails are collected or processed.
- Network access: Use recorded local fixture by default; if fetching live sample from CKAN API, enforce conservative 1 req/sec throttling and cache locally.
- Disclaimer: SLA metrics are for operational tracking demonstrations only and do not constitute legal or regulatory compliance certifications.

## Evidence design

This brief incorporates the [reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md) and [independent validation protocol](../../docs/shipping-pipeline/INDEPENDENT_VALIDATION.md).

### Reviewer-operated scenario

The reviewer adjusts an SLA target response threshold for a service category (e.g., reducing Pothole Repair target from 5 days to 3 days) and re-executes the engine. The operations queue and ward compliance percentages must visibly update with explicit audit reasons.

### Required edge case

Records with missing, invalid, or incomplete completion/target timestamps must be safely routed to an `INCOMPLETE_DATA_REVIEW` queue with explicit reason codes, rather than defaulting to false compliance.

### Proof gate

The vertical proof passes when a reproducible run demonstrates:

- 100% of independently declared fixture labels reproduced exactly;
- at least one record in `COMPLIANT`, `AT_RISK`, `SLA_BREACHED`, and `INCOMPLETE_DATA_REVIEW` states;
- field-level reason codes and audit margins for every record;
- ward-level bottleneck aggregation with compliance percentages;
- reviewer-operated rule adjustment visibly altering queue classifications;
- deterministic JSON/CSV exports and run report;
- passing automated tests;
- frozen `evidence/VALIDATION_PLAN.json`.

After a passing proof, stop at `AWAITING_BUILD_APPROVAL`. Expansion to full interactive UI, larger benchmark, visual PDF, and public hosting requires a separate human approval step.
