# WS-004 independent repair recheck - automated tests

- Validator: `/root/ws004_independent_validator`
- Repaired product candidate: `c624ea5da67e8838ed96064560e83298767cb943`
- Date: 2026-09-13
- Command: `python -B -m unittest discover -s projects/WS-004-corporate-carbon-disclosure-reconciler/tests -v`
- Final observed result: 27 tests, 0 failures, 0 errors, `OK`.

The exact command was executed with ordinary host filesystem access because the managed workspace sandbox denies writes inside the disposable `tests/tmp*` directory used by one export test. A sandboxed invocation reproduced that environmental denial as one `PermissionError`; the exact same command outside that restriction passed all 27 tests in 0.049 seconds. The disposable denied-run directory was removed after its exact path was verified.

The four repair regressions were present and passed by name:

- engine activity-category/factor-category conflict;
- API activity-category/factor-category conflict;
- engine malformed supplied source SHA-256 rejection;
- API malformed supplied source SHA-256 rejection.

The export regression also passed, including identical `runId` values in the JSON envelope and every CSV row. The remaining tests exercise the six-case oracle, decimal normalization, tolerance, deterministic hashes, fail-closed evidence cases, privacy exclusions, API request boundaries, and the controlled MWh-to-kWh change. This is meaningful coverage for the frozen bounded proof.
