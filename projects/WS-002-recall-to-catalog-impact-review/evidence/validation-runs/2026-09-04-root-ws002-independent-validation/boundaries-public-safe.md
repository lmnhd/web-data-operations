# Independent validation - boundaries-public-safe

- Validator: `/root/ws002_independent_validation`
- Checked: 2026-09-04 UTC

The source contract, fixtures, Python adapters, browser code, README, Manifest and PDF were inspected for field scope, acquisition behavior, credentials, file/URL input and prohibited claims.

Observed controls:

- The recall fixture contains exactly the 12 allowlisted enforcement fields and 10 records. Restricted lifecycle status, recall reason, addresses, termination information and GMDN fields are absent.
- Catalog inputs are the documented synthetic fixtures. No private client data was found.
- No API key, password, authorization token or credential is required or embedded in the committed candidate or public fixtures.
- Demo execution loads committed JSON fixtures; neither the local nor hosted adapter performs a live FDA request.
- The public request body accepts exactly one `catalog_row` object containing exactly five string fields, caps each field at 160 characters and requires a nonblank product name.
- Hosted request size is capped at 8 KB, POSTs are same-origin guarded, and the page serves a restrictive Content-Security-Policy.
- Export identifiers are UUID-shaped and only retrieve one of at most 32 in-memory executed runs. No arbitrary path or URL parameter is accepted.
- Reviewer copy repeatedly identifies recorded/synthetic data and rejects medical advice, public alerts, current recall status, recall-lifecycle, completeness, production accuracy/scale and business-impact claims.

## Blocking finding

The ignored local file `projects/WS-002-recall-to-catalog-impact-review/.env.local` exists inside the project and contains a `VERCEL_OIDC_TOKEN`. It is excluded from Git by the project `.gitignore`, so it is not present in frozen commit `69ef14bbf026c93853057e8c7d12dcaf5acdb850` and was not observed in the public demo or repository. However, the independent-validation contract requires the current project tree to contain no credentials, and `scripts/validation_gate.py` does not exclude `.env*` files from its project-wide artifact walk. The current artifact map therefore also includes this file, making a PASS report unsafe and non-portable to a clean checkout.

The boundary check fails until an authorized owner removes the local credential, treats the token as sensitive and revokes it if still valid, and the candidate is revalidated. The validator did not modify or delete the file.
