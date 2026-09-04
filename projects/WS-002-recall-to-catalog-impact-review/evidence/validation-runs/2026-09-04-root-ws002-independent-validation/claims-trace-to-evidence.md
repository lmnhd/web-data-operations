# Independent validation - claims-trace-to-evidence

- Validator: `/root/ws002_independent_validation`
- Checked: 2026-09-04 UTC

README.md, PROJECT_MANIFEST.md, the PDF, RELEASE_CHECKLIST.md, the recorded benchmark and the independently replayed benchmark agree on:

- 20 of 20 independently declared fixture labels reproduced;
- 13 `match`, 1 `no_match`, 6 `review_needed`;
- 21 local automated tests passed;
- one recorded source request retaining 10 selected records from 12 returned;
- default CAT-005 at 6 / 1 / 1 and clarified CAT-005 at 7 / 0 / 1;
- matcher SHA-256 `18f5455515c86c193d433975bcae82fa208c9cc91424d47972c197b5e77c9248`.

The independent benchmark replay in `benchmark-replay/run-report.json` reproduced the recorded 20/20 and 13/1/6 values. The source fixture reports `request_count: 1` and contains 10 records. The 21-test command output independently reproduced the test-count claim.

All reviewed surfaces describe the result as a bounded recorded fixture with synthetic catalog inputs. They explicitly refuse production accuracy, source-wide coverage, medical correctness/advice, public-alert, current-status, lifecycle, business-impact and retailer-integration claims.
