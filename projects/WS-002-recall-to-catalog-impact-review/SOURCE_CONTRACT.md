# openFDA source contract - WS-002 vertical proof

## Verified source

- Endpoint family: `https://api.fda.gov/drug/enforcement.json`
- Official overview: https://open.fda.gov/apis/drug/enforcement/
- Searchable fields: https://open.fda.gov/apis/drug/enforcement/searchable-fields/
- Terms: https://open.fda.gov/terms/
- Licence: https://open.fda.gov/license/
- Authentication and published limits: https://open.fda.gov/apis/authentication/
- Verification date: 2026-09-03 US Eastern / 2026-09-04 UTC

The official documentation says the endpoint exposes publicly releasable Recall Enterprise System records from 2004 onward and is updated weekly. It explicitly warns against medical-care reliance, using the data to issue public alerts, tracking recall lifecycles, or treating the published status as subsequently updated.

## Bounded acquisition

Exactly one source-data request was made:

```text
https://api.fda.gov/drug/enforcement.json?search=openfda.upc:*&sort=report_date:desc&limit=12
```

- Retrieved: `2026-09-04T03:06:10.1206316Z`
- Result used: ten records selected from the twelve returned
- No API key, pagination, retry, rate probing or follow-up record fetch was used
- The published unauthenticated allowance is 240 requests/minute and 1,000/day; this proof used one request

## Persisted allowlist

The fixture retains only:

```text
recall_number, event_id, report_date, recalling_firm,
product_description, code_info, product_type, upc, brand_name,
generic_name, manufacturer_name, product_ndc
```

Addresses, recall reason, distribution details, lifecycle status, termination date and every unneeded source field are dropped. Device-only GMDN content is not collected.

## Observed matching defect

Harmonized identifiers are useful but not sufficient by themselves. In the bounded response, the same UPC or NDC family appeared across multiple strengths or package variants. The proof therefore treats exact identifiers as evidence, checks variant strength and lot/code information, and routes conflicts or unresolved candidates to human review.

## Claims refused

This fixture does not establish source completeness, current recall status, medical correctness, production coverage, public-alert suitability, lifecycle tracking, business savings or retailer integration.
