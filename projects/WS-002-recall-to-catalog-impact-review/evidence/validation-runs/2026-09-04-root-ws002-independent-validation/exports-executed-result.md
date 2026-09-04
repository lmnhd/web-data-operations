# Independent validation - exports-executed-result

- Validator: `/root/ws002_independent_validation`
- Public execution: 2026-09-04T17:20:11.775622+00:00
- Public run ID: `865280a5-0b44-4cc8-83d8-ead47d9b0943`

The public demo executed the default CAT-005 row and displayed run prefix `865280a5`, classification `review_needed`, counts 6 match / 1 review / 1 no match, input hash `d6c3102d548d9ef79561d2b2d7dfd8d1974790e5181d0eda0ea91f2ed166ad5d`, engine hash `18f5455515c86c193d433975bcae82fa208c9cc91424d47972c197b5e77c9248`, both candidate recall numbers and the recorded source provenance.

Both public download controls completed. The downloaded files were retained beside this log as:

- `public-run-865280a5.json`
- `public-run-865280a5.csv`

Inspection confirmed the JSON full run ID matched the displayed prefix, CAT-005 remained `review_needed`, the four displayed reasons and source provenance were preserved, and both hashes matched the display. The CSV CAT-005 row contained `review_needed`, both candidate recall numbers and the same four reasons.

A separate direct hosted-adapter test-client execution also returned HTTP 200 for both JSON and CSV exports and preserved its exact run ID, classification, reasons and provenance. This independently confirms the API export route as well as the browser's executed-result downloads.
