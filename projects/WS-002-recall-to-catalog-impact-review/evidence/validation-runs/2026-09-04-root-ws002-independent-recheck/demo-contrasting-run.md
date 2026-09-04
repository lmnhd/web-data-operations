# Independent repair recheck - demo-contrasting-run

- Validator: `/root/ws002_independent_validation`
- Public URL: `https://product-recall-match-desk.vercel.app/`
- Operated without a demo login on 2026-09-04T17:29:39Z through 2026-09-04T17:30:12Z.

The default CAT-005 execution produced `review_needed`, 6 match / 1 review / 1 no match, and preserved D-0709-2026 and D-0711-2026 as conflicting 50-point candidates. Input SHA-256 was `d6c3102d548d9ef79561d2b2d7dfd8d1974790e5181d0eda0ea91f2ed166ad5d`; engine SHA-256 was `18f5455515c86c193d433975bcae82fa208c9cc91424d47972c197b5e77c9248`.

After **Add decisive evidence**, CAT-005 changed to 75 mcg with NDC `55154-3560` and lot `N02172A`. Rerunning produced `match` to D-0709-2026 at 200 points and 7 match / 0 review / 1 no match. Input SHA-256 changed to `d455abcdc7945e8df951fc1e2034b8729648d823b778631f96ab12c1f2ab0503`; engine SHA-256 remained unchanged.

Source URL, capture time and record fingerprints remained visible. The public **Run automated checks** action passed 13 hosted matcher/demo-engine tests at `2026-09-04T17:30:12.096698+00:00`; HTTP adapter tests were separately included in the 21-test local suite.
