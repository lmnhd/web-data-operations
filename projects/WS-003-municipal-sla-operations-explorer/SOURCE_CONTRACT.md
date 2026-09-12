# Source and fixture contract: Municipal 311 SLA Operations Desk

## Official source context

- **Dataset:** City of Toronto, `311 Service Requests - Customer Initiated`
- **Dataset page:** https://open.toronto.ca/dataset/311-service-requests-customer-initiated/
- **2026 resource:** annual ZIP download, CKAN resource `99b7f283-7345-4f5a-a126-d078ed4f3419`
- **Observed metadata date:** 2026-09-12; CKAN metadata was last modified 2026-09-08
- **Licence page:** https://open.toronto.ca/open-data-licence/
- **Attribution:** Contains information licensed under the Open Government Licence - Toronto.

The official portal permits lawful commercial reuse with attribution. Its CKAN package currently exposes annual ZIP resources; the 2026 resource is not an active CKAN DataStore table.

## Verified 2026 public columns

The downloaded 2026 CSV header contains:

```text
Creation Date,Status,First 3 Chars of Postal Code,Intersection Street 1,
Intersection Street 2,Ward,Service Request Type,Division,Section
```

The public file does **not** expose an internal service-request identifier, target timestamp, closure timestamp, or official SLA rule. Those fields cannot be inferred honestly from the public data.

## Synthetic proof fixture

`tests/fixtures/toronto_311_sample.json` and its evidence copy are synthetic SLA scenarios. Their identifiers, categories, timestamps, rules, and outcomes are fictional and were designed to exercise the engine's branches. They are not copied Toronto requests and do not measure City performance.

Every evaluated JSON/CSV row carries:

```text
fixture_kind = synthetic_sla_scenario
```

| Synthetic field | Relationship to public schema | Production requirement |
|---|---|---|
| `created_date` | Analogous to `Creation Date` | Map and validate the authorized source timestamp |
| `status` | Analogous to `Status` | Normalize source-specific status values |
| `ward` | Analogous to `Ward` | Preserve source ward value and version |
| `service_name` | Analogous to `Service Request Type` | Maintain an approved category mapping |
| `service_request_id` | Synthetic only | Obtain a stable authorized internal identifier |
| `target_date` | Synthetic only | Obtain an authorized target or approved rule contract |
| `closed_date` | Synthetic only | Obtain an authorized work-order completion timestamp |

## Access and privacy boundaries

- The runnable demo performs no live collection and needs no credentials.
- No resident name, contact detail, full address, postal code, or intersection is included.
- No public-data rate claim is needed for the fixture replay.
- Production use requires a separately approved adapter, field contract, retention policy, and source-specific access review.
- Results are scenario outputs, not official Toronto SLA metrics, legal compliance determinations, staffing instructions, or dispatch commands.
