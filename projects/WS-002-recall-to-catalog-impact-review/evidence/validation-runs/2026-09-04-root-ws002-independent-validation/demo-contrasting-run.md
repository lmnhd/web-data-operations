# Independent validation - demo-contrasting-run

- Validator: `/root/ws002_independent_validation`
- Public URL: `https://product-recall-match-desk.vercel.app/`
- Operated without a demo login on 2026-09-04T17:16:09Z through 2026-09-04T17:16:52Z.

## Default CAT-005

- Classification: `review_needed`
- Queue counts: 8 catalog rows, 6 match, 1 review_needed, 1 no_match
- Candidate D-0709-2026: 50 points, review needed
- Candidate D-0711-2026: 50 points, review needed
- Both candidates showed exact UPC, manufacturer overlap, strong product text overlap and strength conflict.
- Input SHA-256: `d6c3102d548d9ef79561d2b2d7dfd8d1974790e5181d0eda0ea91f2ed166ad5d`
- Engine SHA-256: `18f5455515c86c193d433975bcae82fa208c9cc91424d47972c197b5e77c9248`
- Source request, capture time and both source-record fingerprints were visible.

## Clarified CAT-005

After selecting **Add decisive evidence**, the form changed to 75 mcg, NDC family `55154-3560` and lot `N02172A`. Rerunning produced:

- Classification: `match`
- Matched recall: `D-0709-2026`
- Matched-candidate score: 200
- Queue counts: 8 catalog rows, 7 match, 0 review_needed, 1 no_match
- Input SHA-256: `d455abcdc7945e8df951fc1e2034b8729648d823b778631f96ab12c1f2ab0503`
- Engine SHA-256 remained `18f5455515c86c193d433975bcae82fa208c9cc91424d47972c197b5e77c9248`.

The input hash changed and the engine hash did not. The public **Run automated checks** action also completed successfully at `2026-09-04T17:16:51.618210+00:00`: 13 hosted matcher/demo-engine tests ran and passed. The page explicitly said HTTP adapter tests run in CI; the independent local 21-test suite separately executed those adapter tests.
