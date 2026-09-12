# WS-003 release checklist

Closeout resumed 2026-09-12 UTC. Statuses remain fail-closed until evidence is refreshed.

| Gate | Status | Evidence |
|---|---|---|
| Runnable Python web demo | PASS | `app.py`, `src/demo_server.py`, `demo/` |
| Synthetic input disclosed in UI and exports | PASS | `fixture_kind=synthetic_sla_scenario`; source and fixture contracts |
| Meaningful rule change | PASS | Hypothetical Pothole target 5d -> 3d reclassifies synthetic `SR-311-001` |
| Edge/safe state | PASS | Malformed creation timestamp routes to `INCOMPLETE_DATA_REVIEW` |
| JSON/CSV exports | PASS | Labeled rows with reason codes and fingerprints |
| Builder-side automated tests | PASS | `python -m unittest discover projects/WS-003-municipal-sla-operations-explorer/tests`: 15/15 on 2026-09-12, including falsey non-object rule payloads |
| Official source contract | PASS | 2026 ZIP columns verified; missing target/closure timestamps disclosed |
| Visual three-page PDF | FAIL | Fresh validator found page 2 code and footer clipping in the 15/15-test rebuild |
| Actual working-output screenshot | PASS | `evidence/reviewer/working-demo.png` and `evidence/reviewer/working-demo-pdf.png`, captured from the corrected local demo on 2026-09-12 |
| Independent verification | FAIL | `/root/ws003_final_validator` reports 5 PASS, 2 FAIL and four unresolved findings for candidate `3f9f274` |
| Executable hash gate | FAIL | The 29-artifact report is hash-complete, but the release-stage gate rejects its FAIL verdict |
| Signed-out public demo | FAIL | Functional checks pass, but the HTTPS endpoint accepts an equivalent HTTP Origin because only host is compared |
| Upwork publication | PASS | User confirms item number 3 is published; corrected copy/PDF refresh remains |
| Reviewed source integration | BLOCKED | Independent PASS is absent; pull request/default-branch integration is prohibited |
| Immutable release | BLOCKED | `ws-003-v1.0.0` tag and GitHub release required |
| Release authorization | PASS | User authorized closeout before WS-004 on 2026-09-12 |

## Artifact integrity

- Final PDF: `output/pdf/Municipal-311-SLA-Operations-Desk.pdf`
- Source boundary: `SOURCE_CONTRACT.md`
- Fixture boundary: `evidence/FIXTURE_PROVENANCE.md`
- Frozen checks: `evidence/VALIDATION_PLAN.json`
- Independent report: `evidence/INDEPENDENT_VALIDATION.json`
