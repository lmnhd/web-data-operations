# WS-001 Codex Vertical-Proof Brief

## Controlling decision

- **Iteration:** WS-001
- **Concept:** Qualified Tender Change Intelligence
- **Status:** APPROVED for the bounded vertical proof below
- **Human direction:** Proceed rather than launch another automated candidate or adversarial-gate round
- **Date:** 2026-09-03

This document supersedes earlier candidate recommendations for execution purposes without deleting their research history. Prior rejections remain evidence of what was tested; they are not mandatory feature checklists for this revised project.

## Buyer problem

A small contractor or bid-development team should not have to inspect every republished procurement notice to determine whether a relevant opportunity materially changed. The useful output is an explainable queue containing only qualified opportunities with material changes, plus explicit rejected and review-needed records.

## Vertical-proof claim

A bounded, provenance-preserving pipeline can:

1. ingest permitted structured notice snapshots through an allowlisted schema;
2. compare consecutive releases over a pre-declared field set;
3. distinguish material field changes from unchanged republications;
4. apply deterministic opportunity-qualification rules;
5. emit accepted, rejected, and review-needed records with reason codes and source provenance.

The proof does not claim complete amendment recall, real-time monitoring, production scale, or business impact.

## Authorized scope

- Use a small recorded fixture set and, only when compliant and necessary, a bounded one-shot acquisition from the documented public source.
- Never probe for a rate ceiling. Use a fixed conservative delay, strict request/page cap, and stop on `429` or another refusal.
- Persist only an allowlist of organization- and procurement-level fields. Drop `contactPoint` and free-text description/change prose before storage.
- Diff consecutive full snapshots for these initial material fields:
  - tender status;
  - tender deadline;
  - value amount and currency;
  - primary classification code;
  - lot identifiers/status when present.
- Treat source update tags as descriptive metadata only, never as the ground-truth denominator.
- Apply a configuration-driven qualification profile using available structured fields such as classification prefix, value range, deadline window, buyer type, or place of performance. Missing required evidence routes to review rather than a guessed decision.
- Produce JSON and CSV review queues plus a concise run report.
- Include fixture-based tests for unchanged republication, material change, qualification rejection, missing evidence, provenance, and personal-field exclusion.

## Explicit non-goals

- Scheduled or production monitoring
- Authentication, CAPTCHA, or access-control bypass
- Adaptive rate discovery, proxy rotation, or retrying through a refusal
- Named-person/contact enrichment
- PDF or solicitation-document reconciliation
- Cross-source buyer entity resolution
- Deployment, alert delivery, or CRM integration
- Claims of complete source coverage, real-time latency, or measured business savings

PDF/document reconciliation is intentionally reserved for a later project so it can provide distinct portfolio evidence instead of inflating WS-001.

## Proof gate

The vertical proof passes when a reproducible recorded run demonstrates:

- at least one unchanged update-tagged republication correctly excluded from material changes;
- at least one known material field change correctly surfaced;
- deterministic qualification decisions with reason codes;
- rejected and review-needed paths;
- source URL, retrieval timestamp, content fingerprint, release ID, and process ID on retained records;
- no persisted contact or excluded free-text fields;
- passing automated tests and deterministic outputs.

After the proof, stop at `AWAITING_BUILD_APPROVAL`. Expansion is a human decision, not an automatic workflow continuation.

## Recorded proof result - 2026-09-03

**PASS for the bounded fixture-based vertical proof.** The reproducible run used 8 synthetic releases representing 4 procurement processes. Four update-tagged comparisons produced 3 diff-derived material changes: 1 accepted, 1 rejected by qualification, 1 routed to review for missing classification, and 1 unchanged republication rejected as noise. All 6 automated tests passed. No delegated agent turns were used.

The result does not authorize or imply live monitoring, production readiness, measured customer impact, or public release. The workflow now stops at `AWAITING_BUILD_APPROVAL` as required.

## Repairable conditions accepted

- The original tag-count denominator was invalid; the revised proof uses direct field diffs.
- A numeric rate ceiling is unpublished; the proof never probes for it and may run entirely from recorded fixtures.
- Structured qualification is added because it strengthens the buyer outcome, not because the rejected-candidate register is a binding feature checklist.
- Current demand evidence remains indirect and must be strengthened before the final Upwork case study is marketed.

## Manifest positioning

The eventual Manifest should explain that adversarial discovery uncovered a meaningful source-semantic defect before implementation. The portfolio story is not that the system found every source-tagged update. It is that the pipeline measured the difference between republication signals and actual material changes, then converted qualified changes into a trustworthy operator decision queue.
