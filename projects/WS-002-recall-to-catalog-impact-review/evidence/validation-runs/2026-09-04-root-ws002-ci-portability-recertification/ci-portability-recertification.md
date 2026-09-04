# WS-002 CI portability recertification

- Validator: `/root/ws002_independent_validation`
- Candidate: `f7f78f795b75a214cf385898257d301591a7e06d`
- Scope: validation hash portability only; the frozen plan, product, PDF and 54 covered artifacts were unchanged.
- Verdict: **PASS**.

## Executed checks

- `python -B scripts/tests/test_validation_gate.py`: 16 tests ran and passed in 0.303 seconds outside the filesystem sandbox, including direct CSS portability and binary exactness assertions. An earlier sandboxed attempt at the preceding candidate could not create Python temporary directories and was an environment error, not a test result.
- `python -B -m unittest discover -s tests -v` from the project directory: exactly 21 tests ran and passed in 0.700 seconds. The previously recorded non-failing unclosed-response `ResourceWarning` appeared again.
- Recomputed all 54 covered artifact hashes using `validation_gate.digest`. Sixteen generated text hashes change from the prior byte-level report, as expected; the canonical worktree digest matched the canonical Git-object digest for every current covered artifact.
- Confirmed `digest()` equals raw SHA-256 for the PDF and a representative PNG. CRLF/LF byte variants remain unequal for binary-classified paths.

## Resolved adversarial finding

The preceding candidate omitted `.css` from `TEXT_SUFFIXES`, which this review identified because `demo/style.css` is a covered text artifact. Candidate `f7f78f795b75a214cf385898257d301591a7e06d` adds `.css` to the declared text set and adds a direct regression proving LF and CRLF CSS hashes are equal while LF and CRLF PDF byte sequences remain unequal.

The independent 54-file comparison found zero mismatches between canonical worktree digests and canonical Git-object digests. The PDF and a representative PNG retained raw byte-exact SHA-256 values. No portability finding remains unresolved, and all seven frozen product-check results remain supported by the unchanged product artifacts and prior independent evidence.
