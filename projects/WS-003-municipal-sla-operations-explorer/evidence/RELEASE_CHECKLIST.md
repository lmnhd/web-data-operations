# WS-003 release checklist

Closeout resumed 2026-09-12 UTC. Statuses remain fail-closed until evidence is refreshed.

| Gate | Status | Evidence |
|---|---|---|
| Runnable Python web demo | PASS | `app.py`, `src/demo_server.py`, `demo/` |
| Synthetic input disclosed in UI and exports | PASS | `fixture_kind=synthetic_sla_scenario`; source and fixture contracts |
| Meaningful rule change | PASS | Hypothetical Pothole target 5d -> 3d reclassifies synthetic `SR-311-001` |
| Edge/safe state | PASS | Malformed creation timestamp routes to `INCOMPLETE_DATA_REVIEW` |
| JSON/CSV exports | PASS | Labeled rows with reason codes and fingerprints |
| Builder-side automated tests | PASS | `python -m unittest discover projects/WS-003-municipal-sla-operations-explorer/tests`: 17/17 on 2026-09-12, including lifecycle consistency, post-reference closure, cross-scheme Origin, and falsey non-object rule regressions |
| Official source contract | PASS | 2026 ZIP columns verified; missing target/closure timestamps disclosed |
| Visual three-page PDF | PASS | `/root/ws003_remediation_validator` freshly rendered all three pages at 150 DPI; page 2 code and full footer are visible without clipping or overlap |
| Actual working-output screenshot | PASS | `evidence/reviewer/working-demo.png` and `evidence/reviewer/working-demo-pdf.png`, captured from the corrected local demo on 2026-09-12 |
| Independent verification | PASS | `/root/ws003_remediation_validator` reports 7/7 PASS, zero unresolved findings, for candidate `57ac8a4` and deployment `dpl_JBt2EBRSHRN8PKDLTsnBWpYHtjCb` |
| Executable hash gate | PASS | The canonical report covers all 29 required artifacts; the real `VERIFYING -> RELEASE_READY` transition and `scripts/validation_gate.py` accept it |
| Signed-out public demo | PASS | Anonymous default `8/1/5/1`, strict `0/1/13/1`, falsey-rule HTTP 400, cross-scheme Origin 403, and both PDF links verified |
| Upwork publication | PASS | User confirms item number 3 is published; current listing copy and attachment were not reverified because browser control was unavailable |
| Reviewed source integration | PASS | GitHub PR #6 passed archive integrity and merged as `6da79dca1dbfea6d3dbca355caa8ad67173b80f0` |
| Immutable release | PASS | `ws-003-v1.0.0` and the GitHub Release point to the reviewed merge; release page and PDF asset return HTTP 200 signed out |
| Release authorization | PASS | User authorized closeout before WS-004 on 2026-09-12 |

## Artifact integrity

- Final PDF: `output/pdf/Municipal-311-SLA-Operations-Desk.pdf`
- Source boundary: `SOURCE_CONTRACT.md`
- Fixture boundary: `evidence/FIXTURE_PROVENANCE.md`
- Frozen checks: `evidence/VALIDATION_PLAN.json`
- Independent report: `evidence/INDEPENDENT_VALIDATION.json`
