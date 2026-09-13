# WS-004 release checklist

**Candidate status:** VERIFYING - initial independent FAIL preserved; repaired candidate recheck pending

**Date:** 2026-09-13

| Requirement | Status | Evidence / actual result |
|---|---|---|
| Runnable demonstration | PASS | `app.py`, `src/demo_server.py`, `demo/`, and local launch instructions execute the real Python engine. |
| Default run | PASS | `evidence/evaluated_run.json` and `.csv`: six cases, exactly 2 RECONCILED / 1 MISMATCH / 3 REVIEW_REQUIRED. |
| Changed input | PASS | UI and `changed_input_run.*`: 1,000 MWh -> 1,000 kWh changes computed emissions 177.000 -> 0.177 tCO2e and RECONCILED -> MISMATCH. |
| Meaningful edge cases | PASS - BUILDER | Ambiguous gas basis, unsupported image-only evidence, insufficient aggregate breakdown, unknown factor references, and incompatible activity/factor categories fail closed; malformed supplied source digests are rejected. |
| JSON/CSV exports | PASS - BUILDER | Web adapter and CLI exports carry the same `runId` in JSON and every CSV row and agree on decisions, reason codes, values, locators, and hashes. |
| Automated tests | PASS - BUILDER | Exact command passed 27/27 on 2026-09-13 after the bounded repair; independent recheck pending. |
| Actual screenshots | PASS | `evidence/reviewer/working-demo.png` and `changed-input-demo.png`, with capture assertions in `SCREENSHOT_PROVENANCE.md`. |
| Three-page visual PDF | PASS - BUILDER | `output/pdf/Carbon-Disclosure-Reconciliation-Desk.pdf`: exactly three Letter pages rendered at 150 DPI and builder-inspected with no clipping or overlap. Independent visual inspection pending. |
| Creative problem solving | PASS - BUILDER | PDF page 2 documents the observed 2026-to-2025 factor-vintage correction and shows the implemented fail-closed code path. |
| Claim traceability | PASS - BUILDER | PDF counts and before/after values match the frozen oracle and recorded runs; controlled scenarios and limitations are explicit. |
| Source/privacy boundary | PASS - BUILDER | Full archive, workbook, and filings are uncommitted; no company names, personal fields, arbitrary URLs, credentials, or live writes are exposed. |
| Manifest | PASS - BUILDER | `PROJECT_MANIFEST.md` records buyer need, implementation, source correction, roles, evidence, and limitations. |
| Frozen validation plan | PASS | Committed before implementation in `cab1c89`; all seven required categories are present. |
| Independent non-builder validation | BLOCKED | `/root/ws004_independent_validator` independently failed candidate `d95db72`; the hash-complete report and logs are preserved. The repaired candidate still requires the one reserved recheck. |
| Executable hash gate | BLOCKED | The gate correctly cannot accept the preserved FAIL; run it again only after a fresh PASS report covers the repaired candidate. |
| Signed-out public demo | BLOCKED | Hosting is not authorized. The local workbench is runnable; public deployment awaits publication approval. |
| Publication authorization and destinations | BLOCKED | No WS-004 hosting, GitHub release, or Upwork publication is authorized. Prior approvals do not transfer. |

No item marked PASS should be read as independent release validation unless it explicitly says so. Before `RELEASE_READY`, replace the independent-validation and hash-gate blockers with exact report/gate results. Before `RELEASED`, verify any approved public links signed out and record the immutable source release and actual publication destinations.
