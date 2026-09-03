# Government Contract Change Monitor

This portfolio project shows how a contractor or bid team can stop reopening meaningless government-contract updates. It compares versions of an opportunity, identifies important changes, applies the client's qualification rules, and produces separate act, ignore, and review lists.

The internal engineering name is **Qualified Tender Change Intelligence**. The public-facing name is intentionally simpler: **Government Contract Change Monitor**.

## What this proves

- explicit ingest allowlisting rather than retaining entire source payloads;
- provenance on every normalized release;
- field-level diffs over a declared material-field set;
- separation of source tags from actual semantic changes;
- configuration-driven qualification decisions;
- accepted, rejected, and review-needed outputs with reason codes;
- deterministic JSON, CSV, and run-report generation.

It does **not** claim complete amendment recall, production monitoring, real-time alerts, or business impact.

## Run the proof

From the repository root:

```powershell
python projects/WS-001-qualified-tender-change-intelligence/src/run_pipeline.py `
  --input projects/WS-001-qualified-tender-change-intelligence/tests/fixtures/release-package.json `
  --profile projects/WS-001-qualified-tender-change-intelligence/examples/qualification-profile.json `
  --output-dir projects/WS-001-qualified-tender-change-intelligence/evidence/latest-run
```

Run the tests:

```powershell
python -m unittest discover -s projects/WS-001-qualified-tender-change-intelligence/tests -v
```

## Bounded live evidence

The acquisition helper makes exactly one request for one validated procurement-process ID. It does not paginate, retry, probe a rate ceiling, or persist the raw response. Only the declared tender fields and a one-way source fingerprint are written:

```powershell
python projects/WS-001-qualified-tender-change-intelligence/src/fetch_sanitized_record.py `
  --ocid ocds-h6vhtk-06d396 `
  --output projects/WS-001-qualified-tender-change-intelligence/evidence/live/sanitized-record.json
```

The saved package can then be replayed through `run_pipeline.py`. Public evidence must retain the source attribution and clearly separate observed live results from synthetic fixture results.

## Reviewer path

1. Read `evidence/live/LIVE_EVIDENCE_REPORT.md` for the two observed live cases and claim boundaries.
2. Open `output/pdf/Government-Contract-Change-Monitor.pdf` from the repository root for the three-page client work sample.
3. Compare the JSON and CSV outputs under `evidence/live/run-06d396` and `evidence/live/run-06bb7d`.
4. Inspect `src/tender_pipeline.py` for the allowlist, diff, and qualification logic.
5. Run the automated tests to reproduce the deterministic controls.

The synthetic fixture remains deliberately small and supports repeatable edge-case tests. The separate live evidence contains two sanitized records and is labeled independently; neither evidence set is presented as a representative source-wide sample.
