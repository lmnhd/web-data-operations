# WS-003 release checklist

Closeout resumed 2026-09-12 UTC. Statuses remain fail-closed until evidence is refreshed.

| Gate | Status | Evidence |
|---|---|---|
| Runnable Python web demo | PASS | `app.py`, `src/demo_server.py`, `demo/` |
| Synthetic input disclosed in UI and exports | PASS | `fixture_kind=synthetic_sla_scenario`; source and fixture contracts |
| Meaningful rule change | PASS | Hypothetical Pothole target 5d -> 3d reclassifies synthetic `SR-311-001` |
| Edge/safe state | PASS | Malformed creation timestamp routes to `INCOMPLETE_DATA_REVIEW` |
| JSON/CSV exports | PASS | Labeled rows with reason codes and fingerprints |
| Builder-side automated tests | PASS | `python -m unittest discover projects/WS-003-municipal-sla-operations-explorer/tests`: 14/14 on 2026-09-12 |
| Official source contract | PASS | 2026 ZIP columns verified; missing target/closure timestamps disclosed |
| Visual three-page PDF | PASS | Rebuilt after title-overlap repair; synthetic boundaries visible |
| Actual working-output screenshot | PASS | `evidence/reviewer/working-demo.png` and `evidence/reviewer/working-demo-pdf.png`, captured from the corrected local demo on 2026-09-12 |
| Independent verification | FAIL | `/root/ws003_release_validator` failed repair candidate `2addbb6`; falsey non-object `rules` payloads bypass validation |
| Executable hash gate | FAIL | Hash-bound report is complete but verdict is FAIL; the release-stage gate rejects it |
| Signed-out public demo | PASS | Production alias redeployed 2026-09-12; anonymous page/config/default/strict/fractional-rule checks passed and expose `synthetic_sla_scenario` |
| Upwork publication | PASS | User confirms item number 3 is published; corrected copy/PDF refresh remains |
| Reviewed source integration | BLOCKED | Pull request/default-branch integration required |
| Immutable release | BLOCKED | `ws-003-v1.0.0` tag and GitHub release required |
| Release authorization | PASS | User authorized closeout before WS-004 on 2026-09-12 |

## Artifact integrity

- Final PDF: `output/pdf/Municipal-311-SLA-Operations-Desk.pdf`
- Source boundary: `SOURCE_CONTRACT.md`
- Fixture boundary: `evidence/FIXTURE_PROVENANCE.md`
- Frozen checks: `evidence/VALIDATION_PLAN.json`
- Independent report: `evidence/INDEPENDENT_VALIDATION.json`
