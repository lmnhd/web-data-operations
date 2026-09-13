# WS-004 builder test log

**Date:** 2026-09-13

**Role:** Root builder/orchestrator - not independent validation

## Frozen command

```powershell
python -B -m unittest discover -s projects/WS-004-corporate-carbon-disclosure-reconciler/tests -v
```

Observed result after the approved UI expansion: **23 tests passed, 0 failed, 0 errors**.

Coverage includes:

- exact six-case 2 RECONCILED / 1 MISMATCH / 3 REVIEW_REQUIRED oracle;
- decimal kWh/MWh and kgCO2e/tCO2e normalization;
- inclusive tolerance boundary and explicit mismatch arithmetic;
- ambiguous natural-gas gross/net basis, insufficient aggregate breakdown, unsupported image-only source, unknown factor year/ID, invalid numeric input, and unsupported units;
- deterministic input, source, factor-subset, factor-workbook, and engine hashes;
- rejection of company-name and personal/display fields;
- actual Flask routes for the reviewer UI, configuration, code excerpt, default run, changed-input run, and in-memory CSV export;
- rejection of unknown request fields, wrong types, unknown cases, inappropriate unit overrides, non-JSON bodies, oversized bodies, cross-site requests, and cross-scheme Origins.

This log records builder verification only. Release readiness still requires the separate non-builder report and executable hash gate.
