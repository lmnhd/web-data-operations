# Live Evidence Report

## Scope and acquisition boundary

On 2026-09-03, WS-001 made two explicit requests to the documented Find a Tender OCDS record-package endpoint. Each request targeted one previously identified procurement process. There was no pagination, retry, rate-limit probing, browser scraping, authentication, or scheduled monitoring.

The raw responses were processed in memory and were not written to disk. The saved replay packages retain only the declared tender fields, release identifiers and dates, source tags, and a SHA-256 fingerprint of each original release. Contact details, descriptions, and unstructured prose were not persisted.

Find a Tender documents its record-package API, HTTP 429 behavior, and Open Government Licence publication. Its Terms and Conditions prohibit crawling that impairs the system and attempts to avoid system limitations. This proof therefore used two isolated requests and stopped; it does not infer or test an undocumented request ceiling.

## Observed cases

### Case A - `ocds-h6vhtk-06d396`

- 7 releases produced 6 consecutive-release comparisons.
- All 6 later releases carried the `tenderUpdate` tag.
- None changed the declared fields: status, deadline, value, currency, classification, or lot state.
- All 6 were rejected with `NO_MATERIAL_CHANGE`.

This is direct evidence that an update-tag count is not a valid denominator for material-change detection on this record.

### Case B - `ocds-h6vhtk-06bb7d`

- 2 releases produced 1 comparison.
- The later release carried `tenderCancellation`, not `tenderUpdate`.
- Direct comparison surfaced 5 material changes: status, deadline, value amount, value currency, and lot state.
- The later snapshot lacked classification, value, and deadline evidence needed by the qualification profile.
- The result was routed to `review-needed` with three explicit missing-evidence codes.

This is evidence that change detection and opportunity qualification must remain separate decisions.

## Reproducibility

The sanitized input packages, JSON run reports, and CSV queues are stored under this directory. The pipeline automatically reads the recorded source URL and retrieval timestamp from each capture.

```powershell
python projects/WS-001-qualified-tender-change-intelligence/src/run_pipeline.py `
  --input projects/WS-001-qualified-tender-change-intelligence/evidence/live/sanitized-record.json `
  --profile projects/WS-001-qualified-tender-change-intelligence/examples/qualification-profile.json `
  --output-dir projects/WS-001-qualified-tender-change-intelligence/evidence/live/run-06d396
```

```powershell
python projects/WS-001-qualified-tender-change-intelligence/src/run_pipeline.py `
  --input projects/WS-001-qualified-tender-change-intelligence/evidence/live/sanitized-record-06bb7d.json `
  --profile projects/WS-001-qualified-tender-change-intelligence/examples/qualification-profile.json `
  --output-dir projects/WS-001-qualified-tender-change-intelligence/evidence/live/run-06bb7d
```

## Claim boundary

These observations describe two deliberately selected records. They do not estimate source-wide update quality, material-change prevalence, completeness, recall, production throughput, real-time latency, or customer savings.

## Sources and attribution

- [Find a Tender record-package API](https://www.find-tender.service.gov.uk/apidocumentation/1.0/GET-ocdsRecordPackages)
- [Find a Tender Terms and Conditions](https://www.find-tender.service.gov.uk/Home/TermsAndConditions)
- [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

Contains public sector information licensed under the Open Government Licence v3.0.
