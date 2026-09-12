# Municipal 311 SLA Operations Desk (WS-003)

An adapter-ready Python demonstration for evaluating configurable service-response targets, routing malformed timestamps to review, aggregating ward scenarios, and exporting auditable results.

## Evidence boundary

The runnable proof processes 15 explicitly synthetic records. Toronto's licensed public 311 schema inspired the creation-date, status, ward, and request-type fields, but the public 2026 export does not include target or closure timestamps. The demo therefore makes no claim about official Toronto SLA performance.

See [SOURCE_CONTRACT.md](SOURCE_CONTRACT.md) and [evidence/FIXTURE_PROVENANCE.md](evidence/FIXTURE_PROVENANCE.md).

## What the reviewer can test

1. Run the default synthetic scenario and inspect 8 compliant, 1 at-risk, 5 breached, and 1 review record.
2. Change the hypothetical Pothole Repair target from 5 days to 3 days and observe synthetic record `SR-311-001` change from `COMPLIANT` to `SLA_BREACHED`.
3. Inspect malformed timestamp routing to `INCOMPLETE_DATA_REVIEW`.
4. Download JSON and CSV outputs containing `fixture_kind`, reason codes, lifecycle states, and record fingerprints.

## Local demo

```powershell
python -m pip install -r projects/WS-003-municipal-sla-operations-explorer/requirements.txt
python projects/WS-003-municipal-sla-operations-explorer/app.py
```

Open `http://127.0.0.1:5000`.

## Tests

```powershell
python -m unittest discover projects/WS-003-municipal-sla-operations-explorer/tests
```

Expected result: 17 tests, 0 failures, 0 errors. The suite includes invalid chronology, malformed timestamps, unknown or contradictory lifecycle states, post-reference closure dates, unmapped categories, fractional and unknown rules, falsey non-object rule payloads, and cross-scheme Origin rejection.

## CLI and exports

```powershell
python projects/WS-003-municipal-sla-operations-explorer/src/sla_engine.py `
  --output-json tmp/ws003-run.json `
  --output-csv tmp/ws003-run.csv
```

Expected baseline: 15 synthetic records with status counts `8/1/5/1` for compliant/at-risk/breached/review.

## Reviewer evidence

- [Project Manifest](PROJECT_MANIFEST.md)
- [Proof report](evidence/PROOF_REPORT.md)
- [Validation plan](evidence/VALIDATION_PLAN.json)
- [Independent validation](evidence/INDEPENDENT_VALIDATION.json)
- [Release checklist](evidence/RELEASE_CHECKLIST.md)
- [Three-page PDF](../../output/pdf/Municipal-311-SLA-Operations-Desk.pdf)

Public demo target: https://municipal-311-sla-operations-desk.vercel.app

This is a portfolio case study, not a production municipal system.
