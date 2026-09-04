# WS-002 vertical-proof report

## Outcome

**PASS - bounded fixture proof.** Same-agent verification; no independent audit has been performed.

Recorded on 2026-09-03 US Eastern / 2026-09-04 UTC.

## Source capture

- One unauthenticated openFDA request returned 12 records with harmonized UPC annotations.
- Ten selected, allowlisted records were retained in the proof fixture.
- No pagination, retry, rate probing, API key or follow-up record request was used.
- The captured records exposed a real ambiguity: the same harmonized UPC/NDC family can cover multiple strengths or packages.

## Baseline result

- Synthetic catalog rows: 8
- Recorded recall rows: 10
- Independent labels reproduced: 8 of 8
- `match`: 6
- `review_needed`: 1
- `no_match`: 1

`CAT-005` carries a UPC shared by recorded 75 mcg and 150 mcg levothyroxine variants while the catalog row says 100 mcg. The engine refuses a confident match and preserves both candidates, their reasons and their content fingerprints for review.

## Changed-input result

The reviewer scenario changes `CAT-005` from 100 mcg with no NDC/lot to 75 mcg with NDC family `55154-3560` and lot `N02172A`.

- Independent labels reproduced: 8 of 8
- `match`: 7
- `no_match`: 1
- Changed decision: `CAT-005`, `review_needed` -> `match` to `D-0709-2026`
- Match evidence: exact UPC, exact NDC family, exact lot, product overlap and matching strength

## Verification

Commands:

```powershell
python -m unittest discover -s tests -v
python src/run_proof.py --catalog tests/fixtures/catalog.json --recalls tests/fixtures/recalls.json --expected tests/fixtures/expected-labels.json --output-dir evidence/latest-run
python src/run_proof.py --catalog tests/fixtures/catalog-changed.json --recalls tests/fixtures/recalls.json --expected tests/fixtures/expected-labels-changed.json --output-dir evidence/changed-input
```

Observed result: 8 tests passed after one repair pass. Both recorded proof runs reproduced 8 of 8 labels.

The repair added per-candidate fingerprints and raised exact-identifier/strength-conflict evidence above unrelated no-match pairs so the review output remains correctly ordered and auditable.

## Boundaries

This proof does not establish complete recall coverage, current recall status, medical correctness, production accuracy, business impact, retailer integration, public-alert suitability or recall-lifecycle tracking. The catalog is synthetic and the sample is deliberately small.
