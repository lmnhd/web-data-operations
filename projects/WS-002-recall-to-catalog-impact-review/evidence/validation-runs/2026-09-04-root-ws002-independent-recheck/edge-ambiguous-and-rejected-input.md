# Independent repair recheck - edge-ambiguous-and-rejected-input

- Validator: `/root/ws002_independent_validation`
- Checked: 2026-09-04 UTC

The public default 100 mcg row retained D-0709-2026 and D-0711-2026 with distinct fingerprints and stayed `review_needed`; ambiguity was not promoted to match.

An all-whitespace product name failed closed in the public demo with `Product name is required.` and `Run failed. No result is shown as successful.`

Independent hosted-adapter test-client requests confirmed:

- unexpected sixth catalog field: HTTP 400;
- cross-site POST from `https://example.com`: HTTP 403;
- unknown well-formed export identifier: HTTP 404.

The final request is an added adversarial check beyond the frozen plan. All rejected-input paths failed closed without executing a successful result.
