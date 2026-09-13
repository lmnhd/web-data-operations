# Corporate Carbon Disclosure Reconciliation Desk

**Iteration:** WS-004  
**Status:** PROVING - bounded local proof implemented; expansion not approved

This project is a bounded reviewer tool for deciding whether a company-level energy/emissions calculation can be reproduced from explicit activity, unit, factor-category, and factor-year evidence. Unsupported or incomplete disclosures must route to review rather than producing an inferred assurance result.

## Bounded proof result

The deterministic six-case run produces:

| Decision | Count |
|---|---:|
| RECONCILED | 2 |
| MISMATCH | 1 |
| REVIEW_REQUIRED | 3 |

The fixture distinguishes minimized recorded public filing facts from clearly labeled reviewer-supplied controlled scenarios. The proof uses the official UK 2025 Version 1 / Final factor vintage cited by the selected filings. It never treats a numerical match or mismatch as compliance, audit assurance, or proof that reported emissions are true.

## Run locally

Requirements: Python 3.11+; no third-party packages.

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

## Evidence

- [Proof report](evidence/PROOF_REPORT.md)
- [Default JSON run](evidence/evaluated_run.json) and [CSV run](evidence/evaluated_run.csv)
- [Changed-input JSON run](evidence/changed_input_run.json) and [CSV run](evidence/changed_input_run.csv)
- [Declared oracle](evidence/fixtures/benchmark_oracle.json)
- [Selected-source record](evidence/SOURCE_SELECTION.json)
- [Pinned factor subset](evidence/factors/ghg_factors_2025.json)
- [Frozen validation plan](evidence/VALIDATION_PLAN.json)

## Current boundary

Human approval covers this local bounded proof only. A reviewer web UI, visual PDF, broader sample, public hosting, independent release validation, and publication are not yet authorized. No production accuracy, compliance conclusion, audit assurance, environmental-performance claim, or savings claim is made.

Read before work:

- [Approved proof brief](../../iterations/ws-004/CODEX_VERTICAL_PROOF_BRIEF.md)
- [Source contract](SOURCE_CONTRACT.md)
- [Reviewer evidence standard](../../docs/shipping-pipeline/REVIEWER_EVIDENCE_STANDARD.md)
- [Independent validation protocol](../../docs/shipping-pipeline/INDEPENDENT_VALIDATION.md)

The project-local `evidence/VALIDATION_PLAN.json` was frozen in commit `cab1c89` before implementation began.
