# Qualified Tender Change Intelligence

WS-001 is a bounded vertical proof for turning public procurement release histories into an explainable review queue. It distinguishes material field changes from update-tagged republications, then applies deterministic qualification rules so a bid team can focus on relevant changes.

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

## Reviewer path

1. Read the summary in `evidence/latest-run/run-report.json`.
2. Compare `accepted.csv`, `rejected.csv`, and `review-needed.csv`.
3. Inspect `src/tender_pipeline.py` for the allowlist, diff, and qualification logic.
4. Run the fixture tests to reproduce the result.

The included fixture is synthetic and deliberately small. Its scenarios are derived from the live-source defect found during discovery, but its values are not presented as a captured government dataset. A bounded sanitized live evidence capture remains a separate proof step.
