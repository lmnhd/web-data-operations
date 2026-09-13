# Corporate Carbon Disclosure Reconciliation Desk

**Iteration:** WS-004

**Status:** VERIFYING candidate - one bounded independent-validation repair complete; recheck pending

This project is a bounded reviewer tool for deciding whether a company-level energy/emissions calculation can be reproduced from explicit activity, unit, factor-category, and factor-year evidence. Unsupported or incomplete disclosures must route to review rather than producing an inferred assurance result.

## Bounded proof result

The deterministic six-case run produces:

| Decision | Count |
|---|---:|
| RECONCILED | 2 |
| MISMATCH | 1 |
| REVIEW_REQUIRED | 3 |

The fixture distinguishes minimized recorded public filing facts from clearly labeled reviewer-supplied controlled scenarios. The proof uses the official UK 2025 Version 1 / Final factor vintage cited by the selected filings. It never treats a numerical match or mismatch as compliance, audit assurance, or proof that reported emissions are true.

## Run the reviewer workbench locally

Requirements: Python 3.11+ and Flask 3.1.2.

```powershell
cd projects/WS-004-corporate-carbon-disclosure-reconciler
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The six-case engine executes automatically. Click `Try the 1/1,000 unit change` to change the controlled scenario from 1,000 MWh to 1,000 kWh, then inspect the calculation, reason code, locator, and source hash or download the executed JSON/CSV.

## Run the CLI

From the repository root:

```powershell
python -B projects/WS-004-corporate-carbon-disclosure-reconciler/src/reconcile.py `
  --output-json projects/WS-004-corporate-carbon-disclosure-reconciler/evidence/evaluated_run.json `
  --output-csv projects/WS-004-corporate-carbon-disclosure-reconciler/evidence/evaluated_run.csv
```

Exercise the reviewer-operated unit change:

```powershell
python -B projects/WS-004-corporate-carbon-disclosure-reconciler/src/reconcile.py `
  --case-id CASE-02-CONTROLLED-MWH-RECONCILED `
  --override-activity-unit kWh
```

The unchanged numeric value `1000` is interpreted as 1,000 MWh in the baseline and 1,000 kWh after the edit. Normalized activity falls from 1,000,000 to 1,000 kWh; computed emissions fall from 177.000 to 0.177 tCO2e; and the decision changes from RECONCILED to MISMATCH.

Run tests:

```powershell
python -B -m unittest discover -s projects/WS-004-corporate-carbon-disclosure-reconciler/tests -v
```

Builder result after the bounded repair on 2026-09-13: **27 passed, 0 failed, 0 errors**. The initial independent run is preserved as FAIL; the repaired candidate still requires its reserved independent recheck.

## Evidence

- [Proof report](evidence/PROOF_REPORT.md)
- [Default JSON run](evidence/evaluated_run.json) and [CSV run](evidence/evaluated_run.csv)
- [Changed-input JSON run](evidence/changed_input_run.json) and [CSV run](evidence/changed_input_run.csv)
- [Declared oracle](evidence/fixtures/benchmark_oracle.json)
- [Selected-source record](evidence/SOURCE_SELECTION.json)
- [Pinned factor subset](evidence/factors/ghg_factors_2025.json)
- [Frozen validation plan](evidence/VALIDATION_PLAN.json)
- [Builder test log](evidence/BUILDER_TEST_LOG.md)
- [Release checklist](evidence/RELEASE_CHECKLIST.md)
- [Screenshot provenance](evidence/reviewer/SCREENSHOT_PROVENANCE.md)
- [Three-page client-facing PDF](../../output/pdf/Carbon-Disclosure-Reconciliation-Desk.pdf)

## Current boundary

Human approval covers the expanded local UI, visual PDF, evidence package, stable candidate, and independent validation. Public hosting and publication are not authorized. The included `vercel.json` makes the candidate deployment-ready but no deployment has been created. No production accuracy, compliance conclusion, audit assurance, environmental-performance claim, or savings claim is made.

Read before work:

- [Approved proof brief](../../iterations/ws-004/CODEX_VERTICAL_PROOF_BRIEF.md)
- [Source contract](SOURCE_CONTRACT.md)
- [Reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md)
- [Independent validation protocol](../../docs/shipping-pipeline/INDEPENDENT_VALIDATION.md)

The project-local `evidence/VALIDATION_PLAN.json` was frozen in commit `cab1c89` before implementation began, then revised before the single repair to include the four exact independent findings.
