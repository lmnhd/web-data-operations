# WS-002 Codex vertical-proof brief

## Controlling decision

- **Iteration:** WS-002
- **Concept:** Recall-to-Catalog Impact Review
- **Public working name:** Product Recall Match Desk
- **Status:** APPROVED for the bounded vertical proof below
- **Human approval:** "Approved."
- **Date:** 2026-09-03

This approval covers the smallest fixture-based proof only. It does not authorize expansion, hosting, publication, paid services, production use, public alerts, medical decisions or recall-lifecycle tracking.

## Buyer problem and decision

Small e-commerce, wholesale or distribution catalog teams may need to compare regulator recall descriptions with their own product rows when identifiers, manufacturer names, product text and lot/code information are incomplete or inconsistent. The proof helps an operator decide which catalog rows warrant manual verification against the official source record.

## Central claim

A provenance-preserving matcher can compare a bounded synthetic catalog with selected openFDA enforcement records and reproduce an independently labeled `match`, `no_match` and `review_needed` queue using explicit field evidence.

The claim fails if the fixture can be passed only by hidden manual repair, unsafe thresholds, invented values or labels derived from the matcher's own output.

## Authorized scope

- Use a small synthetic catalog and a bounded recorded openFDA enforcement fixture.
- Make at most one conservative source-data request needed to capture the proof fixture; do not probe limits or retry through a refusal.
- Persist only declared recall fields needed for matching, source provenance and the official record URL.
- Normalize without inventing absent identifiers or expanding abbreviations into unsupported facts.
- Apply a deterministic evidence ladder and route ambiguous evidence to `review_needed`.
- Emit JSON and CSV queues plus a machine-readable run report.
- Include tests for exact evidence, normalized text evidence, clear non-match, ambiguity, provenance, determinism and excluded-field handling.

## Source boundary

- openFDA is not used for medical-care decisions.
- The proof does not issue public alerts or claim to track a recall lifecycle.
- Published recall `status` is not treated as a current lifecycle state.
- GMDN content is excluded.
- The source contract and selected field list must be recorded before implementation claims are made.

## Evidence design

This brief incorporates the [reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md).

### Reviewer-operated scenario

The reviewer edits one synthetic catalog identifier or manufacturer spelling and reruns the matcher. The resulting classification and reasons must visibly change, while source provenance remains intact.

### Required edge case

A catalog row and recall record with plausible descriptive overlap but no reliable identifier or sufficiently strong combined evidence must route to `review_needed`, not a confident match.

### Proof gate

The vertical proof passes when a reproducible run demonstrates:

- all independent fixture labels reproduced exactly;
- at least one `match`, `no_match` and `review_needed` decision;
- field-level reasons and deterministic scores/classifications;
- source URL, retrieval timestamp and content fingerprint on retained recall records;
- changed-input behavior and the ambiguity boundary;
- deterministic JSON/CSV exports and run report;
- passing automated tests.

After a passing proof, stop at `AWAITING_BUILD_APPROVAL`. Expansion is a separate human decision.

## Recorded proof result - 2026-09-03 US Eastern

**PASS for the bounded fixture proof.** One permitted openFDA request supplied 12 records; ten selected, allowlisted records were retained. Against eight independently declared catalog labels, the baseline run reproduced 8 of 8: six matches, one no-match and one review-needed ambiguity. Eight automated tests passed.

The observed ambiguity was genuine: harmonized UPC/NDC identifiers spanned multiple strengths or package variants. A 100 mcg catalog row sharing a UPC with recorded 75 mcg and 150 mcg variants routed to review with both candidates and fingerprints. In the reviewer-operated changed-input scenario, adding the matching 75 mcg strength, NDC family and lot changed that row to a single explainable match while again reproducing 8 of 8 labels.

One repair pass added per-candidate fingerprints and corrected review-evidence ordering. Same-agent verification only; no independent audit, expansion or publication claim is made. Full evidence is in `projects/WS-002-recall-to-catalog-impact-review/evidence/PROOF_REPORT.md`.

## Final-project obligations reserved for expansion

If expansion is later approved, the project must receive its own runnable reviewer demo, project-specific three-page visual PDF, sanitized evidence, Manifest and artifact-linked `evidence/RELEASE_CHECKLIST.md`. WS-001 presentation components may be reused structurally, but none of its results or claims may be copied.
