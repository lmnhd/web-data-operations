# Independent repair recheck - tests-full-suite

- Validator: `/root/ws002_independent_validation`
- Candidate head: `a23a3c4c0f7afc95ef6523a6ad098ebf933f740f`
- Repair source commit: `851f9fdc73436d3e6d2ef9129bbcba8f5677ede6`
- Executed: 2026-09-04 UTC
- Project command: from the project directory, `python -B -m unittest discover -s tests -v`
- Result: 21 tests ran in 0.766 seconds; all passed.

The suite again executed 4 demo-engine tests, 3 local HTTP tests, 9 matcher tests and 5 hosted-adapter tests. Assertions exercise the ambiguous and clarified decisions, changed input fingerprints, strict input validation, foreign-origin rejection, real run/export behavior, all three queue states, the 20-row oracle, provenance, fingerprints, determinism, hosted page behavior and hosted verification. These are concrete behavior assertions, not ceremonial checks.

One non-failing `ResourceWarning` was emitted for a test-client response holding `demo/index.html`; it did not produce a test failure or acceptance error.

The repaired validation-gate regression suite was also run independently from repository root with its temporary files outside the restricted sandbox:

```text
..............
----------------------------------------------------------------------
Ran 14 tests in 0.309s

OK
```

The new regression creates `.env.local` in a disposable project fixture and confirms that the gate excludes it as machine-local credential material.
