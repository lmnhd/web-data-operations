# WS-004 independent repair recheck - claim traceability

The PDF, README, Manifest, proof report, oracle, executed outputs, builder test log, source contract, selected-source record, factor subset, screenshots, and source/workbook hashes agree on the bounded result and limits.

Verified quantitative trace:

- deterministic six-case benchmark: 2 RECONCILED, 1 MISMATCH, 3 REVIEW_REQUIRED;
- default run `ws004-6fd5836905285efd` and changed run `ws004-944aa2c7c09f7480`;
- Case 02 controlled change: 1,000 MWh / 1,000,000 kWh / 177.000 tCO2e / RECONCILED to 1,000 kWh / 0.177 tCO2e / MISMATCH;
- repaired factor subset hash `61ad0e9b125f6a072a39414ba5cfc2ebe29d57b0b6d555bb3713c3ea86f75903`;
- repaired engine hash `220b84d987648689d7b92ffaa068ddcf2fe5a6516abdb007abe35fbcc0e7f3a4`;
- source workbook hash `8bfdb45b81ec4a88e3bdf4584637330f62e6bd09ce1940e654c5d7b7f736de94`;
- current exact test result: 27/27.

The 2/1/3 count is consistently identified as a six-case benchmark. The three minimized recorded filing sources are distinguished from the two reviewer-supplied controlled scenarios. The documents do not claim regulatory compliance, audit assurance, emissions truth, environmental performance, savings, exhaustive source coverage, or production accuracy. Historical 13- and 23-test statements in the proof report are explicitly framed as earlier builder stages; the current repaired result is correctly recorded as 27/27.

The repaired Manifest now accurately describes the initial independent FAIL, repaired candidate dispatch, current VERIFYING/recheck-pending status, and no release. It does not claim independent PASS before this report.
