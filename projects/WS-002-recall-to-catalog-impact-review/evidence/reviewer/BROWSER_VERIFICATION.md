# Reviewer workbench browser verification

Verified 2026-09-04 UTC against the local server at `http://127.0.0.1:8766`.

## PASS - actual execution

- Default CAT-005 produced `REVIEW NEEDED`.
- Counts were 8 catalog rows, 6 match, 1 review-needed and 1 no-match.
- Candidates D-0709-2026 and D-0711-2026 each retained exact UPC and `strength_conflict` reasons.
- Source URL, capture timestamp, catalog-input SHA-256, engine SHA-256 and candidate fingerprints were visible.

## PASS - meaningful changed input

- The **Add decisive evidence** preset changed strength to 75 mcg and supplied NDC `55154-3560` and lot `N02172A`.
- CAT-005 changed to `MATCH` for D-0709-2026 at 200 points.
- Counts changed to 7 match, 0 review-needed and 1 no-match.
- Catalog-input SHA-256 changed; engine SHA-256 remained the same.

## PASS - runnable checks and responsive layout

- The in-page **Run automated checks** control returned `Passed`.
- At 390 x 844 CSS pixels, CAT-005 remained executable and no horizontal document overflow was detected.
- Desktop evidence: `ambiguous.png`, `clarified.png`.
- Mobile evidence: `mobile-clarified.png`.

The implementation and browser checks were performed by the same agent. Public signed-out availability was not tested because hosting and publication remain unauthorized.
