# Independent validation - edge-ambiguous-and-rejected-input

- Validator: `/root/ws002_independent_validation`
- Checked: 2026-09-04 UTC

The signed-out public demo kept the default 100 mcg CAT-005 row at `review_needed`. It retained both conflicting source candidates, D-0709-2026 and D-0711-2026, with distinct SHA-256 fingerprints and did not promote either to a match.

The public form rejected an empty product name through required-field validation. An all-whitespace product name reached the server and failed closed with `Product name is required.` and `Run failed. No result is shown as successful.`

Independent Flask test-client requests against the committed hosted adapter confirmed:

- unexpected sixth catalog field: HTTP 400, `Submit exactly the five editable catalog fields.`
- cross-site POST with `Origin: https://example.com`: HTTP 403, `Use the demo from its own page.`
- unknown but well-formed export identifier: HTTP 404.

The predefined ambiguity and rejected-input expectations passed. The unknown-export request was an added adversarial check and also failed closed.
