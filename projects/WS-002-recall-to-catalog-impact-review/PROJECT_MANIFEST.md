# Product Recall Match Desk - Project Manifest

## 1. Project identity

- **Iteration:** WS-002 - Recall-to-Catalog Impact Review
- **Release candidate:** v1.0.0 candidate
- **Status:** Public demo deployed; independent review and source integration in progress
- **Prepared:** 2026-09-03/04 UTC
- **Repository candidate:** [iteration/ws-002-discovery at 46deae7](https://github.com/lmnhd/web-data-operations/tree/46deae7e11e2423424cc02b6d557c5cacd6025db)
- **Public demo:** [product-recall-match-desk.vercel.app](https://product-recall-match-desk.vercel.app)
- **Local demo:** `python -B src/demo_server.py`, then open `http://127.0.0.1:8766`
- **Reviewed commit, pull request and tag:** Pending publication authorization and source integration
- **Primary reviewer:** E-commerce, wholesale or distribution catalog operations buyer

## 2. Executive declaration

Recall records and internal catalog rows often describe products with incomplete or conflicting identifiers. A shared UPC can look decisive while product strength, NDC or lot evidence says otherwise. Catalog staff need to decide what can be linked and what must be verified by a person.

Product Recall Match Desk executes a deterministic, provenance-preserving match over a synthetic catalog and a recorded, allowlisted openFDA fixture. It delivers explainable match, no-match and review-needed queues, exposes candidate evidence and fingerprints, and exports the executed result. It does not make a medical or safety determination.

## 3. Why this project was chosen

### Demand and portfolio evidence

The [concept recommendation](../../iterations/ws-002/CONCEPT_RECOMMENDATION.md) records dated Upwork signals for product matching, SKU cleanup, deterministic extraction, provenance and reviewer-ready reporting. No client interview or exact recall-workflow posting was supplied, so exact-product demand remains unproven.

WS-001 demonstrated version comparison and qualification in public procurement. WS-002 adds cross-schema entity resolution, conflicting-evidence handling and a catalog-side human-review workflow. It reuses provenance and export patterns without reusing WS-001 data or claims.

### Candidate decision

Recall-to-Catalog Impact Review was selected over a Tender Document Evidence Reconciler and 311 Service Operations Explorer. It won on portfolio distinction and its ability to prove an explainable ambiguous-match boundary with a bounded public source. The user approved the fixture proof and later approved expansion into this interface, benchmark, PDF, Manifest and evidence package. Hosting and publication were explicitly reserved.

## 4. Buyer problem and useful outcome

- **User:** Catalog operations analyst at a small e-commerce, wholesale or distribution organization.
- **Current workflow:** Manually compare regulator descriptions, firms, identifiers and lots with internal catalog fields.
- **Risk:** A false match can affect the wrong product; a false non-match can hide a row that needs investigation.
- **Decision enabled:** Link one candidate when evidence is decisive, dismiss unsupported candidates, or open a human verification task.
- **Useful outcome:** Every result has explicit reasons, source provenance and a reproducible input/engine hash.
- **Staleness boundary:** The fixture is a recorded selection, not a current-status feed.

## 5. Solution and processing sequence

```text
Recorded openFDA enforcement fixture + synthetic catalog
  -> allowlisted fields and source metadata
  -> normalized UPC, NDC, lot, manufacturer, product tokens and strengths
  -> deterministic pair evidence and score
  -> match / no_match / review_needed
  -> provenance, fingerprints, JSON and CSV
  -> catalog operator decision
```

The browser workbench edits only five fields on one fixture row and sends a bounded JSON request to the local Python server. The server reloads known fixtures, runs `catalog_matcher.match_catalog`, retains at most 32 in-memory exports, and exposes no arbitrary path or URL input.

## 6. Development Manifest

| Role | Bounded responsibility | Recorded output | Control |
|---|---|---|---|
| Human approver | Select concept; approve proof, expansion and publication | Approval in `ACTIVE_ITERATION.json` | Paid services and production use remain withheld |
| Codex root agent | Source contract, fixture, matcher, tests, UI, benchmark, PDF and evidence | This project and iteration records | Same-agent verification only |

No subagents were used. Consequential concept, expansion and publication decisions were not treated as autonomous.

| Date | Planned outcome | Material result | Evidence |
|---|---|---|---|
| 2026-09-03 | Select one distinct concept | WS-002 chosen from three candidates | [Concept recommendation](../../iterations/ws-002/CONCEPT_RECOMMENDATION.md) |
| 2026-09-03 | Prove the core matching claim | 8/8 fixture labels; changed input moved CAT-005 from review to match | [Proof report](evidence/PROOF_REPORT.md) |
| 2026-09-04 | Expand reviewer evidence | 20/20 labels, runnable interface, 21 tests and visual PDF | [Benchmark report](evidence/benchmark/run-report.json), [release checklist](evidence/RELEASE_CHECKLIST.md) |

The first expansion run reproduced 7/20 labels. One bounded repair pass changed shared matcher logic - short-name overlap, per-unit strength comparison, explicit review threshold and conflict handling - without editing the oracle or output rows. See [expansion repair record](evidence/EXPANSION_REPAIR.md).

## 7. Technical trust and boundaries

- **Source access:** One recorded openFDA drug enforcement request, captured 2026-09-04; no live request occurs in the demo.
- **Provenance:** Request URL, retrieval time and selected-record content fingerprints travel with decisions.
- **Collection policy:** Exact request, allowlist and excluded fields are in [SOURCE_CONTRACT.md](SOURCE_CONTRACT.md).
- **Conflicts:** Shared identifiers with conflicting strength evidence remain review-needed; missing values are not invented.
- **Failure behavior:** Invalid fields, oversized values, foreign origins, unknown exports and malformed requests fail closed.
- **Sensitive data:** Fixtures contain public enforcement fields and invented catalog rows, not private client data.
- **Unavailable source:** The recorded demo remains reproducible but makes no current-status claim.
- **Not supported:** Alerts, medical use, recall-lifecycle tracking, write-back, scheduling, authentication, production scale or private catalog integration.

## 8. Proof and measured results

### Benchmark method

- **Run:** `evidence/benchmark/run-report.json`, generated 2026-09-04T03:48:26Z.
- **Oracle:** `tests/fixtures/benchmark-labels.json`, declared separately from matcher output.
- **Inputs:** 20 synthetic catalog rows and 10 selected recorded enforcement records.
- **Command:** `python -B src/run_proof.py --catalog tests/fixtures/benchmark-catalog.json --recalls tests/fixtures/recalls.json --expected tests/fixtures/benchmark-labels.json --output-dir evidence/benchmark`

| Metric | Result | Interpretation |
|---|---:|---|
| Exact declared labels reproduced | 20/20 | Fixture result only; not production accuracy |
| Output queues | 13 match / 1 no match / 6 review-needed | Review remains an intended safe state |
| Automated tests | 21 passed | Same-agent local run on 2026-09-04; duration is environment-dependent |
| Browser scenarios | Ambiguous and clarified passed | Real Python execution changed CAT-005 and its input hash |
| Responsive check | 390 x 844, no horizontal overflow | One mobile breakpoint, not exhaustive device coverage |

Matcher SHA-256: `18f5455515c86c193d433975bcae82fa208c9cc91424d47972c197b5e77c9248`.

## 9. Limitations and claims not made

- The benchmark is small, selected and synthetic on the catalog side.
- Labels are independently declared but were not reviewed by an external domain specialist.
- The selected openFDA fixture cannot establish recall completeness, currency or lifecycle state.
- Matching reasons support catalog review; they do not determine medical risk, safety or legal obligations.
- No production accuracy, business impact, customer savings, scale or uptime claim is made.
- Browser, implementation and test verification were performed by the same agent and are not an independent audit.

## 10. Five-minute reviewer walkthrough

1. Launch the local workbench from [README.md](README.md).
2. Run the default CAT-005 row; inspect both 50-point candidates and `strength_conflict`.
3. Open source trail and fingerprints, then download JSON or CSV.
4. Click **Add decisive evidence** and rerun; confirm CAT-005 matches D-0709-2026 at 200 points and the input hash changes.
5. Click **Run automated checks**, then inspect the [benchmark](evidence/benchmark/run-report.json), [PDF](../../output/pdf/Product-Recall-Match-Desk.pdf) and [release checklist](evidence/RELEASE_CHECKLIST.md).

## 11. Declaration integrity and release approval

- [x] Selection claims match the recommendation and human approval record.
- [x] Demand claims link to dated evidence and state the evidence gap.
- [x] Architecture, metrics, screenshots and limitations match the candidate implementation.
- [x] Recorded source data is allowlisted; catalog inputs are synthetic.
- [x] Local demo, changed input, exports, tests and rendered PDF were checked.
- [ ] Independent verification or an explicit human-approved exception is recorded.
- [x] The public demo was approved, deployed and returned HTTP 200 in an anonymous check.
- [ ] Reviewed commit, pull request, default-branch integration and immutable tag are recorded.
- [ ] Final release authorization and actual publication are recorded.

**Prepared by:** Codex root agent

**Evidence verified by:** Codex root agent (same-agent; not independent)

**Release approved by:** User, 2026-09-04; actual publication remains pending completion of the recorded gates

**Tracking:** [PORTFOLIO_TRACKING_LOG.md](../../PORTFOLIO_TRACKING_LOG.md)
