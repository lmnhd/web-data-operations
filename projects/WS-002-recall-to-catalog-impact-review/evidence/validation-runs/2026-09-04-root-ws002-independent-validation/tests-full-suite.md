# Independent validation - tests-full-suite

- Validator: `/root/ws002_independent_validation`
- Candidate commit: `69ef14bbf026c93853057e8c7d12dcaf5acdb850`
- Branch: `iteration/ws-002-discovery`
- Executed: 2026-09-04T17:13:00Z to 2026-09-04T17:14:00Z
- Working directory: `projects/WS-002-recall-to-catalog-impact-review`
- Command: `python -B -m unittest discover -s tests -v`
- Exit code: 0
- Result: 21 tests ran in 0.685 seconds; all passed.

## Test inventory and meaningfulness assessment

The suite executed 4 demo-engine tests, 3 local HTTP tests, 9 matcher tests and 5 hosted-adapter tests. The assertions directly exercise:

- ambiguous and clarified CAT-005 decisions plus changed input fingerprints;
- strict editable-field validation, oversized input rejection and foreign-origin rejection;
- real local and hosted-adapter run/export paths and security headers;
- all three queue states, the independently declared 20-row oracle, provenance, per-candidate fingerprints and determinism;
- hosted adapter page behavior, clarified result, cross-site POST rejection and its 13-test hosted verification subset.

The tests are behavior-based rather than ceremonial: they execute the matcher and HTTP adapters and assert concrete decisions, counts, provenance and response statuses. A `ResourceWarning` identified an unclosed `demo/index.html` test response during `test_page_and_security_headers`; it did not produce a test failure or error and is consistent with test-client response cleanup rather than a failed acceptance behavior.

## Exact result summary

```text
Ran 21 tests in 0.685s

OK
```

An additional independent benchmark replay wrote `benchmark-replay/run-report.json` and reproduced all 20 declared labels with 13 match, 1 no_match and 6 review_needed.
