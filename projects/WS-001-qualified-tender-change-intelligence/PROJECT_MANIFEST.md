# Project Manifest

## Project identity

- **Iteration:** WS-001
- **Project:** Qualified Tender Change Intelligence
- **Status:** AWAITING_BUILD_APPROVAL
- **Reviewer audience:** Upwork clients and technical interviewers evaluating web-data and workflow-automation ability

## Why this project was chosen

The discovery process found recurring demand for monitoring, cleaning, qualification, and decision-ready exports. It also found that an update label can describe republication without proving that a buyer-relevant field changed. This project was selected to demonstrate the more trustworthy operation: inspect declared fields directly, retain provenance, and qualify the resulting changes for an operator.

Earlier SAM.gov and cross-source concepts were rejected because of access, source-history, personal-data, or benchmark problems. The UK amendment-monitoring concept exposed a repairable metric defect rather than an unusable transformation problem. WS-001 keeps that useful core and removes unsupported production-monitoring and completeness claims.

## Problem and solution

A bid team can waste time reviewing republished notices that contain no relevant change. The pipeline normalizes an allowlisted subset of consecutive releases, computes material field differences, applies a contractor qualification profile, and routes each comparison to accepted, rejected, or review-needed output with reason codes.

## Development declaration

The original Claude workflow supplied source research and adversarial findings but consumed too many agent passes and treated repairable issues as automatic rejection. On 2026-09-03 the human directed the process to proceed. The Codex migration replaced full-history agent prompts with compact state, bounded delegation, deterministic validation, one repair pass, and a vertical-proof-first sequence.

## Current proof boundary

The bounded vertical proof passed on a deliberately small synthetic fixture. It processed 8 releases across 4 procurement processes and made 4 consecutive-release comparisons. All 4 current releases carried an update tag, but direct field comparison found only 3 material changes. The system routed 1 qualified change to `accepted`, 1 unqualified change and 1 unchanged republication to `rejected`, and 1 incomplete record to `review-needed`. Six automated tests passed.

These are fixture results, not claims about live-source prevalence, production coverage, or business impact. A bounded sanitized live capture, benchmark report, reviewer artifacts, and release approval remain future build decisions.

## What the proof demonstrates

- Source update tags are retained as metadata but do not determine whether a change occurred.
- Qualification is evaluated separately from change detection.
- Missing decision evidence produces an explicit review queue instead of a guessed result.
- Persisted records include source URL, retrieval time, SHA-256 content fingerprint, release ID, and procurement process ID.
- Contact and free-text fields are excluded by the normalization allowlist.

## Known limitations

- Upwork-specific demand evidence is not yet a verified current sample.
- No scheduled live monitoring is included.
- No documents or PDFs are processed.
- No personal contact or free-text fields are persisted.
- No claim of complete amendment recall is made.
