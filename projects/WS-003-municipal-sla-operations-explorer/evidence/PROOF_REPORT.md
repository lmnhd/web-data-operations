# WS-003 proof report

## Corrected proof claim

WS-003 validates a configurable SLA evaluation engine on a bounded **synthetic** 311-style scenario. It does not evaluate recorded Toronto requests or official municipal SLA performance.

The correction follows a 2026-09-12 official-source audit: Toronto's 2026 public ZIP exposes creation date, current status, ward, request type, division, section, and coarse location fields, but not target or closure timestamps. Those missing fields are necessary for the proof's timing calculations.

## Recorded run

- Input kind: `synthetic_sla_scenario`
- Records: 15
- Reference time: `2026-08-08T12:00:00Z`
- Hypothetical rules: Pothole Repair 5 days; Streetlight Maintenance 3; Tree Trimming 10; Garbage Collection 2
- Result counts: 8 `COMPLIANT`, 1 `AT_RISK`, 5 `SLA_BREACHED`, 1 `INCOMPLETE_DATA_REVIEW`
- Predeclared-label agreement: 15 of 15
- Scenario Ward 01 compliance calculation: 40.0% (2 compliant of 5 evaluable records)

These are fixture results, not production accuracy or City performance metrics.

## Reviewer-operated scenario

Changing the hypothetical Pothole Repair target from 5 days to 3 days reclassifies synthetic `SR-311-001` from `COMPLIANT` to `SLA_BREACHED` with `CLOSED_AFTER_SLA_TARGET`.

## Failure case

A malformed creation timestamp routes to `INCOMPLETE_DATA_REVIEW`, lifecycle `DATA_ERROR`, reason `INVALID_CREATED_TIMESTAMP`. The engine does not silently classify the record.

## Reproduction

```powershell
python -m unittest discover projects/WS-003-municipal-sla-operations-explorer/tests
python projects/WS-003-municipal-sla-operations-explorer/src/sla_engine.py `
  --output-json tmp/ws003-run.json `
  --output-csv tmp/ws003-run.csv
```

Expected tests: 17 passed. Expected baseline: 15 records with `8/1/5/1` status counts. Unknown statuses, lifecycle/closure contradictions, and post-reference closure dates must route to `INCOMPLETE_DATA_REVIEW`; the API must reject fractional, unknown, and falsey non-object rule overrides with HTTP 400; and the HTTPS deployment must reject an equivalent HTTP Origin. Each evaluated row must include `fixture_kind=synthetic_sla_scenario`, a reason code, and a fingerprint.

## Evidence

- `evidence/evaluated_run.json`
- `evidence/evaluated_run.csv`
- `evidence/FIXTURE_PROVENANCE.md`
- `evidence/VALIDATION_PLAN.json`
- `evidence/INDEPENDENT_VALIDATION.json`
- `evidence/RELEASE_CHECKLIST.md`

The independent report supersedes builder self-review only when its verdict is PASS and `python scripts/validation_gate.py` passes unchanged hashes.
