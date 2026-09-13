# Claims, sources, privacy, and boundary inspection

Confirmed evidence:

- local archive size `54,357,249` and SHA-256 `cd8733ad05cbb3eeaca514f6b2044d16c6b6098d72535a90354d1863bd5077e5` match the frozen record;
- all three selected archive-entry byte counts and SHA-256 values match `SOURCE_SELECTION.json`;
- local workbook size `505,634` and SHA-256 `8bfdb45b81ec4a88e3bdf4584637330f62e6bd09ce1940e654c5d7b7f736de94` match the frozen record;
- workbook front page says year 2025, status Final, version 1, updated 2025-06-10;
- workbook rows 79, 83, and 3066 match the committed natural-gas net/gross and UK-electricity factor subset;
- the archive, workbook, and full filings are ignored under `tmp/` and do not appear in candidate `d95db72` or repository history;
- committed fixtures and executed exports contain minimized company-level metrics and source identifiers, with no prohibited personal fields, credentials, or full filing bodies;
- no hosting, deployment, publication, live write, arbitrary URL, or arbitrary file route was found or exercised.

Claims are not fully supportable. The PDF and Manifest say the engine refuses calculations without a compatible factor basis/category, but the adversarial activity-category conflict is classified RECONCILED. The Manifest also says `Reviewed commit / PR / tag: Not applicable; no candidate exists` and that the validator is `not yet dispatched`, which is stale relative to stable candidate `d95db72` and the recorded dispatch.

`python scripts/validation_gate.py` reports pass only because the active state remains VERIFYING; the script intentionally does not enforce the independent report until RELEASE_READY. A read-only simulated RELEASE_READY check returned `Independent validation has not passed without unresolved findings`. No state transition was attempted because independent validation failed.
