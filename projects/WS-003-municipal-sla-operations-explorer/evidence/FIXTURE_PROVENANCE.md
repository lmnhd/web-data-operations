# WS-003 fixture provenance

## Classification

- `fixture_kind`: `synthetic_sla_scenario`
- Records: 15
- Reference time: `2026-08-08T12:00:00Z`
- Personal data: none

The fixture was authored to test configurable target windows, open and closed lifecycle states, at-risk margins, breached margins, malformed timestamps, ward aggregation, JSON/CSV export, and deterministic fingerprints. Every valid synthetic event timestamp is at or before the fixed reference time; deliberately invalid temporal cases live in the adversarial test suite and must route to review.

It is not a sample of Toronto service-request rows. Toronto's public 2026 file provides creation date, current status, ward, request type, division, section, and coarse location fields, but not the target and closure timestamps required by this proof.

## Predeclared labels

`tests/fixtures/benchmark_oracle.json` defines the expected labels before execution. Reproducing 15 of 15 labels proves deterministic agreement with this synthetic test oracle; it does not estimate production accuracy or official municipal performance.

## Safe use

Use the fixture to review engine behavior and adapter requirements. Do not use its categories, rules, timestamps, ward rates, or record IDs as facts about the City of Toronto.
