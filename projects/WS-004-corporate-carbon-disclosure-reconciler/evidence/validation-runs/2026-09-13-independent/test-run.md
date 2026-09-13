# Independent test execution

- Candidate: `d95db72`
- Validator: `/root/ws004_independent_validator`
- Frozen command: `python -B -m unittest discover -s projects/WS-004-corporate-carbon-disclosure-reconciler/tests -v`

The first sandboxed execution ran all 23 tests but ended with one error in `test_json_and_csv_exports_agree_and_remain_minimized`: Windows denied creation of `tests/tmpxjxwa2qh/run.json`, then denied cleanup of that temporary directory. The exact command was rerun outside the filesystem sandbox to distinguish environment interference from a candidate failure.

The independent rerun passed: 23 tests, 0 failures, 0 errors, in 0.084 seconds. The abandoned sandbox temporary directory was removed after its exact absolute path was verified. The tests meaningfully exercise the declared six-case oracle, decimal normalization, tolerance boundary, prescribed fail-closed cases, deterministic hashes, export agreement, prohibited keys, web routes, request typing, size limit, and origin checks. Adversarial review identified uncovered contract risks recorded separately.
