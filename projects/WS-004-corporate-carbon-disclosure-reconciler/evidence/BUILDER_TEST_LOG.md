# WS-004 builder test log

**Date:** 2026-09-13

**Role:** Root builder/orchestrator - not independent validation

## Frozen command

```powershell
python -B -m unittest discover -s projects/WS-004-corporate-carbon-disclosure-reconciler/tests -v
```

Observed result after the single bounded independent-validation repair: **27 tests passed, 0 failed, 0 errors**.

Coverage includes:

- exact six-case 2 RECONCILED / 1 MISMATCH / 3 REVIEW_REQUIRED oracle;
- decimal kWh/MWh and kgCO2e/tCO2e normalization;
- inclusive tolerance boundary and explicit mismatch arithmetic;
- ambiguous natural-gas gross/net basis, insufficient aggregate breakdown, unsupported image-only source, unknown factor year/ID, invalid numeric input, and unsupported units;
- exact activity-category/factor-category compatibility in both engine and API paths;
- rejection of malformed supplied source SHA-256 values in both engine and API paths;
- deterministic input, source, factor-subset, factor-workbook, and engine hashes;
- exact JSON/CSV run identity through a `runId` column on every CSV row;
- rejection of company-name and personal/display fields;
- actual Flask routes for the reviewer UI, configuration, code excerpt, default run, changed-input run, and in-memory CSV export;
- rejection of unknown request fields, wrong types, unknown cases, inappropriate unit overrides, non-JSON bodies, oversized bodies, cross-site requests, and cross-scheme Origins.

The first sandboxed repair run encountered the already-documented Windows permission denial for its disposable export-test directory. The exact frozen command was rerun outside that filesystem restriction and passed 27/27; the verified temporary directory was removed. This log records builder verification only. Release readiness still requires the independent repair recheck and executable hash gate.
