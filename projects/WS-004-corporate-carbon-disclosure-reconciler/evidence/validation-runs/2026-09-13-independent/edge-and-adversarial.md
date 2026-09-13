# Edge-case and adversarial validation

The prescribed cases passed:

- aggregate activity without a compatible breakdown -> REVIEW_REQUIRED / INSUFFICIENT_CALCULATION_EVIDENCE / no computed result;
- controlled image-only source -> REVIEW_REQUIRED / UNSUPPORTED_SOURCE_FORMAT / no computed result;
- unknown factor year and unknown factor ID -> REVIEW_REQUIRED / UNKNOWN_FACTOR_REFERENCE / no computed result;
- natural gas without gross/net calorific basis -> REVIEW_REQUIRED / AMBIGUOUS_ACTIVITY_BASIS / no computed result.

Additional engine check failed the frozen source-contract boundary. Changing only Case 01 `activityCategory` from `uk_grid_electricity` to `diesel` while retaining the UK-electricity factor ID produced RECONCILED / WITHIN_TOLERANCE and `697.341060 tCO2e`. The engine checks natural-gas basis and factor activity unit but does not verify that the explicit activity category is compatible with the resolved factor category.

An additional traceability check supplied `sourceSha256: not-a-sha256`; the engine returned the same malformed value in a RECONCILED output instead of rejecting or reviewing it.

Additional API checks passed: cross-origin POST 403; unknown `file` field 400; path-like case ID 400; GET on `/api/run` 405. The executable observations are in `adversarial_checks.py`.
