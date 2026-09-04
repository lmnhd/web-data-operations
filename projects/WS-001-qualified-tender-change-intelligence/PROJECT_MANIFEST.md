# Project Manifest

## Project identity

- **Iteration:** WS-001
- **Public project name:** Government Contract Change Monitor
- **Internal engineering name:** Qualified Tender Change Intelligence
- **Status:** Public Vercel demo deployed and verified; Upwork PDF upload in progress
- **Public demo:** https://contract-monitor-proof-lab.vercel.app
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

The approved expansion added two bounded sanitized live records. In the first, 6 update-tagged comparisons contained zero declared material changes. In the second, a cancellation surfaced 5 declared changes and was routed to review because the new release lacked qualification evidence. The live result validates both noise suppression and the missing-evidence boundary without claiming source-wide prevalence, production coverage, or business impact.

A three-page reviewer work sample now presents the client problem, deliverables, simple operating flow, live proof, trust boundaries, and technical handoff. It deliberately excludes the separate continuous-development workflow. Release approval and default-branch integration remain pending.

## What the proof demonstrates

### Interactive expansion - 2026-09-03 US Eastern

The user rejected a presentation-only claim of proof and approved a local executable demonstration. One implementing agent reused the existing pipeline, added a loopback Python server and browser workbench, and verified real interactions without additional research agents. Every Run invokes the existing Python function; no canned run reports power the UI. Reviewers can change qualification rules, inspect all declared fields, download a run and execute tests themselves.

Seventeen current automated tests passed. Browser checks reproduced both historical cases and showed the synthetic 400,000 GBP opportunity switching from Act to Ignore when the maximum changed from 5,000,000 to 300,000. The screenshot walkthrough records those executions. The revised three-page PDF uses those screenshots and an actual code excerpt, and explains how to reproduce the behavior.

This is implementation-agent verification, not an independent audit. The earlier six- and seven-test counts above refer to earlier phases. No public hosting, main merge or release has been approved by these checks. See `demo/README.md` and `evidence/proof-lab/BROWSER_VERIFICATION.md` for the exact current boundaries.

- Source update tags are retained as metadata but do not determine whether a change occurred.
- Qualification is evaluated separately from change detection.
- Missing decision evidence produces an explicit review queue instead of a guessed result.
- Persisted records include source URL, retrieval time, SHA-256 content fingerprint, release ID, and procurement process ID.
- Contact and free-text fields are excluded by the normalization allowlist.

## Known limitations

### Publication verification

Vercel production deployment `dpl_8xetoYvaEhM9kivL2XWrx3z9Pppy` serves the Flask adapter from the approved existing team. Anonymous HTTP checks returned 200, executed the real noise-case pipeline with six ignored comparisons and zero tracked changes, and passed all 14 hosted core checks. The complete local/CI suite has 22 tests. No paid add-ons were selected. Usage remains subject to the existing account's quotas and billing. The PDF now includes the public demo link. Prior local-only statements record earlier development phases, not current hosting status.

- Upwork-specific demand evidence is not yet a verified current sample.
- No scheduled live monitoring is included.
- No documents or PDFs are processed.
- No personal contact or free-text fields are persisted.
- No claim of complete amendment recall is made.
