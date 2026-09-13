# WS-004 independent repair recheck - fail-closed and adversarial behavior

The validator-owned `adversarial_recheck.py` exercised both the engine and Flask adapter without changing product files.

Observed repair results:

| Finding | Engine result | API result | Recheck |
|---|---|---|---|
| WS004-IV-001: diesel activity paired with UK-electricity factor | `REVIEW_REQUIRED`, `FACTOR_ACTIVITY_CATEGORY_CONFLICT`, computed result `null` | HTTP 200 with the same review result and no computed value | Resolved |
| WS004-IV-002: cross-format run identity | JSON run `ws004-6fd5836905285efd`; all six CSV rows carry exactly that ID | Web JSON/CSV response has the same run ID on six rows | Resolved |
| WS004-IV-003: malformed supplied source SHA-256 | `EvidenceBoundaryError`: `sourceSha256 must be exactly 64 hexadecimal characters` | HTTP 400 with the same boundary message | Resolved |
| WS004-IV-004: stale Manifest | Current Manifest records initial candidate `d95db72`, the preserved independent FAIL, repaired-candidate dispatch, 27-test builder result, VERIFYING status, no release, and recheck pending | Not applicable | Resolved |

The frozen recorded/controlled edge cases also passed in the 27-test suite: aggregate energy without a compatible breakdown, controlled image-only evidence, unknown factor reference, and natural gas without gross/net calorific basis return the prescribed review codes without an arithmetic assurance result. Invalid numerics and unsupported units fail closed. No path infers a fuel mix or factor and no result claims audit assurance, compliance, emissions truth, or environmental performance.
