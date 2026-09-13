# WS-004 independent repair recheck - executed exports

The validator independently generated default and changed-input JSON/CSV files in this recheck directory using the documented CLI.

Default command:

`python -B projects/WS-004-corporate-carbon-disclosure-reconciler/src/reconcile.py --output-json projects/WS-004-corporate-carbon-disclosure-reconciler/evidence/validation-runs/2026-09-13-recheck-c624ea5/executed_default.json --output-csv projects/WS-004-corporate-carbon-disclosure-reconciler/evidence/validation-runs/2026-09-13-recheck-c624ea5/executed_default.csv`

Changed command adds:

`--case-id CASE-02-CONTROLLED-MWH-RECONCILED --override-activity-unit kWh`

Observed default export:

- run ID `ws004-6fd5836905285efd` in the JSON envelope and all six CSV rows;
- exactly six rows and 2 RECONCILED / 1 MISMATCH / 3 REVIEW_REQUIRED;
- zero cross-format field mismatches across case ID, decision, reason, normalized/computed values, tolerance, source locator, factor metadata, and all input/source/factor/engine hashes;
- raw files are byte-identical to committed `evidence/evaluated_run.json` and `.csv`.

Observed changed export:

- run ID `ws004-944aa2c7c09f7480`;
- Case 02 changes from MWh to kWh while numeric activity remains 1000;
- normalized activity changes from `1000000.000000` to `1000.000000` kWh;
- computed emissions change from `177.000000` to `0.177000` tCO2e;
- decision changes RECONCILED to MISMATCH and input SHA-256 changes;
- source, factor-subset, factor-workbook, and engine hashes remain identical;
- raw files are byte-identical to committed `evidence/changed_input_run.json` and `.csv`.

Raw SHA-256 values of the four committed/executed pairs are respectively `6543dfd97762f6516ba602ad0ac43e5e351b45075b32ad13a064d76d4e0d8dfe`, `b92ca78400e912c2d9c99a4122d2cf31699e5702dcdc5f3937d434318972792d`, `9d85514d3ea0146b0c9c2140b30d9d4b6f608ef61d8b3d383edf5917f63baee1`, and `8f95a1458258c2ce7a999e325320fb4e9b3e13a5837941c1ac0a6817f161dace`.

A prohibited-field scan found no company name, personal name, signature, address, email, phone, contact, credential, password, secret, API key, bearer token, or authorization material in the minimized executed exports.
